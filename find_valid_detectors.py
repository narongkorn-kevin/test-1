#!/usr/bin/env python3
"""Find detectors that are actually in the room coordinate range"""

import ezdxf
from shapely.geometry import Polygon, Point

# Read the ORIGINAL file
doc = ezdxf.readfile("RCP-FO10,11,12,16-AR-1.dxf")
msp = doc.modelspace()

print("=" * 70)
print("🔍 FINDING VALID DETECTORS IN ROOM RANGE")
print("=" * 70)

# 1. Get rooms
rooms = []
room_xs, room_ys = [], []
for e in msp.query("LWPOLYLINE"):
    try:
        if e.dxf.layer.upper() == "00_VAV_ZONE" and e.closed:
            pts = [(v[0], v[1]) for v in e.get_points()]
            poly = Polygon(pts)
            if poly.is_valid and poly.area > 0:
                rooms.append(poly)
                bounds = poly.bounds
                room_xs.extend([bounds[0], bounds[2]])
                room_ys.extend([bounds[1], bounds[3]])
    except Exception:
        pass

room_minx, room_maxx = min(room_xs), max(room_xs)
room_miny, room_maxy = min(room_ys), max(room_ys)

print(f"\n📦 ROOMS: {len(rooms)} rooms")
print(f"   Bounds: X:[{room_minx:.0f}, {room_maxx:.0f}], Y:[{room_miny:.0f}, {room_maxy:.0f}]")

# 2. Get ALL detectors
all_detectors = []
for e in msp:
    try:
        if e.dxftype() == "INSERT":
            block_name = e.dxf.name.upper()
            if "SMOKE" in block_name or "SD" in block_name or "DET" in block_name:
                x, y = e.dxf.insert.x, e.dxf.insert.y
                all_detectors.append((x, y))
    except Exception:
        pass

print(f"\n📍 ALL DETECTORS: {len(all_detectors)}")

# 3. Filter detectors within room bounds
valid_detectors = []
for x, y in all_detectors:
    if room_minx <= x <= room_maxx and room_miny <= y <= room_maxy:
        valid_detectors.append((x, y))

print(f"\n✅ DETECTORS IN ROOM COORDINATE RANGE: {len(valid_detectors)}")

if valid_detectors:
    print(f"\n   Sample (first 20):")
    for i, (x, y) in enumerate(valid_detectors[:20]):
        print(f"   {i+1}. ({x:.0f}, {y:.0f})")
    
    # Check how many are actually INSIDE room polygons
    inside_count = 0
    outside_count = 0
    
    for x, y in valid_detectors:
        point = Point(x, y)
        is_inside = any(room.contains(point) for room in rooms)
        if is_inside:
            inside_count += 1
        else:
            outside_count += 1
    
    print(f"\n📊 OF THESE {len(valid_detectors)} DETECTORS:")
    print(f"   ✅ Inside room polygons: {inside_count} ({inside_count/len(valid_detectors)*100:.1f}%)")
    print(f"   ❌ Outside room polygons: {outside_count} ({outside_count/len(valid_detectors)*100:.1f}%)")
    
    if inside_count > 0:
        print(f"\n🎉 Found {inside_count} correctly placed detectors!")
        print(f"   These detectors DON'T need any offset!")
        print(f"\n💡 SOLUTION: Don't apply offset! Rooms and detectors are already aligned!")
        print(f"\n   Use: --offset-x 0 --offset-y 0")
    else:
        print(f"\n❌ Even detectors in coordinate range are outside room polygons")
        print(f"   Need to investigate further...")

# 4. Check detectors in architectural coordinate range
print(f"\n\n🏢 NOW CHECKING ARCHITECTURAL LAYER RANGE:")
arch_xs, arch_ys = [], []
for e in msp.query("LINE LWPOLYLINE"):
    try:
        layer = e.dxf.layer.upper()
        if "WALL" in layer or "A-CLNG" in layer:
            if e.dxftype() == "LINE":
                arch_xs.extend([e.dxf.start.x, e.dxf.end.x])
                arch_ys.extend([e.dxf.start.y, e.dxf.end.y])
            elif e.dxftype() == "LWPOLYLINE":
                for v in e.get_points():
                    arch_xs.append(v[0])
                    arch_ys.append(v[1])
    except Exception:
        pass

if arch_xs:
    arch_minx, arch_maxx = min(arch_xs), max(arch_xs)
    arch_miny, arch_maxy = min(arch_ys), max(arch_ys)
    
    print(f"   Architectural bounds: X:[{arch_minx:.0f}, {arch_maxx:.0f}], Y:[{arch_miny:.0f}, {arch_maxy:.0f}]")
    
    arch_detectors = []
    for x, y in all_detectors:
        if arch_minx <= x <= arch_maxx and arch_miny <= y <= arch_maxy:
            arch_detectors.append((x, y))
    
    print(f"   Detectors in arch range: {len(arch_detectors)}")
    
    if len(arch_detectors) > len(valid_detectors):
        print(f"\n💡 More detectors found in architectural range!")
        print(f"   This suggests detectors should be placed at architectural coordinates,")
        print(f"   NOT at room coordinates.")

print("\n" + "=" * 70)


