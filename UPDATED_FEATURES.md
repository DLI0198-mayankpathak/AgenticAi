# Updated Features - November 7, 2025

## 🆕 What's New

### 1. **Enhanced Description Field Detection**
The agent now intelligently checks multiple fields for issue descriptions:

- **Primary**: Standard "Description" field
- **Fallback**: "Story/Task Description" custom field
- **Automatic**: Detects and uses whichever field has content

This ensures the agent can generate accurate pseudo code, source code, and effort estimates regardless of which field contains the requirements.

### 2. **Assignee Update via API**
You can now automatically assign issues to developers through the API:

```bash
curl -X POST http://127.0.0.1:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "issue_id": "DL-123",
    "language": "BE",
    "max_hours": 8.0,
    "assign_to": "developer@company.com"
  }'
```

The agent will:
- Generate pseudo code, source code, and effort estimates
- Update Jira fields
- Assign the issue to the specified developer
- Return success confirmation

## 📝 API Updates

### AnalysisRequest Schema

```json
{
  "issue_id": "DL-123",           // Required: Jira issue ID
  "language": "BE",                // Required: "BE" (Java) or "UI" (Angular)
  "max_hours": 8.0,                // Optional: Max effort (default: 4.0)
  "assign_to": "dev@email.com"     // Optional: Developer to assign
}
```

### Response

```json
{
  "success": true,
  "message": "Successfully analyzed and updated DL-123",
  "issue_id": "DL-123",
  "total_hours": 6.5,
  "total_days": 0.81
}
```

## 🔄 How It Works

### Description Field Detection Flow

```
1. Fetch Jira issue via REST API
   ↓
2. Check standard "Description" field
   ↓
   Has content? → Use it ✅
   ↓
   Empty? → Check "Story/Task Description"
   ↓
3. Search custom fields for:
   - Field name contains "story" OR "task"
   - Field has content
   ↓
4. Use found description for:
   - Pseudo code generation
   - Source code generation
   - Effort estimation
```

### Assignee Update Flow

```
1. Generate analysis (pseudo code, source code, estimates)
   ↓
2. Update Jira fields
   ↓
3. If assign_to provided:
   ├─ Search for user by email
   ├─ Get user's account ID
   └─ Update issue assignee
   ↓
4. Return success with assignment confirmation
```

## 🧪 Testing

Run the test suite:

```bash
python test_updated_features.py
```

This will test:
- ✅ Backend (Java) analysis with assignee
- ✅ Frontend (Angular) analysis without assignee
- ✅ Description field detection

## 📊 Example Usage

### Example 1: Backend Development Task

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

**Result**:
- Generates Java/Spring Boot implementation
- Updates Jira with pseudo code and source code
- Posts effort estimation table as comment
- Assigns to backend.dev@company.com

### Example 2: Frontend Development Task

```bash
curl -X POST http://127.0.0.1:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "issue_id": "DL-61396",
    "language": "UI",
    "max_hours": 6.0,
    "assign_to": "frontend.dev@company.com"
  }'
```

**Result**:
- Generates Angular component implementation
- Updates Jira with UI-specific pseudo code
- Posts effort estimation
- Assigns to frontend.dev@company.com

### Example 3: Analysis Only (No Assignment)

```bash
curl -X POST http://127.0.0.1:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "issue_id": "DL-61404",
    "language": "BE",
    "max_hours": 8.0
  }'
```

**Result**:
- Generates analysis and updates Jira
- Does NOT change assignee
- Issue remains with current assignee

## 🔍 Technical Details

### Description Field Detection

The agent uses these methods in `MCPJiraClient`:

```python
def get_issue_detail(issue_id: str) -> Dict[str, Any]:
    """
    Fetches issue and checks:
    1. Standard description field
    2. Custom fields containing "story" or "task"
    """
    
def _get_field_name(field_id: str) -> Optional[str]:
    """Maps custom field IDs to display names"""
    
def _adf_to_text(adf_content: Any) -> str:
    """Converts Atlassian Document Format to plain text"""
```

### Assignee Update

```python
def assign_issue(issue_id: str, assignee: str) -> bool:
    """
    1. Search for user by email/name
    2. Get account ID
    3. Update issue assignee via REST API
    """
```

## 🚀 Benefits

### For Teams
- **Automated Assignment**: No need to manually assign after analysis
- **Flexible Description Fields**: Works with any Jira field setup
- **Streamlined Workflow**: Analyze + Assign in one API call

### For Developers
- **Clear Ownership**: Issues automatically assigned after analysis
- **Rich Context**: Pseudo code and estimates already in issue
- **Ready to Work**: Everything needed to start development

### For Project Managers
- **Bulk Processing**: Assign multiple issues programmatically
- **Consistent Estimates**: AI-driven effort estimation
- **Audit Trail**: All updates tracked in Jira history

## 🛠️ Configuration

### Required Environment Variables (.env)

```bash
# Jira Configuration
JIRA_BASE_URL=https://your-domain.atlassian.net
JIRA_USERNAME=your.email@company.com
JIRA_API_TOKEN=your_api_token_here

# Custom Fields (auto-detected if not specified)
PSEUDO_CODE_FIELD=customfield_10249
SOURCE_CODE_FIELD=customfield_10690
```

### API Server

```bash
# Start on localhost
python -m uvicorn web_api:app --host 127.0.0.1 --port 8000 --reload

# Start on network IP (accessible from other machines)
python -m uvicorn web_api:app --host 10.232.187.6 --port 8000 --reload
```

## 📚 Related Documentation

- [API Reference](docs/api_reference.md)
- [MCP Integration Guide](docs/MCP_INTEGRATION_GUIDE.md)
- [Architecture](docs/architecture.md)
- [Quick Start](QUICK_START.md)

## 🐛 Troubleshooting

### Issue: Assignee not found
**Solution**: Verify email address or username is correct in Jira

### Issue: Description field empty
**Solution**: Check if content is in "Story/Task Description" - agent will automatically find it

### Issue: Authentication failed
**Solution**: Check JIRA_API_TOKEN is valid and not expired

## 📞 Support

For issues or questions, check the main README.md or project documentation.
