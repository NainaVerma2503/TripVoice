import requests
import json

# Test your search API to see what data comes from Cleartrip
def test_search_api():
    """Test the search API to see Cleartrip response structure"""
    
    # Test data for your search API
    search_data = {
        "flight": {
            "from": "DEL",
            "to": "BOM", 
            "depart_date": "22/08/2025",
            "adults": 1,
            "intl": "n"
        },
        "hotel": {
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
    }
    
    try:
        print("🚀 Testing Search API...")
        print("📍 Sending request to: http://localhost:5000/api/search")
        print("📋 Request data:")
        print(json.dumps(search_data, indent=2))
        
        # Make the API call
        response = requests.post(
            'http://localhost:5000/api/search',
            json=search_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"\n📡 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ SUCCESS! Here's what we got:")
            print("=" * 50)
            
            # Show search summary
            if 'search_summary' in data:
                print("📊 SEARCH SUMMARY:")
                print(json.dumps(data['search_summary'], indent=2))
            
            # Show flights data structure
            if 'flights' in data:
                print(f"\n✈️ FLIGHTS ({len(data['flights'])} found):")
                if data['flights']:
                    print("First flight structure:")
                    print(json.dumps(data['flights'][0], indent=2))
                else:
                    print("No flights found")
            
            # Show hotels data structure
            if 'hotels' in data:
                print(f"\n🏨 HOTELS ({len(data['hotels'])} found):")
                if data['hotels']:
                    print("First hotel structure:")
                    print(json.dumps(data['hotels'][0], indent=2))
                else:
                    print("No hotels found")
            
            # Show raw response status
            if 'raw_responses' in data:
                print(f"\n🔧 RAW API STATUS:")
                print(json.dumps(data['raw_responses'], indent=2))
            
            # Show full response for debugging
            print(f"\n🔍 FULL RESPONSE:")
            print(json.dumps(data, indent=2))
            
        else:
            print(f"❌ ERROR: {response.status_code}")
            print("Response text:", response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ CONNECTION ERROR: Make sure your Flask server is running on port 5000")
        print("💡 Run: source venv/bin/activate && python app.py")
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

if __name__ == "__main__":
    test_search_api() 