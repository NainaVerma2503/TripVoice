from flask import Blueprint, request, jsonify
import requests
import json
from datetime import datetime
import random

package_bp = Blueprint('package', __name__)

@package_bp.route('/api/package/create-from-search', methods=['POST'])
def create_package_from_search():
    """
    Create personalized packages from search response data based on user interests
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Extract search response data and user interests
        search_response = data.get('search_response', {})
        user_interests = data.get('user_interests', '')
        budget_constraint = data.get('budget_constraint', 100000)  # Default 1L INR
        num_packages = data.get('num_packages', 3)  # Default 3 packages
        
        if not search_response:
            return jsonify({"error": "Search response data required"}), 400
        
        if not user_interests:
            return jsonify({"error": "User interests required"}), 400
        
        # Create personalized packages using OpenAI
        packages = create_personalized_packages(search_response, user_interests, budget_constraint, num_packages)
        
        return jsonify({
            "status": "success",
            "packages": packages,
            "package_count": len(packages),
            "user_interests": user_interests,
            "budget_constraint": budget_constraint,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def create_personalized_packages(search_response, user_interests, budget_constraint, num_packages):
    """
    Create personalized packages using OpenAI API based on search data and user interests
    """
    try:
        # Create prompt for OpenAI
        prompt = create_openai_prompt(search_response, user_interests, budget_constraint, num_packages)
        
        # Call OpenAI API
        response = call_openai_api(prompt)
        
        if response:
            packages = parse_openai_response(response)
            if packages:
                return packages
        
        # If OpenAI fails, create fallback packages
        print("OpenAI API failed, creating fallback packages")
        return create_fallback_packages(search_response, user_interests, budget_constraint, num_packages)
        
    except Exception as e:
        print(f"Error creating personalized packages: {e}")
        return create_fallback_packages(search_response, user_interests, budget_constraint, num_packages)

def create_openai_prompt(search_response, user_interests, budget_constraint, num_packages):
    """
    Create a detailed prompt for OpenAI package creation
    """
    # Get current dates for the prompt
    from datetime import datetime, timedelta
    tomorrow = datetime.now() + timedelta(days=1)
    departure_time = tomorrow.replace(hour=10, minute=0, second=0, microsecond=0)
    arrival_time = tomorrow.replace(hour=12, minute=30, second=0, microsecond=0)
    
    prompt = f"""
    Create {num_packages} personalized travel packages based on the following search response data and user interests:

    USER INTERESTS: {user_interests}
    BUDGET CONSTRAINT: {budget_constraint} INR
    NUMBER OF PACKAGES: {num_packages}
    CURRENT DATE: {tomorrow.strftime('%Y-%m-%d')}

    SEARCH RESPONSE DATA:
    {json.dumps(search_response, indent=2)}

    REQUIREMENTS:
    1. Create {num_packages} different packages that align with the user's interests
    2. Each package must be within the budget constraint of {budget_constraint} INR
    3. Use the flight and hotel data from the search response
    4. Create realistic and appealing package names and descriptions
    5. Include detailed itineraries that match the user's interests
    6. Suggest relevant attractions and activities
    7. Provide accurate price breakdowns
    8. IMPORTANT: Use current dates for all flight times - departure: {departure_time.strftime('%Y-%m-%dT%H:%M:%S')}, arrival: {arrival_time.strftime('%Y-%m-%dT%H:%M:%S')}

    PACKAGE STRUCTURE (return as JSON array):
    [
        {{
            "packageName": "Descriptive package name (e.g., 'One-Way Luxury Arrival: The St. Regis Goa')",
            "packageType": "BUDGET/MID_RANGE/LUXURY/PREMIUM/ONE_WAY_LUXURY",
            "totalPrice": total_price_in_inr,
            "currency": "INR",
            "duration": "X Nights / Y Days Hotel Stay",
            "description": "Detailed package description explaining the experience and what's included",
            "flightDetails": {{
                "airline": "Airline name",
                "flightNumber": "Flight number (can include multiple flights like 'AI 2803 / AI 2657')",
                "price": {{
                    "value": flight_price,
                    "currency": "INR"
                }},
                "departureAirportCode": "Airport code",
                "departureCity": "City name",
                "departureDateTime": "DateTime or 'N/A' if not applicable",
                "arrivalAirportCode": "Airport code",
                "arrivalCity": "City name",
                "arrivalDateTime": "DateTime or 'N/A' if not applicable",
                "stops": "Direct/1 stop/etc",
                "duration": "Xh Ym or '0h 0m' if not applicable"
            }},
            "hotelDetails": {{
                "name": "Hotel name (e.g., 'The St. Regis Goa Resort')",
                "starRating": rating_1_to_5,
                "price": "price_string (e.g., '1300')",
                "address": "Full address with postal code",
                "city": "City name with location (e.g., 'Mobor Beach, Goa')",
                "amenities": ["amenity1", "amenity2", "amenity3", "amenity4"],
                "images": ["image_url1", "image_url2"]
            }},
            "suggestedItinerary": [
                {{
                    "day": day_number,
                    "title": "Day title (e.g., 'Arrival in Paradise')",
                    "activities": ["activity1", "activity2", "activity3"]
                }}
            ],
            "popularAttractions": ["attraction1", "attraction2", "attraction3", "attraction4"]
        }}
    ]

    IMPORTANT: 
    - Ensure all packages are within the budget constraint
    - Make packages relevant to the user's interests
    - Use realistic pricing based on the search data
    - Create varied package types (budget, mid-range, luxury)
    - Include detailed day-wise itineraries
    - Suggest attractions that match user interests
    - Provide compelling reasons for each package recommendation

    Return only valid JSON array with {num_packages} packages.
    """

    return prompt

def call_openai_api(prompt):
    """
    Call the OpenAI API to generate personalized packages
    """
    try:
        # OpenAI API configuration
        api_url = "https://hackathon-openui-test.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2025-01-01-preview"
        api_key = "B4kxaCF6fe7KnBbRsDhk8EZZhvAz7MdVPXab3qJzZbahvpctLIT5JQQJ99BCAC77bzfXJ3w3AAABACOGTN88"
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }
        
        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 4096,
            "temperature": 0.7,
            "top_p": 1
        }
        
        response = requests.post(api_url, headers=headers, json=payload, timeout=300)
        
        if response.status_code == 200:
            result = response.json()
            return result.get('choices', [{}])[0].get('message', {}).get('content', '')
        else:
            print(f"OpenAI API error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return None

def update_package_dates(packages):
    """
    Update all dates in packages to use current dates
    """
    from datetime import datetime, timedelta
    
    tomorrow = datetime.now() + timedelta(days=1)
    departure_time = tomorrow.replace(hour=10, minute=0, second=0, microsecond=0)
    arrival_time = tomorrow.replace(hour=12, minute=30, second=0, microsecond=0)
    
    departure_str = departure_time.strftime('%Y-%m-%dT%H:%M:%S')
    arrival_str = arrival_time.strftime('%Y-%m-%dT%H:%M:%S')
    
    for package in packages:
        if 'flightDetails' in package:
            flight_details = package['flightDetails']
            # Update departure and arrival times to current dates
            if 'departureDateTime' in flight_details:
                flight_details['departureDateTime'] = departure_str
            if 'arrivalDateTime' in flight_details:
                flight_details['arrivalDateTime'] = arrival_str
    
    return packages

def parse_openai_response(response_text):
    """
    Parse the OpenAI response to extract packages
    """
    try:
        if not response_text:
            return []
        
        # Try to extract JSON from the response
        start_idx = response_text.find('[')
        end_idx = response_text.rfind(']')
        
        if start_idx != -1 and end_idx != -1:
            json_str = response_text[start_idx:end_idx + 1]
            packages = json.loads(json_str)
            
            # Update dates to current dates
            packages = update_package_dates(packages)
            
            return packages
        else:
            print("No valid JSON found in OpenAI response")
            return []
            
    except Exception as e:
        print(f"Error parsing OpenAI response: {e}")
        return []

def create_fallback_packages(search_response, user_interests, budget_constraint, num_packages):
    """
    Create fallback packages when OpenAI API fails
    """
    packages = []
    
    # Extract flight and hotel data from search response
    flight_data = search_response.get('flightDetails', {})
    hotel_data = search_response.get('hotelDetails', {})
    
    # Create different package types
    package_types = [
        {
            "type": "BUDGET",
            "name": "Budget Explorer Package",
            "description": "Perfect for budget-conscious travelers who want to explore without breaking the bank.",
            "multiplier": 0.8
        },
        {
            "type": "MID_RANGE", 
            "name": "Comfort Plus Package",
            "description": "Balanced comfort and value with premium amenities and convenient location.",
            "multiplier": 1.0
        },
        {
            "type": "LUXURY",
            "name": "Luxury Experience Package",
            "description": "Ultimate luxury experience with premium services and exclusive amenities.",
            "multiplier": 1.5
        }
    ]
    
    for i in range(min(num_packages, len(package_types))):
        config = package_types[i]
        
        # Calculate prices based on multiplier
        base_flight_price = flight_data.get('price', {}).get('value', 5000)
        base_hotel_price = int(hotel_data.get('price', '5000').replace(',', ''))
        
        flight_price = int(base_flight_price * config['multiplier'])
        hotel_price = int(base_hotel_price * config['multiplier'])
        activities_price = int((flight_price + hotel_price) * 0.2)
        taxes = int((flight_price + hotel_price + activities_price) * 0.1)
        total_price = flight_price + hotel_price + activities_price + taxes
        
        # Ensure package is within budget
        if total_price > budget_constraint:
            # Scale down to fit budget
            scale_factor = budget_constraint / total_price
            flight_price = int(flight_price * scale_factor)
            hotel_price = int(hotel_price * scale_factor)
            activities_price = int(activities_price * scale_factor)
            taxes = int(taxes * scale_factor)
            total_price = flight_price + hotel_price + activities_price + taxes
        
        # Create itinerary based on user interests
        itinerary = create_interest_based_itinerary(user_interests, i + 1)
        
        # Create attractions based on user interests
        attractions = create_interest_based_attractions(user_interests)
        
        package = {
            "packageName": config["name"],
            "packageType": config["type"],
            "totalPrice": total_price,
            "currency": "INR",
            "duration": "4 Nights / 5 Days Hotel Stay",
            "description": config["description"],
            "flightDetails": {
                "airline": flight_data.get('airline', 'Air India'),
                "flightNumber": flight_data.get('flightNumber', 'AI 1234'),
                "price": {
                    "value": flight_price,
                    "currency": "INR"
                },
                "departureAirportCode": flight_data.get('departureAirportCode', 'DEL'),
                "departureCity": flight_data.get('departureCity', 'New Delhi'),
                "departureDateTime": flight_data.get('departureDateTime', get_current_departure_time()),
                "arrivalAirportCode": flight_data.get('arrivalAirportCode', 'BOM'),
                "arrivalCity": flight_data.get('arrivalCity', 'Mumbai'),
                "arrivalDateTime": flight_data.get('arrivalDateTime', get_current_arrival_time()),
                "stops": flight_data.get('stops', 'Direct'),
                "duration": flight_data.get('duration', '2h 0m')
            },
            "hotelDetails": {
                "name": hotel_data.get('name', 'Comfort Hotel'),
                "starRating": hotel_data.get('starRating', 4),
                "price": str(hotel_price),
                "address": hotel_data.get('address', 'Mumbai, India'),
                "city": hotel_data.get('city', 'Mumbai'),
                "amenities": hotel_data.get('amenities', ['WiFi', 'Pool', 'Restaurant']),
                "images": hotel_data.get('images', ['/images/hotels/hotel_001.jpg'])
            },
            "suggestedItinerary": itinerary,
            "popularAttractions": attractions
        }
        
        packages.append(package)
    
    return packages

def create_interest_based_itinerary(user_interests, package_num):
    """
    Create itinerary based on user interests
    """
    interests_lower = user_interests.lower()
    
    if 'beach' in interests_lower or 'sea' in interests_lower:
        return [
            {
                "day": 1,
                "title": "Arrival and Beach Welcome",
                "activities": [
                    "Arrive at destination and check-in to hotel",
                    "Relax at the nearby beach",
                    "Enjoy sunset dinner at beachfront restaurant"
                ]
            },
            {
                "day": 2,
                "title": "Beach Adventure Day",
                "activities": [
                    "Morning beach yoga session",
                    "Water sports activities (jet skiing, parasailing)",
                    "Beachside lunch with fresh seafood"
                ]
            },
            {
                "day": 3,
                "title": "Island Exploration",
                "activities": [
                    "Boat trip to nearby islands",
                    "Snorkeling and diving experience",
                    "Beach bonfire dinner"
                ]
            },
            {
                "day": 4,
                "title": "Cultural Beach Experience",
                "activities": [
                    "Visit local fishing village",
                    "Learn traditional beach activities",
                    "Sunset cruise"
                ]
            },
            {
                "day": 5,
                "title": "Farewell Beach Day",
                "activities": [
                    "Final beach walk and photos",
                    "Spa treatment at beach resort",
                    "Check-out and departure"
                ]
            }
        ]
    elif 'culture' in interests_lower or 'heritage' in interests_lower:
        return [
            {
                "day": 1,
                "title": "Cultural Arrival",
                "activities": [
                    "Arrive and check-in to hotel",
                    "Visit local museum or cultural center",
                    "Traditional welcome dinner"
                ]
            },
            {
                "day": 2,
                "title": "Historical Exploration",
                "activities": [
                    "Guided tour of historical monuments",
                    "Visit ancient temples or churches",
                    "Local art and craft workshop"
                ]
            },
            {
                "day": 3,
                "title": "Traditional Experience",
                "activities": [
                    "Learn traditional cooking methods",
                    "Visit local markets and bazaars",
                    "Cultural dance performance"
                ]
            },
            {
                "day": 4,
                "title": "Heritage Walk",
                "activities": [
                    "Walking tour of old city quarters",
                    "Visit heritage buildings",
                    "Traditional music concert"
                ]
            },
            {
                "day": 5,
                "title": "Cultural Farewell",
                "activities": [
                    "Final cultural site visit",
                    "Traditional farewell ceremony",
                    "Check-out and departure"
                ]
            }
        ]
    elif 'adventure' in interests_lower or 'trek' in interests_lower:
        return [
            {
                "day": 1,
                "title": "Adventure Begins",
                "activities": [
                    "Arrive and check-in to adventure lodge",
                    "Safety briefing and equipment check",
                    "Light evening trek to acclimatize"
                ]
            },
            {
                "day": 2,
                "title": "Mountain Adventure",
                "activities": [
                    "Early morning trek to viewpoint",
                    "Rock climbing session",
                    "Campfire dinner under stars"
                ]
            },
            {
                "day": 3,
                "title": "Wilderness Exploration",
                "activities": [
                    "Full-day trek through wilderness",
                    "Wildlife spotting and photography",
                    "Adventure sports activities"
                ]
            },
            {
                "day": 4,
                "title": "River Adventure",
                "activities": [
                    "White water rafting experience",
                    "River crossing challenges",
                    "Adventure photography workshop"
                ]
            },
            {
                "day": 5,
                "title": "Adventure Farewell",
                "activities": [
                    "Final adventure activity",
                    "Adventure certificate ceremony",
                    "Check-out and departure"
                ]
            }
        ]
    else:
        # Default general itinerary
        return [
            {
                "day": 1,
                "title": "Arrival and Welcome",
                "activities": [
                    "Arrive at destination and check-in",
                    "Local area exploration",
                    "Welcome dinner at hotel"
                ]
            },
            {
                "day": 2,
                "title": "City Discovery",
                "activities": [
                    "Guided city tour",
                    "Visit popular landmarks",
                    "Local cuisine tasting"
                ]
            },
            {
                "day": 3,
                "title": "Local Experience",
                "activities": [
                    "Visit local markets",
                    "Cultural activities",
                    "Evening entertainment"
                ]
            },
            {
                "day": 4,
                "title": "Relaxation Day",
                "activities": [
                    "Spa and wellness activities",
                    "Leisure time at hotel",
                    "Optional excursions"
                ]
            },
            {
                "day": 5,
                "title": "Farewell",
                "activities": [
                    "Final shopping and sightseeing",
                    "Farewell lunch",
                    "Check-out and departure"
                ]
            }
        ]

def create_interest_based_attractions(user_interests):
    """
    Create attractions list based on user interests
    """
    interests_lower = user_interests.lower()
    
    if 'beach' in interests_lower or 'sea' in interests_lower:
        return [
            "Crystal Clear Beaches",
            "Marine Life Sanctuary",
            "Beach Water Sports Center",
            "Island Hopping Tours",
            "Sunset View Points"
        ]
    elif 'culture' in interests_lower or 'heritage' in interests_lower:
        return [
            "Ancient Temples and Churches",
            "Historical Museums",
            "Traditional Art Galleries",
            "Heritage Walking Tours",
            "Cultural Performance Centers"
        ]
    elif 'adventure' in interests_lower or 'trek' in interests_lower:
        return [
            "Mountain Trekking Trails",
            "Adventure Sports Center",
            "Wildlife Sanctuaries",
            "Rock Climbing Sites",
            "River Rafting Points"
        ]
    elif 'food' in interests_lower or 'cuisine' in interests_lower:
        return [
            "Local Food Markets",
            "Traditional Restaurants",
            "Cooking Classes",
            "Wine Tasting Tours",
            "Street Food Walks"
        ]
    elif 'shopping' in interests_lower or 'market' in interests_lower:
        return [
            "Traditional Bazaars",
            "Modern Shopping Malls",
            "Artisan Workshops",
            "Local Craft Centers",
            "Flea Markets"
        ]
    else:
        return [
            "Popular Tourist Attractions",
            "Local Markets",
            "Cultural Centers",
            "Scenic Viewpoints",
            "Entertainment Venues"
        ]

def get_current_departure_time():
    """Get current departure time (tomorrow at 10:00 AM)"""
    from datetime import datetime, timedelta
    tomorrow = datetime.now() + timedelta(days=1)
    departure_time = tomorrow.replace(hour=10, minute=0, second=0, microsecond=0)
    return departure_time.strftime('%Y-%m-%dT%H:%M:%S')

def get_current_arrival_time():
    """Get current arrival time (tomorrow at 12:00 PM)"""
    from datetime import datetime, timedelta
    tomorrow = datetime.now() + timedelta(days=1)
    arrival_time = tomorrow.replace(hour=12, minute=0, second=0, microsecond=0)
    return arrival_time.strftime('%Y-%m-%dT%H:%M:%S')
