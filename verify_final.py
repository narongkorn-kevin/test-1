#!/usr/bin/env python3
"""Verify final detector positions"""

import sys
import ezdxf
from pathlib import Path

# Find the output file
output_files = list(Path(".").glob("*_with_detectors_FINAL.dxf"))
if not output_files:
    # Fallback to old naming
    output_files = list(Path(".").glob("*_clean_with_detectors.dxf"))

if not output_files:
    print("❌ No output file found!")
    sys.exit(1)

output_file = output_files[0]  # Use the first match

doc = ezdxf.readfile(str(output_file))
msp = doc.modelspace()

print("=" * 70)
print("🔍 FINAL VERIFICATION")
print("=" * 70)

# Get detector positions
detectors = []
for e in msp:
    try:
        if e.dxftype() == "INSERT" and "SMOKE" in e.dxf.name.upper():
            detectors.append((e.dxf.insert.x, e.dxf.insert.y))
    except Exception:
        pass

if detectors:
    det_xs = [d[0] for d in detectors]
    det_ys = [d[1] for d in detectors]
    
    det_minx, det_maxx = min(det_xs), max(det_xs)
    det_miny, det_maxy = min(det_ys), max(det_ys)
    
    print(f"\n📍 DETECTORS: {len(detectors)} placed")
    print(f"   X: [{det_minx:.0f}, {det_maxx:.0f}]")
    print(f"   Y: [{det_miny:.0f}, {det_maxy:.0f}]")
    
    print(f"\n   Sample positions:")
    for i, (x, y) in enumerate(detectors[:10]):
        print(f"   {i+1}. ({x:.0f}, {y:.0f})")

# Compare with A-CLNG
clng_xs, clng_ys = [], []
for e in msp:
    try:
        if e.dxf.layer.upper() == "A-CLNG":
            if e.dxftype() == "LINE":
                clng_xs.extend([e.dxf.start.x, e.dxf.end.x])
                clng_ys.extend([e.dxf.start.y, e.dxf.end.y])
            elif e.dxftype() == "LWPOLYLINE":
                for v in e.get_points():
                    clng_xs.append(v[0])
                    clng_ys.append(v[1])
    except Exception:
        pass

if clng_xs:
    clng_minx, clng_maxx = min(clng_xs), max(clng_xs)
    clng_miny, clng_maxy = min(clng_ys), max(clng_ys)
    
    print(f"\n🏢 A-CLNG (Visible Building):")
    print(f"   X: [{clng_minx:.0f}, {clng_maxx:.0f}]")
    print(f"   Y: [{clng_miny:.0f}, {clng_maxy:.0f}]")
    
    # Check alignment
    print(f"\n✨ ALIGNMENT CHECK:")
    
    det_in_x = clng_minx <= det_minx and det_maxx <= clng_maxx
    det_in_y = clng_miny <= det_miny and det_maxy <= clng_maxy
    
    if det_in_x and det_in_y:
        print(f"   ✅ Detectors are WITHIN A-CLNG bounds!")
        print(f"   ✅ Should be visible on the building plan!")
    else:
        print(f"   X aligned: {'✅' if det_in_x else '❌'}")
        print(f"   Y aligned: {'✅' if det_in_y else '❌'}")
        
        if not det_in_x:
            print(f"\n   Detector X range: [{det_minx:.0f}, {det_maxx:.0f}]")
            print(f"   A-CLNG X range: [{clng_minx:.0f}, {clng_maxx:.0f}]")
            if det_minx < clng_minx:
                print(f"   ⚠️  Detectors are {clng_minx - det_minx:.0f} mm too far LEFT")
            if det_maxx > clng_maxx:
                print(f"   ⚠️  Detectors are {det_maxx - clng_maxx:.0f} mm too far RIGHT")

# Also check I-WALL for reference
wall_xs, wall_ys = [], []
for e in msp.query("LINE"):
    try:
        if e.dxf.layer.upper() == "I-WALL":
            wall_xs.extend([e.dxf.start.x, e.dxf.end.x])
            wall_ys.extend([e.dxf.start.y, e.dxf.end.y])
    except Exception:
        pass

if wall_xs:
    wall_minx, wall_maxx = min(wall_xs), max(wall_xs)
    wall_miny, wall_maxy = min(wall_ys), max(wall_ys)
    
    print(f"\n🧱 I-WALL (Interior Walls):")
    print(f"   X: [{wall_minx:.0f}, {wall_maxx:.0f}]")
    print(f"   Y: [{wall_miny:.0f}, {wall_maxy:.0f}]")

print("\n" + "=" * 70)

