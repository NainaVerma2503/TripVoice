#!/usr/bin/env python3
"""
Test script for the search API that extracts both flights and hotels
"""

import requests
import json
from datetime import datetime

def test_search_api():
    """Test the search API with flight and hotel data"""
    
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
                    "adults": {
                        "count": 2,
                        "metadata": []
                    },
                    "children": {
                        "count": 0,
                        "metadata": []
                    }
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
    
    print("🚀 Testing Search API with Flight and Hotel Extraction")
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
            
            # Display flights
            flights = result.get('flights', [])
            print(f"✈️  Flights ({len(flights)} found):")
            print("-" * 30)
            
            for i, flight in enumerate(flights, 1):
                print(f"Flight {i}:")
                print(f"  ID: {flight.get('id')}")
                print(f"  Airline: {flight.get('airline')}")
                print(f"  Flight Number: {flight.get('flightNumber')}")
                print(f"  Route: {flight.get('departureAirport')} → {flight.get('arrivalAirport')}")
                print(f"  Departure: {flight.get('departureTime')} (Terminal {flight.get('departureTerminal')})")
                print(f"  Arrival: {flight.get('arrivalTime')} (Terminal {flight.get('arrivalTerminal')})")
                print(f"  Duration: {flight.get('totalDuration')}")
                print(f"  Stops: {flight.get('stops')} - {flight.get('stopDetails')}")
                print()
            
            # Display hotels
            hotels = result.get('hotels', [])
            print(f"🏨 Hotels ({len(hotels)} found):")
            print("-" * 30)
            
            for i, hotel in enumerate(hotels, 1):
                print(f"Hotel {i}:")
                print(f"  ID: {hotel.get('id')}")
                print(f"  Name: {hotel.get('name')}")
                location = hotel.get('location', {})
                print(f"  Location: {location.get('address')}, {location.get('area')}, {location.get('city')}")
                price = hotel.get('price', {})
                print(f"  Price: {price.get('amount')} {price.get('currency')}")
                print(f"  Rating: {hotel.get('rating')}/5")
                print(f"  Amenities: {', '.join(hotel.get('amenities', []))}")
                print()
            
            # Save response to file
            with open('search_response.json', 'w') as f:
                json.dump(result, f, indent=2)
            print("💾 Full response saved to 'search_response.json'")
            
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
    test_search_api()
    show_curl_command()

