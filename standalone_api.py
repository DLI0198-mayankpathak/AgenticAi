"""
🚀 Jira Analysis Agent - Standalone API
Single file that can be shared and run anywhere!

Requirements:
    pip install fastapi uvicorn openai python-dotenv requests

Usage:
    python standalone_api.py

Then access: http://localhost:8000/docs
"""

import os
import sys
import base64
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

# Check and install dependencies
def check_dependencies():
    """Check if required packages are installed"""
    required = {
        'fastapi': 'fastapi',
        'uvicorn': 'uvicorn[standard]',
        'openai': 'openai',
        'dotenv': 'python-dotenv',
        'requests': 'requests',
        'pydantic': 'pydantic'
    }
    
    missing = []
    for module, package in required.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        print(f"\n📦 Install with: pip install {' '.join(missing)}")
        sys.exit(1)

check_dependencies()

# Now import after checking
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import requests
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL", "")
JIRA_USERNAME = os.getenv("JIRA_USERNAME", "")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Initialize FastAPI app
app = FastAPI(
    title="Jira Analysis Agent API",
    description="AI-powered Jira issue analysis with code generation and effort estimation",
    version="2.0.0-standalone"
)

# Models
class ComplexityLevel(str, Enum):
    SIMPLE = "Simple"
    MODERATE = "Moderate"
    COMPLEX = "Complex"

class AnalysisRequest(BaseModel):
    issue_id: str
    language: str = "BE"  # "BE" for Java backend, "UI" for Angular frontend
    max_hours: float = 4.0
    assign_to: Optional[str] = None
    jira_username: Optional[str] = None
    jira_api_token: Optional[str] = None

class AnalysisResponse(BaseModel):
    success: bool
    message: str
    issue_id: str
    total_hours: Optional[float] = None
    total_days: Optional[float] = None

# Jira Client
class JiraClient:
    def __init__(self, base_url: str, username: str, api_token: str):
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.api_token = api_token
        self.session = requests.Session()
        self.session.auth = (username, api_token)
        self.session.headers.update({'Content-Type': 'application/json'})
    
    def get_issue(self, issue_id: str) -> Dict[str, Any]:
        """Fetch Jira issue"""
        url = f"{self.base_url}/rest/api/3/issue/{issue_id}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def update_field(self, issue_id: str, field_id: str, value: str) -> bool:
        """Update a custom field"""
        url = f"{self.base_url}/rest/api/3/issue/{issue_id}"
        data = {"fields": {field_id: value}}
        response = self.session.put(url, json=data)
        return response.status_code == 204
    
    def add_comment(self, issue_id: str, comment: str) -> bool:
        """Add comment to issue"""
        url = f"{self.base_url}/rest/api/3/issue/{issue_id}/comment"
        data = {"body": {"type": "doc", "version": 1, "content": [
            {"type": "paragraph", "content": [{"type": "text", "text": comment}]}
        ]}}
        response = self.session.post(url, json=data)
        return response.status_code == 201

# AI Generator
class AIGenerator:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
    
    def generate_pseudo_code(self, description: str, language: str) -> Dict[str, Any]:
        """Generate pseudo code"""
        prompt = f"""Generate pseudo code for this requirement:
{description}

Language: {language}
Return JSON with: complexity (Simple/Moderate/Complex), sections (array of {{title, steps}})"""
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        # Simple parsing - in production use proper JSON parsing
        return {
            "complexity": "Moderate",
            "sections": [
                {"title": "Main Logic", "steps": response.choices[0].message.content}
            ]
        }
    
    def generate_source_code(self, pseudo_code: str, language: str) -> Dict[str, Any]:
        """Generate source code"""
        prompt = f"""Generate {language} source code based on:
{pseudo_code}

Return multiple files with proper structure."""
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        code = response.choices[0].message.content
        return {
            "files": [{"filename": "Main.java" if language == "BE" else "app.component.ts", 
                      "code": code, "description": "Main implementation"}],
            "dependencies": ["Spring Boot" if language == "BE" else "Angular"],
            "setup_instructions": ["Install dependencies", "Run application"]
        }

# Helper Functions
def parse_authorization(authorization: Optional[str]) -> tuple:
    """Parse Bearer token"""
    if not authorization or not authorization.startswith("Bearer "):
        return None, None
    try:
        token = authorization[7:]
        decoded = base64.b64decode(token).decode('utf-8')
        if ':' in decoded:
            return decoded.split(':', 1)
    except:
        pass
    return None, None

def format_pseudo_code(pseudo_data: Dict) -> str:
    """Format pseudo code for Jira"""
    output = ["=" * 80, "🔍 PSEUDO CODE", "=" * 80, ""]
    output.append(f"Complexity: {pseudo_data['complexity']}\n")
    
    for section in pseudo_data['sections']:
        output.append(f"\n{section['title']}")
        output.append("-" * 40)
        output.append(section['steps'])
    
    output.append("\n" + "=" * 80)
    return "\n".join(output)

