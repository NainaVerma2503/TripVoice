#!/usr/bin/env python3
"""
Test script for package creation API with GenAI integration
"""

import requests
import json
from datetime import datetime

def test_package_creation():
    """Test the package creation API"""
    
    # API endpoint
    url = "http://localhost:5000/api/package/create"
    
    # Test data with flights, hotels, and user preferences
    test_data = {
        "flights": [
            {
                "id": "flight_001",
                "airline": "IndiGo",
                "flightNumber": "6E-129",
                "departureAirport": "DEL",
                "departureTerminal": "1D",
                "departureTime": "2025-08-22T13:25:00.000+05:30",
                "arrivalAirport": "BOM",
                "arrivalTerminal": "1",
                "arrivalTime": "2025-08-22T15:05:00.000+05:30",
                "totalDuration": "1h 40m",
                "stops": 0,
                "stopDetails": "Direct flight",
                "legs": [
                    {
                        "flightNumber": "6E-129",
                        "departureTerminal": "1D",
                        "arrivalTerminal": "1"
                    }
                ]
            },
            {
                "id": "flight_002",
                "airline": "Vistara",
                "flightNumber": "UK-825",
                "departureAirport": "DEL",
                "departureTerminal": "3",
                "departureTime": "2025-08-22T16:00:00.000+05:30",
                "arrivalAirport": "BOM",
                "arrivalTerminal": "2",
                "arrivalTime": "2025-08-22T18:20:00.000+05:30",
                "totalDuration": "2h 20m",
                "stops": 0,
                "stopDetails": "Direct flight",
                "legs": [
                    {
                        "flightNumber": "UK-825",
                        "departureTerminal": "3",
                        "arrivalTerminal": "2"
                    }
                ]
            },
            {
                "id": "flight_003",
                "airline": "Air India",
                "flightNumber": "AI-101",
                "departureAirport": "DEL",
                "departureTerminal": "1",
                "departureTime": "2025-08-22T14:30:00.000+05:30",
                "arrivalAirport": "BOM",
                "arrivalTerminal": "1",
                "arrivalTime": "2025-08-22T16:45:00.000+05:30",
                "totalDuration": "2h 15m",
                "stops": 0,
                "stopDetails": "Direct flight",
                "legs": [
                    {
                        "flightNumber": "AI-101",
                        "departureTerminal": "1",
                        "arrivalTerminal": "1"
                    }
                ]
            }
        ],
        "hotels": [
            {
                "id": "hotel_001",
                "name": "Taj Palace Hotel",
                "location": {
                    "address": "Apollo Bunder, Mumbai",
                    "area": "Colaba",
                    "city": "Mumbai"
                },
                "price": {
                    "amount": 15000,
                    "currency": "INR"
                },
                "rating": 5,
                "amenities": ["WiFi", "Pool", "Spa", "Restaurant", "Concierge", "Valet Parking"]
            },
            {
                "id": "hotel_002",
                "name": "Oberoi Hotel",
                "location": {
                    "address": "Nariman Point, Mumbai",
                    "area": "Nariman Point",
                    "city": "Mumbai"
                },
                "price": {
                    "amount": 18000,
                    "currency": "INR"
                },
                "rating": 5,
                "amenities": ["WiFi", "Pool", "Spa", "Restaurant", "Fitness Center", "Kids Club"]
            },
            {
                "id": "hotel_003",
                "name": "ITC Grand Central",
                "location": {
                    "address": "Parel, Mumbai",
                    "area": "Parel",
                    "city": "Mumbai"
                },
                "price": {
                    "amount": 12000,
                    "currency": "INR"
                },
                "rating": 4,
                "amenities": ["WiFi", "Pool", "Restaurant", "Business Center", "Airport Shuttle"]
            },
            {
                "id": "hotel_004",
                "name": "Budget Inn",
                "location": {
                    "address": "Andheri, Mumbai",
                    "area": "Andheri",
                    "city": "Mumbai"
                },
                "price": {
                    "amount": 4000,
                    "currency": "INR"
                },
                "rating": 3,
                "amenities": ["WiFi", "Restaurant", "Room Service"]
            }
        ],
        "user_preferences": {
            "budget": "medium",
            "interests": ["cultural", "food", "shopping"],
            "travel_style": "leisure",
            "duration": "3-5 days",
            "group_size": 2,
            "preferred_airlines": ["IndiGo", "Vistara"],
            "preferred_hotel_chains": ["Taj", "Oberoi"],
            "must_have_amenities": ["WiFi", "Restaurant"],
            "optional_amenities": ["Pool", "Spa"]
        }
    }
    
    print("🚀 Package Creation API Test - GenAI Integration")
    print("=" * 60)
    print(f"📅 Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 API Endpoint: {url}")
    print()
    
    try:
        # Make the API call
        print("📤 Sending request to create packages...")
        response = requests.post(url, json=test_data, headers={'Content-Type': 'application/json'})
        
        print(f"📥 Response Status: {response.status_code}")
        print()
        
        if response.status_code == 200:
            result = response.json()
            
            print("✅ SUCCESS! Package Creation Response:")
            print("-" * 40)
            
            # Display status and timestamp
            print(f"Status: {result.get('status')}")
            print(f"Timestamp: {result.get('timestamp')}")
            print(f"Package Count: {result.get('package_count')}")
            print()
            
            # Display packages
            packages = result.get('packages', [])
            print(f"📦 Created {len(packages)} Packages:")
            print()
            
            for i, package in enumerate(packages, 1):
                print(f"🎯 Package {i}: {package.get('package_name')}")
                print(f"   Type: {package.get('package_type')}")
                print(f"   Target Audience: {package.get('target_audience')}")
                print(f"   Duration: {package.get('duration')}")
                print(f"   Total Price: ₹{package.get('total_package_price')}")
                
                # Flight details
                flight = package.get('flight', {})
                print(f"   ✈️  Flight: {flight.get('airline')} {flight.get('flight_number')} - {flight.get('departure')} → {flight.get('arrival')}")
                
                # Hotel details
                hotel = package.get('hotel', {})
                print(f"   🏨 Hotel: {hotel.get('name')} - {hotel.get('rating')}★ - ₹{hotel.get('price_per_night')}/night")
                
                # Highlights
                highlights = package.get('package_highlights', [])
                print(f"   ✨ Highlights: {', '.join(highlights[:3])}")
                
                print()
            
            # Save response to file
            with open('package_creation_response.json', 'w') as f:
                json.dump(result, f, indent=2)
            print("💾 Full response saved to 'package_creation_response.json'")
            
        else:
            print("❌ ERROR! API call failed")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ ERROR! Could not connect to the API")
        print("Make sure the Flask app is running on http://localhost:5000")
    except Exception as e:
        print(f"❌ ERROR! {str(e)}")

