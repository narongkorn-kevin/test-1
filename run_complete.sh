#!/bin/bash
# Complete workflow: Clean + Place detectors

if [ -z "$1" ]; then
    echo "🔥 Smoke Detector Complete Workflow"
    echo ""
    echo "Usage: ./run_complete.sh input.dxf"
    echo ""
    echo "This script will:"
    echo "  1. Clean old detectors from input file"
    echo "  2. Place new detectors in correct positions"
    echo ""
    exit 1
fi

INPUT_FILE="$1"
BASENAME=$(basename "$INPUT_FILE" .dxf)
DIRNAME=$(dirname "$INPUT_FILE")
CLEAN_FILE="${DIRNAME}/${BASENAME}_clean.dxf"
OUTPUT_FILE="${DIRNAME}/${BASENAME}_clean_with_detectors.dxf"

echo "============================================================"
echo "🔥 Smoke Detector Complete Workflow"
echo "============================================================"
echo ""
echo "📁 Input file: $INPUT_FILE"
echo ""

# Step 1: Clean
echo "Step 1/2: Cleaning old detectors..."
python3 clean_detectors.py "$INPUT_FILE"

if [ $? -ne 0 ]; then
    echo "❌ Cleaning failed!"
    exit 1
fi

echo ""

# Step 2: Place detectors with AUTO DETECTION
echo "Step 2/2: Placing new detectors (AUTO MODE)..."
python3 smoke_detector_placer.py "$CLEAN_FILE" --no-pdf

if [ $? -ne 0 ]; then
    echo "❌ Placement failed!"
    exit 1
fi

echo ""
echo "============================================================"
echo "✅ SUCCESS!"
echo "============================================================"
echo ""
echo "📂 Output file:"
echo "   $OUTPUT_FILE"
echo ""
echo "💡 Open this file in AutoCAD/DWG viewer"
echo ""
echo "📊 Files created:"
echo "   1. ${BASENAME}_clean.dxf (cleaned input)"
echo "   2. ${BASENAME}_clean_with_detectors.dxf (final output)"
echo ""
echo "============================================================"

