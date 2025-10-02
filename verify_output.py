#!/usr/bin/env python3
"""Verify the output file to see where detectors actually ended up"""

import ezdxf

# Read the output file
doc = ezdxf.readfile("RCP-FO10,11,12,16-AR-1_with_detectors.dxf")
msp = doc.modelspace()

print("=" * 70)
print("🔍 VERIFYING OUTPUT FILE")
print("=" * 70)

# Find smoke detector symbols
detector_xs = []
detector_ys = []
detector_count = 0

for e in msp:
    try:
        if e.dxftype() == "INSERT":
            if "SMOKE" in e.dxf.name.upper():
                x = e.dxf.insert.x
                y = e.dxf.insert.y
                detector_xs.append(x)
                detector_ys.append(y)
                detector_count += 1
                if detector_count <= 5:
                    print(f"  Detector {detector_count}: ({x:.0f}, {y:.0f})")
    except Exception:
        pass

if detector_xs:
    minx, maxx = min(detector_xs), max(detector_xs)
    miny, maxy = min(detector_ys), max(detector_ys)
    centerx = (minx + maxx) / 2
    centery = (miny + maxy) / 2
    
    print(f"\n📍 DETECTOR POSITIONS:")
    print(f"   Count: {detector_count}")
    print(f"   X range: [{minx:.0f}, {maxx:.0f}]")
    print(f"   Y range: [{miny:.0f}, {maxy:.0f}]")
    print(f"   Center: ({centerx:.0f}, {centery:.0f})")
else:
    print("\n❌ No smoke detectors found in output!")

# Compare with architectural layers
print(f"\n🏢 ARCHITECTURAL LAYERS:")
for layer_name in ["I-WALL", "A-WALL", "A-CLNG"]:
    xs, ys = [], []
    count = 0
    for e in msp.query("LINE LWPOLYLINE"):
        try:
            if e.dxf.layer.upper() == layer_name:
                if e.dxftype() == "LINE":
                    xs.extend([e.dxf.start.x, e.dxf.end.x])
                    ys.extend([e.dxf.start.y, e.dxf.end.y])
                elif e.dxftype() == "LWPOLYLINE":
                    for v in e.get_points():
                        xs.append(v[0])
                        ys.append(v[1])
                count += 1
        except Exception:
            pass
    
    if xs:
        minx, maxx = min(xs), max(xs)
        miny, maxy = min(ys), max(ys)
        centerx = (minx + maxx) / 2
        centery = (miny + maxy) / 2
        print(f"\n  {layer_name}:")
        print(f"    Entities: {count}")
        print(f"    X range: [{minx:.0f}, {maxx:.0f}]")
        print(f"    Y range: [{miny:.0f}, {maxy:.0f}]")
        print(f"    Center: ({centerx:.0f}, {centery:.0f})")

print("\n" + "=" * 70)


