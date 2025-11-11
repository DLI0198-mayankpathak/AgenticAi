# Pseudo Code Field Update Feature

## Overview

The Agentic AI system now updates the dedicated **"Pseudo Code" custom field** in Jira instead of appending to the Description field. This keeps the implementation algorithm separate from the issue requirements and makes it easier to view and update.

## What Changed

### Key Updates

1. **Separate Custom Field** (`src/agent.py`)
   - Pseudo code updates the "Pseudo Code" field in Jira
   - Original description field remains completely unchanged
   - Clear separation between requirements and implementation

2. **Custom Field Mapping** (`src/mcp_client.py`)
   - Automatic mapping from field name to custom field ID
   - Queries Jira API to find field ID (e.g., "Pseudo Code" → `customfield_10249`)
   - Caches field IDs for better performance
   - Supports both field names and direct field IDs

3. **Configurable Field Name** (`src/config.py`)
   - Field name can be configured via `AgentConfig`
   - Defaults to "Pseudo Code"
   - Can use custom field ID directly (e.g., `customfield_10XXX`)

## Jira Issue Structure

```
┌─────────────────────────────────────┐
│ Issue: DL-61731                     │
├─────────────────────────────────────┤
│ Description Field:                  │
│   [Original Requirements]           │
│   - Problem statement               │
│   - Steps to replicate              │
│   - Expected vs Actual behavior     │
│                                     │
├─────────────────────────────────────┤
│ Pseudo Code Field:  ← UPDATED HERE │
│   ### 🔍 Pseudo Code                │
│   BEGIN                             │
│     // Implementation algorithm     │
│   END                               │
│                                     │
├─────────────────────────────────────┤
│ Comments:                           │
│   📊 Effort Estimation Table        │
│   [Task breakdown with hours/days]  │
└─────────────────────────────────────┘
```

## Configuration

### Default Configuration

```python
from src.config import AgentConfig

config = AgentConfig(
    language="angular",
    max_days=3.0,
    pseudo_code_field="Pseudo Code"  # Default field name
)
```

### Using Custom Field ID

If you know the exact custom field ID:

```python
config = AgentConfig(
    language="java",
    pseudo_code_field="customfield_10249"  # Direct field ID
)
```

### Alternative Field Name

If your Jira uses a different field name:

```python
config = AgentConfig(
    language="angular",
    pseudo_code_field="Implementation Plan"  # Your custom field name
)
```

## Usage Examples

### Example 1: Basic Update

```python
from src.agent import JiraAnalysisAgent
from src.config import AgentConfig

# Configure
config = AgentConfig(
    language="angular",
    max_days=3.0,
    pseudo_code_field="Pseudo Code"
)

# Create agent
agent = JiraAnalysisAgent(config)

# Analyze issue
result = agent.analyze_issue(issue_id="DL-61731")

# Update Jira
agent.update_jira_with_analysis(result)
```

**Result in Jira:**
- ✅ Description: Unchanged (original requirements preserved)
- ✅ Pseudo Code field: Updated with implementation algorithm
- ✅ Comment: Effort estimation table added

### Example 2: With Developer Assignment

```python
# Update Jira and assign to developer
agent.update_jira_with_analysis(
    result=result,
    assign_to="developer@example.com"
)
```

**Result in Jira:**
- ✅ Description: Unchanged
- ✅ Pseudo Code field: Updated
- ✅ Comment: Effort estimation
- ✅ Assignee: developer@example.com

### Example 3: Interactive Mode

```bash
python run.py
```

**Session:**
```
Enter Jira Issue ID: DL-61731
Select language: 2 (Angular)
Enter max days: 3
Update Jira issue with analysis? y
Assign to developer: jane.smith@example.com

🔐 Jira credentials loaded from .env
📥 Fetching Jira issue: DL-61731
✅ Issue fetched: Sample Issue Title
🔍 Generating pseudo code for ANGULAR
✅ Pseudo code generated (Complexity: Complex)
💻 Generating source code
✅ Generated 5 source files
📊 Calculating effort estimation
✅ Estimated: 2.0 days (without buffer)
📝 Generating markdown report
✅ Report saved to: output/DL-61731_angular_analysis.md

📝 Updating 'Pseudo Code' field in issue: DL-61731
   Found custom field: 'Pseudo Code' → customfield_10249
✅ Successfully updated 'Pseudo Code' field
📤 Posting effort estimate to Jira comment: DL-61731
✅ Successfully posted effort estimate comment
👤 Assigning issue to: jane.smith@example.com
   Found user: Jane Smith (jane.smith@example.com)
✅ Successfully assigned issue to jane.smith@example.com

✅ Jira issue DL-61731 updated successfully!
```

## Pseudo Code Field Format

The "Pseudo Code" field contains:

```markdown
### 🔍 Pseudo Code (Complexity: Complex)

**Implementation Algorithm**

```
BEGIN
  // Input Validation & Prerequisites
  CREATE FormGroup with validation rules
    SET required validators on mandatory fields
    ADD custom validators for business rules
    BIND form to component
  
  // Form Submission
  ON form submit
    CHECK form.valid status
    IF invalid THEN
      DISPLAY error messages
      RETURN
    END IF
    
  // Main Logic Flow
  SHOW loading spinner
  CALL backend API service method
    PASS validated form data
    SET appropriate HTTP headers
  
  // Success Handling
  ON successful response
    UPDATE component state with response data
    REFRESH data grid/list if needed
    UPDATE UI components with new data
    HIDE loading spinner
    DISPLAY success notification
  
  // Error Handling
  ON HTTP error response
    PARSE error details from response body
    MAP error code to user-friendly message
    DISPLAY error notification/toast
    IF error code = 401 (Unauthorized) THEN
      REDIRECT to login page
    ELSE IF error code = 403 (Forbidden) THEN
      SHOW access denied message
    ELSE IF error code = 500 (Internal Server Error) THEN
      LOG error to console
      SHOW generic error message
    END IF
    HIDE loading indicators
  
  // Component Lifecycle
  ON component destroy
    UNSUBSCRIBE from all observables
    CLEAN UP resources
