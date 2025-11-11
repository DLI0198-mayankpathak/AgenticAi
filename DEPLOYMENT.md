# Jira Analysis Agent - Deployment Guide

## 🚀 Quick Deployment Options

### Option 1: Railway.app (Recommended - Easiest)
1. Push your code to GitHub
2. Go to [Railway.app](https://railway.app)
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway will auto-detect the Dockerfile and deploy
6. Add environment variables in Railway dashboard:
   - `JIRA_BASE_URL`
   - `JIRA_USERNAME`
   - `JIRA_API_TOKEN`
7. Your API will be live at: `https://your-app.railway.app`

### Option 2: Azure App Service
1. Install Azure CLI: `az login`
2. Create app service:
   ```bash
   az webapp create --resource-group myResourceGroup --plan myAppServicePlan --name jira-agent --runtime "PYTHON|3.9"
   ```
3. Deploy:
   ```bash
   az webapp up --name jira-agent --runtime "PYTHON:3.9"
   ```
4. Set environment variables in Azure Portal

### Option 3: Heroku
1. Install Heroku CLI and login: `heroku login`
2. Create app:
   ```bash
   heroku create jira-agent
   ```
3. Set environment variables:
   ```bash
   heroku config:set JIRA_BASE_URL=your_url
   heroku config:set JIRA_USERNAME=your_username
   heroku config:set JIRA_API_TOKEN=your_token
   ```
4. Deploy:
   ```bash
   git push heroku main
   ```

### Option 4: AWS (EC2 or Lambda)
See AWS deployment documentation

## 📡 API Endpoints

Once deployed, your API will have these endpoints:

### 1. Health Check
```bash
GET https://your-url/
```

### 2. Analyze Issue
```bash
POST https://your-url/analyze
Content-Type: application/json

{
  "issue_id": "DL-123",
  "language": "java",
  "max_hours": 4.0,
  "assign_to": "developer@example.com"
}
```

### 3. Health Status
```bash
GET https://your-url/health
```

## 🔧 Local Testing

Test the API locally before deploying:

```bash
# Install web dependencies
pip install fastapi uvicorn[standard]

# Run the API
python web_api.py

# Test in another terminal
curl http://localhost:8000/

# Test analysis
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "issue_id": "DL-123",
    "language": "java",
    "max_hours": 4.0
  }'
```

## 🔒 Environment Variables Required

Make sure to set these in your deployment platform:
- `JIRA_BASE_URL`: Your Jira instance URL (e.g., `https://company.atlassian.net`)
- `JIRA_USERNAME`: Your Jira email
- `JIRA_API_TOKEN`: Your Jira API token

## 📦 Docker Deployment

If using Docker:

```bash
# Build
docker build -t jira-agent .

# Run
docker run -p 8000:8000 \
  -e JIRA_BASE_URL=your_url \
  -e JIRA_USERNAME=your_username \
  -e JIRA_API_TOKEN=your_token \
  jira-agent
```

## 🌐 Using the Deployed API

Once deployed, call it from anywhere:

**JavaScript/TypeScript:**
```javascript
const response = await fetch('https://your-url/analyze', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    issue_id: 'DL-123',
    language: 'java',
    max_hours: 4.0
  })
});
const result = await response.json();
```

**Python:**
```python
import requests

response = requests.post('https://your-url/analyze', json={
    'issue_id': 'DL-123',
    'language': 'java',
    'max_hours': 4.0
})
result = response.json()
```

**cURL:**
```bash
curl -X POST https://your-url/analyze \
  -H "Content-Type: application/json" \
  -d '{"issue_id":"DL-123","language":"java","max_hours":4.0}'
```

## 🎯 Next Steps

1. Push code to GitHub
2. Choose a deployment platform (Railway recommended)
3. Deploy and get your URL
4. Test the endpoints
5. Integrate with your workflow
