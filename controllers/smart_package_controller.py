from flask import Blueprint, request, jsonify
import requests
import json
from datetime import datetime
import random

smart_package_bp = Blueprint('smart_package', __name__)

@smart_package_bp.route('/api/smart-package/create', methods=['POST'])
def create_smart_package():
    """
    Create smart packages based on search criteria and preferences
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Extract search criteria from the request
        search_criteria = extract_search_criteria(data)
        
        # Get filtered flights and hotels based on criteria
        flights, hotels = filter_data_by_criteria(search_criteria)
        
        # Create smart packages using GenAI
        packages = create_smart_packages_with_genai(search_criteria, flights, hotels)
        
        return jsonify({
            "package_count": len(packages),
            "packages": packages,
            "status": "success",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def extract_search_criteria(data):
    """
    Extract and analyze search criteria from the request
    """
    criteria = {
        "budget_level": data.get("budget_level", "medium"),
        "travel_style": data.get("travel_style", "leisure"),
        "group_type": data.get("group_type", "couple"),
        "interests": data.get("interests", []),
        "duration_preference": data.get("duration_preference", "3-5 days"),
        "must_have_amenities": data.get("must_have_amenities", []),
        "optional_amenities": data.get("optional_amenities", []),
        "preferred_airlines": data.get("preferred_airlines", []),
        "preferred_hotel_chains": data.get("preferred_hotel_chains", []),
        "route": data.get("route", {}),
        "dates": data.get("dates", {})
    }
    
    return criteria

def filter_data_by_criteria(criteria):
    """
    Filter flights and hotels based on search criteria
    """
    # Get comprehensive mock data
    all_flights = generate_comprehensive_flights()
    all_hotels = generate_comprehensive_hotels()
    
    # Filter flights based on route
    route = criteria.get("route", {})
    from_airport = route.get("from", "DEL")
    to_airport = route.get("to", "BOM")
    
    filtered_flights = []
    for flight in all_flights:
        if flight["departure"] == from_airport and flight["arrival"] == to_airport:
            # Check preferred airlines if specified
            if criteria.get("preferred_airlines"):
                if flight["airline"] in criteria["preferred_airlines"]:
                    filtered_flights.append(flight)
            else:
                filtered_flights.append(flight)
    
    # Filter hotels based on location and amenities
    dates = criteria.get("dates", {})
    target_city = dates.get("city", "Mumbai")
    
    filtered_hotels = []
    for hotel in all_hotels:
        if target_city.lower() in hotel["location"].lower():
            # Check must-have amenities
            must_have = criteria.get("must_have_amenities", [])
            hotel_amenities = [amenity.lower() for amenity in hotel["amenities"]]
            
            if all(amenity.lower() in hotel_amenities for amenity in must_have):
                # Check preferred hotel chains if specified
                if criteria.get("preferred_hotel_chains"):
                    hotel_name = hotel["name"].lower()
                    if any(chain.lower() in hotel_name for chain in criteria["preferred_hotel_chains"]):
                        filtered_hotels.append(hotel)
                else:
                    filtered_hotels.append(hotel)
    
    # If no filtered results, return some default data
    if not filtered_flights:
        filtered_flights = all_flights[:5]
    if not filtered_hotels:
        filtered_hotels = all_hotels[:5]
    
    return filtered_flights, filtered_hotels

def generate_comprehensive_flights():
    """
    Generate comprehensive mock flight data
    """
    airlines = ["IndiGo", "Air India", "Vistara", "SpiceJet", "GoAir", "AirAsia India"]
    routes = [
        ("DEL", "BOM"), ("BOM", "DEL"), ("DEL", "BLR"), ("BLR", "DEL"),
        ("BOM", "BLR"), ("BLR", "BOM"), ("DEL", "HYD"), ("HYD", "DEL"),
        ("BOM", "HYD"), ("HYD", "BOM"), ("DEL", "MAA"), ("MAA", "DEL")
    ]
    
    flights = []
    for i in range(50):
        airline = random.choice(airlines)
        from_airport, to_airport = random.choice(routes)
        
        # Generate random departure time
        hour = random.randint(6, 22)
        minute = random.choice([0, 15, 30, 45])
        departure_time = f"2025-08-22T{hour:02d}:{minute:02d}:00.000+05:30"
        
        # Calculate arrival time (1-3 hours later)
        duration_hours = random.randint(1, 3)
        duration_minutes = random.randint(0, 59)
        arrival_hour = (hour + duration_hours) % 24
        arrival_time = f"2025-08-22T{arrival_hour:02d}:{minute:02d}:00.000+05:30"
        
        flight = {
            "flight_id": f"flight_{i+1:03d}",
            "airline": airline,
            "flight_number": f"{airline[:2]}-{random.randint(100, 999)}",
            "departure": from_airport,
            "arrival": to_airport,
            "departure_time": departure_time,
            "arrival_time": arrival_time,
            "duration": f"{duration_hours}h {duration_minutes}m",
            "stops": random.choice([0, 1]),
            "stopDetails": "Non-stop" if random.choice([0, 1]) == 0 else "1 stop",
            "price": random.randint(2000, 15000),
            "airline_logo": f"/images/airlines/{airline.lower().replace(' ', '_')}.png",
            "aircraft_image": "/images/flights/aircraft_boeing.jpg",
            "legs": [{
                "flightNumber": f"{airline[:2]}-{random.randint(100, 999)}",
                "departureTerminal": str(random.randint(1, 3)),
                "arrivalTerminal": str(random.randint(1, 3))
            }]
        }
        
        flights.append(flight)
    
    return flights

def generate_comprehensive_hotels():
    """
    Generate comprehensive mock hotel data
    """
    hotel_chains = ["Taj", "Oberoi", "ITC", "Leela", "Trident", "Hyatt", "Marriott", "Hilton"]
    cities = ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad"]
    areas = ["Colaba", "Lower Parel", "Juhu", "Bandra", "Andheri", "Powai", "Worli", "Nariman Point"]
    amenities_list = [
        ["WiFi", "Pool", "Gym", "Restaurant", "Spa"],
        ["WiFi", "Pool", "Restaurant", "Business Center"],
        ["WiFi", "Gym", "Restaurant", "Bar", "Room Service"],
        ["WiFi", "Pool", "Spa", "Restaurant", "Concierge"],
        ["WiFi", "Restaurant", "Bar", "Lounge", "Entertainment"]
    ]
    
    hotels = []
    for i in range(50):
        chain = random.choice(hotel_chains)
        city = random.choice(cities)
        area = random.choice(areas)
        amenities = random.choice(amenities_list)
        
        hotel = {
            "hotel_id": f"hotel_{i+1:03d}",
            "name": f"{chain} {random.choice(['Hotel', 'Palace', 'Resort', 'Grand', 'Premier'])}",
            "location": f"{area}, {city}",
            "rating": random.randint(3, 5),
            "price": {
                "amount": random.randint(3000, 30000),
                "currency": "INR"
            },
            "amenities": amenities,
            "hotel_image": f"/images/hotels/hotel_{i+1:03d}.jpg",
            "room_image": f"/images/hotels/room_{i+1:03d}.jpg",
            "amenity_images": [f"/images/amenities/{amenity.lower()}.jpg" for amenity in amenities[:3]]
        }
        
        hotels.append(hotel)
    
    return hotels

def create_smart_packages_with_genai(criteria, flights, hotels):
    """
    Create smart packages using GenAI
    """
    try:
        # Create prompt for GenAI
        prompt = create_smart_genai_prompt(criteria, flights, hotels)
        
        # Call GenAI API
        response = call_genai_api(prompt)
        
        if response:
            packages = parse_genai_response(response)
            if packages:
                return packages
        
        # Fallback to smart mock packages
        return create_smart_mock_packages(criteria, flights, hotels)
        
    except Exception as e:
        print(f"Error creating smart packages with GenAI: {e}")
        return create_smart_mock_packages(criteria, flights, hotels)

def create_smart_genai_prompt(criteria, flights, hotels):
    """
    Create a detailed prompt for smart package creation
    """
    # Sample flight and hotel data for the prompt
    sample_flights = flights[:3] if flights else []
    sample_hotels = hotels[:3] if hotels else []
    
    prompt = f"""
    Create 4-5 personalized travel packages based on the following detailed criteria and available options:

    SEARCH CRITERIA:
    - Budget Level: {criteria.get('budget_level', 'medium')}
    - Travel Style: {criteria.get('travel_style', 'leisure')}
    - Group Type: {criteria.get('group_type', 'couple')}
    - Interests: {criteria.get('interests', [])}
    - Duration Preference: {criteria.get('duration_preference', '3-5 days')}
    - Must Have Amenities: {criteria.get('must_have_amenities', [])}
    - Optional Amenities: {criteria.get('optional_amenities', [])}
    - Preferred Airlines: {criteria.get('preferred_airlines', [])}
    - Preferred Hotel Chains: {criteria.get('preferred_hotel_chains', [])}
    - Route: {criteria.get('route', {})}
    - Dates: {criteria.get('dates', {})}

    AVAILABLE FLIGHTS (sample):
    {json.dumps(sample_flights, indent=2)}

    AVAILABLE HOTELS (sample):
    {json.dumps(sample_hotels, indent=2)}

    Create 4-5 different packages with the following structure for each:
    {{
        "package_id": "unique_id",
        "package_name": "Descriptive name",
        "package_type": "Budget/Medium/Luxury",
        "target_audience": "Who this package is for",
        "description": "Detailed description",
        "duration": "X days, Y nights",
        "flight": {{flight_details}},
        "hotel": {{hotel_details}},
        "package_highlights": ["feature1", "feature2", "feature3"],
        "included_amenities": ["amenity1", "amenity2"],
        "optional_addons": ["addon1", "addon2"],
        "personalized_features": ["feature1", "feature2"],
        "price_breakdown": {{
            "flight": price,
            "hotel": price,
            "taxes": price
        }},
        "total_package_price": total_price,
        "recommendation_reason": "Why this package is recommended"
    }}

    IMPORTANT: Create 4-5 packages with different combinations of flights and hotels. Each package should have 1 flight and 1 hotel combination.

    Return only valid JSON array with 4-5 packages.
    """

    return prompt

def call_genai_api(prompt):
    """
    Call the GenAI API to generate smart packages
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
    
    # Create 4-5 packages with different combinations
    for i in range(4):
        if i == 0:
            packages.append(create_luxury_package(criteria, flights, hotels, i))
        elif i == 1:
            packages.append(create_cultural_package(criteria, flights, hotels, i))
        elif i == 2:
            packages.append(create_foodie_package(criteria, flights, hotels, i))
        elif i == 3:
            packages.append(create_wellness_package(criteria, flights, hotels, i))
    
    return packages

