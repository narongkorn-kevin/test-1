@echo off
REM ========================================================================
REM Smoke Detector Auto-Placer - GUI Launcher (Windows)
REM ========================================================================

echo.
echo Starting Smoke Detector Auto-Placer GUI...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher from python.org
    pause
    exit /b 1
)

REM Run the GUI
python smoke_detector_gui.py

if errorlevel 1 (
    echo.
    echo Error: Failed to start GUI
    echo Please check that all dependencies are installed:
    echo    pip install -r requirements.txt
    pause
    exit /b 1
)

