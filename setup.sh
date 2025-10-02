#!/bin/bash
################################################################################
# 🔥 Smoke Detector Auto-Placer - Setup Script
# 
# Run this once to set up everything
################################################################################

echo ""
echo "════════════════════════════════════════════════════════════════════════════"
echo "🔥 Smoke Detector Auto-Placer - Setup"
echo "════════════════════════════════════════════════════════════════════════════"
echo ""

# Check Python
echo "Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    echo "   Please install Python 3.7 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python $PYTHON_VERSION found"
echo ""

# Check pip
echo "Checking pip..."
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo "❌ pip is not installed"
    exit 1
fi
echo "✅ pip found"
echo ""

# Install dependencies
echo "Installing dependencies..."
echo ""
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "Making scripts executable..."
chmod +x auto_place_detectors.sh
chmod +x batch_process.sh
chmod +x quick_start.sh
chmod +x run_complete.sh

echo "✅ Scripts are now executable"
echo ""

# Test installation
echo "Testing installation..."
echo ""
python3 -c "import ezdxf, shapely, numpy; print('✅ All Python packages installed correctly')"

if [ $? -ne 0 ]; then
    echo "❌ Some packages failed to import"
    exit 1
fi

# Test tkinter (for GUI)
echo ""
python3 -c "import tkinter; print('✅ Tkinter (GUI support) available')" 2>/dev/null

if [ $? -ne 0 ]; then
    echo "⚠️  Tkinter not available - GUI will not work"
    echo "   Command line interface will work fine"
    echo ""
    echo "   To enable GUI on macOS:"
    echo "   brew install python-tk@3.11"
    echo ""
    echo "   To enable GUI on Ubuntu/Debian:"
    echo "   sudo apt-get install python3-tk"
fi

echo ""
echo "════════════════════════════════════════════════════════════════════════════"
echo "✅ Setup Complete!"
echo "════════════════════════════════════════════════════════════════════════════"
echo ""
echo "You can now use the program:"
echo ""
echo "🖥️  GUI (Recommended):"
echo "  ./run_gui.sh"
echo ""
echo "⌨️  Command Line:"
echo "  ./auto_place_detectors.sh input.dxf"
echo ""
echo "📚 Documentation:"
echo "  cat GUI_GUIDE.md          # GUI guide"
echo "  cat QUICK_START.md        # Quick start"
echo "  cat README.md             # Full documentation"
echo ""
echo "════════════════════════════════════════════════════════════════════════════"
echo ""