def create_luxury_package(criteria, flights, hotels, index):
    """Create luxury package"""
    flight = flights[index] if len(flights) > index else flights[0] if flights else {
        "airline": "IndiGo",
        "arrivalAirport": "BOM",
        "arrivalTerminal": "1",
        "arrivalTime": "2025-08-22T15:05:00.000+05:30",
        "departureAirport": "DEL",
        "departureTerminal": "1D",
        "departureTime": "2025-08-22T13:25:00.000+05:30",
        "flightNumber": "6E-129",
        "id": "sample_flight_001",
        "legs": [{"arrivalTerminal": "1", "departureTerminal": "1D", "flightNumber": "6E-129"}],
        "stopDetails": "Direct flight",
        "stops": 0,
        "totalDuration": "1h 40m",
        "price": {"amount": 5500, "description": "Premium direct flight"}
    }
    
    hotel = hotels[index] if len(hotels) > index else hotels[0] if hotels else {
        "amenities": ["WiFi", "Pool", "Spa", "Restaurant"],
        "id": "sample_hotel_001",
        "location": {"address": "Apollo Bunder, Mumbai", "area": "Colaba", "city": "Mumbai"},
        "name": "Taj Palace Hotel",
        "price": {"amount": 15000, "currency": "INR", "description": "Luxury hotel for 4 nights"},
        "rating": 5
    }
    
    return {
        "package_name": "Luxury Mumbai Getaway",
        "package_type": "Luxury",
        "flight": flight,
        "hotel": hotel,
        "price_breakdown": {
            "flight": {"amount": 5500, "description": "Premium direct flight"},
            "hotel": {"amount": 60000, "description": "Luxury hotel for 4 nights"},
            "taxes": {"amount": 9500, "description": "Government taxes and fees"},
            "total": {"amount": 75000, "description": "Total package price"}
        }
    }

