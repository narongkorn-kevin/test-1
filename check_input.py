#!/usr/bin/env python3
"""Check if input file already has smoke detectors"""

import ezdxf

# Read the INPUT file
doc = ezdxf.readfile("RCP-FO10,11,12,16-AR-1.dxf")
msp = doc.modelspace()

print("=" * 70)
print("🔍 CHECKING INPUT FILE: RCP-FO10,11,12,16-AR-1.dxf")
print("=" * 70)

# Check for existing smoke detector symbols
existing_detectors = 0
for e in msp:
    try:
        if e.dxftype() == "INSERT":
            if "SMOKE" in e.dxf.name.upper():
                existing_detectors += 1
    except Exception:
        pass

if existing_detectors > 0:
    print(f"\n⚠️  INPUT FILE ALREADY HAS {existing_detectors} SMOKE DETECTORS!")
    print(f"    This is why you see many detectors in wrong positions.")
    print(f"\n💡 Solution: Use the original file WITHOUT detectors,")
    print(f"    or the program should create output with a different name.")
else:
    print(f"\n✅ Input file is clean (no existing detectors)")

# List all block definitions
print(f"\n📦 BLOCK DEFINITIONS in input file:")
block_count = 0
for blk_name in doc.blocks:
    if "SMOKE" in blk_name.upper() or "DET" in blk_name.upper():
        print(f"   - {blk_name}")
        block_count += 1

if block_count == 0:
    print(f"   (No smoke detector blocks found)")

# Check all INSERT entities
print(f"\n📍 INSERT ENTITIES (first 20):")
insert_count = 0
for e in msp:
    try:
        if e.dxftype() == "INSERT":
            insert_count += 1
            if insert_count <= 20:
                print(f"   {insert_count}. {e.dxf.name} at ({e.dxf.insert.x:.0f}, {e.dxf.insert.y:.0f})")
    except Exception:
        pass

print(f"\n   Total INSERT entities: {insert_count}")

print("\n" + "=" * 70)


