import requests
import json

def test_different_hotel_formats():
    """Test different hotel data formats to see what Cleartrip accepts"""
    
    # Test different possible formats
    test_formats = [
        {
            "name": "Format 1: Simple structure",
            "data": {
                "city": "Mumbai",
                "checkInDate": "22/08/2025",
                "checkOutDate": "23/08/2025",
                "adults": 1,
                "rooms": 1
            }
        },
        {
            "name": "Format 2: With cityId",
            "data": {
                "cityId": "32550",
                "city": "Mumbai",
                "checkInDate": "22/08/2025",
                "checkOutDate": "23/08/2025",
                "adults": 1,
                "rooms": 1
            }
        },
        {
            "name": "Format 3: String adults",
            "data": {
                "cityId": "32550",
                "city": "Mumbai",
                "checkInDate": "22/08/2025",
                "checkOutDate": "23/08/2025",
                "adults": "1",
                "rooms": "1"
            }
        },
        {
            "name": "Format 4: Minimal required",
            "data": {
                "city": "Mumbai",
                "checkInDate": "22/08/2025",
                "checkOutDate": "23/08/2025"
            }
        },
        {
            "name": "Format 5: Different endpoint structure",
            "data": {
                "destination": "Mumbai",
                "checkin": "22/08/2025",
                "checkout": "23/08/2025",
                "guests": 1
            }
        }
    ]
    
    base_url = "https://qa2new.cleartrip.com/hotel/orchestrator/v2/search"
    
    for i, test_format in enumerate(test_formats, 1):
        print(f"\n{'='*60}")
        print(f"🧪 TESTING FORMAT {i}: {test_format['name']}")
        print(f"{'='*60}")
        
        try:
            print(f"📋 Request data:")
            print(json.dumps(test_format['data'], indent=2))
            
            response = requests.post(
                base_url,
                json=test_format['data'],
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            print(f"📡 Response Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ SUCCESS! Here's the data structure:")
                print(json.dumps(data, indent=2))
                
                # Analyze the structure
                if isinstance(data, dict):
                    print(f"\n🔍 STRUCTURE ANALYSIS:")
                    print(f"Top level keys: {list(data.keys())}")
                    
                    # Look for hotels
                    for key in ['hotels', 'data', 'results', 'items']:
                        if key in data:
                            items = data[key]
                            if isinstance(items, list):
                                print(f"Found '{key}' array with {len(items)} items")
                                if items:
                                    print(f"First item structure:")
                                    print(json.dumps(items[0], indent=2))
                                    break
                
                # Check if this is a successful response (not just 400 status)
                if 'statusCode' in data and data['statusCode'] == 200:
                    print("🎉 THIS FORMAT WORKS PERFECTLY! Use this structure.")
                    return test_format['data']
                elif 'statusCode' in data:
                    print(f"⚠️ Got response but statusCode: {data['statusCode']} - need to fix format")
                else:
                    print("🎉 THIS FORMAT WORKS! Use this structure.")
                    return test_format['data']
                
            else:
                print(f"❌ ERROR: {response.status_code}")
                print("Response text:", response.text[:200])  # Show first 200 chars
                
        except Exception as e:
            print(f"❌ EXCEPTION: {str(e)}")
    
    print("\n❌ No format worked. Let's try a different approach.")
    return None

def test_simple_hotel_search():
    """Try a very simple hotel search"""
    
    print(f"\n{'='*60}")
    print("🧪 TESTING SIMPLE HOTEL SEARCH")
    print(f"{'='*60}")
    
    # Try different possible endpoints
    endpoints = [
        "https://qa2new.cleartrip.com/hotel/search",
        "https://qa2new.cleartrip.com/hotel/v1/search",
        "https://qa2new.cleartrip.com/hotel/api/search"
    ]
    
    simple_data = {
        "city": "Mumbai",
        "checkInDate": "22/08/2025",
        "checkOutDate": "23/08/2025"
    }
    
    for endpoint in endpoints:
        try:
            print(f"\n📍 Trying endpoint: {endpoint}")
            
            response = requests.post(
                endpoint,
                json=simple_data,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            print(f"📡 Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ SUCCESS! This endpoint works!")
                print("Data structure:")
                print(json.dumps(data, indent=2))
                return endpoint, simple_data
            else:
                print(f"❌ Failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
    
    return None, None

if __name__ == "__main__":
    print("🚀 Testing Different Hotel API Formats...")
    
    # Test different data formats
    working_format = test_different_hotel_formats()
    
    if not working_format:
        # Try different endpoints
        working_endpoint, working_data = test_simple_hotel_search()
        
        if working_endpoint:
            print(f"\n🎉 SUCCESS! Use this endpoint and data:")
            print(f"Endpoint: {working_endpoint}")
            print(f"Data: {json.dumps(working_data, indent=2)}")
        else:
            print("\n❌ No working format found. Need to investigate further.") 