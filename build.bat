@echo off
echo Building PrefixeNamerApp executable...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Activate virtual environment if it exists
if exist "appenv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call appenv\Scripts\activate.bat
) else (
    echo No virtual environment found, using system Python
)

REM Install/upgrade required packages
echo Installing required packages...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install packages
    pause
    exit /b 1
)

REM Clean previous builds
echo Cleaning previous builds...
if exist "dist" rmdir /s /q dist
if exist "build" rmdir /s /q build

REM Build the executable
echo Building executable...
pyinstaller build_exe.spec
if errorlevel 1 (
    echo Error: Build failed
    pause
    exit /b 1
)

echo.
echo Build completed successfully!
echo The executable is located in: dist\PrefixeNamerApp.exe
echo.
pause 