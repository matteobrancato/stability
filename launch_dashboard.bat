@echo off
REM Stability Dashboard Launcher
REM Double-click this file to start the dashboard

echo ================================================
echo     Stability Dashboard Launcher
echo ================================================
echo.

REM Change to script directory
cd /d "%~dp0"

echo Checking Python installation...
py --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo Python found!
echo.

echo Checking if Excel file is open...
echo IMPORTANT: Please close the Excel file if it's open!
echo Press any key when ready...
pause >nul

echo.
echo Starting Stability Dashboard...
echo.
echo The dashboard will open in your default browser.
echo.
echo To stop the dashboard, close this window or press Ctrl+C
echo.
echo ================================================
echo.

py -m streamlit run stability_dashboard.py

pause
