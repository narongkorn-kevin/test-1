#!/usr/bin/env python3
"""Remove all smoke detectors from a DXF file"""

import sys
import ezdxf
from pathlib import Path

if len(sys.argv) < 2:
    print("Usage: python3 clean_detectors.py input.dxf")
    print("")
    print("This will create: input_clean.dxf")
    print("(Original file will NOT be modified)")
    sys.exit(1)

input_path = Path(sys.argv[1])
if not input_path.exists():
    print(f"❌ File not found: {input_path}")
    sys.exit(1)

# Create clean output filename
output_path = input_path.parent / f"{input_path.stem}_clean.dxf"

print("=" * 70)
print("🧹 CLEANING SMOKE DETECTORS FROM DXF")
print("=" * 70)
print(f"📁 Input:  {input_path}")
print(f"📁 Output: {output_path}")
print("")

# Read file
doc = ezdxf.readfile(input_path.as_posix())
msp = doc.modelspace()

# Count and remove smoke detector INSERTs
removed_count = 0
to_remove = []

for e in msp:
    try:
        if e.dxftype() == "INSERT":
            block_name = e.dxf.name.upper()
            if "SMOKE" in block_name or "DET" in block_name or "SD" in block_name:
                to_remove.append(e)
                removed_count += 1
    except Exception:
        pass

# Remove entities
for e in to_remove:
    try:
        msp.delete_entity(e)
    except Exception:
        pass

print(f"✅ Removed {removed_count} smoke detector symbols")

# Remove smoke detector layer if it exists
try:
    if "SMOKE_DETECTORS" in doc.layers:
        doc.layers.remove("SMOKE_DETECTORS")
        print(f"✅ Removed SMOKE_DETECTORS layer")
except Exception:
    pass

# Remove smoke detector blocks if they exist
blocks_removed = 0
try:
    for blk_name in doc.blocks:
        blk_name_str = str(blk_name)
        if "SMOKE" in blk_name_str.upper() or "SD" in blk_name_str.upper():
            try:
                doc.blocks.delete_block(blk_name_str, safe=False)
                blocks_removed += 1
            except Exception:
                pass
except Exception:
    pass

if blocks_removed > 0:
    print(f"✅ Removed {blocks_removed} smoke detector block definitions")

# Save clean file
doc.saveas(output_path.as_posix())

print("")
print("=" * 70)
print("✅ CLEAN FILE CREATED")
print("=" * 70)
print(f"📁 {output_path}")
print("")
print("Now you can run:")
print(f'   python3 smoke_detector_placer.py "{output_path.name}"')
print("=" * 70)

