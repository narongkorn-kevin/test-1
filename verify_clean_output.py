#!/usr/bin/env python3
"""Verify the clean output file"""

import ezdxf

# Read the clean output file
doc = ezdxf.readfile("RCP-FO10,11,12,16-AR-1_clean_with_detectors.dxf")
msp = doc.modelspace()

print("=" * 70)
print("🔍 VERIFYING CLEAN OUTPUT FILE")
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
                if detector_count <= 10:
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
print(f"\n🏢 COMPARISON WITH ARCHITECTURAL LAYERS:")

arch_data = {}
for layer_name in ["I-WALL", "A-WALL"]:
    xs, ys = [], []
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
        except Exception:
            pass
    
    if xs:
        arch_data[layer_name] = {
            'minx': min(xs), 'maxx': max(xs),
            'miny': min(ys), 'maxy': max(ys),
            'centerx': (min(xs) + max(xs)) / 2,
            'centery': (min(ys) + max(ys)) / 2
        }

if arch_data and detector_xs:
    # Use I-WALL as reference
    ref = arch_data.get('I-WALL', arch_data.get('A-WALL'))
    
    print(f"\n  Reference layer: I-WALL")
    print(f"    X range: [{ref['minx']:.0f}, {ref['maxx']:.0f}]")
    print(f"    Y range: [{ref['miny']:.0f}, {ref['maxy']:.0f}]")
    print(f"    Center: ({ref['centerx']:.0f}, {ref['centery']:.0f})")
    
    # Check alignment
    det_in_arch_x = ref['minx'] <= centerx <= ref['maxx']
    det_in_arch_y = ref['miny'] <= centery <= ref['maxy']
    
    print(f"\n✨ ALIGNMENT CHECK:")
    if det_in_arch_x and det_in_arch_y:
        print(f"   ✅ Detectors are WITHIN architectural bounds!")
        print(f"   ✅ Placement looks CORRECT! 🎉")
    else:
        print(f"   ❌ Detector center is OUTSIDE architectural bounds")
        print(f"      X aligned: {'✅' if det_in_arch_x else '❌'}")
        print(f"      Y aligned: {'✅' if det_in_arch_y else '❌'}")

print("\n" + "=" * 70)


