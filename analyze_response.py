#!/usr/bin/env python3
"""
Script to analyze the search response structure
"""

import json

def analyze_response():
    """Analyze the search response structure"""
    
    try:
        with open('controllers/search_response.txt', 'r') as f:
            data = json.load(f)
        
        print("🔍 Analyzing Search Response Structure")
        print("=" * 50)
        
        # Check if it's a combined response or separate responses
        if 'flight_response' in data and 'hotel_response' in data:
            print("📋 Found combined response structure")
            
            # Analyze flight response
            flight_response = data.get('flight_response', {})
            print(f"\n✈️ Flight Response Status: {flight_response.get('status_code')}")
            
            flight_data = flight_response.get('data', {})
            if flight_data:
                print("📊 Flight Data Keys:", list(flight_data.keys()))
                
                # Look for travel options
                search_response = flight_data.get('SEARCH_RESPONSE', {})
                print("🔍 SEARCH_RESPONSE Keys:", list(search_response.keys()))
                
                travel_options = search_response.get('TRAVEL_OPTIONS', [])
                print(f"✈️ Found {len(travel_options)} travel options")
                
                if travel_options:
                    print("\n📋 First Travel Option Structure:")
                    first_option = travel_options[0]
                    print("Keys:", list(first_option.keys()))
                    
                    summary = first_option.get('summary', {})
                    print("Summary Keys:", list(summary.keys()))
                    
                    flights = summary.get('flights', [])
                    print(f"Flights in summary: {len(flights)}")
                    
                    if flights:
                        print("First flight structure:", list(flights[0].keys()))
            
            # Analyze hotel response
            hotel_response = data.get('hotel_response', {})
            print(f"\n🏨 Hotel Response Status: {hotel_response.get('status_code')}")
            
            hotel_data = hotel_response.get('data', {})
            if hotel_data:
                print("📊 Hotel Data Keys:", list(hotel_data.keys()))
                
                # Look for hotels
                hotels = hotel_data.get('hotels', [])
                print(f"🏨 Found {len(hotels)} hotels")
                
                if hotels:
                    print("\n📋 First Hotel Structure:")
                    first_hotel = hotels[0]
                    print("Keys:", list(first_hotel.keys()))
        
        else:
            print("📋 Direct response structure")
            print("Top level keys:", list(data.keys()))
            
            # Check for flight data
            if 'SEARCH_RESPONSE' in data:
                search_response = data.get('SEARCH_RESPONSE', {})
                travel_options = search_response.get('TRAVEL_OPTIONS', [])
                print(f"✈️ Found {len(travel_options)} travel options")
            
            # Check for hotel data
            if 'hotels' in data:
                hotels = data.get('hotels', [])
                print(f"🏨 Found {len(hotels)} hotels")
        
        # Save a sample for easier analysis
        with open('sample_response.json', 'w') as f:
            json.dump(data, f, indent=2)
        print("\n💾 Sample response saved to 'sample_response.json'")
        
    except Exception as e:
        print(f"❌ Error analyzing response: {e}")

if __name__ == "__main__":
    analyze_response()