END
```
```

## Benefits

### 1. **Clear Separation of Concerns**
- Requirements in Description field
- Implementation in Pseudo Code field
- Effort tracking in Comments

### 2. **Preserved Context**
- Original issue description never modified
- Easy to compare requirements vs implementation
- Clean audit trail

### 3. **Better Visibility**
- Pseudo Code has its own dedicated field
- Can be viewed separately in Jira issue view
- Searchable and filterable

### 4. **Flexible Configuration**
- Use any custom field name
- Support for direct field IDs
- Automatic field name to ID mapping

### 5. **Workflow Integration**
- Product Owners see requirements in Description
- Developers see implementation in Pseudo Code
- Managers see effort in Comments

## How It Works Internally

### 1. Field Name Resolution

```python
# User provides field name
field_name = "Pseudo Code"

# System queries Jira API
GET /rest/api/3/field

# Finds matching field
{
  "id": "customfield_10249",
  "name": "Pseudo Code",
  "schema": { "type": "string" }
}

# Maps and caches
"Pseudo Code" → "customfield_10249"
```

### 2. Field Update

```python
# Generate pseudo code
pseudo_section = agent._format_pseudo_for_jira(result)

# Update field
PUT /rest/api/3/issue/DL-61731
{
  "fields": {
    "customfield_10249": {
      "version": 1,
      "type": "doc",
      "content": [
        { "type": "heading", ... },
        { "type": "codeBlock", ... }
      ]
    }
  }
}
```

### 3. Markdown to ADF Conversion

- Markdown pseudo code converted to Atlassian Document Format (ADF)
- Preserves formatting (headings, code blocks, lists)
- Renders correctly in Jira UI

## Testing

Run the comprehensive test suite:

```bash
python test_pseudo_code_field.py
```

**Tests verify:**
- ✅ Pseudo code updates correct field
- ✅ Original description unchanged
- ✅ Custom field name configuration
- ✅ Field name to ID mapping
- ✅ Proper formatting

## API Reference

### AgentConfig

```python
@dataclass
class AgentConfig:
    language: Literal["java", "angular"] = "java"
    max_days: float = 2.0
    pseudo_code_field: str = "Pseudo Code"  # ← NEW
    # ... other fields
```

### MCPJiraClient.get_custom_field_id()

```python
def get_custom_field_id(self, field_name: str) -> Optional[str]:
    """
    Get the custom field ID from field name
    
    Args:
        field_name: Display name (e.g., "Pseudo Code") or ID
        
    Returns:
        Custom field ID (e.g., "customfield_10249")
    """
```

### MCPJiraClient.update_issue_field()

```python
def update_issue_field(
    self,
    issue_id: str,
    field_name: str,  # Can be name or ID
    field_value: str  # Markdown format
) -> bool:
    """
    Update a field in Jira (auto-converts to ADF for text fields)
    """
```

## Migration from Previous Version

### Old Behavior (Appended to Description)

```python
# Previous version
agent.update_jira_with_analysis(result)
# Result: Description = [Original] + --- + [Pseudo Code]
```

### New Behavior (Updates Custom Field)

```python
# Current version
config = AgentConfig(pseudo_code_field="Pseudo Code")
agent = JiraAnalysisAgent(config)
agent.update_jira_with_analysis(result)
# Result: Description = [Original]
#         Pseudo Code field = [Algorithm]
```

### No Code Changes Required

If you're already using the system:
- Add `pseudo_code_field` to config (optional, defaults to "Pseudo Code")
- Existing code continues to work
- Better separation of concerns automatically

## Troubleshooting

### Field Not Found

```
⚠️  Custom field 'Pseudo Code' not found, using as-is
```

**Solution:**
1. Check the exact field name in your Jira
2. Use the direct field ID: `pseudo_code_field="customfield_10XXX"`
3. Verify field is available in your Jira project

### Permission Denied

```
❌ Failed to update field: 403
```

**Solution:**
- Ensure your Jira user has edit permissions
- Check field is not locked/protected
- Verify API token has correct permissions

### Invalid Field Type

```
❌ Invalid field or value
```

**Solution:**
- Ensure field accepts text/rich text format
- Field must support ADF (Atlassian Document Format)
- Some fields only accept specific values

## Notes

- System automatically discovers the custom field ID from name
- Field ID is cached after first lookup for performance
- Markdown is converted to ADF for proper Jira rendering
- Standard fields (description, summary, etc.) work without mapping
- Custom field must exist in the Jira project

## Related Documentation

- `docs/JIRA_UPDATE_FEATURE.md` - Main Jira update guide
- `docs/DEVELOPER_ASSIGNMENT_FEATURE.md` - Assignment feature
- `README.md` - Complete usage documentation
- `test_pseudo_code_field.py` - Test examples

---

_Last Updated: 2025-11-06_
_Feature: Pseudo Code Custom Field Update_
