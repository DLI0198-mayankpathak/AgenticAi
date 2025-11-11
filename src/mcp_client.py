"""
MCP Integration Module for Jira and Bitbucket
This module provides interfaces to interact with MCP server tools
Falls back to direct REST API if MCP is not available
"""
import os
import requests
from requests.auth import HTTPBasicAuth
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv
from .models import JiraIssue

# Load environment variables from .env file
load_dotenv()


class MCPJiraClient:
    """Client for interacting with Jira through MCP or direct REST API"""
    
    def __init__(self, provider: str = "jira"):
        self.provider = provider
        # Load credentials from environment
        self.jira_base_url = os.getenv("JIRA_BASE_URL", "")
        self.jira_username = os.getenv("JIRA_USERNAME", "")
        self.jira_api_token = os.getenv("JIRA_API_TOKEN", "")
        self.use_direct_api = bool(self.jira_base_url and self.jira_username and self.jira_api_token)
        
        # Cache for custom field IDs
        self._field_id_cache = {}
        
        # Debug: Print loaded values (masked)
        if self.use_direct_api:
            print(f"🔐 Jira credentials loaded from .env")
            print(f"   Base URL: {self.jira_base_url}")
            print(f"   Username: {self.jira_username}")
            print(f"   API Token: {'*' * 20}...{self.jira_api_token[-4:] if len(self.jira_api_token) > 4 else '****'}")
        else:
            print(f"⚠️  Jira credentials check:")
            print(f"   JIRA_BASE_URL: {'✓' if self.jira_base_url else '✗ Missing'}")
            print(f"   JIRA_USERNAME: {'✓' if self.jira_username else '✗ Missing'}")
            print(f"   JIRA_API_TOKEN: {'✓' if self.jira_api_token else '✗ Missing'}")
    
    def get_issue_detail(
        self, 
        issue_id: str,
        azure_organization: Optional[str] = None,
        azure_project: Optional[str] = None,
        repository_name: Optional[str] = None,
        repository_organization: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Fetch detailed information about a Jira issue
        Checks both Description and Story/Task Description fields
        
        Args:
            issue_id: The Jira issue ID (e.g., "DL-123")
            azure_organization: Optional Azure DevOps organization
            azure_project: Optional Azure DevOps project
            repository_name: Optional repository name (for GitHub/GitLab)
            repository_organization: Optional organization name (for GitHub/GitLab)
            
        Returns:
            Dictionary containing issue details
        """
        if not self.use_direct_api:
            print("⚠️  Jira credentials not found in .env")
            return {
                "issue_id": issue_id,
                "title": "Sample Issue Title",
                "description": "Sample issue description",
                "issue_type": "Feature",
                "priority": "High",
                "status": "Open"
            }
        
        try:
            # Jira REST API endpoint
            url = f"{self.jira_base_url}/rest/api/3/issue/{issue_id}"
            
            # Authentication
            auth = HTTPBasicAuth(self.jira_username, self.jira_api_token)
            
            # Headers
            headers = {"Accept": "application/json"}
            
            # Make request
            response = requests.get(url, auth=auth, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                fields = data.get("fields", {})
                
                # Extract description from either Description or Story/Task Description
                description = ""
                
                # First, try standard description field
                desc_field = fields.get("description")
                if desc_field:
                    description = self._adf_to_text(desc_field)
                
                # If no description, try Story/Task Description custom field
                # We need to search for it since custom field IDs vary
                if not description:
                    for field_key, field_value in fields.items():
                        if field_key.startswith("customfield_") and field_value:
                            # Get field metadata to check name
                            field_name = self._get_field_name(field_key)
                            if field_name and ("story" in field_name.lower() or "task" in field_name.lower()):
                                if isinstance(field_value, dict):
                                    description = self._adf_to_text(field_value)
                                elif isinstance(field_value, str):
                                    description = field_value
                                if description:
                                    print(f"   Using '{field_name}' field as description")
                                    break
                
                # Return issue details
                return {
                    "issue_id": issue_id,
                    "title": fields.get("summary", ""),
                    "description": description or "No description available",
                    "issue_type": fields.get("issuetype", {}).get("name", "Task"),
                    "priority": fields.get("priority", {}).get("name", "Medium"),
                    "status": fields.get("status", {}).get("name", "Open"),
                    "assignee": fields.get("assignee", {}).get("displayName") if fields.get("assignee") else None,
                    "labels": fields.get("labels", []),
                    "components": [c.get("name") for c in fields.get("components", [])],
                    "raw_data": data
                }
            elif response.status_code == 404:
                print(f"❌ Issue not found: {issue_id}")
                raise ValueError(f"Issue {issue_id} not found")
            elif response.status_code == 401:
                print(f"❌ Authentication failed")
                raise ValueError("Authentication failed")
            else:
                print(f"❌ Failed to fetch issue: {response.status_code}")
                raise ValueError(f"Failed to fetch issue: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error fetching issue: {e}")
            raise
    
    def parse_issue_response(self, response: Dict[str, Any]) -> JiraIssue:
        """Parse MCP response into JiraIssue model"""
        return JiraIssue(
            issue_id=response.get("issue_id", ""),
            title=response.get("title", ""),
            description=response.get("description", ""),
            issue_type=response.get("issue_type", "Task"),
            priority=response.get("priority", "Medium"),
            assignee=response.get("assignee"),
            status=response.get("status", "Open"),
            labels=response.get("labels", []),
            components=response.get("components", []),
            raw_data=response
        )
    
    def add_comment(
        self,
        issue_id: str,
        comment: str,
        azure_organization: Optional[str] = None,
        azure_project: Optional[str] = None,
        repository_name: Optional[str] = None,
        repository_organization: Optional[str] = None
    ) -> bool:
        """
        Add a comment to a Jira issue using direct REST API
        
        Uses credentials from .env:
        - JIRA_BASE_URL
        - JIRA_USERNAME  
        - JIRA_API_TOKEN
        
        Args:
            issue_id: The Jira issue ID
            comment: The comment text to add (Markdown format)
            
        Returns:
            True if successful, False otherwise
        """
        if not self.use_direct_api:
            print("⚠️  Jira credentials not found in .env")
            print("   Please configure: JIRA_BASE_URL, JIRA_USERNAME, JIRA_API_TOKEN")
            return False
        
        try:
            # Convert Markdown comment to Atlassian Document Format (ADF)
            adf_content = self._markdown_to_adf(comment)
            
            # Jira REST API endpoint
            url = f"{self.jira_base_url}/rest/api/3/issue/{issue_id}/comment"
            
            # Authentication
            auth = HTTPBasicAuth(self.jira_username, self.jira_api_token)
            
            # Headers
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            
            # Payload with ADF
            payload = {
                "body": adf_content
            }
            
            # Make request
            response = requests.post(url, json=payload, auth=auth, headers=headers)
            
            if response.status_code in [200, 201]:
                print(f"✅ Comment added to Jira issue: {issue_id}")
                print(f"   View issue: {self.jira_base_url}/browse/{issue_id}")
                return True
            elif response.status_code == 404:
                print(f"❌ Failed to add comment: Issue not found (404)")
                print(f"   Issue ID: {issue_id}")
                print(f"   URL checked: {self.jira_base_url}/browse/{issue_id}")
                print(f"   Possible reasons:")
                print(f"   - Issue does not exist")
                print(f"   - Issue ID format is incorrect (e.g., use 'DL-61404' not 'DL61404')")
                print(f"   - You don't have permission to view this issue")
                print(f"   - Issue is in a different Jira instance")
                print(f"   Please verify the issue exists by visiting the URL above")
                return False
            elif response.status_code == 401:
                print(f"❌ Failed to add comment: Authentication failed (401)")
                print(f"   Please check your JIRA_USERNAME and JIRA_API_TOKEN in .env")
                print(f"   API Token may be expired - regenerate at:")
                print(f"   https://id.atlassian.com/manage-profile/security/api-tokens")
                return False
            elif response.status_code == 403:
                print(f"❌ Failed to add comment: Permission denied (403)")
                print(f"   You don't have permission to add comments to this issue")
                return False
            else:
                print(f"❌ Failed to add comment: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error adding comment to Jira: {e}")
            return False
    
    def assign_issue(
        self,
        issue_id: str,
        assignee: str
    ) -> bool:
        """
        Assign a Jira issue to a user
        
        Args:
            issue_id: The Jira issue ID
            assignee: Email address or account ID of the assignee
            
        Returns:
            True if successful, False otherwise
        """
        if not self.use_direct_api:
            print("⚠️  Jira credentials not found in .env")
            return False
        
        try:
            # First, try to find the user by email or name
            account_id = self._get_account_id(assignee)
            
            if not account_id:
                print(f"⚠️  Could not find user: {assignee}")
                print(f"   Please verify the email address or username is correct")
                return False
            
            # Jira REST API endpoint for assignment
            url = f"{self.jira_base_url}/rest/api/3/issue/{issue_id}/assignee"
            
            # Authentication
            auth = HTTPBasicAuth(self.jira_username, self.jira_api_token)
            
            # Headers
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            
            # Payload
            payload = {
                "accountId": account_id
            }
            
            # Make request
            response = requests.put(url, json=payload, auth=auth, headers=headers)
            
            if response.status_code == 204:
                return True
            elif response.status_code == 404:
                print(f"⚠️  Issue or user not found")
                return False
            elif response.status_code == 401:
                print(f"⚠️  Authentication failed")
                return False
            elif response.status_code == 403:
                print(f"⚠️  No permission to assign this issue")
                return False
            else:
                print(f"⚠️  Failed to assign: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"⚠️  Error assigning issue: {e}")
            return False
    
    def _get_account_id(self, email_or_name: str) -> Optional[str]:
        """
        Get Jira account ID from email address or username
        
        Args:
            email_or_name: Email address or display name
            
        Returns:
            Account ID if found, None otherwise
        """
        try:
            # Search for user
            url = f"{self.jira_base_url}/rest/api/3/user/search"
            auth = HTTPBasicAuth(self.jira_username, self.jira_api_token)
            headers = {"Accept": "application/json"}
            
            params = {"query": email_or_name}
            
            response = requests.get(url, params=params, auth=auth, headers=headers)
            
            if response.status_code == 200:
                users = response.json()
                if users and len(users) > 0:
                    # Return the first match
                    user = users[0]
                    print(f"   Found user: {user.get('displayName')} ({user.get('emailAddress')})")
                    return user.get('accountId')
            
            return None
            
        except Exception as e:
            print(f"   Error searching for user: {e}")
            return None
    
    def _get_field_name(self, field_id: str) -> Optional[str]:
        """
        Get field name from field ID
        
        Args:
            field_id: Field ID (e.g., "customfield_10123")
            
        Returns:
            Field name if found, None otherwise
        """
        try:
            # Get all fields
            url = f"{self.jira_base_url}/rest/api/3/field"
            auth = HTTPBasicAuth(self.jira_username, self.jira_api_token)
            headers = {"Accept": "application/json"}
            
            response = requests.get(url, auth=auth, headers=headers)
            
            if response.status_code == 200:
                fields = response.json()
                for field in fields:
                    if field.get("id") == field_id:
                        return field.get("name")
            
            return None
            
        except Exception as e:
            return None
    
    def _adf_to_text(self, adf_content: Any) -> str:
        """
        Convert Atlassian Document Format (ADF) to plain text
        
        Args:
            adf_content: ADF content (dict or string)
            
        Returns:
            Plain text representation
        """
        if isinstance(adf_content, str):
            return adf_content
        
        if not isinstance(adf_content, dict):
            return ""
        
        text_parts = []
        
        def extract_text(node):
            if isinstance(node, dict):
                if node.get("type") == "text":
                    text_parts.append(node.get("text", ""))
                elif "content" in node:
                    for child in node["content"]:
                        extract_text(child)
            elif isinstance(node, list):
                for item in node:
                    extract_text(item)
        
        extract_text(adf_content)
        return " ".join(text_parts)
    
    def get_custom_field_id(self, field_name: str) -> Optional[str]:
        """
        Get the custom field ID from field name
        
        Args:
            field_name: Display name of the field (e.g., "Pseudo Code")
            
        Returns:
            Custom field ID (e.g., "customfield_10123") or the original name if it's already an ID
        """
        # If already a custom field ID, return it
        if field_name.startswith("customfield_"):
            return field_name
        
        # Check cache
        if field_name in self._field_id_cache:
            return self._field_id_cache[field_name]
        
        # Standard fields don't need mapping (including time tracking fields)
        # Note: These must match exact API field names (case-sensitive)
        standard_fields = {
            "description": "description",
            "summary": "summary", 
            "assignee": "assignee",
            "reporter": "reporter",
            "priority": "priority",
            "status": "status",
            "originalEstimate": "originalEstimate",
            "timeestimate": "timeestimate",
            "timespent": "timespent",
            "aggregatetimeoriginalestimate": "aggregatetimeoriginalestimate",
            "originalestimate": "originalEstimate"  # Map lowercase to camelCase
        }
        field_lower = field_name.lower()
        if field_lower in standard_fields:
            return standard_fields[field_lower]
        
        try:
            # Get all fields from Jira
            url = f"{self.jira_base_url}/rest/api/3/field"
            auth = HTTPBasicAuth(self.jira_username, self.jira_api_token)
            headers = {"Accept": "application/json"}
            
            response = requests.get(url, auth=auth, headers=headers)
            
            if response.status_code == 200:
                fields = response.json()
                for field in fields:
                    # Match by name (case-insensitive)
                    if field.get("name", "").lower() == field_name.lower():
                        field_id = field.get("id")
                        # Cache the result
                        self._field_id_cache[field_name] = field_id
                        print(f"   Found custom field: '{field_name}' → {field_id}")
                        return field_id
            
            # If not found, return original name (might be a valid field anyway)
            print(f"   ⚠️  Custom field '{field_name}' not found, using as-is")
            return field_name
            
        except Exception as e:
            print(f"   Error getting custom field ID: {e}")
            return field_name
    
    def update_issue_field(
        self,
        issue_id: str,
        field_name: str,
        field_value: str
    ) -> bool:
        """
        Update a field in a Jira issue (e.g., description, custom fields)
        
        Args:
            issue_id: The Jira issue ID
            field_name: Name of the field to update (e.g., "description", "customfield_10XXX")
            field_value: The value to set (Markdown format for description)
            
        Returns:
            True if successful, False otherwise
        """
        if not self.use_direct_api:
            print("⚠️  Jira credentials not found in .env")
            return False
        
        try:
            # Get the actual field ID (handles custom field name to ID mapping)
            actual_field_id = self.get_custom_field_id(field_name)
            
            # Jira REST API endpoint for updating issue
            url = f"{self.jira_base_url}/rest/api/3/issue/{issue_id}"
            
            # Authentication
            auth = HTTPBasicAuth(self.jira_username, self.jira_api_token)
            
            # Headers
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            
            # Convert markdown to ADF if field is description or a text field
            is_text_field = (
                actual_field_id == "description" or 
                (field_name and ("pseudo" in field_name.lower() or "source" in field_name.lower())) or 
                (actual_field_id and ("pseudo" in actual_field_id.lower() or "source" in actual_field_id.lower()))
            )
            
            # Handle time estimate fields (they require integer values in seconds)
            is_time_field = (
                actual_field_id in ["originalEstimate"] or
                (field_name and "originalEstimate" in field_name.lower()) or
                (actual_field_id and "originalEstimate" in actual_field_id.lower())
            )
            
            if is_text_field:
                adf_content = self._markdown_to_adf(field_value)
                payload = {
                    "fields": {
                        actual_field_id: adf_content
                    }
                }
            elif is_time_field:
                # Time fields require integer values (seconds) and use "update" object
                try:
                    time_value = int(field_value)
                    payload = {
                        "update": {
                            actual_field_id: [{"set": time_value}]
                        }
                    }
                except ValueError:
                    print(f"⚠️  Invalid time value: {field_value} (must be integer seconds)")
                    return False
            else:
                # For other fields, use plain value
                payload = {
                    "fields": {
                        actual_field_id: field_value
                    }
                }
            
            # Make request
            response = requests.put(url, json=payload, auth=auth, headers=headers)
            
            if response.status_code == 204:
                return True
            elif response.status_code == 404:
                print(f"⚠️  Issue not found: {issue_id}")
                return False
            elif response.status_code == 401:
                print(f"⚠️  Authentication failed")
                return False
            elif response.status_code == 403:
                print(f"⚠️  No permission to edit this issue")
                return False
            elif response.status_code == 400:
                print(f"⚠️  Invalid field or value")
                print(f"   Response: {response.text}")
                return False
            else:
                print(f"⚠️  Failed to update field: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"⚠️  Error updating issue field: {e}")
            return False
    
    def _markdown_to_adf(self, markdown_text: str) -> Dict[str, Any]:
        """
        Convert Markdown text to Atlassian Document Format (ADF)
        Simplified conversion for common elements
        """
        content = []
        lines = markdown_text.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # Handle code blocks
            if line.strip().startswith('```'):
                # Extract language if specified
                language = line.strip()[3:].strip() or "text"
                code_lines = []
                i += 1
                
                # Collect code lines until closing ```
                while i < len(lines) and not lines[i].strip().startswith('```'):
                    code_lines.append(lines[i])
                    i += 1
                
                if code_lines:
                    content.append({
                        "type": "codeBlock",
                        "attrs": {"language": language},
                        "content": [{
                            "type": "text",
                            "text": '\n'.join(code_lines)
                        }]
                    })
                i += 1
                continue
            
            # Handle headings
            if line.startswith('###'):
                content.append({
                    "type": "heading",
                    "attrs": {"level": 3},
                    "content": [{"type": "text", "text": line[3:].strip()}]
                })
            elif line.startswith('##'):
                content.append({
                    "type": "heading",
                    "attrs": {"level": 2},
                    "content": [{"type": "text", "text": line[2:].strip()}]
                })
            elif line.startswith('#'):
                content.append({
                    "type": "heading",
                    "attrs": {"level": 1},
                    "content": [{"type": "text", "text": line[1:].strip()}]
                })
            # Handle tables
            elif '|' in line and line.strip().startswith('|'):
                # Parse table
                table_lines = [line]
                i += 1
                while i < len(lines) and '|' in lines[i]:
                    table_lines.append(lines[i])
                    i += 1
                
                table_node = self._parse_table(table_lines)
                if table_node:
                    content.append(table_node)
                continue
            # Handle regular text
            elif line.strip():
                # Check for bold text **text**
                text_content = []
                parts = line.split('**')
                for idx, part in enumerate(parts):
                    if part:
                        if idx % 2 == 1:  # Bold text
                            text_content.append({
                                "type": "text",
                                "text": part,
                                "marks": [{"type": "strong"}]
                            })
                        else:
                            text_content.append({
                                "type": "text",
                                "text": part
                            })
                
                if text_content:
                    content.append({
                        "type": "paragraph",
                        "content": text_content
                    })
            # Handle empty lines
            else:
                content.append({
                    "type": "paragraph",
                    "content": []
                })
            
            i += 1
        
        return {
            "version": 1,
            "type": "doc",
            "content": content
        }
    
    def _parse_table(self, lines: List[str]) -> Optional[Dict[str, Any]]:
        """Parse markdown table to ADF table format"""
        if len(lines) < 2:
            return None
        
        # Parse rows
        rows = []
        for line in lines:
            if '---' in line:  # Skip separator line
                continue
            cells = [cell.strip() for cell in line.split('|') if cell.strip()]
            if cells:
                rows.append(cells)
        
        if not rows:
            return None
        
        # Build ADF table
        table_rows = []
        is_header = True
        
        for row_data in rows:
            cells = []
            for cell_text in row_data:
                # Check if bold
                is_bold = cell_text.startswith('**') and cell_text.endswith('**')
                text = cell_text.strip('*').strip()
                
                cell_content = [{
                    "type": "paragraph",
                    "content": [{
                        "type": "text",
                        "text": text,
                        "marks": [{"type": "strong"}] if is_bold else []
                    }]
                }]
                
                cells.append({
                    "type": "tableHeader" if is_header else "tableCell",
                    "content": cell_content
                })
            
            table_rows.append({
                "type": "tableRow",
                "content": cells
            })
            is_header = False
        
        return {
            "type": "table",
            "attrs": {"isNumberColumnEnabled": False, "layout": "default"},
            "content": table_rows
        }


class MCPBitbucketClient:
    """Client for interacting with Bitbucket through MCP"""
    
    def __init__(self, provider: str = "bitbucket"):
        self.provider = provider
    
    def get_file_content(
        self,
        repository_name: str,
        repository_organization: str,
        file_path: str,
        ref: str = "main",
        azure_project: Optional[str] = None
    ) -> str:
        """
        Get file content from Bitbucket repository
        
        In actual implementation, this would call:
        mcp_gitkraken_repository_get_file_content(
            provider=self.provider,
            repository_name=repository_name,
            repository_organization=repository_organization,
            file_path=file_path,
            ref=ref,
            azure_project=azure_project
        )
        """
        # Placeholder for MCP tool call
        return "// Sample file content"
    
    def create_pull_request(
        self,
        repository_name: str,
        repository_organization: str,
        title: str,
        source_branch: str,
        target_branch: str,
        body: str,
        is_draft: bool = False,
        azure_project: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a pull request in Bitbucket
        
        In actual implementation, this would call:
        mcp_gitkraken_pull_request_create(...)
        """
        # Placeholder for MCP tool call
        return {"pr_id": "123", "url": "https://bitbucket.org/..."}
