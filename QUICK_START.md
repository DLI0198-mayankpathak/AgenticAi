# Quick Setup for Jira Comment Feature

## Install Dependencies

Run this command to install the required `requests` library:

```bash
pip install requests
```

Or install all dependencies:

```bash
pip install -r requirements.txt
```

## Test the Feature

### Option 1: Interactive Mode

```bash
python run.py
```

Then answer:
- Issue ID: `DL-61404`
- Language: `2` (Angular)
- Max days: `2.0`
- **Update Jira: `y`** ← This will post to Jira

### Option 2: Programmatic

```bash
python example_jira_update.py
```

## How It Works

The system now uses **direct Jira REST API** with credentials from `.env`:

```
Python Code
    ↓
MCPJiraClient.add_comment()
    ↓
Jira REST API v3
    ↓
Comment posted to issue
```

### Authentication Flow

1. Reads from `.env`:
   - `JIRA_BASE_URL=https://godigit.atlassian.net`
   - `JIRA_USERNAME=mayank.pathak@godigit.com`
   - `JIRA_API_TOKEN=ATATT3xFfGF0...`

2. Converts Markdown to ADF (Atlassian Document Format)

3. POSTs to Jira API:
   ```
   POST /rest/api/3/issue/{issueId}/comment
   ```

## What Gets Posted

The comment includes:
- ✅ **Pseudo Code** - Complete BEGIN/END block with syntax highlighting
- ✅ **Source Code Summary** - File list and dependencies  
- ✅ **Effort Estimation Table** - Formatted table with hours/days

## Expected Output

```
🔄 Starting analysis...

📥 Fetching Jira issue: DL-61404
✅ Issue fetched: Sample Issue Title
🔍 Generating pseudo code for ANGULAR
✅ Pseudo code generated (Complexity: Complex)
💻 Generating source code
✅ Generated 5 source files
📊 Calculating effort estimation
✅ Estimated: 2.0 days (without buffer)
📝 Generating markdown report
✅ Report saved to: output/DL-61404_angular_analysis.md

📤 Posting analysis to Jira issue: DL-61404
✅ Comment added to Jira issue: DL-61404
✅ Successfully updated Jira issue with analysis

================================================================================
✅ ANALYSIS COMPLETE!
================================================================================

📄 Markdown report saved to: output/DL-61404_angular_analysis.md
📤 Jira issue updated with analysis
📝 Total Effort: 2.0 days
📝 With Buffer: 2.4 days
💻 Files Generated: 5
```

## Verify in Jira

1. Go to: https://godigit.atlassian.net/browse/DL-61404
2. Check the **Comments** section
3. You should see a new comment with:
   - Pseudo code in code blocks
   - Source file list
   - Effort estimation table

## Troubleshooting

### "Jira credentials not found in .env"
- Make sure `.env` file exists in project root
- Check that variables are set correctly

### "Failed to add comment: 401"
- API token may be expired
- Regenerate token at: https://id.atlassian.com/manage-profile/security/api-tokens

### "Failed to add comment: 404"
- Issue ID may not exist
- Check the issue ID is correct

### Import errors
```bash
pip install requests python-dotenv
```
