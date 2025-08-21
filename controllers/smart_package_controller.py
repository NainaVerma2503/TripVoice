from flask import Blueprint, jsonify, request
from datetime import datetime
import requests
import json
import os

smart_package_bp = Blueprint('smart_package', __name__)

@smart_package_bp.route('/api/smart-package/create', methods=['POST'])
def create_smart_package():
    """
    Create smart travel packages by analyzing search criteria and using GenAI
    """
    try:
        # Get the request data
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'No data provided',
                'status': 'error'
            }), 400
        
        # Extract search criteria and preferences
        search_criteria = extract_search_criteria(data)
        
        # Get filtered flights and hotels based on criteria
        filtered_flights, filtered_hotels = filter_data_by_criteria(search_criteria)
        
        # Create packages using GenAI
        packages = create_smart_packages_with_genai(search_criteria, filtered_flights, filtered_hotels)
        
        return jsonify({
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'search_criteria': search_criteria,
            'packages': packages,
            'package_count': len(packages),
            'data_summary': {
                'flights_analyzed': len(filtered_flights),
                'hotels_analyzed': len(filtered_hotels),
                'criteria_matched': search_criteria
            }
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error',
            'timestamp': datetime.now().isoformat()
        }), 500

def extract_search_criteria(data):
    """
    Extract and analyze search criteria from the request
    """
    criteria = {
        'budget_level': 'medium',  # budget, medium, luxury
        'travel_style': 'leisure',  # leisure, business, adventure, romantic
        'group_type': 'couple',  # solo, couple, family, group
        'duration_preference': '3-5 days',
        'interests': [],
        'preferred_airlines': [],
        'preferred_hotel_chains': [],
        'must_have_amenities': [],
        'optional_amenities': [],
        'route': {},
        'dates': {}
    }
    
    # Extract flight search criteria
    flight_data = data.get('flight', {})
    if flight_data:
        criteria['route'] = {
            'from': flight_data.get('from'),
            'to': flight_data.get('to'),
            'departure_date': flight_data.get('depart_date'),
            'adults': flight_data.get('adults', 1)
        }
    
    # Extract hotel search criteria
    hotel_data = data.get('hotel', {})
    if hotel_data:
        criteria['dates'] = {
            'check_in': hotel_data.get('checkInDate'),
            'check_out': hotel_data.get('checkOutDate'),
            'city': hotel_data.get('city'),
            'state': hotel_data.get('state')
        }
    
    # Extract user preferences
    user_prefs = data.get('user_preferences', {})
    if user_prefs:
        criteria['budget_level'] = user_prefs.get('budget', 'medium')
        criteria['travel_style'] = user_prefs.get('travel_style', 'leisure')
        criteria['interests'] = user_prefs.get('interests', [])
        criteria['preferred_airlines'] = user_prefs.get('preferred_airlines', [])
        criteria['preferred_hotel_chains'] = user_prefs.get('preferred_hotel_chains', [])
        criteria['must_have_amenities'] = user_prefs.get('must_have_amenities', [])
        criteria['optional_amenities'] = user_prefs.get('optional_amenities', [])
        criteria['duration_preference'] = user_prefs.get('duration', '3-5 days')
        
        # Determine group type based on adults
        adults = criteria['route'].get('adults', 1)
        if adults == 1:
            criteria['group_type'] = 'solo'
        elif adults == 2:
            criteria['group_type'] = 'couple'
        elif adults <= 4:
            criteria['group_type'] = 'family'
        else:
            criteria['group_type'] = 'group'
    
    # Analyze and enhance criteria
    criteria = analyze_and_enhance_criteria(criteria)
    
    return criteria

