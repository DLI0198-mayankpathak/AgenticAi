@echo off
echo ================================================
echo   Starting Jira Analysis Agent Web API
echo ================================================
echo.
echo API will be available at: http://localhost:8000
echo.
echo Endpoints:
echo   GET  /           - Health check
echo   GET  /health     - Service health
echo   POST /analyze    - Analyze Jira issue
echo.
echo Press Ctrl+C to stop the server
echo ================================================
echo.

D:\DEV\AgenticAi\.venv\Scripts\python.exe -m uvicorn web_api:app --host 0.0.0.0 --port 8000 --reload
