"""
FastAPI Web API for Jira Analysis Agent
Provides REST endpoints to trigger analysis and updates
"""
from fastapi import FastAPI, HTTPException, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
from src.agent import JiraAnalysisAgent, AgentConfig
import base64
import os

app = FastAPI(
    title="Jira Analysis Agent API",
    description="AI-powered Jira issue analysis with code generation and effort estimation",
    version="1.0.0"
)

security = HTTPBearer()

class AnalysisRequest(BaseModel):
    issue_id: str
    language: str = "BE"  # "BE" for Java backend, "UI" for Angular frontend
    max_hours: float = 4.0
    assign_to: Optional[str] = None
    repository_name: Optional[str] = None
    repository_organization: Optional[str] = None
    azure_organization: Optional[str] = None
    azure_project: Optional[str] = None
    jira_base_url: Optional[str] = None  # Optional: override base URL
    jira_username: Optional[str] = None  # Optional: can use token auth instead
    jira_api_token: Optional[str] = None  # Optional: can use token auth instead

class AnalysisResponse(BaseModel):
    success: bool
    message: str
    issue_id: str
    total_hours: Optional[float] = None
    total_days: Optional[float] = None

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "service": "Jira Analysis Agent",
        "version": "1.0.0"
    }

def parse_authorization(authorization: Optional[str] = Header(None)) -> tuple[Optional[str], Optional[str]]:
    """
    Parse Authorization header for Jira credentials
    Supports: Bearer token format "username:api_token" (base64 encoded)
    """
    if not authorization:
        return None, None
    
    try:
        # Remove "Bearer " prefix
        if authorization.startswith("Bearer "):
            token = authorization[7:]
            # Decode base64
            decoded = base64.b64decode(token).decode('utf-8')
            # Split username:token
            if ':' in decoded:
                username, api_token = decoded.split(':', 1)
                return username, api_token
    except Exception:
        pass
    
    return None, None

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_issue(request: AnalysisRequest, authorization: Optional[str] = Header(None)):
    """
    Analyze a Jira issue and update it with pseudo code, source code, and effort estimation
    
    Authentication:
    - Option 1: Include jira_username and jira_api_token in request body
    - Option 2: Use Authorization header: Bearer base64(username:api_token)
    - Option 3: Falls back to .env file if no credentials provided
    
    Args:
        request: Analysis request with issue_id and configuration
        authorization: Optional Authorization header with Jira credentials
        
    Returns:
        AnalysisResponse with success status and details
    """
    try:
        # Determine Jira credentials (priority: body > header > env)
        jira_username = request.jira_username
        jira_api_token = request.jira_api_token
        
        # Try to get from Authorization header if not in body
        if not jira_username or not jira_api_token:
            header_username, header_token = parse_authorization(authorization)
            jira_username = jira_username or header_username
            jira_api_token = jira_api_token or header_token
        
        # Override environment variables if credentials provided
        if jira_username and jira_api_token:
            os.environ['JIRA_USERNAME'] = jira_username
            os.environ['JIRA_API_TOKEN'] = jira_api_token
            print(f"🔐 Using provided Jira credentials for user: {jira_username}")
        else:
            print(f"🔐 Using Jira credentials from .env file")

        # Override base URL if provided
        if request.jira_base_url:
            os.environ['JIRA_BASE_URL'] = request.jira_base_url
            print(f"🔗 Using provided Jira base URL: {request.jira_base_url}")
        
        # Create agent with configuration
        config = AgentConfig(
            language=request.language,  # type: ignore
            max_hours=request.max_hours
        )
        
        agent = JiraAnalysisAgent(config)
        
        # Analyze the issue
        print(f"🚀 Starting analysis for {request.issue_id}")
        result = agent.analyze_issue(
            issue_id=request.issue_id,
            repository_name=request.repository_name,
            repository_organization=request.repository_organization,
            azure_organization=request.azure_organization,
            azure_project=request.azure_project
        )
        
        # Update Jira with the analysis
        print(f"📤 Updating Jira issue {request.issue_id}")
        success = agent.update_jira_with_analysis(
            result=result,
            repository_name=request.repository_name,
            repository_organization=request.repository_organization,
            azure_organization=request.azure_organization,
            azure_project=request.azure_project,
            assign_to=request.assign_to
        )
        
        if success:
            return AnalysisResponse(
                success=True,
                message=f"Successfully analyzed and updated {request.issue_id}",
                issue_id=request.issue_id,
                total_hours=result.effort_estimate.total_hours,
                total_days=result.effort_estimate.total_days
            )
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to update Jira issue"
            )
            
    except ValueError as e:
        # Propagate known validation issues (e.g., Jira returns 404)
        message = str(e)
        print(f"❌ Error: {message}")
        raise HTTPException(status_code=404, detail=message)
    except Exception as e:
        # Unknown/unhandled errors
        print(f"❌ Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """Health check for monitoring"""
    return {"status": "healthy"}

def start():
    """Start the API server - can be called from anywhere"""
    import uvicorn
    print("\n" + "="*60)
    print("  🚀 Starting Jira Analysis Agent API")
    print("="*60)
    print("\n📍 API Endpoints:")
    print("   • Health Check:  http://localhost:8000/")
    print("   • API Docs:      http://localhost:8000/docs")
    print("   • Health Status: http://localhost:8000/health")
    print("   • Analyze Issue: http://localhost:8000/analyze (POST)")
    print("\n⚡ Server starting on http://localhost:8000")
    print("📖 Interactive docs available at http://localhost:8000/docs")
    print("\n✨ Press Ctrl+C to stop the server\n")
    print("="*60 + "\n")
    
    # Use import string for reload to work properly
    uvicorn.run("web_api:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    start()
