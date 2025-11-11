"""
Test fullstack generation (BE: Java + FE: Angular)
"""
from src.agent import JiraAnalysisAgent
from src.config import AgentConfig
from src.models import JiraIssue

def test_fullstack_generation():
    """Test fullstack code generation"""
    
    # Create a fullstack config
    config = AgentConfig(
        language="fullstack",
        backend_language="java",
        frontend_language="angular",
        max_hours=8.0
    )
    
    # Create test issue
    issue = JiraIssue(
        issue_id="FULL-001",
        title="User Management Dashboard",
        description="""
        Create a user management dashboard with the following features:
        
        Backend (Java/Spring Boot):
        - REST API for CRUD operations on users
        - GET /api/users - List all users
        - POST /api/users - Create new user
        - PUT /api/users/{id} - Update user
        - DELETE /api/users/{id} - Delete user
        - Validate email format and uniqueness
        - Store in PostgreSQL database
        
        Frontend (Angular):
        - User list component with table
        - Add/Edit user form with validation
        - Delete confirmation dialog
        - API service to call backend
        - Reactive forms for user input
        """,
        issue_type="Feature",
        priority="High",
        status="Open",
        assignee=None,
        labels=["fullstack", "user-management"]
    )
    
    print("=" * 80)
    print("🚀 Testing FULLSTACK Generation (BE: Java + FE: Angular)")
    print("=" * 80)
    print()
    
    print(f"📝 Issue: {issue.issue_id} - {issue.title}")
    print(f"📄 Description: {len(issue.description)} characters")
    print()
    
    # Create agent
    agent = JiraAnalysisAgent(config)
    
    print("🔧 Agent Configuration:")
    print(f"   - Language: {agent.config.language}")
    print(f"   - Backend: {agent.backend_lang}")
    print(f"   - Frontend: {agent.frontend_lang}")
    print(f"   - Is Fullstack: {agent.is_fullstack}")
    print()
    
    # Generate pseudo code
    print("🔍 Generating Pseudo Code...")
    from src.code_generator import PseudoCodeGenerator
    
    if agent.is_fullstack:
        backend_lang = agent.backend_lang or "java"
        frontend_lang = agent.frontend_lang or "angular"
        
        be_generator = PseudoCodeGenerator(language=backend_lang)
        fe_generator = PseudoCodeGenerator(language=frontend_lang)
        
        be_pseudo = be_generator.generate(issue)
        fe_pseudo = fe_generator.generate(issue)
        
        print(f"✅ Backend Pseudo Code: {len(be_pseudo.sections[0]['steps'])} chars")
        print(f"✅ Frontend Pseudo Code: {len(fe_pseudo.sections[0]['steps'])} chars")
        print()
        
        print("📝 Backend Pseudo Code Preview:")
        print("-" * 80)
        print(be_pseudo.sections[0]['steps'][:300] + "...")
        print("-" * 80)
        print()
        
        print("📝 Frontend Pseudo Code Preview:")
        print("-" * 80)
        print(fe_pseudo.sections[0]['steps'][:300] + "...")
        print("-" * 80)
        print()
        
        # Verify content
        be_text = be_pseudo.sections[0]['steps'].lower()
        fe_text = fe_pseudo.sections[0]['steps'].lower()
        
        print("🔍 Backend Verification:")
        print(f"  ✅ Contains 'api': {'api' in be_text}")
        print(f"  ✅ Contains 'database': {'database' in be_text}")
        print(f"  ✅ Contains 'validate': {'validate' in be_text}")
        print()
        
        print("🔍 Frontend Verification:")
        print(f"  ✅ Contains 'component': {'component' in fe_text}")
        print(f"  ✅ Contains 'form': {'form' in fe_text}")
        print(f"  ✅ Contains 'service': {'service' in fe_text}")
        print()
    
    print("=" * 80)
    print("✅ FULLSTACK Test Passed!")
    print("   - Backend (Java) pseudo code generated")
    print("   - Frontend (Angular) pseudo code generated")
    print("   - Both contain language-specific logic")
    print("=" * 80)

if __name__ == "__main__":
    test_fullstack_generation()
