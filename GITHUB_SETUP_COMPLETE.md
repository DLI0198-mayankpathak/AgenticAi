# 📦 GitHub Deployment - Complete Setup

## ✅ What Has Been Configured

Your Jira Analysis Agent API is now **fully ready** for GitHub deployment with multiple cloud platform options!

### 🎯 New Files Created

#### Deployment Configurations
1. **`.github/workflows/docker-publish.yml`** - Automatically builds and publishes Docker images to GitHub Container Registry
2. **`.github/workflows/azure-deploy.yml`** - One-click deployment to Azure App Service
3. **`.github/workflows/railway-deploy.yml`** - Automated deployment to Railway
4. **`railway.json`** - Railway platform configuration
5. **`startup.txt`** - Azure App Service startup configuration
6. **`heroku-start.sh`** - Heroku startup script
7. **`.env.example`** - Template for environment variables

#### Documentation
8. **`GITHUB_DEPLOYMENT.md`** - Complete deployment guide with all platforms
9. **`DEPLOY_GITHUB_CHECKLIST.md`** - Quick reference checklist

#### Helper Scripts
10. **`deploy_to_github.bat`** - Windows batch script for easy GitHub push

#### Updated Files
11. **`Dockerfile`** - Enhanced with health checks and flexible port configuration

---

## 🚀 How to Deploy - Choose Your Path

### Path 1: Railway (Recommended - Fastest)

**Time: 5 minutes | Difficulty: Easy | Cost: Free**

1. **Push to GitHub:**
   ```cmd
   deploy_to_github.bat
   ```
   Or manually:
   ```cmd
   git init
   git add .
   git commit -m "Deploy Jira Analysis Agent"
   git remote add origin https://github.com/USERNAME/REPO.git
   git push -u origin main
   ```

