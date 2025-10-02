#!/bin/bash
# Quick Start Script for Smoke Detector Auto-Placer
# Usage: ./quick_start.sh input.dxf

if [ -z "$1" ]; then
    echo "🔥 Smoke Detector Auto-Placer - Quick Start"
    echo ""
    echo "Usage: ./quick_start.sh input.dxf"
    echo ""
    echo "Example:"
    echo "  ./quick_start.sh RCP-FO10,11,12,16-AR-1.dxf"
    echo ""
    echo "The program will automatically:"
    echo "  ✅ Detect units (m, mm, ft, in)"
    echo "  ✅ Find room layers"
    echo "  ✅ Calculate offset for proper alignment"
    echo "  ✅ Place smoke detectors per NFPA 72"
    echo "  ✅ Generate DXF with detectors"
    exit 1
fi

INPUT_FILE="$1"

if [ ! -f "$INPUT_FILE" ]; then
    echo "❌ Error: File not found: $INPUT_FILE"
    exit 1
fi

echo "============================================================"
echo "🔥 Smoke Detector Auto-Placer - Quick Start"
echo "============================================================"
echo ""
echo "📁 Input file: $INPUT_FILE"
echo ""
echo "Starting auto-placement..."
echo ""

# Run the smoke detector placer with no-pdf flag for speed
python3 smoke_detector_placer.py "$INPUT_FILE" --no-pdf

if [ $? -eq 0 ]; then
    echo ""
    echo "============================================================"
    echo "✅ SUCCESS! Output file created."
    echo "============================================================"
    echo ""
    echo "📂 Output file:"
    BASENAME=$(basename "$INPUT_FILE" .dxf)
    DIRNAME=$(dirname "$INPUT_FILE")
    OUTPUT_FILE="${DIRNAME}/${BASENAME}_with_detectors.dxf"
    echo "   $OUTPUT_FILE"
    echo ""
    echo "💡 Open this file in AutoCAD/DWG viewer to see the results."
    echo ""
else
    echo ""
    echo "❌ Error occurred. Please check the error message above."
    exit 1
fi
