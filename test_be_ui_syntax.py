"""
Test BE and UI language syntax
"""
from src.agent import JiraAnalysisAgent
from src.config import AgentConfig
from src.models import JiraIssue

def test_be_language():
    """Test BE (Backend/Java) generation"""
    
    print("=" * 70)
    print("🧪 Testing BE (Java) Language Syntax")
    print("=" * 70)
    print()
    
    # Create config with "BE"
    config = AgentConfig(language="BE", max_hours=4.0)
    
    agent = JiraAnalysisAgent(config)
    
    print(f"✅ Config language: {agent.config.language}")
    print(f"✅ Backend lang: {agent.backend_lang}")
    print(f"✅ Frontend lang: {agent.frontend_lang}")
    print(f"✅ Is fullstack: {agent.is_fullstack}")
    
    assert agent.backend_lang == "java", "BE should map to java"
    assert agent.frontend_lang is None, "BE should not have frontend"
    assert not agent.is_fullstack, "BE should not be fullstack"
    
    print()
    print("✅ BE correctly maps to Java backend")
    print()

def test_ui_language():
    """Test UI (Frontend/Angular) generation"""
    
    print("=" * 70)
    print("🧪 Testing UI (Angular) Language Syntax")
    print("=" * 70)
    print()
    
    # Create config with "UI"
    config = AgentConfig(language="UI", max_hours=4.0)
    
    agent = JiraAnalysisAgent(config)
    
    print(f"✅ Config language: {agent.config.language}")
    print(f"✅ Backend lang: {agent.backend_lang}")
    print(f"✅ Frontend lang: {agent.frontend_lang}")
    print(f"✅ Is fullstack: {agent.is_fullstack}")
    
    assert agent.frontend_lang == "angular", "UI should map to angular"
    assert agent.backend_lang is None, "UI should not have backend"
    assert not agent.is_fullstack, "UI should not be fullstack"
    
    print()
    print("✅ UI correctly maps to Angular frontend")
    print()

def test_api_payload():
    """Test API payload examples"""
    
    print("=" * 70)
    print("📡 API Payload Examples")
    print("=" * 70)
    print()
    
    be_payload = {
        "issue_id": "DL-123",
        "language": "BE",
        "max_hours": 8.0
    }
    
    ui_payload = {
        "issue_id": "DL-456",
        "language": "UI",
        "max_hours": 4.0
    }
    
    print("Backend Request:")
    print(f"  {be_payload}")
    print()
    
    print("Frontend Request:")
    print(f"  {ui_payload}")
    print()
    
    print("✅ Simplified API payload structure")
    print()

if __name__ == "__main__":
    test_be_language()
    test_ui_language()
    test_api_payload()
    
    print("=" * 70)
    print("🎉 All Tests Passed!")
    print("=" * 70)
    print()
    print("✅ BE → Java backend")
    print("✅ UI → Angular frontend")
    print()
    print("🌐 API Usage:")
    print("   curl -X POST http://10.232.187.6:8000/analyze \\")
    print("     -H 'Content-Type: application/json' \\")
    print("     -d '{\"issue_id\":\"DL-123\",\"language\":\"BE\",\"max_hours\":8.0}'")
    print()
