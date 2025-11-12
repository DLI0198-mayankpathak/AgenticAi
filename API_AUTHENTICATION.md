# 🔐 API Authentication Guide

The Jira Analysis Agent API supports **three authentication methods** for Jira credentials:

## Authentication Methods

### Method 1: Request Body (Easiest)
Include Jira credentials directly in the request body:

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "issue_id": "DL-123",
    "language": "BE",
    "max_hours": 4.0,
    "jira_username": "your-email@company.com",
    "jira_api_token": "your_jira_api_token"
  }'
```

**Python Example:**
```python
import requests

response = requests.post('http://localhost:8000/analyze', json={
    'issue_id': 'DL-123',
    'language': 'BE',
    'max_hours': 4.0,
    'jira_username': 'your-email@company.com',
    'jira_api_token': 'your_jira_api_token'
})
print(response.json())
```

---

### Method 2: Bearer Token (Most Secure)
Encode your credentials as `username:api_token` in base64 and send as Bearer token:

**Step 1: Create the token**
```python
import base64

username = "your-email@company.com"
api_token = "your_jira_api_token"
credentials = f"{username}:{api_token}"
token = base64.b64encode(credentials.encode()).decode()
print(f"Bearer {token}")
```

**Step 2: Use in API call**
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eW91ci1lbWFpbEBjb21wYW55LmNvbTp5b3VyX2ppcmFfYXBpX3Rva2Vu" \
  -d '{
    "issue_id": "DL-123",
    "language": "BE",
    "max_hours": 4.0
  }'
```

**Python Example:**
```python
import requests
import base64

username = "your-email@company.com"
api_token = "your_jira_api_token"
credentials = f"{username}:{api_token}"
token = base64.b64encode(credentials.encode()).decode()

headers = {
    "Authorization": f"Bearer {token}"
}

response = requests.post('http://localhost:8000/analyze', 
    headers=headers,
    json={
        'issue_id': 'DL-123',
        'language': 'BE',
        'max_hours': 4.0
    }
)
print(response.json())
```

---

### Method 3: Environment Variables (Fallback)
If no credentials are provided, the API falls back to `.env` file:

**.env file:**
```env
JIRA_BASE_URL=https://your-company.atlassian.net
JIRA_USERNAME=your-email@company.com
JIRA_API_TOKEN=your_jira_api_token
```

**API Call (no credentials needed):**
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "issue_id": "DL-123",
    "language": "BE",
    "max_hours": 4.0
  }'
```

---

## Priority Order

The API uses credentials in this priority:
1. **Request Body** (`jira_username` and `jira_api_token`)
2. **Authorization Header** (Bearer token)
3. **Environment Variables** (.env file)

---

## Complete Request Example

### Full Request Body
```json
{
  "issue_id": "DL-123",
  "language": "BE",
  "max_hours": 4.0,
  "assign_to": "developer@company.com",
  "jira_username": "your-email@company.com",
  "jira_api_token": "your_jira_api_token",
  "repository_name": "my-repo",
  "repository_organization": "my-org",
  "azure_organization": "my-azure-org",
  "azure_project": "my-project"
}
```

### JavaScript/TypeScript Example
```javascript
const credentials = btoa('your-email@company.com:your_jira_api_token');

const response = await fetch('http://localhost:8000/analyze', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${credentials}`
  },
  body: JSON.stringify({
    issue_id: 'DL-123',
    language: 'BE',
    max_hours: 4.0
  })
});

const result = await response.json();
console.log(result);
```

---

## Security Best Practices

### ✅ DO:
- Use **Bearer token method** for production APIs
- Store tokens in environment variables or secure vaults
- Use HTTPS in production (not HTTP)
- Rotate API tokens regularly
- Use separate tokens for different environments

### ❌ DON'T:
- Hardcode credentials in code
- Commit tokens to version control
- Share tokens via insecure channels
- Use the same token for dev and production
- Log or display tokens in plain text

---

## Testing Authentication

### Test with cURL (Request Body):
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "issue_id": "DL-123",
    "language": "BE",
    "max_hours": 4.0,
    "jira_username": "test@company.com",
    "jira_api_token": "test_token_123"
  }'
```

### Test with cURL (Bearer Token):
```bash
# Generate token
TOKEN=$(echo -n "test@company.com:test_token_123" | base64)

# Use token
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "issue_id": "DL-123",
    "language": "BE",
    "max_hours": 4.0
  }'
```

---

## Interactive API Documentation

Visit **http://localhost:8000/docs** to:
- Try authentication methods interactively
- See all request parameters
- Test the API without writing code
- View response schemas

---

## Getting Your Jira API Token

1. Go to: https://id.atlassian.com/manage-profile/security/api-tokens
2. Click **"Create API token"**
3. Name it: "Jira Analysis Agent"
4. Copy the token (you won't see it again!)
5. Use it in one of the authentication methods above

---

## Troubleshooting

### Authentication Failed
**Problem:** API returns 500 error or "Authentication failed"

**Solutions:**
1. Verify Jira username is your email address
2. Ensure API token is copied correctly (no extra spaces)
3. Check JIRA_BASE_URL is set correctly in .env
4. Test credentials directly in Jira API

### Token Encoding Issues
**Problem:** Bearer token doesn't work

**Solutions:**
1. Ensure format is exactly: `username:api_token`
2. Use base64 encoding (not URL encoding)
3. Remove any newline characters from encoded token
4. Test encoding: `echo -n "user:token" | base64`

### Priority Confusion
**Problem:** Not sure which credentials are being used

**Solutions:**
1. Check console output: API logs which method is used
2. Request body credentials override header
3. Header credentials override .env
4. Remove .env to force token authentication

---

**Recommended for Production:** Use Bearer token method with HTTPS 🔒
