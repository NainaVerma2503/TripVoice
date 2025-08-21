#!/usr/bin/env python3
"""
Final test script to verify the API returns both flights and hotels
"""

import requests
import json
from datetime import datetime

def test_final_api():
    """Test the final API with both flights and hotels"""
    
    # API endpoint
    url = "http://localhost:5000/api/search"
    
    # Test data
    test_data = {
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
                    "adults": {"count": 2, "metadata": []},
                    "children": {"count": 0, "metadata": []}
                }
            ],
            "cityId": "32550",
            "city": "Bangalore",
            "state": "Karnataka",
            "country": "IN",
            "checkInDate": "29/08/2025",
            "checkOutDate": "30/08/2025",
            "version": "V2"
        }
    }
    
    print("🚀 Final API Test - Both Flights and Hotels")
    print("=" * 60)
    print(f"📅 Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 API Endpoint: {url}")
    print()
    
    try:
        # Make the API call
        print("📤 Sending request...")
        response = requests.post(url, json=test_data, headers={'Content-Type': 'application/json'})
        
        print(f"📥 Response Status: {response.status_code}")
        print()
        
        if response.status_code == 200:
            result = response.json()
            
            print("✅ SUCCESS! API Response:")
            print("-" * 40)
            
            # Display status and timestamp
            print(f"Status: {result.get('status')}")
            print(f"Timestamp: {result.get('timestamp')}")
            print()
            
            # Display search summary
            search_summary = result.get('search_summary', {})
            print("📊 Search Summary:")
            print(f"  From: {search_summary.get('from')}")
            print(f"  To: {search_summary.get('to')}")
            print(f"  Departure Date: {search_summary.get('departure_date')}")
            print(f"  Adults: {search_summary.get('adults')}")
            print(f"  Total Flights Found: {search_summary.get('total_flights_found')}")
            print(f"  Total Hotels Found: {search_summary.get('total_hotels_found')}")
            print()
            
            # Display flights count
            flights = result.get('flights', [])
            print(f"✈️  Flights: {len(flights)} found")
            
            if flights:
                print("📋 Sample Flights (first 3):")
                for i, flight in enumerate(flights[:3], 1):
                    print(f"  {i}. {flight.get('airline')} {flight.get('flightNumber')} - {flight.get('departureAirport')} → {flight.get('arrivalAirport')} ({flight.get('totalDuration')})")
                print()
            
            # Display hotels count
            hotels = result.get('hotels', [])
            print(f"🏨 Hotels: {len(hotels)} found")
            
            if hotels:
                print("📋 Sample Hotels (first 3):")
                for i, hotel in enumerate(hotels[:3], 1):
                    location = hotel.get('location', {})
                    price = hotel.get('price', {})
                    print(f"  {i}. {hotel.get('name')} - {location.get('city')} (₹{price.get('amount')}) - {hotel.get('rating')}★")
                print()
            
            # Save response to file
            with open('final_response.json', 'w') as f:
                json.dump(result, f, indent=2)
            print("💾 Full response saved to 'final_response.json'")
            
            # Show success message
            if len(flights) > 0 and len(hotels) > 0:
                print("🎉 SUCCESS! API is returning both flights and hotels!")
                print(f"   ✈️  {len(flights)} flights")
                print(f"   🏨 {len(hotels)} hotels")
            else:
                print("⚠️  WARNING: Missing data!")
                if len(flights) == 0:
                    print("   ❌ No flights returned")
                if len(hotels) == 0:
                    print("   ❌ No hotels returned")
            
        else:
            print("❌ ERROR! API call failed")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ ERROR! Could not connect to the API")
        print("Make sure the Flask app is running on http://localhost:5000")
    except Exception as e:
        print(f"❌ ERROR! {str(e)}")

def show_curl_command():
    """Show the curl command for manual testing"""
    
    print("\n" + "=" * 60)
    print("🔧 CURL Command for Manual Testing:")
    print("=" * 60)
    
    curl_command = '''curl -X POST "http://localhost:5000/api/search" \\
  -H "Content-Type: application/json" \\
  -d '{
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
          "adults": {"count": 2, "metadata": []},
          "children": {"count": 0, "metadata": []}
        }
      ],
      "cityId": "32550",
      "city": "Bangalore",
      "state": "Karnataka",
      "country": "IN",
      "checkInDate": "29/08/2025",
      "checkOutDate": "30/08/2025",
      "version": "V2"
    }
  }' | jq '.' '''
    
    print(curl_command)

if __name__ == "__main__":
    test_final_api()
    show_curl_command()
