#!/usr/bin/env python3
import ezdxf
from shapely.geometry import Polygon
from collections import defaultdict

doc = ezdxf.readfile('RCP-FO10,11,12,16-AR-1.dxf')
msp = doc.modelspace()

# Check for rooms in the main drawing area (X > 300000)
print('Looking for closed polygons in main drawing area (X > 300k)...')
print()

room_layers = defaultdict(int)

for e in msp.query('LWPOLYLINE'):
    try:
        if e.closed:
            pts = [(v[0], v[1]) for v in e.get_points()]
            if pts:
                # Check if in main drawing area
                xs = [p[0] for p in pts]
                if min(xs) > 300000:  # In main drawing
                    poly = Polygon(pts)
                    if poly.is_valid and poly.area > 0:
                        room_layers[e.dxf.layer] += 1
    except Exception:
        pass

if room_layers:
    print('Found closed polygons in main drawing:')
    for layer, count in sorted(room_layers.items(), key=lambda x: -x[1]):
        print(f'  {layer}: {count} polygons')
else:
    print('❌ No closed polygons found in main drawing area')
    print('   Main drawing may not have room boundaries')