def create_cultural_package(criteria, flights, hotels, index):
    """Create cultural package"""
    flight = flights[index] if len(flights) > index else flights[0] if flights else {
        "airline": "Vistara",
        "arrivalAirport": "BOM",
        "arrivalTerminal": "2",
        "arrivalTime": "2025-08-22T16:00:00.000+05:30",
        "departureAirport": "DEL",
        "departureTerminal": "3",
        "departureTime": "2025-08-22T14:00:00.000+05:30",
        "flightNumber": "UK-825",
        "id": "cultural_flight_002",
        "legs": [
            {
                "arrivalTerminal": "2",
                "departureTerminal": "3",
                "flightNumber": "UK-825"
            }
        ],
        "stopDetails": "Direct flight",
        "stops": 0,
        "totalDuration": "2h 0m",
        "price": 7500
    }
    
    hotel = hotels[index] if len(hotels) > index else hotels[0] if hotels else {
        "amenities": ["WiFi", "Pool", "Restaurant", "Business Center"],
        "id": "cultural_hotel_002",
        "location": {
            "address": "Lower Parel, Mumbai",
            "area": "Lower Parel",
            "city": "Mumbai"
        },
        "name": "The St. Regis Mumbai",
        "price": {
            "amount": 22000,
            "currency": "INR"
        },
        "rating": 5
    }
    
    return {
        "package_name": "Mumbai Cultural Explorer",
        "package_type": "Mid-range",
        "flight": flight,
        "hotel": hotel,
        "price_breakdown": {
            "flight": {"amount": 7500, "description": "Premium economy flight"},
            "hotel": {"amount": 88000, "description": "Comfortable hotel for 4 nights"},
            "taxes": {"amount": 3500, "description": "Basic taxes and fees"},
            "total": 99000
        }
    }

