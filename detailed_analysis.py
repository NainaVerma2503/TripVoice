#!/usr/bin/env python3
"""
Detailed analysis of the search response structure
"""

import json

def detailed_analysis():
    """Perform detailed analysis of the response structure"""
    
    try:
        with open('controllers/search_response.txt', 'r') as f:
            data = json.load(f)
        
        print("🔍 Detailed Analysis of Search Response")
        print("=" * 50)
        
        # Analyze flight data
        flight_response = data.get('flight_response', {})
        flight_data = flight_response.get('data', {})
        
        print("\n✈️ FLIGHT DATA ANALYSIS:")
        print("-" * 30)
        
        # Check flights key
        if 'flights' in flight_data:
            flights = flight_data['flights']
            print(f"📊 Found 'flights' key with {len(flights)} items")
            
            if flights:
                print("📋 First flight structure:")
                first_flight = flights[0]
                print(f"Keys: {list(first_flight.keys())}")
                
                # Show some sample data
                for key in list(first_flight.keys())[:5]:  # Show first 5 keys
                    value = first_flight[key]
                    if isinstance(value, (str, int, float)):
                        print(f"  {key}: {value}")
                    elif isinstance(value, list):
                        print(f"  {key}: List with {len(value)} items")
                    elif isinstance(value, dict):
                        print(f"  {key}: Dict with keys {list(value.keys())[:3]}...")
        
        # Check subTravelOptions
        if 'subTravelOptions' in flight_data:
            sub_travel_options = flight_data['subTravelOptions']
            print(f"\n📊 Found 'subTravelOptions' with {len(sub_travel_options)} items")
            
            if sub_travel_options:
                print("📋 First subTravelOption structure:")
                first_option = sub_travel_options[0]
                print(f"Keys: {list(first_option.keys())}")
        
        # Analyze hotel data
        hotel_response = data.get('hotel_response', {})
        hotel_data = hotel_response.get('data', {})
        
        print("\n🏨 HOTEL DATA ANALYSIS:")
        print("-" * 30)
        
        # Check response key
        if 'response' in hotel_data:
            response = hotel_data['response']
            print(f"📊 Found 'response' key")
            print(f"Response keys: {list(response.keys())}")
            
            # Check for hotels in response
            if 'hotels' in response:
                hotels = response['hotels']
                print(f"🏨 Found {len(hotels)} hotels in response")
                
                if hotels:
                    print("📋 First hotel structure:")
                    first_hotel = hotels[0]
                    print(f"Keys: {list(first_hotel.keys())}")
        
        # Check searchV3Bucket
        if 'searchV3Bucket' in hotel_data:
            search_bucket = hotel_data['searchV3Bucket']
            print(f"\n📊 Found 'searchV3Bucket'")
            print(f"SearchV3Bucket keys: {list(search_bucket.keys())}")
            
            if 'hotels' in search_bucket:
                hotels = search_bucket['hotels']
                print(f"🏨 Found {len(hotels)} hotels in searchV3Bucket")
                
                if hotels:
                    print("📋 First hotel structure:")
                    first_hotel = hotels[0]
                    print(f"Keys: {list(first_hotel.keys())}")
        
        # Save detailed sample
        sample = {
            'flight_sample': {},
            'hotel_sample': {}
        }
        
        if 'flights' in flight_data and flight_data['flights']:
            sample['flight_sample'] = flight_data['flights'][0]
        
        if 'response' in hotel_data and 'hotels' in hotel_data['response'] and hotel_data['response']['hotels']:
            sample['hotel_sample'] = hotel_data['response']['hotels'][0]
        
        with open('detailed_sample.json', 'w') as f:
            json.dump(sample, f, indent=2)
        print("\n💾 Detailed sample saved to 'detailed_sample.json'")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    detailed_analysis()
