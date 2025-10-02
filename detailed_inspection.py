#!/usr/bin/env python3
"""Detailed inspection of detector positions vs room boundaries"""

import ezdxf
from shapely.geometry import Polygon, Point

# Read the clean output file
doc = ezdxf.readfile("RCP-FO10,11,12,16-AR-1_clean_with_detectors.dxf")
msp = doc.modelspace()

print("=" * 70)
print("🔍 DETAILED POSITION INSPECTION")
print("=" * 70)

# 1. Get room polygons
rooms = []
for e in msp.query("LWPOLYLINE"):
    try:
        if e.dxf.layer.upper() == "00_VAV_ZONE" and e.closed:
            pts = [(v[0], v[1]) for v in e.get_points()]
            if pts and pts[0] != pts[-1]:
                pts.append(pts[0])
            poly = Polygon(pts)
            if poly.is_valid and poly.area > 0:
                rooms.append(poly)
    except Exception:
        pass

print(f"\n📦 Found {len(rooms)} room polygons")

if rooms:
    # Calculate room bounds
    all_room_xs = []
    all_room_ys = []
    for room in rooms:
        bounds = room.bounds
        all_room_xs.extend([bounds[0], bounds[2]])
        all_room_ys.extend([bounds[1], bounds[3]])
    
    room_minx, room_maxx = min(all_room_xs), max(all_room_xs)
    room_miny, room_maxy = min(all_room_ys), max(all_room_ys)
    
    print(f"\n📏 Room boundaries (original coordinates):")
    print(f"   X: [{room_minx:.0f}, {room_maxx:.0f}]")
    print(f"   Y: [{room_miny:.0f}, {room_maxy:.0f}]")

# 2. Get detector positions
detectors = []
for e in msp:
    try:
        if e.dxftype() == "INSERT" and "SMOKE" in e.dxf.name.upper():
            detectors.append((e.dxf.insert.x, e.dxf.insert.y))
    except Exception:
        pass

print(f"\n📍 Found {len(detectors)} detectors")

if detectors:
    det_xs = [d[0] for d in detectors]
    det_ys = [d[1] for d in detectors]
    
    det_minx, det_maxx = min(det_xs), max(det_xs)
    det_miny, det_maxy = min(det_ys), max(det_ys)
    
    print(f"\n📏 Detector positions:")
    print(f"   X: [{det_minx:.0f}, {det_maxx:.0f}]")
    print(f"   Y: [{det_miny:.0f}, {det_maxy:.0f}]")
    
    # Sample positions
    print(f"\n📋 Sample detector coordinates:")
    for i, (x, y) in enumerate(detectors[:10]):
        print(f"   {i+1}. ({x:.0f}, {y:.0f})")

# 3. Check if detectors are inside rooms
if rooms and detectors:
    print(f"\n🔍 CHECKING IF DETECTORS ARE INSIDE ROOMS:")
    
    inside_count = 0
    outside_count = 0
    
    for x, y in detectors:
        point = Point(x, y)
        is_inside = any(room.contains(point) for room in rooms)
        if is_inside:
            inside_count += 1
        else:
            outside_count += 1
            if outside_count <= 5:  # Show first 5 outside points
                print(f"   ❌ Detector at ({x:.0f}, {y:.0f}) is OUTSIDE all rooms")
    
    print(f"\n📊 Results:")
    print(f"   ✅ Inside rooms: {inside_count} ({inside_count/len(detectors)*100:.1f}%)")
    print(f"   ❌ Outside rooms: {outside_count} ({outside_count/len(detectors)*100:.1f}%)")
    
    if outside_count > 0:
        print(f"\n⚠️  WARNING: {outside_count} detectors are outside room boundaries!")
        print(f"   This means the offset calculation may be incorrect.")
        
        # Try to figure out what offset would work
        print(f"\n💡 DEBUGGING:")
        print(f"   Current detector range: X:[{det_minx:.0f}, {det_maxx:.0f}], Y:[{det_miny:.0f}, {det_maxy:.0f}]")
        print(f"   Room range: X:[{room_minx:.0f}, {room_maxx:.0f}], Y:[{room_miny:.0f}, {room_maxy:.0f}]")
        
        # Calculate what offset was actually applied
        # Detectors should be at room position + offset
        # So offset = detector position - room position
        actual_offset_x = det_minx - room_minx
        actual_offset_y = det_miny - room_miny
        
        print(f"\n   Offset that was applied: ({actual_offset_x:.0f}, {actual_offset_y:.0f})")
    else:
        print(f"\n✅ PERFECT! All detectors are inside room boundaries!")

print("\n" + "=" * 70)


