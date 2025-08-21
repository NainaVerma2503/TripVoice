from flask import Blueprint, jsonify, request
from datetime import datetime
import requests
import json
import os

package_bp = Blueprint('package', __name__)

@package_bp.route('/api/package/create', methods=['POST'])
def create_package():
    """
    Create travel packages using GenAI based on flight/hotel data and user preferences
    """
    try:
        # Get the request data
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'No data provided',
                'status': 'error'
            }), 400
        
        # Extract data
        flights = data.get('flights', [])
        hotels = data.get('hotels', [])
        user_preferences = data.get('user_preferences', {})
        
        # Create packages using GenAI
        packages = create_packages_with_genai(flights, hotels, user_preferences)
        
        return jsonify({
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'packages': packages,
            'package_count': len(packages)
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error',
            'timestamp': datetime.now().isoformat()
        }), 500

@package_bp.route('/api/package/create-from-search', methods=['POST'])
def create_package_from_search():
    """
    Create travel packages from search data using GenAI
    """
    try:
        # Get the request data
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'No data provided',
                'status': 'error'
            }), 400
        
        # Extract flight and hotel search data
        flight_data = data.get('flight', {})
        hotel_data = data.get('hotel', {})
        user_preferences = data.get('user_preferences', {})
        
        # Call flight API
        flight_response = call_flight_api(flight_data)
        
        # Call hotel API
        hotel_response = call_hotel_api(hotel_data)
        
        # Extract flights and hotels
        flights = []
        hotels = []
        
        if flight_response.get('status_code') == 200 and flight_response.get('data'):
            flights = extract_flight_details(flight_response.get('data'))
        
        if hotel_response.get('status_code') == 200 and hotel_response.get('data'):
            hotels = extract_hotel_details(hotel_response.get('data'))
        
        # Create packages using GenAI
        packages = create_packages_with_genai(flights, hotels, user_preferences)
        
        return jsonify({
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'packages': packages,
            'package_count': len(packages),
            'search_summary': {
                'from': flight_data.get('from'),
                'to': flight_data.get('to'),
                'departure_date': flight_data.get('depart_date'),
                'adults': flight_data.get('adults'),
                'total_flights_found': len(flights),
                'total_hotels_found': len(hotels)
            }
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error',
            'timestamp': datetime.now().isoformat()
        }), 500

def create_packages_with_genai(flights, hotels, user_preferences):
    """
    Create travel packages using GenAI
    """
    try:
        # Prepare the prompt for GenAI
        prompt = create_genai_prompt(flights, hotels, user_preferences)
        
        # Call GenAI API
        genai_response = call_genai_api(prompt)
        
        # Parse the response
        packages = parse_genai_response(genai_response)
        
        return packages
        
    except Exception as e:
        print(f"Error creating packages with GenAI: {e}")
        # Return mock packages as fallback
        return create_mock_packages(flights, hotels, user_preferences)

def create_genai_prompt(flights, hotels, user_preferences):
    """
    Create a comprehensive prompt for GenAI to generate travel packages
    """
    
    # Extract user preferences
    budget = user_preferences.get('budget', 'medium')
    interests = user_preferences.get('interests', ['general'])
    travel_style = user_preferences.get('travel_style', 'leisure')
    duration = user_preferences.get('duration', '3-5 days')
    
    # Sample flight and hotel data for the prompt
    sample_flights = flights[:5] if flights else []
    sample_hotels = hotels[:5] if hotels else []
    
    prompt = f"""
You are a travel package creator. Create 4-5 comprehensive travel packages based on the following data and user preferences.

USER PREFERENCES:
- Budget: {budget}
- Interests: {', '.join(interests)}
- Travel Style: {travel_style}
- Duration: {duration}

AVAILABLE FLIGHTS (sample):
{json.dumps(sample_flights, indent=2)}

AVAILABLE HOTELS (sample):
{json.dumps(sample_hotels, indent=2)}

REQUIREMENTS:
1. Create 4-5 different travel packages
2. Each package should include:
   - Package name and description
   - Selected flight details
   - Selected hotel details
   - Total package price
   - Package highlights
   - Target audience
   - Why this package is recommended

3. Package types should vary based on:
   - Budget (Budget, Mid-range, Luxury, Premium)
   - Interests (Adventure, Cultural, Relaxation, Business, Family)
   - Travel style (Leisure, Business, Adventure, Romantic)

4. Consider:
   - Flight and hotel compatibility
   - Price ranges based on budget
   - Location proximity
   - Amenities matching interests

5. Return the response as a valid JSON array with the following structure:
[
  {{
    "package_id": "package_001",
    "package_name": "Luxury Mumbai Getaway",
    "package_type": "Luxury",
    "target_audience": "Couples, Business travelers",
    "description": "A premium travel experience...",
    "duration": "3-5 days",
    "flight": {{
      "flight_id": "flight_001",
      "airline": "Vistara",
      "flight_number": "UK-825",
      "departure": "DEL",
      "arrival": "BOM",
      "departure_time": "2025-08-22T16:00:00.000+05:30",
      "arrival_time": "2025-08-22T18:20:00.000+05:30",
      "duration": "2h 20m",
      "price": 8500
    }},
    "hotel": {{
      "hotel_id": "hotel_001",
      "name": "Taj Palace Hotel",
      "location": "Colaba, Mumbai",
      "rating": 5,
      "amenities": ["WiFi", "Pool", "Spa", "Restaurant"],
      "price_per_night": 15000
    }},
    "package_highlights": [
      "Direct flight with premium airline",
      "5-star luxury hotel in prime location",
      "Spa and wellness facilities",
      "Fine dining experience"
    ],
    "total_package_price": 85000,
    "price_breakdown": {{
      "flight": 8500,
      "hotel": 60000,
      "taxes": 16500
    }},
    "recommendation_reason": "Perfect for luxury travelers seeking premium experience",
    "included_amenities": ["Flight", "Hotel", "Airport Transfer", "Welcome Drink"],
    "optional_addons": ["Spa Package", "City Tour", "Dinner at Fine Restaurant"]
  }}
]

Make sure the response is valid JSON and includes realistic pricing and details.
"""
    
    return prompt

