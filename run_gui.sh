#!/bin/bash
################################################################################
# 🔥 Smoke Detector Auto-Placer - GUI Launcher
################################################################################

echo ""
echo "🔥 Starting Smoke Detector Auto-Placer GUI..."
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    echo "   Please install Python 3.7 or higher"
    exit 1
fi

# Run the GUI
python3 smoke_detector_gui.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Failed to start GUI"
    echo "   Please check that all dependencies are installed:"
    echo "   pip install -r requirements.txt"
    exit 1
fi

