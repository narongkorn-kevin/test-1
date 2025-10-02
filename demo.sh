#!/bin/bash
################################################################################
# 🔥 Smoke Detector Auto-Placer - Demo
# 
# This script demonstrates the program with the example file
################################################################################

echo ""
echo "════════════════════════════════════════════════════════════════════════════"
echo "🔥 Smoke Detector Auto-Placer - Demo"
echo "════════════════════════════════════════════════════════════════════════════"
echo ""
echo "This demo will process the example file: RCP-FO10,11,12,16-AR-1.dxf"
echo ""
read -p "Press ENTER to continue..."
echo ""

# Check if example file exists
if [ ! -f "RCP-FO10,11,12,16-AR-1.dxf" ]; then
    echo "❌ Example file not found!"
    echo "   Please make sure RCP-FO10,11,12,16-AR-1.dxf is in the current directory"
    exit 1
fi

# Run the main script
./auto_place_detectors.sh "RCP-FO10,11,12,16-AR-1.dxf"

# Show result
echo ""
echo "════════════════════════════════════════════════════════════════════════════"
echo "🎓 Demo Complete!"
echo "════════════════════════════════════════════════════════════════════════════"
echo ""
echo "Output file created:"
ls -lh RCP-FO10,11,12,16-AR-1_with_detectors_FINAL.dxf 2>/dev/null | awk '{print "  " $9 " (" $5 ")"}'
echo ""
echo "Try it yourself with your own DXF file:"
echo "  ./auto_place_detectors.sh your_file.dxf"
echo ""


