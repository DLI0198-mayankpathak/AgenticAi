@echo off
REM Quick Deploy to GitHub Script for Windows
REM This script helps you push your code to GitHub

echo.
echo ========================================
echo   GitHub Deployment Helper
echo ========================================
echo.

REM Check if git is initialized
if not exist ".git" (
    echo Initializing Git repository...
    git init
    git branch -M main
)

REM Add all files
echo Adding files to git...
git add .

REM Prompt for commit message
set /p commit_msg="Enter commit message (or press Enter for default): "
if "%commit_msg%"=="" set commit_msg="Update: Deploy to GitHub"

REM Commit changes
echo Committing changes...
git commit -m "%commit_msg%"

REM Check if remote exists
git remote -v | findstr origin >nul
if errorlevel 1 (
    echo.
    echo No remote repository configured.
    set /p repo_url="Enter your GitHub repository URL: "
    git remote add origin !repo_url!
)

REM Push to GitHub
echo.
echo Pushing to GitHub...
git push -u origin main

if errorlevel 0 (
    echo.
    echo ========================================
    echo   ✅ Successfully pushed to GitHub!
    echo ========================================
    echo.
    echo Next steps:
    echo 1. Go to https://railway.app to deploy
    echo 2. Or use GitHub Actions for automatic deployment
    echo 3. See GITHUB_DEPLOYMENT.md for detailed instructions
    echo.
) else (
    echo.
    echo ❌ Push failed. Please check:
    echo 1. GitHub repository URL is correct
    echo 2. You have push permissions
    echo 3. You're logged in to GitHub
    echo.
)

pause