def analyze_and_enhance_criteria(criteria):
    """
    Analyze and enhance search criteria with intelligent defaults
    """
    # Set default interests based on travel style
    if not criteria['interests']:
        if criteria['travel_style'] == 'leisure':
            criteria['interests'] = ['relaxation', 'sightseeing', 'food']
        elif criteria['travel_style'] == 'business':
            criteria['interests'] = ['business', 'convenience', 'networking']
        elif criteria['travel_style'] == 'adventure':
            criteria['interests'] = ['adventure', 'outdoor', 'exploration']
        elif criteria['travel_style'] == 'romantic':
            criteria['interests'] = ['romance', 'privacy', 'luxury']
    
    # Set default amenities based on interests
    if not criteria['must_have_amenities']:
        if 'business' in criteria['interests']:
            criteria['must_have_amenities'] = ['WiFi', 'Business Center']
        elif 'relaxation' in criteria['interests']:
            criteria['must_have_amenities'] = ['WiFi', 'Spa']
        elif 'adventure' in criteria['interests']:
            criteria['must_have_amenities'] = ['WiFi', 'Gym']
        else:
            criteria['must_have_amenities'] = ['WiFi']
    
    # Set default optional amenities
    if not criteria['optional_amenities']:
        criteria['optional_amenities'] = ['Pool', 'Restaurant', 'Concierge']
    
    return criteria

def filter_data_by_criteria(criteria):
    """
    Filter flights and hotels based on search criteria
    """
    # Get comprehensive mock data
    all_flights = get_comprehensive_flight_data()
    all_hotels = get_comprehensive_hotel_data()
    
    filtered_flights = []
    filtered_hotels = []
    
    # Filter flights based on route
    route = criteria.get('route', {})
    from_airport = route.get('from')
    to_airport = route.get('to')
    
    for flight in all_flights:
        if (flight.get('departureAirport') == from_airport and 
            flight.get('arrivalAirport') == to_airport):
            filtered_flights.append(flight)
    
    # Filter hotels based on criteria
    for hotel in all_hotels:
        if matches_hotel_criteria(hotel, criteria):
            filtered_hotels.append(hotel)
    
    # Limit results for better performance
    filtered_flights = filtered_flights[:20]  # Top 20 flights
    filtered_hotels = filtered_hotels[:20]    # Top 20 hotels
    
    return filtered_flights, filtered_hotels

def matches_hotel_criteria(hotel, criteria):
    """
    Check if hotel matches the search criteria
    """
    # Check budget level
    price = hotel.get('price', {}).get('amount', 0)
    budget_level = criteria.get('budget_level', 'medium')
    
    if budget_level == 'budget' and price > 8000:
        return False
    elif budget_level == 'medium' and (price < 3000 or price > 15000):
        return False
    elif budget_level == 'luxury' and price < 10000:
        return False
    
    # Check amenities
    hotel_amenities = hotel.get('amenities', [])
    must_have = criteria.get('must_have_amenities', [])
    
    for amenity in must_have:
        if amenity not in hotel_amenities:
            return False
    
    # Check hotel chain preference
    preferred_chains = criteria.get('preferred_hotel_chains', [])
    if preferred_chains:
        hotel_name = hotel.get('name', '').lower()
        matches_chain = any(chain.lower() in hotel_name for chain in preferred_chains)
        if not matches_chain:
            return False
    
    return True

def get_comprehensive_flight_data():
    """
    Get comprehensive flight data (same as in search_controller.py)
    """
    # This would be the same logic as in search_controller.py
    # For brevity, returning sample data
    return [
        {
            "id": "flight_001",
            "airline": "IndiGo",
            "flightNumber": "6E-129",
            "departureAirport": "DEL",
            "arrivalAirport": "BOM",
            "departureTime": "2025-08-22T13:25:00.000+05:30",
            "arrivalTime": "2025-08-22T15:05:00.000+05:30",
            "totalDuration": "1h 40m",
            "stops": 0,
            "price": 3500
        },
        {
            "id": "flight_002",
            "airline": "Vistara",
            "flightNumber": "UK-825",
            "departureAirport": "DEL",
            "arrivalAirport": "BOM",
            "departureTime": "2025-08-22T16:00:00.000+05:30",
            "arrivalTime": "2025-08-22T18:20:00.000+05:30",
            "totalDuration": "2h 20m",
            "stops": 0,
            "price": 8500
        }
    ]

