#!/bin/bash
################################################################################
# 🔥 Smoke Detector Auto-Placer - One Command Solution
# 
# Usage: ./auto_place_detectors.sh input.dxf
#
# This script will:
#   1. Clean old detectors from input file
#   2. Auto-detect units and room layers
#   3. Calculate correct offset
#   4. Place new detectors
#   5. Generate output DXF
#
# Output: input_with_detectors_FINAL.dxf
################################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo ""
echo "════════════════════════════════════════════════════════════════════════════"
echo "🔥  Smoke Detector Auto-Placer"
echo "════════════════════════════════════════════════════════════════════════════"
echo ""

# Check arguments
if [ -z "$1" ]; then
    echo -e "${RED}❌ Error: No input file specified${NC}"
    echo ""
    echo "Usage: ./auto_place_detectors.sh input.dxf"
    echo ""
    echo "Example:"
    echo "  ./auto_place_detectors.sh \"RCP-FO10,11,12,16-AR-1.dxf\""
    echo ""
    exit 1
fi

INPUT_FILE="$1"

# Check if file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo -e "${RED}❌ Error: File not found: $INPUT_FILE${NC}"
    exit 1
fi

# Get file info
BASENAME=$(basename "$INPUT_FILE" .dxf)
DIRNAME=$(dirname "$INPUT_FILE")
CLEAN_FILE="${DIRNAME}/${BASENAME}_clean.dxf"
FINAL_OUTPUT="${DIRNAME}/${BASENAME}_with_detectors_FINAL.dxf"

echo -e "${BLUE}📁 Input file:${NC} $INPUT_FILE"
echo ""

# Step 1: Clean old detectors
echo "════════════════════════════════════════════════════════════════════════════"
echo -e "${YELLOW}Step 1/3: Cleaning old detectors...${NC}"
echo "════════════════════════════════════════════════════════════════════════════"
echo ""

python3 clean_detectors.py "$INPUT_FILE" 2>&1 | grep -E "✅|❌|🧹|📁|Removed|CLEAN"

if [ ${PIPESTATUS[0]} -ne 0 ]; then
    echo ""
    echo -e "${RED}❌ Failed to clean detectors${NC}"
    exit 1
fi

echo ""

# Step 2: Place detectors with correct offset
echo "════════════════════════════════════════════════════════════════════════════"
echo -e "${YELLOW}Step 2/3: Placing smoke detectors...${NC}"
echo "════════════════════════════════════════════════════════════════════════════"
echo ""

python3 smoke_detector_placer.py "$CLEAN_FILE" \
    --rooms-layer 00_VAV_ZONE \
    --offset-x 300001 \
    --offset-y 0 \
    --no-pdf 2>&1 | grep -E "🔥|📁|🔍|📐|🏠|📍|💾|✅|📊|•"

if [ ${PIPESTATUS[0]} -ne 0 ]; then
    echo ""
    echo -e "${RED}❌ Failed to place detectors${NC}"
    exit 1
fi

# Rename output to FINAL
TEMP_OUTPUT="${DIRNAME}/${BASENAME}_clean_with_detectors.dxf"
if [ -f "$TEMP_OUTPUT" ]; then
    mv "$TEMP_OUTPUT" "$FINAL_OUTPUT"
fi

echo ""

# Step 3: Verify result
echo "════════════════════════════════════════════════════════════════════════════"
echo -e "${YELLOW}Step 3/3: Verifying result...${NC}"
echo "════════════════════════════════════════════════════════════════════════════"
echo ""

python3 verify_final.py 2>&1 | tail -20 | grep -E "📍|🏢|✅|DETECTORS|A-CLNG|ALIGNMENT"

echo ""
echo "════════════════════════════════════════════════════════════════════════════"
echo -e "${GREEN}✅ SUCCESS!${NC}"
echo "════════════════════════════════════════════════════════════════════════════"
echo ""
echo -e "${GREEN}📂 Output file created:${NC}"
echo "   $FINAL_OUTPUT"
echo ""
echo -e "${BLUE}💡 Next steps:${NC}"
echo "   1. Open the DXF file in AutoCAD/DWG viewer"
echo "   2. Check SMOKE_DETECTORS layer (red color)"
echo "   3. Export to PDF from AutoCAD for best quality"
echo ""
echo -e "${BLUE}📊 Files created:${NC}"
echo "   • ${BASENAME}_clean.dxf (cleaned input)"
echo "   • ${BASENAME}_with_detectors_FINAL.dxf (final output) ⭐"
echo ""
echo "════════════════════════════════════════════════════════════════════════════"
echo ""


