#!/usr/bin/env python3
"""Calculate the correct offset between rooms and main drawing"""

import ezdxf
from shapely.geometry import Polygon

# Read the DXF
doc = ezdxf.readfile("RCP-FO10,11,12,16-AR-1.dxf")
msp = doc.modelspace()

# 1. Get room bounds (from 00_VAV_ZONE layer - มีห้องเยอะสุด)
room_xs = []
room_ys = []
room_count = 0

for e in msp.query("LWPOLYLINE"):
    try:
        if e.dxf.layer.upper() == "00_VAV_ZONE" and e.closed:
            pts = [(v[0], v[1]) for v in e.get_points()]
            poly = Polygon(pts)
            if poly.is_valid and poly.area > 0:
                bounds = poly.bounds
                room_xs.extend([bounds[0], bounds[2]])
                room_ys.extend([bounds[1], bounds[3]])
                room_count += 1
    except Exception:
        pass

if room_xs:
    room_minx, room_maxx = min(room_xs), max(room_xs)
    room_miny, room_maxy = min(room_ys), max(room_ys)
    room_centerx = (room_minx + room_maxx) / 2
    room_centery = (room_miny + room_maxy) / 2
    
    print(f"📦 Rooms (00_VAV_ZONE layer):")
    print(f"   Count: {room_count}")
    print(f"   Bounds: X:[{room_minx:.0f}, {room_maxx:.0f}], Y:[{room_miny:.0f}, {room_maxy:.0f}]")
    print(f"   Center: ({room_centerx:.0f}, {room_centery:.0f})")

# 2. Get main drawing bounds (from all architectural layers)
main_xs = []
main_ys = []
entity_count = 0

for e in msp:
    try:
        layer = e.dxf.layer.upper()
        # Skip room layers
        if layer in ["00_VAV_ZONE", "E-FIRE"]:
            continue
            
        dxftype = e.dxftype()
        
        if dxftype == "LINE":
            main_xs.extend([e.dxf.start.x, e.dxf.end.x])
            main_ys.extend([e.dxf.start.y, e.dxf.end.y])
            entity_count += 1
        elif dxftype == "LWPOLYLINE":
            for v in e.get_points():
                main_xs.append(v[0])
                main_ys.append(v[1])
            entity_count += 1
    except Exception:
        pass

if main_xs:
    main_minx, main_maxx = min(main_xs), max(main_xs)
    main_miny, main_maxy = min(main_ys), max(main_ys)
    main_centerx = (main_minx + main_maxx) / 2
    main_centery = (main_miny + main_maxy) / 2
    
    print(f"\n🏢 Main drawing (all other layers):")
    print(f"   Entities: {entity_count}")
    print(f"   Bounds: X:[{main_minx:.0f}, {main_maxx:.0f}], Y:[{main_miny:.0f}, {main_maxy:.0f}]")
    print(f"   Center: ({main_centerx:.0f}, {main_centery:.0f})")
    
    # 3. Calculate offset
    offset_x = main_centerx - room_centerx
    offset_y = main_centery - room_centery
    
    print(f"\n✅ RECOMMENDED OFFSET:")
    print(f"   --offset-x {offset_x:.0f} --offset-y {offset_y:.0f}")
    print(f"\n📋 Full command:")
    print(f'   python3 smoke_detector_placer.py "RCP-FO10,11,12,16-AR-1.dxf" \\')
    print(f'       --offset-x {offset_x:.0f} --offset-y {offset_y:.0f} \\')
    print(f'       --rooms-layer 00_VAV_ZONE')


