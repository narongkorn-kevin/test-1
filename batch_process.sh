#!/bin/bash
################################################################################
# 🔥 Smoke Detector Auto-Placer - Batch Processing
# 
# Usage: ./batch_process.sh *.dxf
#        ./batch_process.sh file1.dxf file2.dxf file3.dxf
#
# Processes multiple DXF files at once
################################################################################

if [ $# -eq 0 ]; then
    echo "Usage: ./batch_process.sh file1.dxf file2.dxf ..."
    echo "   or: ./batch_process.sh *.dxf"
    exit 1
fi

TOTAL=$#
SUCCESS=0
FAILED=0

echo ""
echo "════════════════════════════════════════════════════════════════════════════"
echo "🔥 Smoke Detector Auto-Placer - Batch Mode"
echo "════════════════════════════════════════════════════════════════════════════"
echo ""
echo "Processing $TOTAL file(s)..."
echo ""

for file in "$@"; do
    echo "────────────────────────────────────────────────────────────────────────────"
    echo "Processing: $file"
    echo "────────────────────────────────────────────────────────────────────────────"
    
    if ./auto_place_detectors.sh "$file"; then
        SUCCESS=$((SUCCESS + 1))
        echo "✅ Success: $file"
    else
        FAILED=$((FAILED + 1))
        echo "❌ Failed: $file"
    fi
    
    echo ""
done

echo "════════════════════════════════════════════════════════════════════════════"
echo "📊 Batch Processing Complete"
echo "════════════════════════════════════════════════════════════════════════════"
echo ""
echo "Total files: $TOTAL"
echo "✅ Success: $SUCCESS"
echo "❌ Failed: $FAILED"
echo ""


