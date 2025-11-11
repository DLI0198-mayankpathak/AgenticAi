# 🚀 GitHub Deployment Guide for Jira Analysis Agent

This guide will help you deploy the Jira Analysis Agent API using GitHub as your code repository and various cloud platforms for hosting.

## 📋 Prerequisites

1. GitHub account
2. Code pushed to a GitHub repository
3. Environment variables ready:
   - `JIRA_BASE_URL`
   - `JIRA_USERNAME`
   - `JIRA_API_TOKEN`

## 🎯 Quick Start - Push to GitHub

### Step 1: Initialize Git Repository (if not done)

```bash
# Navigate to your project
cd d:\DEV\AgenticAi

# Initialize git (if not already initialized)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Jira Analysis Agent API"
```

### Step 2: Create GitHub Repository

1. Go to [GitHub](https://github.com)
2. Click "+" → "New repository"
3. Name it: `jira-analysis-agent` (or your preferred name)
4. Choose public or private
5. **DO NOT** initialize with README (you already have one)
6. Click "Create repository"

### Step 3: Push to GitHub

```bash
# Add remote origin (replace USERNAME and REPO)
git remote add origin https://github.com/USERNAME/REPO.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## 🐳 Deployment Options from GitHub

### Option 1: GitHub Container Registry + Cloud Run (Recommended)

This uses GitHub Actions to build Docker images and deploy to various platforms.

**Setup:**

1. **Enable GitHub Actions** (already configured in `.github/workflows/docker-publish.yml`)
2. **Push to main branch** - triggers automatic Docker image build
3. **Image is published to**: `ghcr.io/USERNAME/REPO:main`

**Deploy to Cloud Run:**

```bash
# Pull the image from GitHub Container Registry
docker pull ghcr.io/USERNAME/REPO:main

# Deploy to Google Cloud Run
gcloud run deploy jira-agent \
  --image ghcr.io/USERNAME/REPO:main \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="JIRA_BASE_URL=https://your-jira.atlassian.net,JIRA_USERNAME=your@email.com,JIRA_API_TOKEN=your_token"
```

### Option 2: Railway.app (Easiest - No Config Needed)

Railway automatically detects Dockerfile and deploys.

**Setup:**

1. Go to [Railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Authorize Railway to access your repository
5. Select your repository
6. Railway auto-detects Dockerfile and deploys
7. Add environment variables in Railway dashboard:
   - `JIRA_BASE_URL`
   - `JIRA_USERNAME`
   - `JIRA_API_TOKEN`
8. Get your URL: `https://your-app.up.railway.app`

**Or use GitHub Action:**

1. Get Railway token from [Railway dashboard](https://railway.app/account/tokens)
2. Add to GitHub Secrets:
   - Go to repo → Settings → Secrets and variables → Actions
   - Add secret: `RAILWAY_TOKEN`
3. Trigger workflow: Actions → "Deploy to Railway" → Run workflow

### Option 3: Azure App Service from GitHub

**Setup:**

1. **Create Azure Web App:**

   ```bash
   # Login to Azure
   az login
   
   # Create resource group
   az group create --name jira-agent-rg --location eastus
   
   # Create app service plan
   az appservice plan create --name jira-agent-plan --resource-group jira-agent-rg --is-linux --sku B1
   
   # Create web app
   az webapp create --resource-group jira-agent-rg --plan jira-agent-plan --name jira-agent-api --runtime "PYTHON:3.9"
   ```

2. **Configure GitHub Deployment:**

   - Go to Azure Portal → Your Web App → Deployment Center
   - Select "GitHub" as source
   - Authorize and select repository
   - Azure creates GitHub Action automatically

3. **Set Environment Variables:**

   ```bash
   az webapp config appsettings set --resource-group jira-agent-rg --name jira-agent-api --settings \
     JIRA_BASE_URL="https://your-jira.atlassian.net" \
     JIRA_USERNAME="your@email.com" \
     JIRA_API_TOKEN="your_token"
   ```

4. **Access:** `https://jira-agent-api.azurewebsites.net`

**Or use GitHub Action:**

1. Download publish profile from Azure Portal → Your Web App → Get publish profile
2. Add to GitHub Secrets as `AZURE_WEBAPP_PUBLISH_PROFILE`
3. Trigger workflow: Actions → "Deploy to Azure App Service" → Run workflow

### Option 4: AWS Elastic Beanstalk from GitHub

**Setup:**

1. **Create Elastic Beanstalk Application:**

   ```bash
   # Install EB CLI
   pip install awsebcli
   
   # Initialize EB
   eb init -p docker jira-agent-api --region us-east-1
   
   # Create environment
   eb create jira-agent-env
   
   # Set environment variables
   eb setenv JIRA_BASE_URL="https://your-jira.atlassian.net" \
     JIRA_USERNAME="your@email.com" \
     JIRA_API_TOKEN="your_token"
   ```

2. **Configure GitHub Action:**

   - Add AWS credentials to GitHub Secrets:
     - `AWS_ACCESS_KEY_ID`
     - `AWS_SECRET_ACCESS_KEY`
   - Use AWS deployment action (create workflow if needed)

3. **Access:** `http://jira-agent-env.REGION.elasticbeanstalk.com`

### Option 5: Heroku from GitHub

**Setup:**

1. **Create Heroku App:**

   ```bash
   # Install Heroku CLI
   # Windows: Download from https://devcenter.heroku.com/articles/heroku-cli
   
   # Login
   heroku login
   
   # Create app
   heroku create jira-agent-api
   
   # Add container registry
   heroku container:login
   ```

2. **Connect GitHub:**

   - Go to Heroku Dashboard → Your App → Deploy
   - Select "GitHub" as deployment method
   - Connect to repository
   - Enable automatic deploys from main branch

3. **Set Environment Variables:**

   ```bash
   heroku config:set JIRA_BASE_URL="https://your-jira.atlassian.net" \
     JIRA_USERNAME="your@email.com" \
     JIRA_API_TOKEN="your_token" \
     --app jira-agent-api
   ```

4. **Access:** `https://jira-agent-api.herokuapp.com`

## 🔒 Security Best Practices

### 1. Never Commit Secrets

Your `.gitignore` already excludes `.env` files. Make sure it stays that way!

### 2. Use GitHub Secrets for CI/CD

Store sensitive values in GitHub repository secrets:

- Go to repo → Settings → Secrets and variables → Actions
- Add secrets:
  - `JIRA_BASE_URL`
  - `JIRA_USERNAME`
  - `JIRA_API_TOKEN`
  - `RAILWAY_TOKEN` (if using Railway)
  - `AZURE_WEBAPP_PUBLISH_PROFILE` (if using Azure)
  - `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` (if using AWS)

### 3. Use Environment-Specific Branches

Consider using branches for different environments:
- `main` → Production
- `staging` → Staging/Testing
- `dev` → Development

## 📊 Monitoring Your Deployment

### Check Deployment Status

1. **GitHub Actions:**
   - Go to your repo → Actions tab
   - View workflow runs and logs

2. **Platform Dashboards:**
   - Railway: [railway.app/dashboard](https://railway.app/dashboard)
   - Azure: [portal.azure.com](https://portal.azure.com)
   - Heroku: [dashboard.heroku.com](https://dashboard.heroku.com)
   - AWS: [console.aws.amazon.com](https://console.aws.amazon.com)

### Test Your API

```bash
# Health check
curl https://your-deployed-url.com/

# Test analysis
curl -X POST https://your-deployed-url.com/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "issue_id": "DL-123",
    "language": "BE",
    "max_hours": 4.0
  }'
```

## 🔄 Continuous Deployment Workflow

Once set up, your workflow is:

1. **Make changes locally**
2. **Commit and push to GitHub:**
   ```bash
   git add .
   git commit -m "Add new feature"
   git push origin main
   ```
3. **GitHub Action automatically:**
   - Builds Docker image
   - Pushes to container registry
   - Deploys to your platform (if configured)
4. **Your API is updated!** ✅

## 🆘 Troubleshooting

### Build Fails
- Check GitHub Actions logs
- Ensure Dockerfile is valid
- Verify requirements.txt has all dependencies

### Deployment Fails
- Verify environment variables are set
- Check platform-specific logs
- Ensure your account has proper permissions

### API Not Responding
- Check if container is running
- Verify port 8000 is exposed
- Check platform logs for errors

## 📞 Support

- **GitHub Issues:** Create issue in your repository
- **Platform Docs:**
  - [Railway Docs](https://docs.railway.app)
  - [Azure Docs](https://docs.microsoft.com/azure)
  - [Heroku Docs](https://devcenter.heroku.com)
  - [AWS Docs](https://docs.aws.amazon.com)

## 🎉 Quick Deploy Summary

**Fastest path to production:**

1. Push code to GitHub ✅ (already done if you're reading this)
2. Go to [Railway.app](https://railway.app)
3. Deploy from GitHub repo (2 clicks)
4. Add environment variables (3 variables)
5. Get your URL and start using! 🚀

**Total time:** < 5 minutes
