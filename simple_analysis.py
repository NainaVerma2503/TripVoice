#!/usr/bin/env python3
"""
Simple analysis of the search response structure
"""

import json

def simple_analysis():
    """Simple analysis of the response structure"""
    
    try:
        with open('controllers/search_response.txt', 'r') as f:
            data = json.load(f)
        
        print("🔍 Simple Analysis of Search Response")
        print("=" * 50)
        
        # Flight data
        flight_response = data.get('flight_response', {})
        flight_data = flight_response.get('data', {})
        
        print("\n✈️ FLIGHT DATA:")
        print(f"Status: {flight_response.get('status_code')}")
        
        if 'flights' in flight_data:
            flights = flight_data['flights']
            print(f"Found {len(flights)} flights")
            
            if flights:
                first_flight = flights[0]
                print(f"First flight keys: {list(first_flight.keys())}")
        
        # Hotel data
        hotel_response = data.get('hotel_response', {})
        hotel_data = hotel_response.get('data', {})
        
        print("\n🏨 HOTEL DATA:")
        print(f"Status: {hotel_response.get('status_code')}")
        
        if 'response' in hotel_data:
            response = hotel_data['response']
            if 'hotels' in response:
                hotels = response['hotels']
                print(f"Found {len(hotels)} hotels")
                
                if hotels:
                    first_hotel = hotels[0]
                    print(f"First hotel keys: {list(first_hotel.keys())}")
        
        # Save a small sample
        sample = {
            'flight_keys': list(flight_data.keys()) if flight_data else [],
            'hotel_keys': list(hotel_data.keys()) if hotel_data else []
        }
        
        if 'flights' in flight_data and flight_data['flights']:
            sample['first_flight_keys'] = list(flight_data['flights'][0].keys())
        
        if 'response' in hotel_data and 'hotels' in hotel_data['response'] and hotel_data['response']['hotels']:
            sample['first_hotel_keys'] = list(hotel_data['response']['hotels'][0].keys())
        
        with open('simple_sample.json', 'w') as f:
            json.dump(sample, f, indent=2)
        print("\n💾 Simple sample saved to 'simple_sample.json'")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    simple_analysis()

