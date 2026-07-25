@echo off
title KSNDMC Daily Rainfall Status Auto-Updater
cd /d "%~dp0"
echo ============================================================
echo   Checking KSNDMC Website and Updating Rainfall Status...
echo ============================================================
python auto_update_rainfall.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] An error occurred while updating rainfall status.
    pause
)
