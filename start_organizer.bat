@echo off
:: ---------------------------------------------------------
:: Windows Launcher for Python File Organizer
:: ---------------------------------------------------------

:: 1. Navigate to the folder where this batch file is located
:: (%~dp0 is a variable that stands for "Drive and Path of script")
cd /d "%~dp0"

:: 2. Check if python is installed (Optional debug check)
where pythonw >nul 2>nul
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH.
    pause
    exit /b
)

:: 3. Run the script silently in the background
:: "start" launches a separate process so this window can close
start "" pythonw organizer.py

exit