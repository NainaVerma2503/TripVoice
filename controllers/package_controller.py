from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta

package_bp = Blueprint('package', __name__)

# Pre-computed data for ultra-fast response
PACKAGE_TYPES = [
    {"type": "BUDGET", "name": "Budget Explorer Package", "multiplier": 0.8},
    {"type": "MID_RANGE", "name": "Comfort Plus Package", "multiplier": 1.0},
    {"type": "LUXURY", "name": "Luxury Experience Package", "multiplier": 1.3},
    {"type": "PREMIUM", "name": "Premium Deluxe Package", "multiplier": 1.6},
    {"type": "ULTRA_LUXURY", "name": "Ultra Luxury Package", "multiplier": 2.0},
    {"type": "ONE_WAY_LUXURY", "name": "One-Way Luxury Package", "multiplier": 1.8}
]

# Pre-computed itineraries
ITINERARIES = {
    'beach': [
        {"day": 1, "title": "Beach Welcome", "activities": ["Check-in", "Beach", "Dinner"]},
        {"day": 2, "title": "Water Sports", "activities": ["Swimming", "Jet ski", "Lunch"]},
        {"day": 3, "title": "Island Trip", "activities": ["Boat ride", "Snorkeling", "Sunset"]},
        {"day": 4, "title": "Culture", "activities": ["Village", "Cooking", "Bonfire"]},
        {"day": 5, "title": "Farewell", "activities": ["Spa", "Shopping", "Departure"]}
    ],
    'mountain': [
        {"day": 1, "title": "Mountain Arrival", "activities": ["Check-in", "Acclimatize", "Tea"]},
        {"day": 2, "title": "Trekking", "activities": ["Trek", "Lakes", "Campfire"]},
        {"day": 3, "title": "Peak", "activities": ["Summit", "Photos", "Village"]},
        {"day": 4, "title": "Culture", "activities": ["Temple", "Cooking", "Stars"]},
        {"day": 5, "title": "Descent", "activities": ["Down", "Shopping", "Lunch"]}
    ],
    'city': [
        {"day": 1, "title": "City Arrival", "activities": ["Check-in", "Tour", "Square"]},
        {"day": 2, "title": "Culture", "activities": ["Monuments", "Markets", "Food"]},
        {"day": 3, "title": "Modern", "activities": ["Malls", "Building", "Shows"]},
        {"day": 4, "title": "Nightlife", "activities": ["Rooftop", "Lights", "Music"]},
        {"day": 5, "title": "Farewell", "activities": ["Landmarks", "Shopping", "Departure"]}
    ],
    'default': [
        {"day": 1, "title": "Welcome", "activities": ["Check-in", "Explore", "Dinner"]},
        {"day": 2, "title": "Discovery", "activities": ["Tour", "Attractions", "Food"]},
        {"day": 3, "title": "Adventure", "activities": ["Activities", "Nature", "Relax"]},
        {"day": 4, "title": "Culture", "activities": ["Sites", "Traditional", "Shopping"]},
        {"day": 5, "title": "Farewell", "activities": ["Sightseeing", "Souvenirs", "Departure"]}
    ]
}

# Pre-computed attractions
ATTRACTIONS = {
    'beach': ["Beaches", "Reefs", "Water Sports", "Cafes"],
    'mountain': ["Peaks", "Trails", "Lakes", "Adventure"],
    'city': ["Monuments", "Shopping", "Museums", "Entertainment"],
    'default': ["Landmarks", "Culture", "Nature", "Activities"]
}

# Pre-computed times
TOMORROW = datetime.now() + timedelta(days=1)
DEPARTURE_TIME = TOMORROW.replace(hour=10, minute=0, second=0, microsecond=0).strftime('%Y-%m-%dT%H:%M:%S')
ARRIVAL_TIME = TOMORROW.replace(hour=12, minute=0, second=0, microsecond=0).strftime('%Y-%m-%dT%H:%M:%S')

@package_bp.route('/api/package/create-from-search', methods=['POST'])
def create_package_from_search():
    data = request.get_json()
    if not data or not data.get('search_response') or not data.get('user_interests'):
        return jsonify({"error": "Missing required data"}), 400
    
    search_response = data['search_response']
    user_interests = data['user_interests']
    budget_constraint = data.get('budget_constraint', 100000)
    num_packages = max(data.get('num_packages', 6), 6)
    
    flights = search_response.get('flights', [])
    hotels = search_response.get('hotels', [])
    
    if not flights or not hotels:
        packages = create_minimal_packages(user_interests, budget_constraint, num_packages)
    else:
        packages = create_packages_from_backend_data(flights, hotels, user_interests, budget_constraint, num_packages)
    
    return jsonify({
        "status": "success",
        "packages": packages,
        "package_count": len(packages),
        "timestamp": datetime.now().isoformat()
    })

