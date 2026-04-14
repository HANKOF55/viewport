@echo off
REM Build script for Windows

echo Building Linux Spacedesk Clone for Windows...

REM Check if PyInstaller is installed
pip install pyinstaller

REM Create executable
echo Creating executable...
pyinstaller --onefile --windowed --name linux-spacedesk main.py

REM Create GUI executable
echo Creating GUI executable...
pyinstaller --onefile --windowed --name linux-spacedesk-gui gui.py

echo Build complete!
echo Executables created in dist\ directory
echo Run: dist\linux-spacedesk-gui.exe