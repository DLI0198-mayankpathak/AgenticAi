@echo off
REM ============================================================
REM   Quick Start - Jira Analysis Agent API
REM   Double-click this file to start the API server
REM ============================================================

cd /d "%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.9+
    pause
    exit /b 1
)

REM Check if virtual environment exists
if exist ".venv\Scripts\activate.bat" (
    echo 🔧 Activating virtual environment...
    call .venv\Scripts\activate.bat
)

REM Install dependencies if needed
echo 📦 Checking dependencies...
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo 📥 Installing required packages...
    pip install -r requirements.txt
)

REM Start the API
echo.
python start.py

pause