def get_comprehensive_hotel_data():
    """
    Get comprehensive hotel data (same as in search_controller.py)
    """
    # This would be the same logic as in search_controller.py
    # For brevity, returning sample data
    return [
        {
            "id": "hotel_001",
            "name": "Taj Palace Hotel",
            "location": {"city": "Mumbai"},
            "price": {"amount": 15000},
            "rating": 5,
            "amenities": ["WiFi", "Pool", "Spa", "Restaurant"],
            "hotel_image": "/images/hotels/hotel_exterior.jpg",
            "room_image": "/images/hotels/hotel_room.jpg"
        },
        {
            "id": "hotel_002",
            "name": "Budget Inn",
            "location": {"city": "Mumbai"},
            "price": {"amount": 4000},
            "rating": 3,
            "amenities": ["WiFi", "Restaurant"],
            "hotel_image": "/images/hotels/hotel_exterior.jpg",
            "room_image": "/images/hotels/hotel_room.jpg"
        }
    ]

def create_smart_packages_with_genai(criteria, flights, hotels):
    """
    Create smart packages using GenAI based on analyzed criteria
    """
    try:
        # Prepare the prompt for GenAI
        prompt = create_smart_genai_prompt(criteria, flights, hotels)
        
        # Call GenAI API
        genai_response = call_genai_api(prompt)
        
        # Parse the response
        packages = parse_genai_response(genai_response)
        
        # If GenAI fails, create smart mock packages
        if not packages:
            packages = create_smart_mock_packages(criteria, flights, hotels)
        
        return packages
        
    except Exception as e:
        print(f"Error creating smart packages with GenAI: {e}")
        return create_smart_mock_packages(criteria, flights, hotels)

def create_smart_genai_prompt(criteria, flights, hotels):
    """
    Create a comprehensive prompt for GenAI to generate smart packages
    """
    
    prompt = f"""
You are an intelligent travel package creator. Create 3-5 personalized travel packages based on the analyzed search criteria and available data.

ANALYZED SEARCH CRITERIA:
- Budget Level: {criteria.get('budget_level')}
- Travel Style: {criteria.get('travel_style')}
- Group Type: {criteria.get('group_type')}
- Duration: {criteria.get('duration_preference')}
- Interests: {', '.join(criteria.get('interests', []))}
- Route: {criteria.get('route', {}).get('from')} → {criteria.get('route', {}).get('to')}
- Preferred Airlines: {', '.join(criteria.get('preferred_airlines', []))}
- Preferred Hotel Chains: {', '.join(criteria.get('preferred_hotel_chains', []))}
- Must-Have Amenities: {', '.join(criteria.get('must_have_amenities', []))}
- Optional Amenities: {', '.join(criteria.get('optional_amenities', []))}

AVAILABLE FLIGHTS ({len(flights)} found):
{json.dumps(flights[:5], indent=2)}

AVAILABLE HOTELS ({len(hotels)} found):
{json.dumps(hotels[:5], indent=2)}

REQUIREMENTS:
1. Create 3-5 different packages based on the criteria
2. Each package should match the budget level and travel style
3. Select flights and hotels that best match the preferences
4. Include personalized recommendations and reasoning
5. Consider the group type and interests
6. Provide realistic pricing and package highlights

Return the response as a valid JSON array with the following structure:
[
  {{
    "package_id": "smart_package_001",
    "package_name": "Personalized Package Name",
    "package_type": "Budget/Mid-range/Luxury",
    "target_audience": "Based on group type and interests",
    "description": "Personalized description based on criteria",
    "duration": "Based on duration preference",
    "flight": {{
      "flight_id": "selected flight id",
      "airline": "airline name",
      "flight_number": "flight number",
      "departure": "from airport",
      "arrival": "to airport",
      "departure_time": "departure time",
      "arrival_time": "arrival time",
      "duration": "flight duration",
      "price": "flight price",
      "selection_reason": "Why this flight was chosen"
    }},
    "hotel": {{
      "hotel_id": "selected hotel id",
      "name": "hotel name",
      "location": "hotel location",
      "rating": "hotel rating",
      "amenities": ["amenities"],
      "price_per_night": "hotel price",
      "selection_reason": "Why this hotel was chosen"
    }},
    "package_highlights": [
      "Personalized highlights based on interests"
    ],
    "total_package_price": "calculated total price",
    "price_breakdown": {{
      "flight": "flight price",
      "hotel": "hotel price",
      "taxes": "estimated taxes"
    }},
    "recommendation_reason": "Why this package is perfect for the user",
    "personalized_features": [
      "Features specifically chosen for this user"
    ],
    "included_amenities": ["amenities included"],
    "optional_addons": ["optional services"]
  }}
]

Make sure the response is valid JSON and includes realistic pricing and personalized details.
"""
    
    return prompt

