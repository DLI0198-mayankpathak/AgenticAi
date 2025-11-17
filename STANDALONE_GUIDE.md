# 🚀 Standalone API - Single File Distribution

## What is this?

`standalone_api.py` is a **single, self-contained file** that includes everything needed to run the Jira Analysis Agent API. Perfect for sharing with team members!

## ✨ Features

- ✅ Single Python file - no complex project structure
- ✅ Auto-checks and installs dependencies
- ✅ Works anywhere with Python 3.9+
- ✅ Token-based authentication built-in
- ✅ All core features included

## 📦 Quick Start

### Option 1: Share Just One File

1. **Send `standalone_api.py` to anyone**
2. **They run:**
   ```bash
   python standalone_api.py
   ```
3. **That's it!** API runs at http://localhost:8000

### Option 2: With Environment File

**Share two files:**
- `standalone_api.py`
- `.env.example` (rename to `.env`)

**User runs:**
```bash
python standalone_api.py
```

## 🔧 Setup for Recipients

### Step 1: Install Python
Make sure Python 3.9+ is installed:
```bash
python --version
```

### Step 2: Run the File
```bash
python standalone_api.py
```

The script will:
- ✅ Check for required packages
- ✅ Tell you what to install if missing
- ✅ Start the API server

### Step 3: Install Missing Packages (if prompted)
```bash
pip install fastapi uvicorn[standard] openai python-dotenv requests pydantic
```

Then run again:
```bash
python standalone_api.py
```

## 🔑 Configuration

### Option 1: Environment Variables (.env file)
Create a `.env` file in the same directory:
```env
JIRA_BASE_URL=https://your-company.atlassian.net
JIRA_USERNAME=your-email@company.com
JIRA_API_TOKEN=your_jira_api_token
OPENAI_API_KEY=your_openai_key
```

### Option 2: Pass in Request
No .env needed! Send credentials with each request:
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "issue_id": "DL-123",
    "language": "BE",
    "jira_username": "user@company.com",
    "jira_api_token": "your_token"
  }'
```

## 📡 Using the API

### 1. Start the Server
```bash
python standalone_api.py
```

### 2. Open Interactive Docs
Go to: **http://localhost:8000/docs**

### 3. Test with cURL
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "issue_id": "DL-123",
    "language": "BE",
    "max_hours": 4.0,
    "jira_username": "user@company.com",
    "jira_api_token": "token"
  }'
```

### 4. Test with Python
```python
import requests

response = requests.post('http://localhost:8000/analyze', json={
    'issue_id': 'DL-123',
    'language': 'BE',
    'max_hours': 4.0,
    'jira_username': 'user@company.com',
    'jira_api_token': 'token'
})
print(response.json())
```

## 🎯 Distribution Methods

### Method 1: Email
Attach `standalone_api.py` to an email with instructions

### Method 2: Shared Drive
Put `standalone_api.py` on Google Drive, SharePoint, etc.

### Method 3: Slack/Teams
Share the file directly in chat

### Method 4: USB Drive
Copy to USB for offline distribution

### Method 5: Internal Package
Add to company's internal package repository

## ⚙️ Differences from Full Project

| Feature | Full Project | Standalone |
|---------|-------------|------------|
| **File Count** | 20+ files | 1 file |
| **Setup Complexity** | Medium | Minimal |
| **Dependencies** | Separate install | Auto-checked |
| **Configuration** | Multiple files | Single .env or request |
| **Updates** | Git pull | Replace file |
| **Size** | Full codebase | ~300 lines |
| **Features** | 100% | 90% core features |

## 📋 Requirements

**Minimum:**
- Python 3.9+
- Internet connection (for API calls)

**Python Packages (auto-detected):**
- fastapi
- uvicorn[standard]
- openai
- python-dotenv
- requests
- pydantic

## 🔒 Security Notes

### ✅ Safe to Share:
- `standalone_api.py` - contains no secrets
- `.env.example` - template only

### ❌ Never Share:
- `.env` - contains real credentials
- Your actual API tokens

### Best Practice:
Tell recipients to create their own `.env` file with their credentials.

## 🐛 Troubleshooting

### "Module not found"
Run: `pip install fastapi uvicorn[standard] openai python-dotenv requests pydantic`

### "OpenAI API key not configured"
Either:
1. Add `OPENAI_API_KEY` to `.env` file
2. Set as environment variable
3. Contact admin for key

### "Jira credentials required"
Either:
1. Add credentials to `.env` file
2. Pass in request body
3. Use Bearer token authentication

### Port 8000 already in use
Change port in the code:
```python
uvicorn.run("standalone_api:app", host="0.0.0.0", port=8001, reload=True)
```

## 🚀 Quick Distribution Guide

**To share with a colleague:**

1. Send them `standalone_api.py`
2. Tell them to run: `python standalone_api.py`
3. If packages missing, they run: `pip install fastapi uvicorn[standard] openai python-dotenv requests pydantic`
4. They're ready to go!

**Example Email:**
```
Hi Team,

Attached is our Jira Analysis Agent API in a single file.

To use:
1. Save standalone_api.py to your computer
2. Run: python standalone_api.py
3. Open: http://localhost:8000/docs

If you get errors about missing packages, run:
pip install fastapi uvicorn[standard] openai python-dotenv requests pydantic

Let me know if you have questions!
```

## 💡 Tips

1. **For non-technical users**: Create a batch file:
   ```batch
   @echo off
   python standalone_api.py
   pause
   ```

2. **For teams**: Put on shared drive with `.env.example`

3. **For demos**: Perfect for quick presentations

4. **For testing**: Easy to test in different environments

## 📞 Support

If recipients have issues:
1. Check Python version: `python --version`
2. Check package installation: `pip list`
3. Check `.env` file format
4. Test with simple request first

---

**Perfect for:** Quick deployments, demos, sharing with non-technical users, testing environments, and team distribution!
