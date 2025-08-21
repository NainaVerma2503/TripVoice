#!/usr/bin/env python3
"""
Simple test script for TripVoice API
"""

import requests
import json

def test_trip_planning():
    """Test the trip planning endpoint"""
    
    # Test data
    test_text = "From Delhi to Mumbai for 2 adults"
    
    # Make request
    url = "http://localhost:5001/api/trip/plan"
    headers = {"Content-Type": "application/json"}
    data = {"text": test_text}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
    except Exception as e:
        print(f"Error: {e}")

def test_health():
    """Test the health endpoint"""
    
    url = "http://localhost:5001/api/trip/health"
    
    try:
        response = requests.get(url)
        print(f"Health Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Testing TripVoice API...")
    print("=" * 40)
    
    print("\n1. Testing Health Endpoint:")
    test_health()
    
    print("\n2. Testing Trip Planning:")
    test_trip_planning() 