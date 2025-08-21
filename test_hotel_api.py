import requests
import json

def test_hotel_api_directly():
    """Test hotel API directly to see what's happening"""
    
    # Test hotel data
    hotel_data = {
        "pageSize": 5,
        "pageNo": 1,
        "useCaseContext": "SRP_PAGE",
        "roomAllocations": [
            {
                "adults": 1,
                "children": 0,
                "infants": 0
            }
        ],
        "cityId": "32550",
        "city": "Mumbai",
        "state": "Maharashtra", 
        "country": "IN",
        "checkInDate": "22/08/2025",
        "checkOutDate": "23/08/2025",
        "version": "V2"
    }
    
    try:
        print("🏨 Testing Hotel API Directly...")
        print("📍 Cleartrip Hotel API URL: https://qa2new.cleartrip.com/hotel/orchestrator/v2/search")
        print("📋 Request data:")
        print(json.dumps(hotel_data, indent=2))
        
        # Test Cleartrip API directly
        response = requests.post(
            'https://qa2new.cleartrip.com/hotel/orchestrator/v2/search',
            json=hotel_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"\n📡 Cleartrip API Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ SUCCESS! Here's the raw Cleartrip hotel data:")
            print("=" * 50)
            print(json.dumps(data, indent=2))
            
            # Try to understand the structure
            if isinstance(data, dict):
                print(f"\n🔍 DATA STRUCTURE ANALYSIS:")
                print(f"Top level keys: {list(data.keys())}")
                
                # Look for hotels array
                if 'hotels' in data:
                    print(f"Found 'hotels' array with {len(data['hotels'])} items")
                    if data['hotels']:
                        print("First hotel structure:")
                        print(json.dumps(data['hotels'][0], indent=2))
                
                # Look for other possible keys
                for key in ['data', 'results', 'items']:
                    if key in data:
                        print(f"Found '{key}' key: {type(data[key])}")
                        if isinstance(data[key], list) and data[key]:
                            print(f"First item in '{key}':")
                            print(json.dumps(data[key][0], indent=2))
            
        else:
            print(f"❌ ERROR: {response.status_code}")
            print("Response text:", response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ CONNECTION ERROR: Cannot connect to Cleartrip API")
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

def test_hotel_api_through_flask():
    """Test hotel API through your Flask app"""
    
    hotel_data = {
        "pageSize": 5,
        "pageNo": 1,
        "useCaseContext": "SRP_PAGE",
        "roomAllocations": [
            {
                "adults": 1,
                "children": 0,
                "infants": 0
            }
        ],
        "cityId": "32550",
        "city": "Mumbai",
        "state": "Maharashtra", 
        "country": "IN",
        "checkInDate": "22/08/2025",
        "checkOutDate": "23/08/2025",
        "version": "V2"
    }
    
    try:
        print("\n🏨 Testing Hotel API Through Flask...")
        print("📍 Flask Hotel API: http://localhost:5000/api/hotel/search")
        
        response = requests.post(
            'http://localhost:5000/api/hotel/search',
            json=hotel_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"📡 Flask API Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ SUCCESS! Flask hotel API response:")
            print(json.dumps(data, indent=2))
        else:
            print(f"❌ ERROR: {response.status_code}")
            print("Response text:", response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ CONNECTION ERROR: Make sure Flask server is running")
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

if __name__ == "__main__":
    # Test Cleartrip API directly
    test_hotel_api_directly()
    
    # Test through Flask
    test_hotel_api_through_flask() 