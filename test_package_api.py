import requests
import json

def test_package_creation():
    """
    Test the package creation API with sample search response data and user interests
    """
    
    # Sample search response data (similar to what you provided)
    search_response = {
        "packageName": "One-Way Luxury Arrival: The St. Regis Goa",
        "packageType": "ONE_WAY_LUXURY",
        "totalPrice": 62800,
        "currency": "INR",
        "duration": "4 Nights / 5 Days Hotel Stay",
        "description": "This package arranges your luxury one-way arrival to Goa and a magnificent 4-night stay at the St. Regis Resort. Perfect for travelers with flexible return plans, it combines a seamless arrival with an extended, opulent beachfront experience.",
        "flightDetails": {
            "airline": "Air India",
            "flightNumber": "AI 2803 / AI 2657",
            "price": {
                "value": 15000,
                "currency": "INR"
            },
            "departureAirportCode": "DEL",
            "departureCity": "New Delhi",
            "departureDateTime": "2025-08-22T10:00:00",
            "arrivalAirportCode": "GOI",
            "arrivalCity": "Goa",
            "arrivalDateTime": "2025-08-22T12:30:00",
            "stops": "1 stop",
            "duration": "2h 30m"
        },
        "hotelDetails": {
            "name": "The St. Regis Goa Resort",
            "starRating": 5,
            "price": "13000",
            "address": "Mobor, Cavelossim, Goa, 403731, India",
            "city": "Mobor Beach, Goa",
            "amenities": [
                "Private Beach Access",
                "24-hour St. Regis Butler Service",
                "Spa and Wellness Center",
                "Championship Golf Course"
            ],
            "images": [
                "https://example-cdn.com/cms/6554/6554918/images/xr-goixr-goixr-aerial-resort-hero-26597_Classic-Hor_T.jpg",
                "https://example-cdn.com/cms/6554/6554918/images/xr-goixr-lagoon-34791_Classic-Hor_T.jpg"
            ]
        },
        "suggestedItinerary": [
            {
                "day": 1,
                "title": "Arrival in Paradise",
                "activities": [
                    "Arrive in Goa and take a private transfer to The St. Regis.",
                    "Check-in and relax by the resort's private beach or pool.",
                    "Enjoy dinner at Susegado, the seaside restaurant."
                ]
            },
            {
                "day": 2,
                "title": "Serene Beaches of the South",
                "activities": [
                    "Day trip to the tranquil Palolem and Agonda beaches.",
                    "Lunch at a highly-rated restaurant in Palolem."
                ]
            },
            {
                "day": 3,
                "title": "A Day of Indulgence",
                "activities": [
                    "Morning: Tee off at the resort's 12-hole golf course.",
                    "Afternoon: Indulge in a signature therapy session at the St. Regis Spa."
                ]
            },
            {
                "day": 4,
                "title": "Cultural & Historical Goa",
                "activities": [
                    "Guided tour of the magnificent ancestral home, the Figueiredo Mansion in Loutolim.",
                    "Explore the vibrant Latin Quarter (Fontainhas) in Panjim."
                ]
            },
            {
                "day": 5,
                "title": "Check-out & Onward Journey",
                "activities": [
                    "Enjoy a final Goan breakfast at the resort.",
                    "Check-out from the hotel.",
                    "Proceed with your own arrangements for your onward journey."
                ]
            }
        ],
        "popularAttractions": [
            "Mobor Beach",
            "Cavelossim Beach",
            "Palolem Beach",
            "Sal River Boating"
        ]
    }
    
    # Test different user interests
    test_cases = [
        {
            "user_interests": "beach, water sports, relaxation",
            "budget_constraint": 80000,
            "num_packages": 3
        },
        {
            "user_interests": "culture, heritage, traditional food",
            "budget_constraint": 60000,
            "num_packages": 2
        },
        {
            "user_interests": "adventure, trekking, wildlife",
            "budget_constraint": 100000,
            "num_packages": 3
        }
    ]
    
    base_url = "http://localhost:6000"
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"TEST CASE {i}: {test_case['user_interests']}")
        print(f"{'='*60}")
        
        # Prepare request data
        request_data = {
            "search_response": search_response,
            "user_interests": test_case["user_interests"],
            "budget_constraint": test_case["budget_constraint"],
            "num_packages": test_case["num_packages"]
        }
        
        try:
            # Make API call
            response = requests.post(
                f"{base_url}/api/package/create-from-search",
                headers={"Content-Type": "application/json"},
                json=request_data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ SUCCESS: Created {result['package_count']} packages")
                print(f"📊 Budget: {result['budget_constraint']} INR")
                print(f"🎯 Interests: {result['user_interests']}")
                
                # Display package summaries
                for j, package in enumerate(result['packages'], 1):
                    print(f"\n📦 Package {j}: {package['packageName']}")
                    print(f"   Type: {package['packageType']}")
                    print(f"   Price: {package['totalPrice']} INR")
                    print(f"   Duration: {package['duration']}")
                    print(f"   Flight: {package['flightDetails']['airline']} {package['flightDetails']['flightNumber']}")
                    print(f"   Hotel: {package['hotelDetails']['name']} ({package['hotelDetails']['starRating']}★)")
                    print(f"   Why: {package.get('whyThisPackage', 'N/A')}")
                    
            else:
                print(f"❌ ERROR: {response.status_code}")
                print(f"Response: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ REQUEST ERROR: {e}")
        except Exception as e:
            print(f"❌ UNEXPECTED ERROR: {e}")

def test_with_custom_data():
    """
    Test with custom search response data
    """
    print(f"\n{'='*60}")
    print("CUSTOM DATA TEST")
    print(f"{'='*60}")
    
    # Custom search response for Mumbai
    custom_search_response = {
        "packageName": "Mumbai City Explorer Package",
        "packageType": "CITY_EXPLORER",
        "totalPrice": 45000,
        "currency": "INR",
        "duration": "3 Nights / 4 Days",
        "description": "Explore the vibrant city of Mumbai with this comprehensive package.",
        "flightDetails": {
            "airline": "IndiGo",
            "flightNumber": "6E-129",
            "price": {
                "value": 8000,
                "currency": "INR"
            },
            "departureAirportCode": "DEL",
            "departureCity": "New Delhi",
            "departureDateTime": "2025-08-22T08:00:00",
            "arrivalAirportCode": "BOM",
            "arrivalCity": "Mumbai",
            "arrivalDateTime": "2025-08-22T10:15:00",
            "stops": "Direct",
            "duration": "2h 15m"
        },
        "hotelDetails": {
            "name": "Taj Mahal Palace",
            "starRating": 5,
            "price": "12000",
            "address": "Apollo Bunder, Mumbai, Maharashtra, India",
            "city": "Mumbai",
            "amenities": [
                "WiFi",
                "Pool",
                "Spa",
                "Restaurant",
                "Concierge"
            ],
            "images": [
                "https://example.com/taj-mumbai-1.jpg",
                "https://example.com/taj-mumbai-2.jpg"
            ]
        }
    }
    
    request_data = {
        "search_response": custom_search_response,
        "user_interests": "shopping, food, nightlife, bollywood",
        "budget_constraint": 60000,
        "num_packages": 2
    }
    
    try:
        response = requests.post(
            "http://localhost:6000/api/package/create-from-search",
            headers={"Content-Type": "application/json"},
            json=request_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ SUCCESS: Created {result['package_count']} Mumbai packages")
            
            for i, package in enumerate(result['packages'], 1):
                print(f"\n📦 Package {i}: {package['packageName']}")
                print(f"   Price: {package['totalPrice']} INR")
                print(f"   Attractions: {', '.join(package['popularAttractions'][:3])}")
                
        else:
            print(f"❌ ERROR: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    print("🚀 Testing Package Creation API")
    print("Make sure the Flask app is running on localhost:6000")
    
    # Test with sample data
    test_package_creation()
    
    # Test with custom data
    test_with_custom_data()
    
    print(f"\n{'='*60}")
    print("✅ Testing completed!")
    print(f"{'='*60}")