def create_packages_from_backend_data(flights, hotels, user_interests, budget_constraint, num_packages):
    interests_lower = user_interests.lower()
    itinerary = ITINERARIES.get('beach' if 'beach' in interests_lower else 'mountain' if 'mountain' in interests_lower else 'city' if 'city' in interests_lower else 'default')
    attractions = ATTRACTIONS.get('beach' if 'beach' in interests_lower else 'mountain' if 'mountain' in interests_lower else 'city' if 'city' in interests_lower else 'default')
    
    packages = []
    
    for i in range(num_packages):
        config = PACKAGE_TYPES[i % len(PACKAGE_TYPES)]
        flight = flights[i % len(flights)]
        hotel = hotels[i % len(hotels)]
        
        # Extract prices
        flight_price = flight.get('price', 0) if isinstance(flight.get('price'), (int, float)) else 0
        hotel_price = hotel.get('price', {}).get('amount', 0) if isinstance(hotel.get('price'), dict) else 0
        
        # Calculate package price
        adjusted_flight_price = int(flight_price * config['multiplier'])
        adjusted_hotel_price = int(hotel_price * config['multiplier'])
        total_price = int((adjusted_flight_price + adjusted_hotel_price) * 1.25)  # Simplified calculation
        
        if total_price > budget_constraint:
            total_price = budget_constraint
        
        package = {
            "packageName": config["name"],
            "packageType": config["type"],
            "totalPrice": total_price,
            "currency": "INR",
            "duration": "4 Nights / 5 Days Hotel Stay",
            "description": f"Experience {config['type'].lower()} travel with premium amenities.",
            "flightDetails": {
                "airline": flight.get('airline', 'Air India'),
                "flightNumber": flight.get('flight_number', 'AI 1234'),
                "price": {"value": adjusted_flight_price, "currency": "INR"},
                "departureAirportCode": flight.get('departure', 'DEL'),
                "departureCity": flight.get('departure', 'New Delhi'),
                "departureDateTime": flight.get('departure_time', DEPARTURE_TIME),
                "arrivalAirportCode": flight.get('arrival', 'BOM'),
                "arrivalCity": flight.get('arrival', 'Mumbai'),
                "arrivalDateTime": flight.get('arrival_time', ARRIVAL_TIME),
                "stops": flight.get('stopDetails', 'Direct'),
                "duration": flight.get('duration', '2h 0m')
            },
            "hotelDetails": {
                "name": hotel.get('name', 'Comfort Hotel'),
                "starRating": hotel.get('rating', 4),
                "price": str(adjusted_hotel_price),
                "city": hotel.get('location', 'Mumbai'),
                "amenities": ["WiFi", "Pool", "Restaurant", "Gym", "Spa", "Business Center"]
            },
            "suggestedItinerary": itinerary,
            "popularAttractions": attractions
        }
        
        packages.append(package)
    
    return packages

def create_minimal_packages(user_interests, budget_constraint, num_packages):
    interests_lower = user_interests.lower()
    itinerary = ITINERARIES.get('beach' if 'beach' in interests_lower else 'mountain' if 'mountain' in interests_lower else 'city' if 'city' in interests_lower else 'default')
    attractions = ATTRACTIONS.get('beach' if 'beach' in interests_lower else 'mountain' if 'mountain' in interests_lower else 'city' if 'city' in interests_lower else 'default')
    
    packages = []
    
    for i in range(num_packages):
        config = PACKAGE_TYPES[i % len(PACKAGE_TYPES)]
        
        # Calculate prices
        flight_price = int(5000 * config['multiplier'])
        hotel_price = int(8000 * config['multiplier'])
        total_price = int((flight_price + hotel_price) * 1.25)
        
        if total_price > budget_constraint:
            total_price = budget_constraint
        
        package = {
            "packageName": config["name"],
            "packageType": config["type"],
            "totalPrice": total_price,
            "currency": "INR",
            "duration": "4 Nights / 5 Days Hotel Stay",
            "description": f"Experience {config['type'].lower()} travel with premium amenities.",
            "flightDetails": {
                "airline": "Air India",
                "flightNumber": "AI 1234",
                "price": {"value": flight_price, "currency": "INR"},
                "departureAirportCode": "DEL",
                "departureCity": "New Delhi",
                "departureDateTime": DEPARTURE_TIME,
                "arrivalAirportCode": "BOM",
                "arrivalCity": "Mumbai",
                "arrivalDateTime": ARRIVAL_TIME,
                "stops": "Direct",
                "duration": "2h 0m"
            },
            "hotelDetails": {
                "name": "Comfort Hotel",
                "starRating": 4,
                "price": str(hotel_price),
                "city": "Mumbai",
                "amenities": ["WiFi", "Pool", "Restaurant", "Gym", "Spa", "Business Center"]
            },
            "suggestedItinerary": itinerary,
            "popularAttractions": attractions
        }
        
        packages.append(package)
    
    return packages