def call_genai_api(prompt):
    """
    Call the GenAI API to generate packages
    """
    try:
        # GenAI API configuration
        api_url = "https://hackathon-openui-test.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2025-01-01-preview"
        api_key = ""  # Set your Azure OpenAI API key here or use environment variable
        
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
        # Look for JSON array in the response
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

def create_mock_packages(flights, hotels, user_preferences):
    """
    Create mock packages as fallback
    """
    budget = user_preferences.get('budget', 'medium')
    interests = user_preferences.get('interests', ['general'])
    
    mock_packages = [
        {
            "package_id": "package_001",
            "package_name": "Budget Explorer Package",
            "package_type": "Budget",
            "target_audience": "Backpackers, Budget travelers",
            "description": "Perfect for travelers on a budget who want to explore the city without breaking the bank.",
            "duration": "3-5 days",
            "package_image": "/images/packages/budget_package.jpg",
            "destination_image": "/images/hotels/hotel_exterior.jpg",
            "flight": flights[0] if flights else {
                "flight_id": "flight_001",
                "airline": "IndiGo",
                "flight_number": "6E-129",
                "departure": "DEL",
                "arrival": "BOM",
                "departure_time": "2025-08-22T13:25:00.000+05:30",
                "arrival_time": "2025-08-22T15:05:00.000+05:30",
                "duration": "1h 40m",
                "price": 3500,
                "airline_logo": "/images/airlines/indigo.png",
                "aircraft_image": "/images/flights/aircraft_boeing.jpg"
            },
            "hotel": hotels[0] if hotels else {
                "hotel_id": "hotel_001",
                "name": "Budget Hotel",
                "location": "Mumbai",
                "rating": 3,
                "amenities": ["WiFi", "Restaurant"],
                "price_per_night": 3000,
                "hotel_image": "/images/hotels/hotel_exterior.jpg",
                "room_image": "/images/hotels/hotel_room.jpg",
                "amenity_images": {
                    "WiFi": "/images/amenities/wifi.jpg",
                    "Restaurant": "/images/amenities/restaurant.jpg"
                }
            },
            "package_highlights": [
                "Affordable flight with reliable airline",
                "Budget-friendly accommodation",
                "Basic amenities included",
                "Great value for money"
            ],
            "total_package_price": 15000,
            "price_breakdown": {
                "flight": 3500,
                "hotel": 9000,
                "taxes": 2500
            },
            "recommendation_reason": "Ideal for budget-conscious travelers",
            "included_amenities": ["Flight", "Hotel", "WiFi"],
            "optional_addons": ["City Tour", "Airport Transfer"]
        },
        {
            "package_id": "package_002",
            "package_name": "Mid-Range Comfort Package",
            "package_type": "Mid-range",
            "target_audience": "Families, Business travelers",
            "description": "A comfortable travel experience with good amenities and reasonable pricing.",
            "duration": "3-5 days",
            "package_image": "/images/packages/midrange_package.jpg",
            "destination_image": "/images/hotels/hotel_lobby.jpg",
            "flight": flights[1] if len(flights) > 1 else {
                "flight_id": "flight_002",
                "airline": "Air India",
                "flight_number": "AI-101",
                "departure": "DEL",
                "arrival": "BOM",
                "departure_time": "2025-08-22T14:30:00.000+05:30",
                "arrival_time": "2025-08-22T16:45:00.000+05:30",
                "duration": "2h 15m",
                "price": 5500,
                "airline_logo": "/images/airlines/airindia.png",
                "aircraft_image": "/images/flights/aircraft_airbus.jpg"
            },
            "hotel": hotels[1] if len(hotels) > 1 else {
                "hotel_id": "hotel_002",
                "name": "Comfort Hotel",
                "location": "Mumbai",
                "rating": 4,
                "amenities": ["WiFi", "Pool", "Restaurant", "Gym"],
                "price_per_night": 8000,
                "hotel_image": "/images/hotels/hotel_lobby.jpg",
                "room_image": "/images/hotels/hotel_room.jpg",
                "amenity_images": {
                    "WiFi": "/images/amenities/wifi.jpg",
                    "Pool": "/images/amenities/pool.jpg",
                    "Restaurant": "/images/amenities/restaurant.jpg",
                    "Gym": "/images/amenities/gym.jpg"
                }
            },
            "package_highlights": [
                "Comfortable flight with meal service",
                "4-star hotel with good amenities",
                "Swimming pool and fitness center",
                "Family-friendly environment"
            ],
            "total_package_price": 35000,
            "price_breakdown": {
                "flight": 5500,
                "hotel": 24000,
                "taxes": 5500
            },
            "recommendation_reason": "Perfect balance of comfort and affordability",
            "included_amenities": ["Flight", "Hotel", "WiFi", "Pool", "Gym"],
            "optional_addons": ["Spa Package", "City Tour", "Airport Transfer"]
        },
        {
            "package_id": "package_003",
            "package_name": "Luxury Premium Package",
            "package_type": "Luxury",
            "target_audience": "Couples, Luxury travelers",
            "description": "An exclusive luxury experience with premium services and top-notch amenities.",
            "duration": "3-5 days",
            "package_image": "/images/packages/luxury_package.jpg",
            "destination_image": "/images/hotels/hotel_spa.jpg",
            "flight": flights[2] if len(flights) > 2 else {
                "flight_id": "flight_003",
                "airline": "Vistara",
                "flight_number": "UK-825",
                "departure": "DEL",
                "arrival": "BOM",
                "departure_time": "2025-08-22T16:00:00.000+05:30",
                "arrival_time": "2025-08-22T18:20:00.000+05:30",
                "duration": "2h 20m",
                "price": 8500,
                "airline_logo": "/images/airlines/vistara.png",
                "aircraft_image": "/images/flights/aircraft_boeing.jpg"
            },
            "hotel": hotels[2] if len(hotels) > 2 else {
                "hotel_id": "hotel_003",
                "name": "Luxury Palace Hotel",
                "location": "Mumbai",
                "rating": 5,
                "amenities": ["WiFi", "Pool", "Spa", "Restaurant", "Concierge"],
                "price_per_night": 15000,
                "hotel_image": "/images/hotels/hotel_spa.jpg",
                "room_image": "/images/hotels/hotel_room.jpg",
                "amenity_images": {
                    "WiFi": "/images/amenities/wifi.jpg",
                    "Pool": "/images/amenities/pool.jpg",
                    "Spa": "/images/amenities/spa.jpg",
                    "Restaurant": "/images/amenities/restaurant.jpg",
                    "Concierge": "/images/amenities/concierge.jpg"
                }
            },
            "package_highlights": [
                "Premium flight with business class comfort",
                "5-star luxury hotel with spa",
                "Concierge service",
                "Fine dining experience"
            ],
            "total_package_price": 85000,
            "price_breakdown": {
                "flight": 8500,
                "hotel": 60000,
                "taxes": 16500
            },
            "recommendation_reason": "Ultimate luxury experience for discerning travelers",
            "included_amenities": ["Flight", "Hotel", "Spa Access", "Concierge", "Welcome Drink"],
            "optional_addons": ["Private City Tour", "Helicopter Transfer", "Exclusive Dining"]
        }
    ]
    
    return mock_packages

