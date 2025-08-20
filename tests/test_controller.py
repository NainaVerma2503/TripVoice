

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_endpoint(endpoint, method="GET", data=None, params=None):
    """Test a single endpoint and return the result"""
    try:
        if method == "GET":
            response = requests.get(f"{BASE_URL}{endpoint}", params=params)
        elif method == "POST":
            response = requests.post(f"{BASE_URL}{endpoint}", json=data)
        else:
            return f"❌ Unsupported method: {method}"
        
        if response.status_code == 200:
            return f"✅ {method} {endpoint}: {response.status_code}"
        else:
            return f"❌ {method} {endpoint}: {response.status_code} - {response.text}"
    
    except requests.exceptions.ConnectionError:
        return f"❌ {method} {endpoint}: Connection failed - Is the Flask service running?"
    except Exception as e:
        return f"❌ {method} {endpoint}: Error - {str(e)}"

def run_tests():
    """Run all controller tests"""
    print("🚀 Testing TripVoice Controller Endpoints")
    print("=" * 50)
    
    # Test basic endpoints
    print("\n📋 Basic Endpoints:")
    print(test_endpoint("/"))
    print(test_endpoint("/health"))
    print(test_endpoint("/api/status"))
    
    # Test controller endpoints
    print("\n🎮 Controller Test Endpoints:")
    print(test_endpoint("/test/hello"))
    print(test_endpoint("/test/random"))
    print(test_endpoint("/test/headers"))
    print(test_endpoint("/test/params"))
    print(test_endpoint("/test/params", params={"name": "test", "value": "123"}))
    
    # Test POST endpoint
    print("\n📤 POST Endpoint Test:")
    test_data = {"message": "Hello Controller!", "user": "Tester"}
    print(test_endpoint("/test/echo", method="POST", data=test_data))
    
    # Test status code endpoints
    print("\n🔢 Status Code Tests:")
    for status in [200, 201, 400, 404, 500]:
        print(test_endpoint(f"/test/status/{status}"))
    
    print("\n" + "=" * 50)
    print("✨ Controller testing completed!")

if __name__ == "__main__":
    run_tests() 