def test_package_from_search():
    """Test the package creation from search API"""
    
    # API endpoint
    url = "http://localhost:5000/api/package/create-from-search"
    
    # Test data with search parameters and user preferences
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
        },
        "user_preferences": {
            "budget": "luxury",
            "interests": ["adventure", "wellness", "fine_dining"],
            "travel_style": "leisure",
            "duration": "5-7 days",
            "group_size": 2,
            "preferred_airlines": ["Vistara", "Air India"],
            "preferred_hotel_chains": ["Taj", "Oberoi", "ITC"],
            "must_have_amenities": ["WiFi", "Pool", "Spa"],
            "optional_amenities": ["Concierge", "Fine Dining", "Helicopter Transfer"]
        }
    }
    
    print("🚀 Package Creation from Search API Test")
    print("=" * 60)
    print(f"📅 Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 API Endpoint: {url}")
    print()
    
    try:
        # Make the API call
        print("📤 Sending request to create packages from search...")
        response = requests.post(url, json=test_data, headers={'Content-Type': 'application/json'})
        
        print(f"📥 Response Status: {response.status_code}")
        print()
        
        if response.status_code == 200:
            result = response.json()
            
            print("✅ SUCCESS! Package Creation from Search Response:")
            print("-" * 40)
            
            # Display status and timestamp
            print(f"Status: {result.get('status')}")
            print(f"Timestamp: {result.get('timestamp')}")
            print(f"Package Count: {result.get('package_count')}")
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
            
            # Display packages
            packages = result.get('packages', [])
            print(f"📦 Created {len(packages)} Packages:")
            print()
            
            for i, package in enumerate(packages, 1):
                print(f"🎯 Package {i}: {package.get('package_name')}")
                print(f"   Type: {package.get('package_type')}")
                print(f"   Total Price: ₹{package.get('total_package_price')}")
                print()
            
            # Save response to file
            with open('package_from_search_response.json', 'w') as f:
                json.dump(result, f, indent=2)
            print("💾 Full response saved to 'package_from_search_response.json'")
            
        else:
            print("❌ ERROR! API call failed")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ ERROR! Could not connect to the API")
        print("Make sure the Flask app is running on http://localhost:5000")
    except Exception as e:
        print(f"❌ ERROR! {str(e)}")

def show_curl_commands():
    """Show curl commands for manual testing"""
    
    print("\n" + "=" * 60)
    print("🔧 CURL Commands for Manual Testing:")
    print("=" * 60)
    
    print("\n1️⃣ Package Creation API:")
    curl_command_1 = '''curl -X POST "http://localhost:5000/api/package/create" \\
  -H "Content-Type: application/json" \\
  -d '{
    "flights": [
      {
        "id": "flight_001",
        "airline": "IndiGo",
        "flightNumber": "6E-129",
        "departureAirport": "DEL",
        "arrivalAirport": "BOM",
        "departureTime": "2025-08-22T13:25:00.000+05:30",
        "arrivalTime": "2025-08-22T15:05:00.000+05:30",
        "totalDuration": "1h 40m",
        "stops": 0
      }
    ],
    "hotels": [
      {
        "id": "hotel_001",
        "name": "Taj Palace Hotel",
        "location": {"city": "Mumbai"},
        "price": {"amount": 15000},
        "rating": 5,
        "amenities": ["WiFi", "Pool", "Spa"]
      }
    ],
    "user_preferences": {
      "budget": "medium",
      "interests": ["cultural", "food"],
      "travel_style": "leisure",
      "duration": "3-5 days"
    }
  }' | jq '.' '''
    
    print(curl_command_1)
    
    print("\n2️⃣ Package Creation from Search API:")
    curl_command_2 = '''curl -X POST "http://localhost:5000/api/package/create-from-search" \\
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
    },
    "user_preferences": {
      "budget": "luxury",
      "interests": ["adventure", "wellness"],
      "travel_style": "leisure",
      "duration": "5-7 days"
    }
  }' | jq '.' '''
    
    print(curl_command_2)

if __name__ == "__main__":
    print("🧪 Testing Package Creation APIs with GenAI Integration")
    print("=" * 80)
    
    # Test package creation with provided data
    test_package_creation()
    
    print("\n" + "=" * 80)
    
    # Test package creation from search
    test_package_from_search()
    
    # Show curl commands
    show_curl_commands()

