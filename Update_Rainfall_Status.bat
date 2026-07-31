@echo off
title KSNDMC Daily Rainfall Status Auto-Updater
cd /d "%~dp0"
echo ============================================================
echo   Checking KSNDMC Website, Updating & Syncing to GitHub...
echo ============================================================
python auto_update_rainfall.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] An error occurred while updating rainfall status.
    pause
    exit /b %ERRORLEVEL%
)
echo.
echo ============================================================
echo   [SUCCESS] Live Dashboard Updated on GitHub Pages!
echo   [LIVE URL] https://amith1994.github.io/Rainfall_status_of_Karnataka/
echo ============================================================
echo.
pause