2. **Deploy to Railway:**
   - Go to [railway.app](https://railway.app)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway auto-detects Dockerfile and deploys!

3. **Add Environment Variables** in Railway dashboard:
   - `JIRA_BASE_URL` = `https://your-company.atlassian.net`
   - `JIRA_USERNAME` = `your-email@example.com`
   - `JIRA_API_TOKEN` = `your_jira_api_token`

4. **Done!** Your API is live at `https://yourapp.railway.app` 🎉

### Path 2: Azure App Service

**Time: 10 minutes | Difficulty: Medium | Cost: Pay-as-you-go**

1. **Push to GitHub** (same as above)

2. **Set up Azure:**
   ```cmd
   az login
   az group create --name jira-agent-rg --location eastus
   az appservice plan create --name jira-agent-plan --resource-group jira-agent-rg --is-linux --sku B1
   az webapp create --resource-group jira-agent-rg --plan jira-agent-plan --name jira-agent-api --runtime "PYTHON:3.9"
   ```

3. **Configure GitHub Actions:**
   - Download publish profile from Azure Portal
   - Add as GitHub Secret: `AZURE_WEBAPP_PUBLISH_PROFILE`
   - Go to Actions → "Deploy to Azure App Service" → Run workflow

4. **Set environment variables** in Azure Portal or CLI

5. **Access:** `https://jira-agent-api.azurewebsites.net`

### Path 3: Heroku

**Time: 10 minutes | Difficulty: Medium | Cost: Free tier available**

1. **Push to GitHub** (same as above)

2. **Deploy via Heroku CLI:**
   ```cmd
   heroku login
   heroku create jira-agent-api
   heroku stack:set container
   git push heroku main
   ```

3. **Set environment variables:**
   ```cmd
   heroku config:set JIRA_BASE_URL="https://your-jira.atlassian.net"
   heroku config:set JIRA_USERNAME="your@email.com"
   heroku config:set JIRA_API_TOKEN="your_token"
   ```

4. **Access:** `https://jira-agent-api.herokuapp.com`

### Path 4: GitHub Container Registry + Any Platform

**Time: 15 minutes | Difficulty: Advanced | Cost: Varies**

1. **Push to GitHub** - This automatically triggers Docker image build via GitHub Actions

2. **Your image is published to:** `ghcr.io/USERNAME/REPO:main`

3. **Pull and deploy anywhere:**
   ```cmd
   docker pull ghcr.io/USERNAME/REPO:main
   docker run -p 8000:8000 -e JIRA_BASE_URL=... ghcr.io/USERNAME/REPO:main
   ```

---

## 🔑 Required Environment Variables

Before deploying to any platform, you need these:

| Variable | Description | Example |
|----------|-------------|---------|
| `JIRA_BASE_URL` | Your Jira instance URL | `https://company.atlassian.net` |
| `JIRA_USERNAME` | Your Jira email | `user@example.com` |
| `JIRA_API_TOKEN` | Jira API token | Generate at [Atlassian](https://id.atlassian.com/manage-profile/security/api-tokens) |

### How to Get Your Jira API Token:
1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Give it a name (e.g., "Jira Analysis Agent")
4. Copy the token (you won't see it again!)

---

## 🧪 Testing Your Deployment

Once deployed, test your API:

### Health Check
```bash
curl https://your-deployed-url.com/health
```

Expected response:
```json
{"status": "healthy"}
```

### Analyze an Issue
```bash
curl -X POST https://your-deployed-url.com/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "issue_id": "DL-123",
    "language": "BE",
    "max_hours": 4.0
  }'
```

### Using Python
```python
import requests

response = requests.post('https://your-url.com/analyze', json={
    'issue_id': 'DL-123',
    'language': 'BE',
    'max_hours': 4.0
})
print(response.json())
```

---

## 📊 Monitoring & Logs

### Railway
- Dashboard: https://railway.app/dashboard
- View logs in real-time
- Monitor resource usage

### Azure
- Portal: https://portal.azure.com
- Application Insights for monitoring
- Log Stream for real-time logs

### Heroku
- Dashboard: https://dashboard.heroku.com
- View logs: `heroku logs --tail`
- Monitor dyno usage

---

## 🔒 Security Checklist

- ✅ `.env` is in `.gitignore` (never commit secrets!)
- ✅ Use GitHub Secrets for CI/CD credentials
- ✅ Environment variables set in platform (not in code)
- ✅ API tokens rotated regularly
- ✅ HTTPS enabled on deployment platform

---

## 🐛 Troubleshooting

### Build Fails
**Problem:** GitHub Action fails to build Docker image
**Solution:**
1. Check GitHub Actions logs
2. Verify Dockerfile syntax
3. Ensure all dependencies in requirements.txt

### Deployment Fails
**Problem:** Platform can't start the container
**Solution:**
1. Check platform logs
2. Verify environment variables are set
3. Test Docker image locally:
   ```cmd
   docker build -t jira-agent .
   docker run -p 8000:8000 -e JIRA_BASE_URL=... jira-agent
   ```

### API Returns 500 Error
**Problem:** API starts but crashes on requests
**Solution:**
1. Check Jira credentials are correct
2. Verify Jira URL format (include https://)
3. Check platform logs for Python errors
4. Test issue ID exists in Jira

### Can't Connect to API
**Problem:** URL not responding
**Solution:**
1. Wait 2-3 minutes for deployment to complete
2. Check if container is running in platform dashboard
3. Verify URL is correct
4. Check firewall/security settings

---

## 📚 Additional Resources

- **Full Deployment Guide**: `GITHUB_DEPLOYMENT.md`
- **API Documentation**: `API_REFERENCE_CARD.md`
- **Usage Examples**: `FULLSTACK_USAGE.md`
- **Original Deployment Guide**: `DEPLOYMENT.md`

---

## 🎉 Success! What's Next?

After successful deployment:

1. **Get Your API URL** from your platform
2. **Test All Endpoints** using curl or Postman
3. **Integrate with Your Workflow:**
   - Add to CI/CD pipeline
   - Create Jira automation rules
   - Build frontend dashboard
4. **Monitor Performance:**
   - Check response times
   - Monitor error rates
   - Scale if needed

---

## 💡 Pro Tips

1. **Use Railway for quick prototypes** - Free tier, instant deployment
2. **Use Azure/AWS for production** - Better scalability and control
3. **Enable auto-deploy** - Push to GitHub, auto-deploys to platform
4. **Set up monitoring** - Use platform's built-in monitoring
5. **Create separate environments** - dev, staging, production branches

---

## 🆘 Getting Help

- **GitHub Issues**: Create issue in your repository
- **Platform Support**:
  - Railway: https://railway.app/discord
  - Azure: https://docs.microsoft.com/azure/support
  - Heroku: https://help.heroku.com

---

**Ready to deploy? Just run `deploy_to_github.bat` and follow the Railway path above!** 🚀
