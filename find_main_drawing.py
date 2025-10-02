#!/usr/bin/env python3
"""Find the main drawing area with most entities"""

import ezdxf
from collections import defaultdict

doc = ezdxf.readfile("RCP-FO10,11,12,16-AR-1.dxf")
msp = doc.modelspace()

# Collect all entity coordinates
coords = []

for e in msp:
    try:
        if e.dxftype() == "LINE":
            coords.append((e.dxf.start.x, e.dxf.start.y))
            coords.append((e.dxf.end.x, e.dxf.end.y))
        elif e.dxftype() == "LWPOLYLINE":
            for v in e.get_points():
                coords.append((v[0], v[1]))
        elif e.dxftype() == "CIRCLE":
            coords.append((e.dxf.center.x, e.dxf.center.y))
    except Exception:
        pass

if coords:
    xs = [c[0] for c in coords]
    ys = [c[1] for c in coords]
    
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)
    
    print("Overall drawing extents (all entities):")
    print(f"  X: {minx:.2f} to {maxx:.2f} (width: {maxx-minx:.2f})")
    print(f"  Y: {miny:.2f} to {maxy:.2f} (height: {maxy-miny:.2f})")
    
    # Find entity concentration
    print("\nEntity distribution analysis:")
    
    # Divide into regions
    x_regions = {}
    bins = 20
    x_bin_size = (maxx - minx) / bins
    
    for x, y in coords:
        bin_idx = int((x - minx) / x_bin_size) if x_bin_size > 0 else 0
        x_regions[bin_idx] = x_regions.get(bin_idx, 0) + 1
    
    # Find regions with most entities
    sorted_regions = sorted(x_regions.items(), key=lambda x: x[1], reverse=True)
    
    print(f"\nTop 3 X-regions with most entities:")
    for i, (bin_idx, count) in enumerate(sorted_regions[:3]):
        x_start = minx + bin_idx * x_bin_size
        x_end = x_start + x_bin_size
        print(f"  {i+1}. X: {x_start:.0f}-{x_end:.0f} ({count} points)")
    
    # Check specific layers
    print("\n" + "="*60)
    print("Checking specific layers for the visible plan...")
    
    for layer_pattern in ["WALL", "ARCH", "FLOOR", "A-", "0"]:
        print(f"\nLayers containing '{layer_pattern}':")
        layer_coords = defaultdict(list)
        
        for e in msp:
            try:
                layer = e.dxf.layer
                if layer_pattern.lower() in layer.lower():
                    if e.dxftype() == "LINE":
                        layer_coords[layer].append((e.dxf.start.x, e.dxf.start.y))
                    elif e.dxftype() == "LWPOLYLINE":
                        for v in e.get_points():
                            layer_coords[layer].append((v[0], v[1]))
            except Exception:
                pass
        
        for layer, coords_list in list(layer_coords.items())[:5]:  # Show first 5
            if coords_list:
                xs = [c[0] for c in coords_list]
                ys = [c[1] for c in coords_list]
                print(f"  {layer}: X:{min(xs):.0f}-{max(xs):.0f}, Y:{min(ys):.0f}-{max(ys):.0f} ({len(coords_list)} pts)")


