#!/usr/bin/env python3
"""Find the correct offset by comparing room polygons with ceiling layer"""

import ezdxf
from shapely.geometry import Polygon

doc = ezdxf.readfile("RCP-FO10,11,12,16-AR-1_clean.dxf")
msp = doc.modelspace()

print("=" * 70)
print("🔍 FINDING CORRECT OFFSET")
print("=" * 70)

# 1. Get room polygons (00_VAV_ZONE)
rooms = []
for e in msp.query("LWPOLYLINE"):
    try:
        if e.dxf.layer.upper() == "00_VAV_ZONE" and e.closed:
            pts = [(v[0], v[1]) for v in e.get_points()]
            poly = Polygon(pts)
            if poly.is_valid and poly.area > 0:
                rooms.append(poly)
    except Exception:
        pass

room_xs, room_ys = [], []
for room in rooms:
    bounds = room.bounds
    room_xs.extend([bounds[0], bounds[2]])
    room_ys.extend([bounds[1], bounds[3]])

room_minx, room_maxx = min(room_xs), max(room_xs)
room_miny, room_maxy = min(room_ys), max(room_ys)

print(f"\n📦 ROOMS (00_VAV_ZONE): {len(rooms)} rooms")
print(f"   Bounds: X:[{room_minx:.0f}, {room_maxx:.0f}], Y:[{room_miny:.0f}, {room_maxy:.0f}]")
print(f"   Width: {room_maxx - room_minx:.0f}, Height: {room_maxy - room_miny:.0f}")

# 2. Get A-CLNG polygons (ceiling - should match room layout)
clng_polys = []
for e in msp.query("LWPOLYLINE"):
    try:
        if e.dxf.layer.upper() == "A-CLNG" and e.closed:
            pts = [(v[0], v[1]) for v in e.get_points()]
            poly = Polygon(pts)
            if poly.is_valid and poly.area > 0:
                clng_polys.append(poly)
    except Exception:
        pass

if clng_polys:
    clng_xs, clng_ys = [], []
    for poly in clng_polys:
        bounds = poly.bounds
        clng_xs.extend([bounds[0], bounds[2]])
        clng_ys.extend([bounds[1], bounds[3]])
    
    clng_minx, clng_maxx = min(clng_xs), max(clng_xs)
    clng_miny, clng_maxy = min(clng_ys), max(clng_ys)
    
    print(f"\n🏢 CEILING (A-CLNG): {len(clng_polys)} polygons")
    print(f"   Bounds: X:[{clng_minx:.0f}, {clng_maxx:.0f}], Y:[{clng_miny:.0f}, {clng_maxy:.0f}]")
    print(f"   Width: {clng_maxx - clng_minx:.0f}, Height: {clng_maxy - clng_miny:.0f}")
    
    # Calculate offset based on matching dimensions
    room_width = room_maxx - room_minx
    clng_width = clng_maxx - clng_minx
    
    room_height = room_maxy - room_miny
    clng_height = clng_maxy - clng_miny
    
    print(f"\n📏 DIMENSION COMPARISON:")
    print(f"   Room width: {room_width:.0f} mm")
    print(f"   Ceiling width: {clng_width:.0f} mm")
    print(f"   Difference: {abs(room_width - clng_width):.0f} mm ({abs(room_width - clng_width)/room_width*100:.1f}%)")
    
    # If dimensions are similar, calculate offset
    if abs(room_width - clng_width) / room_width < 0.10:  # Within 10%
        offset_x = clng_minx - room_minx
        offset_y = clng_miny - room_miny
        
        print(f"\n✅ RECOMMENDED OFFSET (based on min points):")
        print(f"   X: {offset_x:.0f}")
        print(f"   Y: {offset_y:.0f}")
        
        # Alternative: use center points
        room_centerx = (room_minx + room_maxx) / 2
        room_centery = (room_miny + room_maxy) / 2
        clng_centerx = (clng_minx + clng_maxx) / 2
        clng_centery = (clng_miny + clng_maxy) / 2
        
        offset_center_x = clng_centerx - room_centerx
        offset_center_y = clng_centery - room_centery
        
        print(f"\n✅ ALTERNATIVE OFFSET (based on centers):")
        print(f"   X: {offset_center_x:.0f}")
        print(f"   Y: {offset_center_y:.0f}")
    else:
        print(f"\n⚠️  Dimensions don't match well - ceiling may not be aligned with rooms")

# 3. Try to match individual room with ceiling polygon
print(f"\n🔍 TRYING TO MATCH INDIVIDUAL ROOMS WITH CEILING:")
matches = 0
for i, room in enumerate(rooms[:5]):  # Check first 5 rooms
    room_bounds = room.bounds
    room_w = room_bounds[2] - room_bounds[0]
    room_h = room_bounds[3] - room_bounds[1]
    
    for j, clng in enumerate(clng_polys):
        clng_bounds = clng.bounds
        clng_w = clng_bounds[2] - clng_bounds[0]
        clng_h = clng_bounds[3] - clng_bounds[1]
        
        # Check if dimensions match (within 5%)
        w_match = abs(room_w - clng_w) / room_w < 0.05
        h_match = abs(room_h - clng_h) / room_h < 0.05
        
        if w_match and h_match:
            offset_x = clng_bounds[0] - room_bounds[0]
            offset_y = clng_bounds[1] - room_bounds[1]
            print(f"   Room {i+1} matches Ceiling {j+1}")
            print(f"     Offset: ({offset_x:.0f}, {offset_y:.0f})")
            matches += 1
            break

if matches > 0:
    print(f"\n✅ Found {matches} matching room-ceiling pairs")
else:
    print(f"\n⚠️  No matching room-ceiling pairs found")

print("\n" + "=" * 70)


