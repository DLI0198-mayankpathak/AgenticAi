@echo off
echo.
echo ================================================================================
echo   📦 GitHub Deployment Files - Quick Reference
echo ================================================================================
echo.
echo GitHub Actions (Automated CI/CD):
echo   - .github\workflows\docker-publish.yml    [Auto-build Docker images]
echo   - .github\workflows\azure-deploy.yml      [Deploy to Azure]
echo   - .github\workflows\railway-deploy.yml    [Deploy to Railway]
echo.
echo Platform Configuration:
echo   - railway.json                            [Railway deployment config]
echo   - railway.toml                            [Railway settings]
echo   - startup.txt                             [Azure App Service startup]
echo   - heroku-start.sh                         [Heroku startup script]
echo   - Dockerfile                              [Docker containerization]
echo.
echo Documentation:
echo   - GITHUB_DEPLOYMENT.md                    [Complete deployment guide]
echo   - DEPLOY_GITHUB_CHECKLIST.md              [Quick checklist]
echo   - GITHUB_SETUP_COMPLETE.md                [Setup summary]
echo   - DEPLOYMENT_SUMMARY.txt                  [Quick reference]
echo.
echo Helper Scripts:
echo   - deploy_to_github.bat                    [Push to GitHub (this folder)]
echo   - show_deployment_files.bat               [This file]
echo.
echo Security:
echo   - .env.example                            [Environment variables template]
echo   - .gitignore                              [Prevents committing secrets]
echo.
echo ================================================================================
echo   🚀 READY TO DEPLOY!
echo ================================================================================
echo.
echo Quick Deploy Steps:
echo   1. Run: deploy_to_github.bat
echo   2. Go to: https://railway.app
echo   3. Deploy from GitHub (auto-detects Dockerfile)
echo   4. Add environment variables (JIRA credentials)
echo   5. Done! API is live
echo.
echo Need help? Read: GITHUB_DEPLOYMENT.md
echo.
pause