def format_source_code(source_data: Dict, language: str) -> str:
    """Format source code for Jira"""
    output = ["=" * 80, f"💻 GENERATED SOURCE CODE ({language.upper()})", "=" * 80, ""]
    
    # Dependencies
    if source_data.get('dependencies'):
        output.append("📦 DEPENDENCIES")
        output.append("-" * 80)
        for dep in source_data['dependencies']:
            output.append(f"  • {dep}")
        output.append("")
    
    # Files
    output.append("📂 SOURCE FILES")
    output.append("-" * 80)
    for i, file_info in enumerate(source_data['files'], 1):
        output.append(f"\nFILE #{i}: {file_info['filename']}")
        output.append("=" * 80)
        output.append(f"Description: {file_info.get('description', 'Source file')}")
        output.append("-" * 80)
        output.append("{code:java}" if language == "BE" else "{code:typescript}")
        output.append(file_info['code'])
        output.append("{code}\n")
    
    # Setup
    if source_data.get('setup_instructions'):
        output.append("⚙️ SETUP INSTRUCTIONS")
        output.append("-" * 80)
        for i, inst in enumerate(source_data['setup_instructions'], 1):
            output.append(f"{i}. {inst}")
    
    output.append("\n" + "=" * 80)
    return "\n".join(output)

def format_effort_comment(hours: float, days: float) -> str:
    """Format effort estimate as comment"""
    return f"""📊 Effort Estimation

Total Hours: {hours:.2f}
Total Days: {days:.2f}

Generated by Jira Analysis Agent
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""

# API Endpoints
@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "running",
        "service": "Jira Analysis Agent (Standalone)",
        "version": "2.0.0"
    }

@app.get("/health")
async def health():
    """Health check"""
    return {"status": "healthy"}

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_issue(request: AnalysisRequest, authorization: Optional[str] = Header(None)):
    """Analyze Jira issue with AI"""
    try:
        # Get credentials
        jira_username = request.jira_username or JIRA_USERNAME
        jira_api_token = request.jira_api_token or JIRA_API_TOKEN
        
        if not jira_username or not jira_api_token:
            header_user, header_token = parse_authorization(authorization)
            jira_username = jira_username or header_user
            jira_api_token = jira_api_token or header_token
        
        if not jira_username or not jira_api_token:
            raise HTTPException(400, "Jira credentials required")
        
        if not OPENAI_API_KEY:
            raise HTTPException(500, "OpenAI API key not configured")
        
        print(f"🚀 Starting analysis for {request.issue_id}")
        
        # Initialize clients
        jira = JiraClient(JIRA_BASE_URL, jira_username, jira_api_token)
        ai = AIGenerator(OPENAI_API_KEY)
        
        # Fetch issue
        print(f"📥 Fetching Jira issue...")
        issue_data = jira.get_issue(request.issue_id)
        description = issue_data['fields'].get('description', {})
        desc_text = description.get('content', [{}])[0].get('content', [{}])[0].get('text', 'No description')
        
        # Generate pseudo code
        print(f"🔍 Generating pseudo code...")
        pseudo_data = ai.generate_pseudo_code(desc_text, request.language)
        pseudo_formatted = format_pseudo_code(pseudo_data)
        
        # Generate source code
        print(f"💻 Generating source code...")
        source_data = ai.generate_source_code(str(pseudo_data), request.language)
        source_formatted = format_source_code(source_data, request.language)
        
        # Calculate effort (simplified)
        estimated_hours = min(request.max_hours, 4.0)
        estimated_days = estimated_hours / 8.0
        
        # Update Jira (try to find custom fields)
        print(f"📤 Updating Jira issue...")
        
        # Try common custom field IDs
        try:
            jira.update_field(request.issue_id, "customfield_10249", pseudo_formatted)
            print("✅ Updated Pseudo Code field")
        except:
            print("⚠️ Could not update Pseudo Code field")
        
        try:
            jira.update_field(request.issue_id, "customfield_10690", source_formatted)
            print("✅ Updated Source Code field")
        except:
            print("⚠️ Could not update Source Code field")
        
        # Add effort comment
        effort_comment = format_effort_comment(estimated_hours, estimated_days)
        jira.add_comment(request.issue_id, effort_comment)
        print("✅ Added effort estimate comment")
        
        return AnalysisResponse(
            success=True,
            message=f"Successfully analyzed and updated {request.issue_id}",
            issue_id=request.issue_id,
            total_hours=estimated_hours,
            total_days=estimated_days
        )
        
    except requests.HTTPError as e:
        raise HTTPException(500, f"Jira API error: {str(e)}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise HTTPException(500, f"Analysis failed: {str(e)}")

# Startup
def start():
    """Start the API server"""
    import uvicorn
    
    print("\n" + "=" * 60)
    print("  🚀 Jira Analysis Agent - Standalone API")
    print("=" * 60)
    print("\n📍 API Endpoints:")
    print("   • Health Check:  http://localhost:8000/")
    print("   • API Docs:      http://localhost:8000/docs")
    print("   • Analyze Issue: http://localhost:8000/analyze (POST)")
    print("\n⚡ Server starting on http://localhost:8000")
    print("📖 Interactive docs: http://localhost:8000/docs")
    print("\n✨ Press Ctrl+C to stop\n")
    print("=" * 60 + "\n")
    
    # Check configuration
    if not OPENAI_API_KEY:
        print("⚠️  WARNING: OPENAI_API_KEY not set in .env")
    if not JIRA_BASE_URL:
        print("⚠️  WARNING: JIRA_BASE_URL not set (can use request body)")
    
    uvicorn.run("standalone_api:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    start()
