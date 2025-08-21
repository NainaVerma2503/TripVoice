#!/usr/bin/env python3
"""
Test script to verify hotel images are included in search response
"""

import requests
import json
from datetime import datetime

def test_hotel_images():
    """Test that hotel images are included in the search response"""
    
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
    
    print("🏨 Testing Hotel Images in Search Response")
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
            
            print("✅ SUCCESS! Hotel Images Found:")
            print("-" * 40)
            
            # Display search summary
            search_summary = result.get('search_summary', {})
            print(f"Total Hotels Found: {search_summary.get('total_hotels_found')}")
            print()
            
            # Display hotels with images
            hotels = result.get('hotels', [])
            print(f"🏨 Hotels with Images ({len(hotels)} found):")
            print()
            
            for i, hotel in enumerate(hotels[:5], 1):  # Show first 5 hotels
                print(f"  {i}. {hotel.get('name')}")
                print(f"     Location: {hotel.get('location', {}).get('city')}")
                print(f"     Rating: {hotel.get('rating')}★")
                print(f"     Price: ₹{hotel.get('price', {}).get('amount')}")
                print(f"     Hotel Image: {hotel.get('hotel_image')}")
                print(f"     Room Image: {hotel.get('room_image')}")
                
                # Show amenity images
                amenity_images = hotel.get('amenity_images', {})
                if amenity_images:
                    print(f"     Amenity Images: {len(amenity_images)} available")
                    for amenity, image_url in list(amenity_images.items())[:3]:  # Show first 3
                        print(f"       - {amenity}: {image_url}")
                
                print()
            
            # Save response to file
            with open('hotel_images_response.json', 'w') as f:
                json.dump(result, f, indent=2)
            print("💾 Full response saved to 'hotel_images_response.json'")
            
            # Test image URLs
            print("🔗 Testing Image URLs:")
            print("-" * 20)
            
            if hotels:
                first_hotel = hotels[0]
                hotel_image_url = first_hotel.get('hotel_image')
                room_image_url = first_hotel.get('room_image')
                
                print(f"Hotel Image URL: {hotel_image_url}")
                print(f"Room Image URL: {room_image_url}")
                
                # Test if images are accessible
                base_url = "http://localhost:5000"
                try:
                    hotel_img_response = requests.get(f"{base_url}{hotel_image_url}")
                    room_img_response = requests.get(f"{base_url}{room_image_url}")
                    
                    print(f"Hotel Image Status: {hotel_img_response.status_code}")
                    print(f"Room Image Status: {room_img_response.status_code}")
                    
                    if hotel_img_response.status_code == 200 and room_img_response.status_code == 200:
                        print("✅ All images are accessible!")
                    else:
                        print("⚠️ Some images may not be accessible")
                        
                except Exception as e:
                    print(f"❌ Error testing image URLs: {e}")
            
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
  }' | jq '.hotels[0]' '''
    
    print(curl_command)

if __name__ == "__main__":
    test_hotel_images()
    show_curl_command()
