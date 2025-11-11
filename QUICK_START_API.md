# 🚀 Quick Start Guide

## Start the API - Multiple Ways

### Method 1: Double-Click (Easiest)
Just double-click: **`START_API_HERE.bat`**

The API will automatically:
- Check for Python
- Activate virtual environment (if exists)
- Install dependencies (if needed)
- Start the server at http://localhost:8000

### Method 2: Python Command
```bash
python start.py
```

### Method 3: Direct Python Module
```bash
python web_api.py
```

### Method 4: Original Batch Script
```bash
start_api.bat
```

### Method 5: Uvicorn Command
```bash
uvicorn web_api:app --reload
```

---

## 🎯 What Happens When You Start

The API automatically:
1. ✅ Loads configuration from `.env`
2. ✅ Starts FastAPI server on port 8000
3. ✅ Enables hot-reload for development
4. ✅ Shows all available endpoints
5. ✅ Opens interactive documentation

---

## 📡 Access Your API

Once started, visit:

- **Health Check**: http://localhost:8000/
- **API Documentation**: http://localhost:8000/docs (Interactive!)
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Status**: http://localhost:8000/health

---

## 🧪 Test the API

### Using the Interactive Docs (Easiest)
1. Go to http://localhost:8000/docs
2. Click on `/analyze` endpoint
3. Click "Try it out"
4. Fill in the request body
5. Click "Execute"

### Using cURL
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d "{\"issue_id\":\"DL-123\",\"language\":\"BE\",\"max_hours\":4.0}"
```

### Using Python
```python
import requests

response = requests.post('http://localhost:8000/analyze', json={
    'issue_id': 'DL-123',
    'language': 'BE',
    'max_hours': 4.0
})
print(response.json())
```

---

## ⚙️ Configuration

Before starting, make sure `.env` file has:
```env
JIRA_BASE_URL=https://your-company.atlassian.net
JIRA_USERNAME=your-email@example.com
JIRA_API_TOKEN=your_jira_api_token
```

---

## 🛑 Stop the Server

Press **Ctrl+C** in the terminal window

---

## 🐛 Troubleshooting

### Port Already in Use
If port 8000 is busy, modify `web_api.py` to use a different port:
```python
uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)
```

### Module Not Found
Install dependencies:
```bash
pip install -r requirements.txt
```

### Virtual Environment Issues
Activate manually:
```bash
.venv\Scripts\activate    # Windows
source .venv/bin/activate # Linux/Mac
```

---

**Recommended:** Just double-click `START_API_HERE.bat` and you're ready! 🚀