def call_genai_api(prompt):
    """
    Call the GenAI API to generate smart packages
    """
    try:
        # GenAI API configuration
        api_url = ""
        api_data = ""
        
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
        
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            return result.get('choices', [{}])[0].get('message', {}).get('content', '')
        else:
            print(f"GenAI API error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"Error calling GenAI API: {e}")
        return None

def parse_genai_response(response_text):
    """
    Parse the GenAI response to extract packages
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
            return packages
        else:
            print("No valid JSON found in GenAI response")
            return []
            
    except Exception as e:
        print(f"Error parsing GenAI response: {e}")
        return []

def create_smart_mock_packages(criteria, flights, hotels):
    """
    Create smart mock packages based on criteria
    """
    budget_level = criteria.get('budget_level', 'medium')
    travel_style = criteria.get('travel_style', 'leisure')
    group_type = criteria.get('group_type', 'couple')
    interests = criteria.get('interests', [])
    
    packages = []
    
    # Create packages based on budget level
    if budget_level == 'budget':
        packages.extend(create_budget_packages(criteria, flights, hotels))
    elif budget_level == 'medium':
        packages.extend(create_midrange_packages(criteria, flights, hotels))
    elif budget_level == 'luxury':
        packages.extend(create_luxury_packages(criteria, flights, hotels))
    
    # Create packages based on travel style
    if travel_style == 'adventure':
        packages.extend(create_adventure_packages(criteria, flights, hotels))
    elif travel_style == 'romantic':
        packages.extend(create_romantic_packages(criteria, flights, hotels))
    
    # Limit to 5 packages
    return packages[:5]

def create_budget_packages(criteria, flights, hotels):
    """Create budget packages"""
    return [
        {
            "package_id": "smart_budget_001",
            "package_name": "Smart Budget Explorer",
            "package_type": "Budget",
            "target_audience": f"{criteria.get('group_type', 'couple').title()} travelers",
            "description": f"Perfect {criteria.get('travel_style', 'leisure')} experience on a budget",
            "duration": criteria.get('duration_preference', '3-5 days'),
            "flight": flights[0] if flights else {"flight_id": "flight_001", "airline": "IndiGo"},
            "hotel": hotels[0] if hotels else {"hotel_id": "hotel_001", "name": "Budget Hotel"},
            "package_highlights": ["Affordable pricing", "Essential amenities", "Great value"],
            "total_package_price": 15000,
            "price_breakdown": {"flight": 3500, "hotel": 9000, "taxes": 2500},
            "recommendation_reason": f"Perfect for {criteria.get('budget_level')} travelers",
            "personalized_features": ["Budget-friendly", "Essential amenities"],
            "included_amenities": ["Flight", "Hotel", "WiFi"],
            "optional_addons": ["City Tour", "Airport Transfer"]
        }
    ]

def create_midrange_packages(criteria, flights, hotels):
    """Create mid-range packages"""
    return [
        {
            "package_id": "smart_midrange_001",
            "package_name": "Smart Comfort Package",
            "package_type": "Mid-range",
            "target_audience": f"{criteria.get('group_type', 'couple').title()} travelers",
            "description": f"Comfortable {criteria.get('travel_style', 'leisure')} experience",
            "duration": criteria.get('duration_preference', '3-5 days'),
            "flight": flights[1] if len(flights) > 1 else flights[0] if flights else {"flight_id": "flight_002", "airline": "Air India"},
            "hotel": hotels[1] if len(hotels) > 1 else hotels[0] if hotels else {"hotel_id": "hotel_002", "name": "Comfort Hotel"},
            "package_highlights": ["Comfortable travel", "Good amenities", "Balanced pricing"],
            "total_package_price": 35000,
            "price_breakdown": {"flight": 5500, "hotel": 24000, "taxes": 5500},
            "recommendation_reason": f"Perfect balance for {criteria.get('budget_level')} travelers",
            "personalized_features": ["Comfortable", "Good amenities"],
            "included_amenities": ["Flight", "Hotel", "WiFi", "Pool"],
            "optional_addons": ["Spa Package", "City Tour"]
        }
    ]

def create_luxury_packages(criteria, flights, hotels):
    """Create luxury packages"""
    return [
        {
            "package_id": "smart_luxury_001",
            "package_name": "Smart Luxury Experience",
            "package_type": "Luxury",
            "target_audience": f"{criteria.get('group_type', 'couple').title()} travelers",
            "description": f"Premium {criteria.get('travel_style', 'leisure')} experience",
            "duration": criteria.get('duration_preference', '3-5 days'),
            "flight": flights[-1] if flights else {"flight_id": "flight_003", "airline": "Vistara"},
            "hotel": hotels[-1] if hotels else {"hotel_id": "hotel_003", "name": "Luxury Hotel"},
            "package_highlights": ["Premium service", "Luxury amenities", "Exclusive experience"],
            "total_package_price": 85000,
            "price_breakdown": {"flight": 8500, "hotel": 60000, "taxes": 16500},
            "recommendation_reason": f"Ultimate luxury for {criteria.get('budget_level')} travelers",
            "personalized_features": ["Premium", "Luxury amenities"],
            "included_amenities": ["Flight", "Hotel", "Spa", "Concierge"],
            "optional_addons": ["Private Tour", "Helicopter Transfer"]
        }
    ]

def create_adventure_packages(criteria, flights, hotels):
    """Create adventure packages"""
    return [
        {
            "package_id": "smart_adventure_001",
            "package_name": "Smart Adventure Package",
            "package_type": "Adventure",
            "target_audience": "Adventure seekers",
            "description": "Thrilling adventure experience",
            "duration": criteria.get('duration_preference', '3-5 days'),
            "flight": flights[0] if flights else {"flight_id": "flight_001", "airline": "IndiGo"},
            "hotel": hotels[0] if hotels else {"hotel_id": "hotel_001", "name": "Adventure Hotel"},
            "package_highlights": ["Adventure activities", "Outdoor experiences", "Thrilling tours"],
            "total_package_price": 25000,
            "price_breakdown": {"flight": 4000, "hotel": 15000, "taxes": 6000},
            "recommendation_reason": "Perfect for adventure enthusiasts",
            "personalized_features": ["Adventure-focused", "Outdoor activities"],
            "included_amenities": ["Flight", "Hotel", "Gym", "Adventure Guide"],
            "optional_addons": ["Adventure Tours", "Equipment Rental"]
        }
    ]

def create_romantic_packages(criteria, flights, hotels):
    """Create romantic packages"""
    return [
        {
            "package_id": "smart_romantic_001",
            "package_name": "Smart Romantic Getaway",
            "package_type": "Romantic",
            "target_audience": "Couples",
            "description": "Perfect romantic experience",
            "duration": criteria.get('duration_preference', '3-5 days'),
            "flight": flights[1] if len(flights) > 1 else flights[0] if flights else {"flight_id": "flight_002", "airline": "Vistara"},
            "hotel": hotels[1] if len(hotels) > 1 else hotels[0] if hotels else {"hotel_id": "hotel_002", "name": "Romantic Hotel"},
            "package_highlights": ["Romantic setting", "Privacy", "Special amenities"],
            "total_package_price": 45000,
            "price_breakdown": {"flight": 6000, "hotel": 30000, "taxes": 9000},
            "recommendation_reason": "Perfect for romantic couples",
            "personalized_features": ["Romantic", "Private"],
            "included_amenities": ["Flight", "Hotel", "Spa", "Romantic Dinner"],
            "optional_addons": ["Couple Spa", "Romantic Tours"]
        }
    ]

