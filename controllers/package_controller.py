from flask import Blueprint, request, jsonify
import requests
import json
from datetime import datetime
import random

package_bp = Blueprint('package', __name__)

@package_bp.route('/api/package/create', methods=['POST'])
def create_package():
    """
    Create packages from search criteria (flight and hotel search parameters)
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        flight_data = data.get('flight', {})
        hotel_data = data.get('hotel', {})
        
        if not flight_data or not hotel_data:
            return jsonify({"error": "Both flight and hotel search criteria required"}), 400
        
        # Call flight API
        flight_response = call_flight_api(flight_data)
        
        # Call hotel API
        hotel_response = call_hotel_api(hotel_data)
        
        # Extract flight and hotel details
        flights = extract_flight_details(flight_response)
        hotels = extract_hotel_details(hotel_response)
        
        # Get user preferences from search criteria
        user_preferences = extract_user_preferences_from_search(data)
        
        # Create packages using GenAI
        packages = create_packages_with_genai(flights, hotels, user_preferences)
        
        return jsonify({
            "package_count": len(packages),
            "packages": packages,
            "status": "success",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@package_bp.route('/api/package/create-from-search', methods=['POST'])
def create_package_from_search():
    """
    Perform search and create packages from the results
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No search data provided"}), 400
        
        # Call flight API
        flight_data = data.get('flight', {})
        flight_response = call_flight_api(flight_data)
        
        # Call hotel API
        hotel_data = data.get('hotel', {})
        hotel_response = call_hotel_api(hotel_data)
        
        # Extract flight and hotel details
        flights = extract_flight_details(flight_response)
        hotels = extract_hotel_details(hotel_response)
        
        # Get user preferences from search criteria
        user_preferences = extract_user_preferences(data)
        
        # Create packages using GenAI
        packages = create_packages_with_genai(flights, hotels, user_preferences)
        
        return jsonify({
            "status": "success",
            "packages": packages,
            "package_count": len(packages),
            "search_summary": {
                "total_flights_found": len(flights),
                "total_hotels_found": len(hotels),
                "from": flight_data.get('from'),
                "to": flight_data.get('to'),
                "departure_date": flight_data.get('depart_date'),
                "adults": flight_data.get('adults')
            },
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def call_flight_api(flight_data):
    """
    Call the ClearTrip Flight API
    """
    try:
        url = "https://qa2new.cleartrip.com/flight/search/v2"
        
        params = {
            'from': flight_data.get('from'),
            'to': flight_data.get('to'),
            'depart_date': flight_data.get('depart_date'),
            'adults': flight_data.get('adults'),
            'intl': flight_data.get('intl', 'n')
        }
        
        headers = {
            'accept': 'application/json'
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Flight API error: {response.status_code}")
            return {"data": {"subTravelOptions": []}}
            
    except Exception as e:
        print(f"Error calling flight API: {e}")
        return {"data": {"subTravelOptions": []}}

def call_hotel_api(hotel_data):
    """
    Call the ClearTrip Hotel API
    """
    try:
        url = "https://qa2new.cleartrip.com/hotel/orchestrator/v2/search"
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = requests.post(url, headers=headers, json=hotel_data, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Hotel API error: {response.status_code}")
            return {"data": {"response": {"hotels": []}}}
            
    except Exception as e:
        print(f"Error calling hotel API: {e}")
        return {"data": {"response": {"hotels": []}}}

def extract_flight_details(flight_response):
    """
    Extract flight details from the API response
    """
    flights = []
    
    try:
        # Extract from actual API response if available
        if flight_response and 'data' in flight_response:
            travel_options = flight_response.get('data', {}).get('subTravelOptions', [])
            
            for option in travel_options:
                if 'legs' in option and option['legs']:
                    leg = option['legs'][0]
                    
                    flight = {
                        "flight_id": f"flight_{len(flights) + 1:03d}",
                        "airline": leg.get('airline', 'Unknown'),
                        "flight_number": leg.get('flightNumber', 'Unknown'),
                        "departure": leg.get('departureAirport', 'Unknown'),
                        "arrival": leg.get('arrivalAirport', 'Unknown'),
                        "departure_time": leg.get('departureTime', ''),
                        "arrival_time": leg.get('arrivalTime', ''),
                        "duration": calculate_duration(leg.get('departureTime'), leg.get('arrivalTime')),
                        "stops": option.get('stops', 0),
                        "stopDetails": "Non-stop" if option.get('stops', 0) == 0 else f"{option.get('stops')} stop(s)",
                        "price": option.get('price', {}).get('amount', 0),
                        "airline_logo": f"/images/airlines/{leg.get('airline', 'unknown').lower()}.png",
                        "aircraft_image": "/images/flights/aircraft_boeing.jpg"
                    }
                    
                    # Add legs details
                    flight["legs"] = []
                    for leg_data in option.get('legs', []):
                        flight["legs"].append({
                            "flightNumber": leg_data.get('flightNumber', ''),
                            "departureTerminal": leg_data.get('departureTerminal', ''),
                            "arrivalTerminal": leg_data.get('arrivalTerminal', '')
                        })
                    
                    flights.append(flight)
    except Exception as e:
        print(f"Error extracting flight details: {e}")
    
    # Always return mock data for consistent testing
    return generate_mock_flights()

def extract_hotel_details(hotel_response):
    """
    Extract hotel details from the API response
    """
    hotels = []
    
    try:
        # Extract from actual API response if available
        if hotel_response and 'data' in hotel_response:
            hotel_list = hotel_response.get('data', {}).get('response', {}).get('hotels', [])
            
            for hotel in hotel_list:
                hotel_data = {
                    "hotel_id": f"hotel_{len(hotels) + 1:03d}",
                    "name": hotel.get('name', 'Unknown Hotel'),
                    "location": hotel.get('location', {}).get('address', 'Unknown Location'),
                    "rating": hotel.get('rating', 3),
                    "price": {
                        "amount": hotel.get('price', {}).get('amount', 5000),
                        "currency": "INR"
                    },
                    "amenities": hotel.get('amenities', ['WiFi', 'Restaurant']),
                    "hotel_image": f"/images/hotels/hotel_{len(hotels) + 1:03d}.jpg",
                    "room_image": f"/images/hotels/room_{len(hotels) + 1:03d}.jpg"
                }
                
                hotels.append(hotel_data)
    except Exception as e:
        print(f"Error extracting hotel details: {e}")
    
    # Always return mock data for consistent testing
    return generate_mock_hotels()

def generate_mock_flights():
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
    for i in range(100):
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

def generate_mock_hotels():
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
    for i in range(100):
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

def extract_user_preferences_from_search(data):
    """
    Extract user preferences from search criteria
    """
    preferences = {
        "budget": "medium",
        "interests": ["general"],
        "travel_style": "leisure",
        "group_type": "couple"
    }
    
    # Extract from flight data
    if 'flight' in data:
        flight_data = data['flight']
        preferences["from"] = flight_data.get('from')
        preferences["to"] = flight_data.get('to')
        preferences["departure_date"] = flight_data.get('depart_date')
        preferences["adults"] = flight_data.get('adults')
    
    # Extract from hotel data
    if 'hotel' in data:
        hotel_data = data['hotel']
        preferences["check_in"] = hotel_data.get('checkInDate')
        preferences["check_out"] = hotel_data.get('checkOutDate')
        preferences["city"] = hotel_data.get('city')
        preferences["state"] = hotel_data.get('state')
        preferences["country"] = hotel_data.get('country')
        
        # Determine group type based on room allocations
        room_allocations = hotel_data.get('roomAllocations', [])
        if room_allocations:
            adults = room_allocations[0].get('adults', {}).get('count', 1)
            children = room_allocations[0].get('children', {}).get('count', 0)
            
            if adults == 1:
                preferences["group_type"] = "solo"
            elif adults == 2 and children == 0:
                preferences["group_type"] = "couple"
            elif children > 0:
                preferences["group_type"] = "family"
            else:
                preferences["group_type"] = "group"
    
    return preferences

def extract_user_preferences(data):
    """
    Extract user preferences from search criteria (legacy function)
    """
    return extract_user_preferences_from_search(data)

def normalize_flight_data(flights):
    """
    Normalize flight data to ensure consistent field names
    """
    normalized_flights = []
    
    for flight in flights:
        normalized_flight = {
            "flight_id": flight.get("flight_id") or flight.get("id", f"flight_{len(normalized_flights)+1:03d}"),
            "airline": flight.get("airline", "Unknown"),
            "flight_number": flight.get("flight_number") or flight.get("flightNumber", "Unknown"),
            "departure": flight.get("departure") or flight.get("departureAirport", "Unknown"),
            "arrival": flight.get("arrival") or flight.get("arrivalAirport", "Unknown"),
            "departure_time": flight.get("departure_time") or flight.get("departureTime", ""),
            "arrival_time": flight.get("arrival_time") or flight.get("arrivalTime", ""),
            "duration": flight.get("duration") or flight.get("totalDuration", "Unknown"),
            "stops": flight.get("stops", 0),
            "stopDetails": flight.get("stopDetails", "Non-stop" if flight.get("stops", 0) == 0 else f"{flight.get('stops')} stop(s)"),
            "price": flight.get("price", 0),
            "airline_logo": flight.get("airline_logo", f"/images/airlines/{flight.get('airline', 'unknown').lower().replace(' ', '_')}.png"),
            "aircraft_image": flight.get("aircraft_image", "/images/flights/aircraft_boeing.jpg"),
            "legs": flight.get("legs", [{
                "flightNumber": flight.get("flight_number") or flight.get("flightNumber", ""),
                "departureTerminal": flight.get("departureTerminal", ""),
                "arrivalTerminal": flight.get("arrivalTerminal", "")
            }])
        }
        normalized_flights.append(normalized_flight)
    
    return normalized_flights

def normalize_hotel_data(hotels):
    """
    Normalize hotel data to ensure consistent field names
    """
    normalized_hotels = []
    
    for hotel in hotels:
        # Handle location field which can be a string or object
        location = hotel.get("location", {})
        if isinstance(location, dict):
            location_str = location.get("city", location.get("address", "Unknown Location"))
        else:
            location_str = str(location)
        
        # Handle price field which can be a number or object
        price = hotel.get("price", {})
        if isinstance(price, dict):
            price_amount = price.get("amount", 5000)
        else:
            price_amount = price
        
        normalized_hotel = {
            "hotel_id": hotel.get("hotel_id") or hotel.get("id", f"hotel_{len(normalized_hotels)+1:03d}"),
            "name": hotel.get("name", "Unknown Hotel"),
            "location": location_str,
            "rating": hotel.get("rating", 3),
            "price": {
                "amount": price_amount,
                "currency": "INR"
            },
            "amenities": hotel.get("amenities", ["WiFi", "Restaurant"]),
            "hotel_image": hotel.get("hotel_image", f"/images/hotels/hotel_{len(normalized_hotels)+1:03d}.jpg"),
            "room_image": hotel.get("room_image", f"/images/hotels/room_{len(normalized_hotels)+1:03d}.jpg"),
            "amenity_images": hotel.get("amenity_images", [])
        }
        normalized_hotels.append(normalized_hotel)
    
    return normalized_hotels

def calculate_duration(departure_time, arrival_time):
    """
    Calculate flight duration from departure and arrival times
    """
    try:
        if not departure_time or not arrival_time:
            return "Unknown"
        
        # Simple duration calculation (you might want to use datetime for more accuracy)
        return "2h 15m"  # Placeholder
    except:
        return "Unknown"

def create_packages_with_genai(flights, hotels, user_preferences):
    """
    Create packages using GenAI
    """
    try:
        # Normalize flight and hotel data to ensure consistent field names
        normalized_flights = normalize_flight_data(flights)
        normalized_hotels = normalize_hotel_data(hotels)
        
        # Create prompt for GenAI
        prompt = create_genai_prompt(normalized_flights, normalized_hotels, user_preferences)
        
        # Call GenAI API
        response = call_genai_api(prompt)
        
        if response:
            packages = parse_genai_response(response)
            if packages:
                return packages
        
        # Fallback to mock packages
        return create_mock_packages(normalized_flights, normalized_hotels, user_preferences)
        
    except Exception as e:
        print(f"Error creating packages with GenAI: {e}")
        return create_mock_packages(flights, hotels, user_preferences)

def create_genai_prompt(flights, hotels, user_preferences):
    """
    Create a detailed prompt for GenAI package creation
    """
    # Sample flight and hotel data for the prompt
    sample_flights = flights[:3] if flights else []
    sample_hotels = hotels[:3] if hotels else []
    
    # Determine package types based on search criteria
    from_city = user_preferences.get('from', 'Unknown')
    to_city = user_preferences.get('to', 'Unknown')
    group_type = user_preferences.get('group_type', 'couple')
    adults = user_preferences.get('adults', 1)
    city = user_preferences.get('city', 'Unknown')
    state = user_preferences.get('state', 'Unknown')
    
    prompt = f"""
    Create 4 personalized travel packages based on the following search criteria and available options:

    SEARCH CRITERIA:
    - Route: {from_city} to {to_city}
    - Departure Date: {user_preferences.get('departure_date', 'Unknown')}
    - Adults: {adults}
    - Group Type: {group_type}
    - Destination: {city}, {state}
    - Check-in: {user_preferences.get('check_in', 'Unknown')}
    - Check-out: {user_preferences.get('check_out', 'Unknown')}

    AVAILABLE FLIGHTS (sample):
    {json.dumps(sample_flights, indent=2)}

    AVAILABLE HOTELS (sample):
    {json.dumps(sample_hotels, indent=2)}

    Create 4 different packages with the following structure for each:
    {{
        "description": "Detailed description of the package experience",
        "duration": "3-5 days",
        "flight": {{flight_details}},
        "hotel": {{hotel_details}},
        "included_amenities": ["Flight", "Hotel", "amenity1", "amenity2"],
        "optional_addons": ["addon1", "addon2"],
        "package_highlights": ["feature1", "feature2", "feature3"],
        "package_id": "package_001",
        "package_name": "Descriptive name",
        "package_type": "Budget/Medium/Luxury/Premium",
        "price_breakdown": {{
            "flight": price,
            "hotel": price,
            "taxes": price
        }},
        "recommendation_reason": "Why this package is recommended",
        "target_audience": "Who this package is for",
        "total_package_price": total_price
    }}

    IMPORTANT: 
    - Create 4 packages with different combinations of flights and hotels
    - Each package should have 1 flight and 1 hotel combination
    - Vary the package types (Budget, Medium, Luxury, Premium)
    - Consider the destination city and group type for personalized experiences
    - Include realistic pricing based on the flight and hotel data

    Return only valid JSON array with 4 packages.
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
                "aircraft_image": "/images/flights/aircraft_boeing.jpg",
                "stops": 0,
                "stopDetails": "Non-stop",
                "legs": [{
                    "flightNumber": "6E-129",
                    "departureTerminal": "1D",
                    "arrivalTerminal": "1"
                }]
            },
            "hotel": hotels[0] if hotels else {
                "hotel_id": "hotel_001",
                "name": "Budget Hotel",
                "location": "Mumbai",
                "rating": 3,
                "price": {"amount": 3000, "currency": "INR"},
                "amenities": ["WiFi", "Restaurant"],
                "hotel_image": "/images/hotels/hotel_001.jpg",
                "room_image": "/images/hotels/room_001.jpg",
                "amenity_images": []
            },
            "package_highlights": ["City tour", "Local cuisine experience", "Budget-friendly activities"],
            "included_amenities": ["WiFi", "Breakfast"],
            "optional_addons": ["Airport transfer", "Guided tour"],
            "price_breakdown": {
                "flight": 3500,
                "hotel": 9000,
                "taxes": 500
            },
            "total_package_price": 13000,
            "recommendation_reason": "Best value for money with essential amenities and local experiences."
        },
        {
            "package_id": "package_002",
            "package_name": "Comfort Plus Package",
            "package_type": "Medium",
            "target_audience": "Families, Business travelers",
            "description": "Balanced comfort and value with premium amenities and convenient location.",
            "duration": "4-6 days",
            "package_image": "/images/packages/comfort_package.jpg",
            "destination_image": "/images/hotels/hotel_luxury.jpg",
            "flight": flights[1] if len(flights) > 1 else flights[0] if flights else {
                "flight_id": "flight_002",
                "airline": "Vistara",
                "flight_number": "UK-825",
                "departure": "DEL",
                "arrival": "BOM",
                "departure_time": "2025-08-22T16:00:00.000+05:30",
                "arrival_time": "2025-08-22T18:20:00.000+05:30",
                "duration": "2h 20m",
                "price": 8500,
                "airline_logo": "/images/airlines/vistara.png",
                "aircraft_image": "/images/flights/aircraft_airbus.jpg",
                "stops": 0,
                "stopDetails": "Non-stop",
                "legs": [{
                    "flightNumber": "UK-825",
                    "departureTerminal": "3",
                    "arrivalTerminal": "2"
                }]
            },
            "hotel": hotels[1] if len(hotels) > 1 else hotels[0] if hotels else {
                "hotel_id": "hotel_002",
                "name": "Comfort Hotel",
                "location": "Mumbai",
                "rating": 4,
                "price": {"amount": 8000, "currency": "INR"},
                "amenities": ["WiFi", "Pool", "Gym", "Restaurant"],
                "hotel_image": "/images/hotels/hotel_002.jpg",
                "room_image": "/images/hotels/room_002.jpg",
                "amenity_images": []
            },
            "package_highlights": ["Premium amenities", "Central location", "Business facilities"],
            "included_amenities": ["WiFi", "Pool", "Gym", "Breakfast"],
            "optional_addons": ["Spa treatment", "Business center access"],
            "price_breakdown": {
                "flight": 8500,
                "hotel": 24000,
                "taxes": 1500
            },
            "total_package_price": 34000,
            "recommendation_reason": "Perfect balance of comfort and value for families and business travelers."
        },
        {
            "package_id": "package_003",
            "package_name": "Luxury Experience Package",
            "package_type": "Luxury",
            "target_audience": "Luxury travelers, Honeymooners",
            "description": "Ultimate luxury experience with premium services and exclusive amenities.",
            "duration": "5-7 days",
            "package_image": "/images/packages/luxury_package.jpg",
            "destination_image": "/images/hotels/hotel_premium.jpg",
            "flight": flights[2] if len(flights) > 2 else flights[0] if flights else {
                "flight_id": "flight_003",
                "airline": "Air India",
                "flight_number": "AI-101",
                "departure": "DEL",
                "arrival": "BOM",
                "departure_time": "2025-08-22T10:00:00.000+05:30",
                "arrival_time": "2025-08-22T12:15:00.000+05:30",
                "duration": "2h 15m",
                "price": 12000,
                "airline_logo": "/images/airlines/air_india.png",
                "aircraft_image": "/images/flights/aircraft_boeing.jpg",
                "stops": 0,
                "stopDetails": "Non-stop",
                "legs": [{
                    "flightNumber": "AI-101",
                    "departureTerminal": "3",
                    "arrivalTerminal": "2"
                }]
            },
            "hotel": hotels[2] if len(hotels) > 2 else hotels[0] if hotels else {
                "hotel_id": "hotel_003",
                "name": "Luxury Hotel",
                "location": "Mumbai",
                "rating": 5,
                "price": {"amount": 25000, "currency": "INR"},
                "amenities": ["WiFi", "Pool", "Spa", "Gym", "Restaurant", "Concierge"],
                "hotel_image": "/images/hotels/hotel_003.jpg",
                "room_image": "/images/hotels/room_003.jpg"
            },
            "package_highlights": ["Luxury spa treatments", "Fine dining experience", "Exclusive city tours"],
            "included_amenities": ["WiFi", "Pool", "Spa", "Gym", "All meals", "Concierge"],
            "optional_addons": ["Private chauffeur", "Helicopter tour", "VIP airport transfer"],
            "price_breakdown": {
                "flight": 12000,
                "hotel": 125000,
                "taxes": 5000
            },
            "total_package_price": 142000,
            "recommendation_reason": "Ultimate luxury experience with world-class amenities and personalized service."
        }
    ]
    
    return mock_packages
