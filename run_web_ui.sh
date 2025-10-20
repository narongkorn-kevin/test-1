#!/bin/bash
# Web UI Launcher for Smoke Detector Auto-Placer
# Usage: ./run_web_ui.sh

echo "🔥 Smoke Detector Auto-Placer - Web UI"
echo "======================================"
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    exit 1
fi

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ Error: pip3 is not installed"
    exit 1
fi

# Install dependencies if needed
echo "📦 Checking dependencies..."
pip3 install -r requirements.txt

# Make sure the script is executable
chmod +x run_web_ui.sh

echo ""
echo "🚀 Starting Web UI..."
echo "Open your browser and go to: http://localhost:8080"
echo ""
echo "Press Ctrl+C to stop the server"
echo "======================================"

# Run the Flask app
python3 app.py
