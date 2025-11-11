# 🚀 Railway Deployment - Step by Step Guide

## ✅ Easy Way: Deploy via Railway Website (Recommended)

### Step 1: Sign up/Login to Railway
1. Go to **[railway.app](https://railway.app)**
2. Click "Login" and sign in with GitHub

### Step 2: Create New Project
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Authorize Railway to access your GitHub repositories (if first time)

### Step 3: Select Your Repository
1. Find and select: **`DLI0198-mayankpathak/AgenticAi`**
2. Railway will automatically detect your `Dockerfile`
3. Deployment starts automatically! ✨

### Step 4: Configure Environment Variables
Once deployed, add your Jira credentials:

1. In Railway dashboard, click on your service
2. Go to **"Variables"** tab
3. Add these variables:
   ```
   JIRA_BASE_URL     = https://your-company.atlassian.net
   JIRA_USERNAME     = your-email@example.com
   JIRA_API_TOKEN    = your_jira_api_token
   ```
4. Railway will automatically redeploy with new variables

### Step 5: Get Your URL
1. Go to **"Settings"** tab
2. Under **"Domains"**, click **"Generate Domain"**
3. Your API will be available at: `https://your-app.up.railway.app`

### Step 6: Test Your API
```bash
# Health check
curl https://your-app.up.railway.app/health

# Test analysis
curl -X POST https://your-app.up.railway.app/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "issue_id": "DL-123",
    "language": "BE",
    "max_hours": 4.0
  }'
```

---

## 🔧 Advanced: Deploy via Railway CLI

If you prefer using the command line:

### Step 1: Install Railway CLI

**Windows (PowerShell):**
```powershell
npm install -g @railway/cli
```

**Or download from:** https://docs.railway.app/develop/cli

### Step 2: Login to Railway
```bash
railway login
```
This opens a browser for authentication.

### Step 3: Link Your Project
```bash
cd d:\DEV\AgenticAi
railway link
```
Select your project or create a new one.

### Step 4: Set Environment Variables
```bash
railway variables set JIRA_BASE_URL="https://your-company.atlassian.net"
railway variables set JIRA_USERNAME="your-email@example.com"
railway variables set JIRA_API_TOKEN="your_jira_api_token"
```

### Step 5: Deploy
```bash
railway up
```

### Step 6: Open Your App
```bash
railway open
```

---

## 🔑 Get Your Jira API Token

1. Go to: https://id.atlassian.com/manage-profile/security/api-tokens
2. Click **"Create API token"**
3. Name it: **"Jira Analysis Agent"**
4. Copy the token (you won't see it again!)
5. Use it as `JIRA_API_TOKEN`

---

## 📊 Monitor Your Deployment

### View Logs
```bash
railway logs
```

Or in Railway dashboard → "Deployments" → Click on deployment → "View Logs"

### Check Status
In Railway dashboard, you'll see:
- ✅ Build status
- ✅ Deployment status
- ✅ Health checks
- ✅ Resource usage

---

## 🐛 Troubleshooting

### Build Failed
**Problem:** Railway can't build the Docker image

**Solutions:**
1. Check Railway logs for specific errors
2. Verify Dockerfile is valid
3. Ensure all files are pushed to GitHub

### Deployment Failed
**Problem:** Build succeeded but deployment fails

**Solutions:**
1. Check environment variables are set correctly
2. Verify port configuration (Railway sets `PORT` automatically)
3. Check logs: `railway logs`

### API Returns 500 Errors
**Problem:** API starts but crashes on requests

**Solutions:**
1. Verify Jira credentials are correct
2. Check `JIRA_BASE_URL` includes `https://`
3. Test Jira connectivity
4. Check Railway logs for Python errors

### Can't Access API
**Problem:** URL not responding

**Solutions:**
1. Wait 2-3 minutes for deployment to complete
2. Check deployment status in Railway dashboard
3. Verify domain is generated (Settings → Domains)
4. Check health endpoint: `/health`

---

## 💡 Pro Tips

1. **Auto-Deploy from GitHub:** Railway automatically redeploys when you push to main branch
2. **Multiple Environments:** Create separate Railway projects for dev/staging/production
3. **Custom Domain:** Add your own domain in Railway Settings → Domains
4. **Scale Resources:** Upgrade plan for more CPU/RAM if needed
5. **Monitor Costs:** Railway shows cost estimates in dashboard

---

## 🎯 Quick Command Reference

```bash
# CLI Commands
railway login              # Authenticate
railway link               # Link to project
railway up                 # Deploy
railway logs               # View logs
railway logs -f            # Follow logs (live)
railway open               # Open app in browser
railway status             # Check deployment status
railway variables          # List variables
railway variables set KEY=VALUE  # Set variable
railway run python web_api.py    # Run commands in Railway environment
```

---

## 🆘 Need Help?

- **Railway Docs:** https://docs.railway.app
- **Railway Discord:** https://discord.gg/railway
- **Railway Status:** https://status.railway.app
- **Project Docs:** See `GITHUB_DEPLOYMENT.md`

---

**Recommended:** Use the Railway website for first deployment - it's much easier! 🚀