def create_foodie_package(criteria, flights, hotels, index):
    """Create foodie package"""
    flight = flights[index] if len(flights) > index else flights[0] if flights else {
        "airline": "Air India",
        "arrivalAirport": "BOM",
        "arrivalTerminal": "2",
        "arrivalTime": "2025-08-22T12:15:00.000+05:30",
        "departureAirport": "DEL",
        "departureTerminal": "3",
        "departureTime": "2025-08-22T10:00:00.000+05:30",
        "flightNumber": "AI-101",
        "id": "foodie_flight_003",
        "legs": [
            {
                "arrivalTerminal": "2",
                "departureTerminal": "3",
                "flightNumber": "AI-101"
            }
        ],
        "stopDetails": "Direct flight",
        "stops": 0,
        "totalDuration": "2h 15m",
        "price": 6500
    }
    
    hotel = hotels[index] if len(hotels) > index else hotels[0] if hotels else {
        "amenities": ["WiFi", "Pool", "Restaurant", "Bar", "Room Service"],
        "id": "foodie_hotel_003",
        "location": {
            "address": "Juhu, Mumbai",
            "area": "Juhu",
            "city": "Mumbai"
        },
        "name": "JW Marriott Mumbai Juhu",
        "price": {
            "amount": 23000,
            "currency": "INR"
        },
        "rating": 5
    }
    
    return {
        "package_name": "Mumbai Foodie Adventure",
        "package_type": "Mid-range",
        "flight": flight,
        "hotel": hotel,
        "price_breakdown": {
            "flight": {"amount": 6500, "description": "Economy class flight"},
            "hotel": {"amount": 92000, "description": "Hotel with dining facilities for 4 nights"},
            "taxes": {"amount": 5500, "description": "Taxes including food tour fees"},
            "total": 104000
        }
    }

def create_wellness_package(criteria, flights, hotels, index):
    """Create wellness package"""
    flight = flights[index] if len(flights) > index else flights[0] if flights else {
        "airline": "GoAir",
        "arrivalAirport": "BOM",
        "arrivalTerminal": "2",
        "arrivalTime": "2025-08-22T09:30:00.000+05:30",
        "departureAirport": "DEL",
        "departureTerminal": "1",
        "departureTime": "2025-08-22T06:30:00.000+05:30",
        "flightNumber": "Go-522",
        "id": "wellness_flight_004",
        "legs": [
            {
                "arrivalTerminal": "2",
                "departureTerminal": "1",
                "flightNumber": "Go-217"
            }
        ],
        "stopDetails": "1 stop",
        "stops": 1,
        "totalDuration": "3h 0m",
        "price": 4500
    }
    
    hotel = hotels[index] if len(hotels) > index else hotels[0] if hotels else {
        "amenities": ["WiFi", "Pool", "Spa", "Restaurant", "Yoga Studio"],
        "id": "wellness_hotel_004",
        "location": {
            "address": "Powai, Mumbai",
            "area": "Powai",
            "city": "Mumbai"
        },
        "name": "The Oberoi Mumbai",
        "price": {
            "amount": 28000,
            "currency": "INR"
        },
        "rating": 5
    }
    
    return {
        "package_name": "Mumbai Wellness Retreat",
        "package_type": "Premium",
        "flight": flight,
        "hotel": hotel,
        "price_breakdown": {
            "flight": {"amount": 4500, "description": "Economy class flight"},
            "hotel": {"amount": 112000, "description": "Wellness hotel for 4 nights"},
            "taxes": {"amount": 12500, "description": "Taxes including spa treatments"},
            "total": 129000
        }
    }
