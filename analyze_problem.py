#!/usr/bin/env python3
"""Detailed analysis of the coordinate problem"""

import ezdxf
from shapely.geometry import Polygon

# Read the DXF
doc = ezdxf.readfile("RCP-FO10,11,12,16-AR-1.dxf")
msp = doc.modelspace()

print("=" * 70)
print("🔍 DETAILED COORDINATE ANALYSIS")
print("=" * 70)

# 1. Analyze room polygons
room_layers = ["00_VAV_ZONE", "E-FIRE"]
print(f"\n📦 ROOM POLYGONS:")
for layer_name in room_layers:
    xs, ys = [], []
    count = 0
    for e in msp.query("LWPOLYLINE"):
        try:
            if e.dxf.layer.upper() == layer_name.upper() and e.closed:
                pts = [(v[0], v[1]) for v in e.get_points()]
                poly = Polygon(pts)
                if poly.is_valid and poly.area > 0:
                    bounds = poly.bounds
                    xs.extend([bounds[0], bounds[2]])
                    ys.extend([bounds[1], bounds[3]])
                    count += 1
        except Exception:
            pass
    
    if xs:
        print(f"\n  Layer: {layer_name}")
        print(f"    Count: {count} rooms")
        print(f"    X range: [{min(xs):.0f}, {max(xs):.0f}]")
        print(f"    Y range: [{min(ys):.0f}, {max(ys):.0f}]")
        print(f"    Center: ({(min(xs)+max(xs))/2:.0f}, {(min(ys)+max(ys))/2:.0f})")

# 2. Analyze main drawing entities (sample from different layers)
print(f"\n🏢 MAIN DRAWING ENTITIES (sample by layer):")

from collections import defaultdict
layer_coords = defaultdict(lambda: {"xs": [], "ys": [], "count": 0})

for e in msp:
    try:
        layer = e.dxf.layer.upper()
        if layer in ["00_VAV_ZONE", "E-FIRE"]:
            continue
        
        dxftype = e.dxftype()
        if dxftype == "LINE":
            layer_coords[layer]["xs"].extend([e.dxf.start.x, e.dxf.end.x])
            layer_coords[layer]["ys"].extend([e.dxf.start.y, e.dxf.end.y])
            layer_coords[layer]["count"] += 1
        elif dxftype == "LWPOLYLINE":
            for v in e.get_points():
                layer_coords[layer]["xs"].append(v[0])
                layer_coords[layer]["ys"].append(v[1])
            layer_coords[layer]["count"] += 1
    except Exception:
        pass

# Sort by entity count
sorted_layers = sorted(layer_coords.items(), key=lambda x: -x[1]["count"])

print(f"\n  Top 10 layers with most entities:")
for i, (layer, data) in enumerate(sorted_layers[:10]):
    if data["xs"]:
        minx, maxx = min(data["xs"]), max(data["xs"])
        miny, maxy = min(data["ys"]), max(data["ys"])
        centerx = (minx + maxx) / 2
        centery = (miny + maxy) / 2
        print(f"\n  {i+1}. {layer}")
        print(f"     Entities: {data['count']}")
        print(f"     X range: [{minx:.0f}, {maxx:.0f}]")
        print(f"     Y range: [{miny:.0f}, {maxy:.0f}]")
        print(f"     Center: ({centerx:.0f}, {centery:.0f})")

# 3. Calculate overall drawing bounds (excluding room layers)
print(f"\n📊 OVERALL STATISTICS:")
all_xs, all_ys = [], []
for layer, data in layer_coords.items():
    all_xs.extend(data["xs"])
    all_ys.extend(data["ys"])

if all_xs:
    minx, maxx = min(all_xs), max(all_xs)
    miny, maxy = min(all_ys), max(all_ys)
    print(f"\n  All entities (excluding room layers):")
    print(f"    X range: [{minx:.0f}, {maxx:.0f}]")
    print(f"    Y range: [{miny:.0f}, {maxy:.0f}]")
    print(f"    Center: ({(minx+maxx)/2:.0f}, {(miny+maxy)/2:.0f})")
    print(f"    Size: {maxx-minx:.0f} x {maxy-miny:.0f}")

# 4. Check if there's a specific architectural layer we should use
print(f"\n🔍 RECOMMENDED APPROACH:")
print(f"\n  Looking at the coordinate ranges, it seems the main drawing")
print(f"  might be in a specific layer that represents the actual floor plan.")
print(f"\n  The offset should align rooms with the architectural elements.")

print("\n" + "=" * 70)


