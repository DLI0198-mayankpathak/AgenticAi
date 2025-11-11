"""
Test script for updated features:
1. Check both Description and Story/Task Description fields
2. Update assignee through API
"""
import requests
import json

# API endpoint
API_URL = "http://127.0.0.1:8000/analyze"

def test_be_with_assignee():
    """Test Backend (Java) analysis with assignee update"""
    print("\n" + "="*60)
    print("Test 1: Backend (Java) with Assignee")
    print("="*60)
    
    payload = {
        "issue_id": "DL-61395",
        "language": "BE",
        "max_hours": 8.0,
        "assign_to": "mayank.pathak@godigit.com"  # Replace with actual developer email
    }
    
    print(f"\n📤 Sending request:")
    print(json.dumps(payload, indent=2))
    
    response = requests.post(API_URL, json=payload)
    
    print(f"\n📥 Response ({response.status_code}):")
    print(json.dumps(response.json(), indent=2))
    
    return response.status_code == 200


def test_ui_without_assignee():
    """Test Frontend (Angular) analysis without assignee"""
    print("\n" + "="*60)
    print("Test 2: Frontend (Angular) without Assignee")
    print("="*60)
    
    payload = {
        "issue_id": "DL-61396",
        "language": "UI",
        "max_hours": 6.0
    }
    
    print(f"\n📤 Sending request:")
    print(json.dumps(payload, indent=2))
    
    response = requests.post(API_URL, json=payload)
    
    print(f"\n📥 Response ({response.status_code}):")
    print(json.dumps(response.json(), indent=2))
    
    return response.status_code == 200


def test_description_fields():
    """Test that agent checks both Description and Story/Task Description"""
    print("\n" + "="*60)
    print("Test 3: Description Field Detection")
    print("="*60)
    print("\nThe agent will now:")
    print("1. First check standard 'Description' field")
    print("2. If empty, check 'Story/Task Description' custom field")
    print("3. Use whichever has content for code generation")
    
    payload = {
        "issue_id": "DL-61404",
        "language": "BE",
        "max_hours": 8.0
    }
    
    print(f"\n📤 Sending request:")
    print(json.dumps(payload, indent=2))
    print("\n⏳ Watch the console output to see which field is used...")
    
    response = requests.post(API_URL, json=payload)
    
    print(f"\n📥 Response ({response.status_code}):")
    print(json.dumps(response.json(), indent=2))
    
    return response.status_code == 200


def main():
    print("\n" + "="*60)
    print("🧪 TESTING UPDATED FEATURES")
    print("="*60)
    
    print("\n📋 Features being tested:")
    print("  ✓ Check Description field")
    print("  ✓ Check Story/Task Description field")
    print("  ✓ Update assignee via API")
    print("  ✓ BE/UI language syntax")
    
    results = []
    
    # Run tests
    try:
        results.append(("BE with Assignee", test_be_with_assignee()))
        results.append(("UI without Assignee", test_ui_without_assignee()))
        results.append(("Description Fields", test_description_fields()))
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status} - {test_name}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n🎉 All tests passed!")
    else:
        print("\n⚠️  Some tests failed")


if __name__ == "__main__":
    main()
