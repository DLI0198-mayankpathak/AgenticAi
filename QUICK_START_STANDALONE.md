# 🚀 Jira Analysis Agent - Standalone Package

## What's in this ZIP?

- **standalone_api.py** - The complete API in one file
- **START_HERE.bat** - Double-click to run (Windows)
- **STANDALONE_GUIDE.md** - Full documentation
- **.env.example** - Configuration template
- **README.md** - Project overview

## ⚡ Quick Start (3 Steps)

### Step 1: Extract the ZIP
Unzip to any folder on your computer

### Step 2: Configure (Optional)
Copy `.env.example` to `.env` and add your credentials:
```env
JIRA_BASE_URL=https://your-company.atlassian.net
JIRA_USERNAME=your-email@company.com
JIRA_API_TOKEN=your_jira_api_token
OPENAI_API_KEY=your_openai_key
```

### Step 3: Run!

**Windows:**
```
Double-click: START_HERE.bat
```

**Mac/Linux:**
```bash
python standalone_api.py
```

**Manual:**
```bash
# Install dependencies first (if needed)
pip install fastapi uvicorn[standard] openai python-dotenv requests pydantic

# Run the API
python standalone_api.py
```

## 📡 Access the API

Once running, open your browser:
- **Interactive Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🔑 Using Without .env File

You can pass credentials in each request:
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

## 📚 Full Documentation

See **STANDALONE_GUIDE.md** for:
- Complete setup instructions
- API usage examples
- Authentication options
- Troubleshooting guide

## ✨ Features

✅ Single file - no complex setup  
✅ Auto-checks dependencies  
✅ Token authentication built-in  
✅ Works on Windows/Mac/Linux  
✅ Interactive API documentation  
✅ AI-powered code generation  
✅ Jira integration  

## 🆘 Need Help?

1. Make sure Python 3.9+ is installed
2. Check that all packages are installed
3. Verify your .env file format
4. See STANDALONE_GUIDE.md for detailed help

## 🔒 Security Note

Never commit or share your `.env` file with real credentials!

---

**Ready?** Double-click `START_HERE.bat` (Windows) or run `python standalone_api.py`! 🚀
