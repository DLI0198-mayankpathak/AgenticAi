"""
Test script for the Web API
Run this after starting the API with: python web_api.py
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the root endpoint"""
    print("🧪 Testing health check...")
    response = requests.get(f"{BASE_URL}/")
    print(f"✅ Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    print()

def test_health():
    """Test the health endpoint"""
    print("🧪 Testing /health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"✅ Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    print()

def test_analyze(issue_id="DL-123"):
    """Test the analyze endpoint"""
    print(f"🧪 Testing analysis for issue: {issue_id}...")
    
    payload = {
        "issue_id": issue_id,
        "language": "BE",  # "BE" for Java backend, "UI" for Angular frontend
        "max_hours": 4.0
    }
    
    response = requests.post(
        f"{BASE_URL}/analyze",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"✅ Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   Success: {result.get('success')}")
        print(f"   Message: {result.get('message')}")
        print(f"   Total Hours: {result.get('total_hours')}")
        print(f"   Total Days: {result.get('total_days')}")
    else:
        print(f"   Error: {response.text}")
    print()

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Web API Test Suite")
    print("=" * 60)
    print()
    
    try:
        test_health_check()
        test_health()
        
        # Uncomment to test actual analysis (requires valid Jira issue)
        # test_analyze("DL-123")
        
        print("=" * 60)
        print("✅ All tests completed!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to API")
        print("   Make sure the API is running: python web_api.py")
    except Exception as e:
        print(f"❌ Error: {e}")
