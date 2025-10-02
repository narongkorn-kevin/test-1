#!/usr/bin/env python3
"""Analyze the original detectors in the input file to find the correct offset"""

import ezdxf
from shapely.geometry import Polygon

# Read the ORIGINAL file (with old detectors)
doc = ezdxf.readfile("RCP-FO10,11,12,16-AR-1.dxf")
msp = doc.modelspace()

print("=" * 70)
print("🔍 ANALYZING ORIGINAL DETECTORS")
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

# 2. Get original detectors
orig_detectors = []
for e in msp:
    try:
        if e.dxftype() == "INSERT":
            block_name = e.dxf.name.upper()
            if "SMOKE" in block_name or "SD" in block_name or "DET" in block_name:
                orig_detectors.append((e.dxf.insert.x, e.dxf.insert.y))
    except Exception:
        pass

print(f"\n📍 ORIGINAL DETECTORS: {len(orig_detectors)} found")

if orig_detectors:
    det_xs = [d[0] for d in orig_detectors]
    det_ys = [d[1] for d in orig_detectors]
    
    det_minx, det_maxx = min(det_xs), max(det_xs)
    det_miny, det_maxy = min(det_ys), max(det_ys)
    
    print(f"   Bounds: X:[{det_minx:.0f}, {det_maxx:.0f}], Y:[{det_miny:.0f}, {det_maxy:.0f}]")
    
    # Sample
    print(f"\n   Sample positions:")
    for i, (x, y) in enumerate(orig_detectors[:10]):
        print(f"   {i+1}. ({x:.0f}, {y:.0f})")
    
    # Calculate what offset the original detectors used
    # If original detectors were placed correctly, we can reverse-engineer the offset
    
    print(f"\n🔍 REVERSE-ENGINEERING THE CORRECT OFFSET:")
    
    # The offset should align room center with detector distribution center
    room_centerx = (room_minx + room_maxx) / 2
    room_centery = (room_miny + room_maxy) / 2
    
    det_centerx = (det_minx + det_maxx) / 2
    det_centery = (det_miny + det_maxy) / 2
    
    implied_offset_x = det_centerx - room_centerx
    implied_offset_y = det_centery - room_centery
    
    print(f"   Room center: ({room_centerx:.0f}, {room_centery:.0f})")
    print(f"   Original detector center: ({det_centerx:.0f}, {det_centery:.0f})")
    print(f"   Implied offset: ({implied_offset_x:.0f}, {implied_offset_y:.0f})")
    
    # Alternative: use min points
    implied_offset_minx = det_minx - room_minx
    implied_offset_miny = det_miny - room_miny
    
    print(f"\n   Alternative (using min points):")
    print(f"   Implied offset: ({implied_offset_minx:.0f}, {implied_offset_miny:.0f})")
    
    # Check room dimensions vs detector distribution
    room_width = room_maxx - room_minx
    det_width = det_maxx - det_minx
    room_height = room_maxy - room_miny
    det_height = det_maxy - det_miny
    
    print(f"\n📏 DIMENSION CHECK:")
    print(f"   Room size: {room_width:.0f} x {room_height:.0f} mm")
    print(f"   Detector distribution size: {det_width:.0f} x {det_height:.0f} mm")
    
    width_ratio = det_width / room_width
    height_ratio = det_height / room_height
    
    print(f"   Width ratio: {width_ratio:.3f}")
    print(f"   Height ratio: {height_ratio:.3f}")
    
    if 0.8 <= width_ratio <= 1.2 and 0.8 <= height_ratio <= 1.2:
        print(f"\n✅ Dimensions match well! Original detectors were likely placed correctly.")
        print(f"\n📋 RECOMMENDED OFFSET:")
        print(f"   {implied_offset_x:.0f}, {implied_offset_y:.0f}")
    else:
        print(f"\n⚠️  Dimensions don't match - original detectors may have been incorrect")

print("\n" + "=" * 70)


