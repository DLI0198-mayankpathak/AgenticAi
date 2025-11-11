"""
FastAPI Web API for Jira Analysis Agent
Provides REST endpoints to trigger analysis and updates
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from src.agent import JiraAnalysisAgent
from src.config import AgentConfig

app = FastAPI(
    title="Jira Analysis Agent API",
    description="AI-powered Jira issue analysis with code generation and effort estimation",
    version="1.0.0"
)

class AnalysisRequest(BaseModel):
    issue_id: str
    language: str = "BE"  # "BE" for Java backend, "UI" for Angular frontend
    max_hours: float = 4.0
    assign_to: Optional[str] = None
    repository_name: Optional[str] = None
    repository_organization: Optional[str] = None
    azure_organization: Optional[str] = None
    azure_project: Optional[str] = None

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

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_issue(request: AnalysisRequest):
    """
    Analyze a Jira issue and update it with pseudo code, source code, and effort estimation
    
    Args:
        request: Analysis request with issue_id and configuration
        
    Returns:
        AnalysisResponse with success status and details
    """
    try:
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
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """Health check for monitoring"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
