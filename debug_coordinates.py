#!/usr/bin/env python3
"""Debug script to check coordinates of rooms vs drawing extents"""

import ezdxf
from shapely.geometry import Polygon

# Read the DXF
doc = ezdxf.readfile("RCP-FO10,11,12,16-AR-1.dxf")
msp = doc.modelspace()

# Get drawing extents
try:
    bbox = msp.bbox()
    print(f"Drawing extents:")
    print(f"  Min: ({bbox.extmin.x:.2f}, {bbox.extmin.y:.2f})")
    print(f"  Max: ({bbox.extmax.x:.2f}, {bbox.extmax.y:.2f})")
    print(f"  Size: {bbox.size.x:.2f} x {bbox.size.y:.2f}")
except Exception as e:
    print(f"Could not get bbox: {e}")

print("\n" + "="*60)

# Check room polygons
room_layers = ["00_VAV_ZONE", "E-FIRE"]
print(f"\nChecking rooms on layers: {room_layers}")

for layer in room_layers:
    print(f"\n--- Layer: {layer} ---")
    count = 0
    for e in msp.query("LWPOLYLINE"):
        try:
            if e.dxf.layer.upper() == layer.upper() and e.closed:
                pts = [(v[0], v[1]) for v in e.get_points()]
                if pts:
                    poly = Polygon(pts)
                    if poly.is_valid and poly.area > 0:
                        bounds = poly.bounds
                        centroid = poly.centroid
                        count += 1
                        if count <= 3:  # Show first 3 rooms
                            print(f"  Room {count}:")
                            print(f"    Bounds: ({bounds[0]:.2f}, {bounds[1]:.2f}) to ({bounds[2]:.2f}, {bounds[3]:.2f})")
                            print(f"    Centroid: ({centroid.x:.2f}, {centroid.y:.2f})")
        except Exception:
            pass
    print(f"  Total: {count} rooms")

print("\n" + "="*60)

# Check where entities actually are
print("\nSample entity coordinates:")
count = 0
for e in msp.query("LINE"):
    try:
        x1, y1 = e.dxf.start.x, e.dxf.start.y
        x2, y2 = e.dxf.end.x, e.dxf.end.y
        count += 1
        if count <= 3:
            print(f"  Line {count}: ({x1:.2f}, {y1:.2f}) to ({x2:.2f}, {y2:.2f})")
    except Exception:
        pass
print(f"  Total lines: {count}")


