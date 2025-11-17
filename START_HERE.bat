@echo off
REM ============================================================
REM   Jira Analysis Agent - Quick Start
REM   Double-click to run the API!
REM ============================================================

echo.
echo ========================================
echo   Jira Analysis Agent - Standalone API
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo.
    echo Please install Python 3.9 or higher from:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Check and install dependencies
echo Checking dependencies...
python standalone_api.py

pause
