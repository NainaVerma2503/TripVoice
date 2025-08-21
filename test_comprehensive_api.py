#!/usr/bin/env python3
"""
Test script to demonstrate the API with comprehensive mock data
(100 flights and 100 hotels across different locations)
"""

import requests
import json
from datetime import datetime

def test_comprehensive_api():
    """Test the API with comprehensive mock data"""
    
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
    
    print("🚀 Testing Search API with Comprehensive Mock Data")
    print("=" * 70)
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
            
            # Display flights summary
            flights = result.get('flights', [])
            print(f"✈️  Flights Summary ({len(flights)} found):")
            print("-" * 40)
            
            # Group flights by airline
            airlines = {}
            routes = {}
            for flight in flights:
                airline = flight.get('airline', 'Unknown')
                route = f"{flight.get('departureAirport')} → {flight.get('arrivalAirport')}"
                
                airlines[airline] = airlines.get(airline, 0) + 1
                routes[route] = routes.get(route, 0) + 1
            
            print("📊 Airlines Distribution:")
            for airline, count in sorted(airlines.items()):
                print(f"  {airline}: {count} flights")
            
            print("\n📊 Routes Distribution:")
            for route, count in sorted(routes.items()):
                print(f"  {route}: {count} flights")
            
            # Show sample flights
            print(f"\n📋 Sample Flights (showing first 5):")
            for i, flight in enumerate(flights[:5], 1):
                print(f"Flight {i}:")
                print(f"  ID: {flight.get('id')}")
                print(f"  Airline: {flight.get('airline')}")
                print(f"  Flight Number: {flight.get('flightNumber')}")
                print(f"  Route: {flight.get('departureAirport')} → {flight.get('arrivalAirport')}")
                print(f"  Duration: {flight.get('totalDuration')}")
                print(f"  Stops: {flight.get('stops')} - {flight.get('stopDetails')}")
                print()
            
            # Display hotels summary
            hotels = result.get('hotels', [])
            print(f"🏨 Hotels Summary ({len(hotels)} found):")
            print("-" * 40)
            
            # Group hotels by city
            cities = {}
            price_ranges = {"Budget": 0, "Mid-range": 0, "Luxury": 0}
            ratings = {"3★": 0, "4★": 0, "5★": 0}
            
            for hotel in hotels:
                city = hotel.get('location', {}).get('city', 'Unknown')
                price = hotel.get('price', {}).get('amount', 0)
                rating = hotel.get('rating', 0)
                
                cities[city] = cities.get(city, 0) + 1
                
                if price < 5000:
                    price_ranges["Budget"] += 1
                elif price < 10000:
                    price_ranges["Mid-range"] += 1
                else:
                    price_ranges["Luxury"] += 1
                
                if rating == 3:
                    ratings["3★"] += 1
                elif rating == 4:
                    ratings["4★"] += 1
                else:
                    ratings["5★"] += 1
            
            print("📊 Cities Distribution:")
            for city, count in sorted(cities.items()):
                print(f"  {city}: {count} hotels")
            
            print("\n📊 Price Range Distribution:")
            for range_name, count in price_ranges.items():
                print(f"  {range_name}: {count} hotels")
            
            print("\n📊 Rating Distribution:")
            for rating, count in ratings.items():
                print(f"  {rating}: {count} hotels")
            
            # Show sample hotels
            print(f"\n📋 Sample Hotels (showing first 5):")
            for i, hotel in enumerate(hotels[:5], 1):
                print(f"Hotel {i}:")
                print(f"  ID: {hotel.get('id')}")
                print(f"  Name: {hotel.get('name')}")
                location = hotel.get('location', {})
                print(f"  Location: {location.get('city')}, {location.get('area')}")
                price = hotel.get('price', {})
                print(f"  Price: {price.get('amount')} {price.get('currency')}")
                print(f"  Rating: {hotel.get('rating')}/5")
                print(f"  Amenities: {', '.join(hotel.get('amenities', [])[:3])}...")
                print()
            
            # Save response to file
            with open('comprehensive_response.json', 'w') as f:
                json.dump(result, f, indent=2)
            print("💾 Full response saved to 'comprehensive_response.json'")
            
            # Show statistics
            print("\n📈 Data Statistics:")
            print("-" * 30)
            print(f"Total Flights: {len(flights)}")
            print(f"Total Hotels: {len(hotels)}")
            print(f"Unique Airlines: {len(airlines)}")
            print(f"Unique Routes: {len(routes)}")
            print(f"Unique Cities: {len(cities)}")
            
            # Calculate average prices
            if hotels:
                avg_price = sum(h.get('price', {}).get('amount', 0) for h in hotels) / len(hotels)
                print(f"Average Hotel Price: ₹{avg_price:.0f}")
            
            # Calculate average duration
            if flights:
                durations = []
                for flight in flights:
                    duration_str = flight.get('totalDuration', '0h 0m')
                    try:
                        parts = duration_str.split()
                        hours = int(parts[0].replace('h', ''))
                        minutes = int(parts[1].replace('m', ''))
                        durations.append(hours * 60 + minutes)
                    except:
                        durations.append(0)
                
                if durations:
                    avg_duration_minutes = sum(durations) / len(durations)
                    avg_hours = avg_duration_minutes // 60
                    avg_minutes = avg_duration_minutes % 60
                    print(f"Average Flight Duration: {avg_hours}h {avg_minutes}m")
            
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
    
    print("\n" + "=" * 70)
    print("🔧 CURL Command for Manual Testing:")
    print("=" * 70)
    
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
    test_comprehensive_api()
    show_curl_command()
