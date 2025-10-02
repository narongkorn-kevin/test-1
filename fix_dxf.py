#!/usr/bin/env python3
"""
Fix and validate DXF files before processing
"""

import sys
import ezdxf
from pathlib import Path

def fix_dxf(input_path):
    """Try to fix and validate DXF file"""
    input_path = Path(input_path)
    
    print("=" * 70)
    print("🔧 DXF File Fixer & Validator")
    print("=" * 70)
    print(f"📁 Input: {input_path}")
    print("")
    
    if not input_path.exists():
        print(f"❌ File not found: {input_path}")
        return False
    
    # Try different methods to read the file
    print("🔍 Attempting to read DXF file...")
    
    # Method 1: Normal read
    try:
        print("   Method 1: Normal read...")
        doc = ezdxf.readfile(str(input_path))
        print("   ✅ Success with normal read!")
        
        # Validate
        print("\n🔍 Validating file...")
        msp = doc.modelspace()
        entity_count = len(list(msp))
        print(f"   ✅ Found {entity_count} entities")
        
        return True
        
    except Exception as e1:
        print(f"   ❌ Failed: {e1}")
        
        # Method 2: Recover mode
        try:
            print("\n   Method 2: Recovery mode...")
            doc = ezdxf.recover.readfile(str(input_path))
            if doc:
                print("   ✅ Success with recovery mode!")
                
                # Save fixed version
                output_path = input_path.parent / f"{input_path.stem}_fixed.dxf"
                doc.saveas(str(output_path))
                print(f"\n   💾 Saved fixed version: {output_path.name}")
                print(f"\n   💡 Please use the fixed file instead:")
                print(f"      {output_path}")
                
                return True
        except Exception as e2:
            print(f"   ❌ Failed: {e2}")
    
    # All methods failed
    print("\n" + "=" * 70)
    print("❌ UNABLE TO READ DXF FILE")
    print("=" * 70)
    print("\n💡 Possible solutions:")
    print("   1. Open the file in AutoCAD/DWG viewer")
    print("   2. Save As → Choose DXF format → R2018 or newer")
    print("   3. Run AUDIT command in AutoCAD to fix errors")
    print("   4. Simplify the drawing (remove complex objects)")
    print("\nCommon causes:")
    print("   • File is corrupted")
    print("   • File uses very old DXF version")
    print("   • File contains unsupported entities")
    print("   • File has encoding issues")
    print("")
    
    return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 fix_dxf.py input.dxf")
        sys.exit(1)
    
    success = fix_dxf(sys.argv[1])
    sys.exit(0 if success else 1)

