#!/usr/bin/env python3
"""Find offset to align rooms with the VISIBLE building plan"""

import ezdxf
from shapely.geometry import Polygon

doc = ezdxf.readfile("RCP-FO10,11,12,16-AR-1_clean.dxf")
msp = doc.modelspace()

print("=" * 70)
print("🔍 FINDING OFFSET FOR VISIBLE BUILDING ALIGNMENT")
print("=" * 70)

# 1. Room polygons
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
room_width = room_maxx - room_minx
room_height = room_maxy - room_miny

print(f"\n📦 ROOMS (00_VAV_ZONE):")
print(f"   Count: {len(rooms)}")
print(f"   X: [{room_minx:.0f}, {room_maxx:.0f}] (width: {room_width:.0f})")
print(f"   Y: [{room_miny:.0f}, {room_maxy:.0f}] (height: {room_height:.0f})")

# 2. Find all closed polygons that match room dimensions
print(f"\n🔍 SEARCHING FOR BUILDING OUTLINE WITH MATCHING DIMENSIONS:")

all_layers = set()
for e in msp:
    try:
        all_layers.add(e.dxf.layer)
    except:
        pass

print(f"   Total layers in file: {len(all_layers)}")

# Check closed polygons on all layers
matches = []
for layer in sorted(all_layers):
    if layer.upper() in ["00_VAV_ZONE", "E-FIRE"]:
        continue
    
    for e in msp.query("LWPOLYLINE"):
        try:
            if e.dxf.layer == layer and e.closed:
                pts = [(v[0], v[1]) for v in e.get_points()]
                poly = Polygon(pts)
                if poly.is_valid and poly.area > 0:
                    bounds = poly.bounds
                    w = bounds[2] - bounds[0]
                    h = bounds[3] - bounds[1]
                    
                    # Check if dimensions match (within 10%)
                    w_match = 0.9 <= w/room_width <= 1.1
                    h_match = 0.9 <= h/room_height <= 1.1
                    
                    if w_match and h_match:
                        offset_x = bounds[0] - room_minx
                        offset_y = bounds[1] - room_miny
                        matches.append({
                            'layer': layer,
                            'bounds': bounds,
                            'width': w,
                            'height': h,
                            'offset_x': offset_x,
                            'offset_y': offset_y
                        })
        except Exception:
            pass

if matches:
    print(f"\n✅ FOUND {len(matches)} MATCHING BUILDING OUTLINE(S):")
    for i, match in enumerate(matches):
        print(f"\n   Match {i+1}: Layer '{match['layer']}'")
        print(f"      X: [{match['bounds'][0]:.0f}, {match['bounds'][2]:.0f}]")
        print(f"      Y: [{match['bounds'][1]:.0f}, {match['bounds'][3]:.0f}]")
        print(f"      Size: {match['width']:.0f} x {match['height']:.0f}")
        print(f"      OFFSET: ({match['offset_x']:.0f}, {match['offset_y']:.0f})")
else:
    print(f"\n⚠️  No matching closed polygons found")
    print(f"   Trying alternative approach...")

# 3. Alternative: Check A-CLNG layer extent
print(f"\n🏢 CHECKING A-CLNG LAYER (Ceiling - usually matches visible building):")
clng_xs, clng_ys = [], []
clng_count = 0

for e in msp:
    try:
        if e.dxf.layer.upper() == "A-CLNG":
            dxftype = e.dxftype()
            if dxftype == "LINE":
                clng_xs.extend([e.dxf.start.x, e.dxf.end.x])
                clng_ys.extend([e.dxf.start.y, e.dxf.end.y])
                clng_count += 1
            elif dxftype == "LWPOLYLINE":
                for v in e.get_points():
                    clng_xs.append(v[0])
                    clng_ys.append(v[1])
                clng_count += 1
    except Exception:
        pass

if clng_xs:
    clng_minx, clng_maxx = min(clng_xs), max(clng_xs)
    clng_miny, clng_maxy = min(clng_ys), max(clng_ys)
    clng_width = clng_maxx - clng_minx
    clng_height = clng_maxy - clng_miny
    
    print(f"   Entities: {clng_count}")
    print(f"   X: [{clng_minx:.0f}, {clng_maxx:.0f}] (width: {clng_width:.0f})")
    print(f"   Y: [{clng_miny:.0f}, {clng_maxy:.0f}] (height: {clng_height:.0f})")
    
    # Check if dimensions match
    w_ratio = clng_width / room_width
    h_ratio = clng_height / room_height
    
    print(f"   Width ratio: {w_ratio:.3f}")
    print(f"   Height ratio: {h_ratio:.3f}")
    
    if 0.9 <= w_ratio <= 1.1 and 0.9 <= h_ratio <= 1.1:
        offset_x = clng_minx - room_minx
        offset_y = clng_miny - room_miny
        
        print(f"\n✅ DIMENSIONS MATCH!")
        print(f"\n🎯 RECOMMENDED OFFSET:")
        print(f"   --offset-x {offset_x:.0f}")
        print(f"   --offset-y {offset_y:.0f}")
        
        print(f"\n📋 COMMAND TO RUN:")
        print(f'   python3 smoke_detector_placer.py "RCP-FO10,11,12,16-AR-1_clean.dxf" \\')
        print(f'       --rooms-layer 00_VAV_ZONE \\')
        print(f'       --offset-x {offset_x:.0f} --offset-y {offset_y:.0f} \\')
        print(f'       --no-pdf')

print("\n" + "=" * 70)