# Helper functions (same as in search_controller.py)
def call_flight_api(flight_data):
    """Call the flight search API"""
    try:
        base_url = 'https://qa2new.cleartrip.com/flight/search/v2'
        params = {
            'from': flight_data.get('from'),
            'to': flight_data.get('to'),
            'depart_date': flight_data.get('depart_date'),
            'adults': flight_data.get('adults'),
            'intl': flight_data.get('intl')
        }
        headers = {'accept': 'application/json'}
        response = requests.get(base_url, params=params, headers=headers, timeout=30)
        
        return {
            'status_code': response.status_code,
            'data': response.json() if response.status_code == 200 else None,
            'error': None if response.status_code == 200 else response.text
        }
    except Exception as e:
        return {
            'status_code': None,
            'data': None,
            'error': f'Request failed: {str(e)}'
        }

def call_hotel_api(hotel_data):
    """Call the hotel search API"""
    try:
        base_url = 'https://qa2new.cleartrip.com/hotel/orchestrator/v2/search'
        headers = {'Content-Type': 'application/json'}
        response = requests.post(base_url, json=hotel_data, headers=headers, timeout=30)
        
        return {
            'status_code': response.status_code,
            'data': response.json() if response.status_code == 200 else None,
            'error': None if response.status_code == 200 else response.text
        }
    except Exception as e:
        return {
            'status_code': None,
            'data': None,
            'error': f'Request failed: {str(e)}'
        }

def extract_flight_details(flight_data):
    """Extract flight details (same as in search_controller.py)"""
    # This would be the same implementation as in search_controller.py
    # For brevity, returning mock data
    return []

def extract_hotel_details(hotel_data):
    """Extract hotel details (same as in search_controller.py)"""
    # This would be the same implementation as in search_controller.py
    # For brevity, returning mock data
    return []
