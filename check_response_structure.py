#!/usr/bin/env python3
"""
Script to check the structure of the search response file
"""

import json
import sys

def check_structure():
    """Check the structure of the search response file"""
    
    try:
        print("🔍 Reading search response file...")
        
        with open('controllers/search_response.txt', 'r') as f:
            # Read the first 1000 characters to see the structure
            content = f.read(1000)
            print("📋 First 1000 characters:")
            print(content)
            print("\n" + "="*50)
            
            # Reset file pointer and try to parse as JSON
            f.seek(0)
            data = json.load(f)
            
            print("✅ Successfully parsed JSON")
            print(f"📊 Top level keys: {list(data.keys())}")
            
            # Check if it's a combined response
            if 'flight_response' in data and 'hotel_response' in data:
                print("\n📋 Found combined response structure")
                
                # Check flight response
                flight_response = data.get('flight_response', {})
                print(f"✈️ Flight status: {flight_response.get('status_code')}")
                
                flight_data = flight_response.get('data', {})
                if flight_data:
                    print(f"📊 Flight data keys: {list(flight_data.keys())}")
                    
                    # Check for SEARCH_RESPONSE
                    if 'SEARCH_RESPONSE' in flight_data:
                        search_response = flight_data['SEARCH_RESPONSE']
                        print(f"🔍 SEARCH_RESPONSE keys: {list(search_response.keys())}")
                        
                        if 'TRAVEL_OPTIONS' in search_response:
                            travel_options = search_response['TRAVEL_OPTIONS']
                            print(f"✈️ Found {len(travel_options)} travel options")
                            
                            if travel_options:
                                first_option = travel_options[0]
                                print(f"📋 First travel option keys: {list(first_option.keys())}")
                                
                                if 'summary' in first_option:
                                    summary = first_option['summary']
                                    print(f"📊 Summary keys: {list(summary.keys())}")
                
                # Check hotel response
                hotel_response = data.get('hotel_response', {})
                print(f"\n🏨 Hotel status: {hotel_response.get('status_code')}")
                
                hotel_data = hotel_response.get('data', {})
                if hotel_data:
                    print(f"📊 Hotel data keys: {list(hotel_data.keys())}")
                    
                    # Check for hotels
                    if 'hotels' in hotel_data:
                        hotels = hotel_data['hotels']
                        print(f"🏨 Found {len(hotels)} hotels")
                        
                        if hotels:
                            first_hotel = hotels[0]
                            print(f"📋 First hotel keys: {list(first_hotel.keys())}")
            
            else:
                print("\n📋 Direct response structure")
                print(f"📊 All keys: {list(data.keys())}")
                
                # Check for flight data
                if 'SEARCH_RESPONSE' in data:
                    search_response = data['SEARCH_RESPONSE']
                    if 'TRAVEL_OPTIONS' in search_response:
                        travel_options = search_response['TRAVEL_OPTIONS']
                        print(f"✈️ Found {len(travel_options)} travel options")
                
                # Check for hotel data
                if 'hotels' in data:
                    hotels = data['hotels']
                    print(f"🏨 Found {len(hotels)} hotels")
            
            # Save a small sample for analysis
            sample_data = {}
            if 'flight_response' in data:
                sample_data['flight_response'] = {
                    'status_code': data['flight_response'].get('status_code'),
                    'data_keys': list(data['flight_response'].get('data', {}).keys()) if data['flight_response'].get('data') else []
                }
            if 'hotel_response' in data:
                sample_data['hotel_response'] = {
                    'status_code': data['hotel_response'].get('status_code'),
                    'data_keys': list(data['hotel_response'].get('data', {}).keys()) if data['hotel_response'].get('data') else []
                }
            
            with open('response_structure_sample.json', 'w') as f:
                json.dump(sample_data, f, indent=2)
            print("\n💾 Structure sample saved to 'response_structure_sample.json'")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"Error type: {type(e)}")

if __name__ == "__main__":
    check_structure()

