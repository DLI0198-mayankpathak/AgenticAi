@echo off
echo ================================================
echo   Starting Jira Analysis Agent Web API
echo ================================================
echo.
echo API will be available at: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
echo Endpoints:
echo   GET  /           - Health check
echo   GET  /health     - Service health
echo   POST /analyze    - Analyze Jira issue
echo.
echo Press Ctrl+C to stop the server
echo ================================================
echo.

REM Auto-start: Change directory and run the API
cd /d "%~dp0"
python web_api.py
