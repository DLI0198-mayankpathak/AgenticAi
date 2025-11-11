# 🚀 Quick API Reference

## Base URL
```
http://127.0.0.1:8000
```

## Endpoints

### 1. Health Check
```bash
GET /health
```

**Response:**
```json
{"status": "healthy"}
```

---

### 2. Analyze Jira Issue
```bash
POST /analyze
```

**Request Body:**
```json
{
  "issue_id": "DL-123",              // Required
  "language": "BE",                   // Required: "BE" or "UI"
  "max_hours": 8.0,                   // Optional (default: 4.0)
  "assign_to": "dev@email.com"        // Optional
}
```

**Response:**
```json
{
  "success": true,
  "message": "Successfully analyzed and updated DL-123",
  "issue_id": "DL-123",
  "total_hours": 6.5,
  "total_days": 0.81
}
```

---

## Language Options

| Code | Language | Type | Generates |
|------|----------|------|-----------|
| `BE` | Java | Backend | Spring Boot REST API, Services, Repositories |
| `UI` | Angular | Frontend | Components, Services, Models, Templates |

---

## Examples

### Backend with Assignment
```bash
curl -X POST http://127.0.0.1:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "issue_id": "DL-61395",
    "language": "BE",
    "max_hours": 8.0,
    "assign_to": "backend.dev@company.com"
  }'
```

### Frontend without Assignment
```bash
curl -X POST http://127.0.0.1:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "issue_id": "DL-61396",
    "language": "UI",
    "max_hours": 6.0
  }'
```

### Using PowerShell (Windows)
```powershell
$body = @{
    issue_id = "DL-123"
    language = "BE"
    max_hours = 8.0
    assign_to = "dev@email.com"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/analyze" `
  -Method Post `
  -ContentType "application/json" `
  -Body $body
```

### Using Python
```python
import requests

response = requests.post(
    "http://127.0.0.1:8000/analyze",
    json={
        "issue_id": "DL-123",
        "language": "BE",
        "max_hours": 8.0,
        "assign_to": "dev@email.com"
    }
)

print(response.json())
```

---

## What Gets Updated in Jira

| Field | Content | Format |
|-------|---------|--------|
| **Pseudo Code** | Implementation algorithm | Custom field |
| **Source Code** | Generated source files | Custom field |
| **Comments** | Effort estimation table | Comment |
| **Assignee** | Developer assignment | Standard field |
| **Original Estimate** | Calculated hours | Standard field |

---

## Features

✅ Checks both "Description" and "Story/Task Description" fields  
✅ Generates context-aware pseudo code from requirements  
✅ Creates production-ready source code  
✅ Calculates detailed effort estimates with task breakdown  
✅ Automatically assigns to developers  
✅ Updates multiple Jira fields in one call  

---

## Error Codes

| Code | Meaning | Solution |
|------|---------|----------|
| 200 | Success | Issue analyzed and updated |
| 404 | Not Found | Check issue ID format (e.g., "DL-123") |
| 401 | Unauthorized | Check JIRA_API_TOKEN in .env |
| 403 | Forbidden | User lacks permission for this issue |
| 500 | Server Error | Check logs for details |

---

## Interactive Documentation

Visit in your browser:
```
http://127.0.0.1:8000/docs
```

This provides a Swagger UI where you can:
- Test endpoints interactively
- See detailed schema documentation
- Try different parameter combinations
- View example requests/responses

---

## Quick Start

1. **Start the API:**
   ```bash
   python -m uvicorn web_api:app --host 127.0.0.1 --port 8000 --reload
   ```

2. **Test it:**
   ```bash
   curl http://127.0.0.1:8000/health
   ```

3. **Analyze an issue:**
   ```bash
   curl -X POST http://127.0.0.1:8000/analyze \
     -H "Content-Type: application/json" \
     -d '{"issue_id":"DL-123","language":"BE","max_hours":8.0}'
   ```

---

## Notes

- **Issue ID Format**: Use hyphenated format (e.g., "DL-123", not "DL123")
- **Email for Assignment**: Must match a Jira user's email or display name
- **Max Hours**: Limits task breakdown granularity, doesn't cap total estimate
- **Description**: Agent automatically finds content in Description or Story/Task Description fields

---

For detailed documentation, see [UPDATED_FEATURES.md](UPDATED_FEATURES.md)
