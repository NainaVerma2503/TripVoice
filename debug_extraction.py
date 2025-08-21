#!/usr/bin/env python3
"""
Debug script to understand the exact ClearTrip API response structure
"""

import json
import requests

def debug_api_call():
    """Make a real API call and debug the response structure"""
    
    print("🔍 Debugging API Call and Response Structure")
    print("=" * 60)
    
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
    
    try:
        # Make the API call
        response = requests.post("http://localhost:5000/api/search", 
                               json=test_data, 
                               headers={'Content-Type': 'application/json'})
        
        print(f"📥 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            # Check if we have raw responses
            if 'flight_response' in result and 'hotel_response' in result:
                print("\n📋 Found raw responses in result")
                
                # Analyze flight response
                flight_response = result['flight_response']
                print(f"✈️ Flight Response Status: {flight_response.get('status_code')}")
                
                if flight_response.get('data'):
                    flight_data = flight_response['data']
                    print(f"📊 Flight Data Keys: {list(flight_data.keys())}")
                    
                    # Check for flights
                    if 'flights' in flight_data:
                        flights = flight_data['flights']
                        print(f"✈️ Found {len(flights)} flights")
                        
                        if flights:
                            print("📋 First Flight Structure:")
                            first_flight = flights[0]
                            print(f"Keys: {list(first_flight.keys())}")
                            
                            # Show some key fields
                            for key in ['airlineCode', 'flightNumber', 'departure', 'arrival']:
                                if key in first_flight:
                                    print(f"  {key}: {first_flight[key]}")
                
                # Analyze hotel response
                hotel_response = result['hotel_response']
                print(f"\n🏨 Hotel Response Status: {hotel_response.get('status_code')}")
                
                if hotel_response.get('data'):
                    hotel_data = hotel_response['data']
                    print(f"📊 Hotel Data Keys: {list(hotel_data.keys())}")
                    
                    # Check for response
                    if 'response' in hotel_data:
                        response = hotel_data['response']
                        print(f"📊 Response Keys: {list(response.keys())}")
                        
                        if 'hotels' in response:
                            hotels = response['hotels']
                            print(f"🏨 Found {len(hotels)} hotels")
                            
                            if hotels:
                                print("📋 First Hotel Structure:")
                                first_hotel = hotels[0]
                                print(f"Keys: {list(first_hotel.keys())}")
            
            else:
                print("\n📋 No raw responses found, checking extracted data")
                print(f"📊 Result Keys: {list(result.keys())}")
                
                flights = result.get('flights', [])
                hotels = result.get('hotels', [])
                
                print(f"✈️ Extracted Flights: {len(flights)}")
                print(f"🏨 Extracted Hotels: {len(hotels)}")
        
        # Save the full response for analysis
        with open('debug_response.json', 'w') as f:
            json.dump(result, f, indent=2)
        print("\n💾 Full response saved to 'debug_response.json'")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def test_extraction_functions():
    """Test the extraction functions with sample data"""
    
    print("\n🧪 Testing Extraction Functions")
    print("=" * 40)
    
    # Sample flight data structure based on what we know
    sample_flight_data = {
        "flights": [
            {
                "airlineCode": "6E",
                "flightNumber": "129",
                "departure": {
                    "airportCode": "DEL",
                    "time": "2025-08-22T13:25:00.000+05:30",
                    "terminal": "1D"
                },
                "arrival": {
                    "airportCode": "BOM",
                    "time": "2025-08-22T15:05:00.000+05:30",
                    "terminal": "1"
                },
                "stops": 0,
                "stopDetails": "Direct flight"
            }
        ]
    }
    
    # Sample hotel data structure
    sample_hotel_data = {
        "response": {
            "hotels": [
                {
                    "name": "Taj Palace Hotel",
                    "address": "Apollo Bunder, Mumbai",
                    "area": "Colaba",
                    "city": "Mumbai",
                    "price": {
                        "amount": 15000,
                        "currency": "INR"
                    },
                    "rating": 5,
                    "amenities": ["WiFi", "Pool", "Spa", "Restaurant"]
                }
            ]
        }
    }
    
    # Import and test the functions
    import sys
    sys.path.append('controllers')
    
    from search_controller import extract_flight_details, extract_hotel_details
    
    print("Testing flight extraction...")
    extracted_flights = extract_flight_details(sample_flight_data)
    print(f"Extracted {len(extracted_flights)} flights")
    
    print("Testing hotel extraction...")
    extracted_hotels = extract_hotel_details(sample_hotel_data)
    print(f"Extracted {len(extracted_hotels)} hotels")
    
    # Show results
    if extracted_flights:
        print("\n📋 Sample Extracted Flight:")
        print(json.dumps(extracted_flights[0], indent=2))
    
    if extracted_hotels:
        print("\n📋 Sample Extracted Hotel:")
        print(json.dumps(extracted_hotels[0], indent=2))

if __name__ == "__main__":
    debug_api_call()
    test_extraction_functions()
