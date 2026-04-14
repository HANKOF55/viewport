#!/bin/bash
# Build script for macOS

echo "Building Linux Spacedesk Clone for macOS..."

# Check if PyInstaller is installed
if ! command -v pyinstaller &> /dev/null; then
    echo "PyInstaller not found. Installing..."
    pip install pyinstaller
fi

# Create executable
echo "Creating executable..."
pyinstaller --onefile --windowed --name linux-spacedesk main.py

# Create GUI executable
echo "Creating GUI executable..."
pyinstaller --onefile --windowed --name linux-spacedesk-gui gui.py

echo "Build complete!"
echo "Executables created in dist/ directory"
echo "Run: ./dist/linux-spacedesk-gui"