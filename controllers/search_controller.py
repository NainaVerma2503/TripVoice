from flask import Blueprint, jsonify, request
from datetime import datetime
import requests
import json

search_bp = Blueprint('search', __name__)

@search_bp.route('/api/search', methods=['POST'])
def search_flights_and_hotels():
    """
    API endpoint that accepts flight and hotel search data and calls external APIs
    Expected request body format:
    {
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
            "roomAllocations": [...],
            "cityId": "32550",
            "city": "Bangalore",
            "state": "Karnataka", 
            "country": "IN",
            "checkInDate": "29/08/2025",
            "checkOutDate": "30/08/2025",
            "version": "V2"
        }
    }
    """
    try:
        # Get the request data
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'No data provided',
                'status': 'error'
            }), 400
        
        # Extract flight and hotel data
        flight_data = data.get('flight', {})
        hotel_data = data.get('hotel', {})
        
        # Call flight API
        flight_response = call_flight_api(flight_data)
        
        # Call hotel API
        hotel_response = call_hotel_api(hotel_data)
        
        # Debug: Check what we got from Cleartrip APIs
        print("🔍 DEBUG: Flight API Response Status:", flight_response.get('status_code'))
        print("🔍 DEBUG: Hotel API Response Status:", hotel_response.get('status_code'))
        
        # Transform raw Cleartrip data into desired format
        transformed_flights = transform_flight_data(flight_response)
        transformed_hotels = transform_hotel_data(hotel_response)
        
        return jsonify({
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'search_summary': {
                'from': flight_data.get('from'),
                'to': flight_data.get('to'),
                'departure_date': flight_data.get('depart_date'),
                'adults': flight_data.get('adults'),
                'total_flights_found': len(transformed_flights),
                'total_hotels_found': len(transformed_hotels)
            },
            'flights': transformed_flights,  # ← TRANSFORMED DATA (your desired format)
            'hotels': transformed_hotels     # ← TRANSFORMED DATA (your desired format)
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error',
            'timestamp': datetime.now().isoformat()
        }), 500

def call_flight_api(flight_data):
    """
    Call the flight search API with the provided data
    """
    try:
        # Build the flight API URL with query parameters
        base_url = 'https://qa2new.cleartrip.com/flight/search/v2'
        
        # Extract parameters from flight_data
        params = {
            'from': flight_data.get('from'),
            'to': flight_data.get('to'),
            'depart_date': flight_data.get('depart_date'),
            'adults': flight_data.get('adults'),
            'intl': flight_data.get('intl')
        }
        
        print(f"🔍 DEBUG: Calling Cleartrip Flight API with params: {params}")
        
        # Make the API call
        headers = {
            'accept': 'application/json'
        }
        
        response = requests.get(base_url, params=params, headers=headers, timeout=30)
        
        print(f"🔍 DEBUG: Flight API Response Status: {response.status_code}")
        print(f"🔍 DEBUG: Flight API Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            response_data = response.json()
            print(f"🔍 DEBUG: Flight API Response Data Keys: {list(response_data.keys()) if isinstance(response_data, dict) else 'Not a dict'}")
        else:
            print(f"🔍 DEBUG: Flight API Error Response: {response.text}")
        
        return {
            'status_code': response.status_code,
            'data': response.json() if response.status_code == 200 else None,
            'error': None if response.status_code == 200 else response.text
        }
        
    except requests.exceptions.RequestException as e:
        print(f"🔍 DEBUG: Flight API Request Exception: {e}")
        return {
            'status_code': None,
            'data': None,
            'error': f'Request failed: {str(e)}'
        }
    except Exception as e:
        print(f"🔍 DEBUG: Flight API Unexpected Error: {e}")
        return {
            'status_code': None,
            'data': None,
            'error': f'Unexpected error: {str(e)}'
        }

def generate_simulated_flights_for_search(flight_data):
    """Generate realistic simulated flight data for search results"""
    
    from_city = flight_data.get('from', 'DEL')
    to_city = flight_data.get('to', 'BOM')
    depart_date = flight_data.get('depart_date', '22/08/2025')
    adults = flight_data.get('adults', 1)
    
    # Different airlines for variety
    airlines = [
        {
            'name': 'Air India',
            'code': 'AI',
            'type': 'Full Service',
            'base_price': 12000
        },
        {
            'name': 'IndiGo',
            'code': '6E',
            'type': 'Low Cost',
            'base_price': 8000
        },
        {
            'name': 'Vistara',
            'code': 'UK',
            'type': 'Full Service',
            'base_price': 15000
        },
        {
            'name': 'SpiceJet',
            'code': 'SG',
            'type': 'Low Cost',
            'base_price': 7000
        },
        {
            'name': 'GoAir',
            'code': 'G8',
            'type': 'Low Cost',
            'base_price': 6500
        },
        {
            'name': 'Jet Airways',
            'code': '9W',
            'type': 'Full Service',
            'base_price': 18000
        },
        {
            'name': 'AirAsia India',
            'code': 'I5',
            'type': 'Low Cost',
            'base_price': 5500
        },
        {
            'name': 'Alliance Air',
            'code': '9I',
            'type': 'Regional',
            'base_price': 9000
        },
        {
            'name': 'TruJet',
            'code': '2T',
            'type': 'Regional',
            'base_price': 7500
        },
        {
            'name': 'Star Air',
            'code': 'S5',
            'type': 'Regional',
            'base_price': 8500
        }
    ]
    
    flights = []
    
    for i, airline in enumerate(airlines):
        # Add some price variation
        price_variation = 1 + (i * 0.15)  # 15% variation per flight
        final_price = int(airline['base_price'] * price_variation)
        
        # Generate departure and arrival times
        departure_hour = 6 + (i * 2)  # 6 AM, 8 AM, 10 AM, 12 PM, 2 PM
        arrival_hour = departure_hour + 2  # 2 hours flight duration
        
        flight = {
            'id': f"FLT_{from_city}_{to_city}_{i+1:03d}",
            'airline': airline['name'],
            'airline_code': airline['code'],
            'type': airline['type'],
            'flight_number': f"{airline['code']}{100 + i}",
            'price': {
                'amount': final_price,
                'currency': 'INR',
                'original_price': final_price + 3000,  # Show discount
                'discount': 3000
            },
            'departure': {
                'airport': f"{from_city} Airport",
                'time': f"{departure_hour:02d}:{30 + (i * 10):02d}",
                'terminal': f"T{(i % 3) + 1}",
                'city': from_city
            },
            'arrival': {
                'airport': f"{to_city} Airport",
                'time': f"{arrival_hour:02d}:{30 + (i * 10):02d}",
                'terminal': f"T{(i % 2) + 1}",
                'city': to_city
            },
            'duration': f"{2 + (i % 2)}h {15 + (i * 5)}m",
            'stops': i % 3,  # 0, 1, or 2 stops
            'cabin_class': 'Economy',
            'baggage': {
                'checked': f"{15 + (i * 2)}kg",
                'hand': f"{7 + (i % 3)}kg"
            },
            'refundable': i % 2 == 0,  # Alternate refundable
            'meal_included': airline['type'] == 'Full Service',
            'source': 'Simulated Data (Cleartrip API needs authentication)'
        }
        
        flights.append(flight)
    
    return flights

def call_hotel_api(hotel_data):
    """
    Call the hotel search API with the provided data
    """
    try:
        # Hotel API endpoint
        url = 'https://qa2new.cleartrip.com/hotel/orchestrator/v2/search'
        
        print(f"🏨 DEBUG: Calling Cleartrip Hotel API with data: {hotel_data}")
        
        # Headers for hotel API
        headers = {
            'Content-Type': 'application/json'
        }
        
        # Make the API call
        response = requests.post(url, json=hotel_data, headers=headers, timeout=30)
        
        print(f"🏨 DEBUG: Hotel API Response Status: {response.status_code}")
        print(f"🏨 DEBUG: Hotel API Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            response_data = response.json()
            print(f"🏨 DEBUG: Hotel API Response Data Keys: {list(response_data.keys()) if isinstance(response_data, dict) else 'Not a dict'}")
        else:
            print(f"🏨 DEBUG: Hotel API Error Response: {response.text}")
        
        return {
            'status_code': response.status_code,
            'data': response.json() if response.status_code == 200 else None,
            'error': None if response.status_code == 200 else response.text
        }
        
    except requests.exceptions.RequestException as e:
        print(f"🏨 DEBUG: Hotel API Request Exception: {e}")
        return {
            'status_code': None,
            'data': None,
            'error': f'Request failed: {str(e)}'
        }
    except Exception as e:
        print(f"🏨 DEBUG: Hotel API Unexpected Error: {e}")
        return {
            'status_code': None,
            'data': None,
            'error': f'Unexpected error: {str(e)}'
        }

def generate_simulated_hotels_for_search(hotel_data):
    """Generate realistic simulated hotel data for search results"""
    
    city = hotel_data.get('city', 'Mumbai')
    checkin = hotel_data.get('checkInDate', '22/08/2025')
    checkout = hotel_data.get('checkOutDate', '23/08/2025')
    
    # Different hotel types for variety
    hotel_types = [
        {
            'name': f"Grand {city} Hotel",
            'type': 'Luxury',
            'base_price': 12000,
            'rating': 4.8,
            'stars': 5
        },
        {
            'name': f"Comfort Inn {city}",
            'type': 'Business',
            'base_price': 8000,
            'rating': 4.2,
            'stars': 4
        },
        {
            'name': f"Royal {city} Palace",
            'type': 'Heritage',
            'base_price': 15000,
            'rating': 4.9,
            'stars': 5
        },
        {
            'name': f"Business {city} Center",
            'type': 'Corporate',
            'base_price': 6000,
            'rating': 3.8,
            'stars': 3
        },
        {
            'name': f"Seaside {city} Resort",
            'type': 'Resort',
            'base_price': 18000,
            'rating': 4.7,
            'stars': 5
        },
        {
            'name': f"Heritage {city} Lodge",
            'type': 'Boutique',
            'base_price': 22000,
            'rating': 4.9,
            'stars': 5
        },
        {
            'name': f"Modern {city} Suites",
            'type': 'Apartment',
            'base_price': 9500,
            'rating': 4.3,
            'stars': 4
        },
        {
            'name': f"Garden {city} Inn",
            'type': 'Eco-Friendly',
            'base_price': 11000,
            'rating': 4.5,
            'stars': 4
        },
        {
            'name': f"Executive {city} Plaza",
            'type': 'Business',
            'base_price': 13500,
            'rating': 4.6,
            'stars': 4
        },
        {
            'name': f"Luxury {city} Tower",
            'type': 'Premium',
            'base_price': 25000,
            'rating': 5.0,
            'stars': 5
        }
    ]
    
    hotels = []
    
    for i, hotel_type in enumerate(hotel_types):
        # Add some price variation
        price_variation = 1 + (i * 0.1)  # 10% variation per hotel
        final_price = int(hotel_type['base_price'] * price_variation)
        
        hotel = {
            'id': f"HOT_{city.upper()}_{i+1:03d}",
            'name': hotel_type['name'],
            'type': hotel_type['type'],
            'rating': hotel_type['rating'],
            'star_rating': hotel_type['stars'],
            'price': {
                'amount': final_price,
                'currency': 'INR',
                'per_night': True,
                'original_price': final_price + 2000,  # Show discount
                'discount': 2000
            },
            'location': {
                'address': f"Main Street, {city}",
                'city': city,
                'state': hotel_data.get('state', 'Maharashtra'),
                'country': hotel_data.get('country', 'IN'),
                'landmarks': ['City Center', 'Shopping Mall', 'Metro Station'],
                'distance_from_airport': f"{5 + i} km"
            },
            'amenities': [
                'WiFi', 'AC', 'Restaurant', 'Room Service', 'Gym',
                'Swimming Pool', 'Spa', 'Business Center'
            ],
            'images': [
                f"https://example.com/hotels/{city.lower()}_{i+1}_1.jpg",
                f"https://example.com/hotels/{city.lower()}_{i+1}_2.jpg"
            ],
            'description': f"Beautiful {hotel_type['type'].lower()} hotel in the heart of {city}",
            'cancellation_policy': 'Free cancellation until 24 hours before check-in',
            'checkin_time': '14:00',
            'checkout_time': '11:00',
            'source': 'Simulated Data (Cleartrip API returning 400)'
        }
        
        hotels.append(hotel)
    
    return hotels

@search_bp.route('/api/flight/search', methods=['POST'])
def search_flights_only():
    """
    API endpoint for flight search only
    """
    try:
        flight_data = request.get_json()
        
        if not flight_data:
            return jsonify({
                'error': 'No flight data provided',
                'status': 'error'
            }), 400
        
        flight_response = call_flight_api(flight_data)
        
        return jsonify({
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'flight_response': flight_response
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error',
            'timestamp': datetime.now().isoformat()
        }), 500

@search_bp.route('/api/hotel/search', methods=['POST'])
def search_hotels_only():
    """
    API endpoint for hotel search only
    """
    try:
        hotel_data = request.get_json()
        
        if not hotel_data:
            return jsonify({
                'error': 'No hotel data provided',
                'status': 'error'
            }), 400
        
        hotel_response = call_hotel_api(hotel_data)
        
        return jsonify({
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'hotel_response': hotel_response
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error',
            'timestamp': datetime.now().isoformat()
        }), 500

# def process_flight_response(flight_response):
#     """Extract only important fields from Cleartrip flight response"""
#     try:
#         if not flight_response or flight_response.get('status_code') != 200:
#             return []
#
#         raw_data = flight_response.get('data', {})
#         cleaned_flights = []
#
#         # Extract flights from Cleartrip response structure
#         # This structure may vary - adjust based on actual Cleartrip response
#         flights = raw_data.get('flights', []) or raw_data.get('data', []) or []
#
#         for flight in flights[:10]:  # Limit to top 10 flights
#             cleaned_flight = {
#                 'id': flight.get('id', flight.get('flightId', '')),
#                 'airline': flight.get('airline', {}).get('name', flight.get('airlineName', '')),
#                 'flight_number': flight.get('flightNumber', flight.get('flightNo', '')),
#                 'price': {
#                     'amount': flight.get('price', {}).get('amount', flight.get('fare', 0)),
#                     'currency': flight.get('price', {}).get('currency', 'INR')
#                 },
#                 'departure': {
#                     'airport': flight.get('departure', {}).get('airport', flight.get('from', '')),
#                     'time': flight.get('departure', {}).get('time', flight.get('departureTime', '')),
#                     'terminal': flight.get('departure', {}).get('terminal', '')
#                 },
#                 'arrival': {
#                     'airport': flight.get('arrival', {}).get('airport', flight.get('to', '')),
#                     'time': flight.get('arrival', {}).get('time', flight.get('arrivalTime', '')),
#                     'terminal': flight.get('arrival', {}).get('terminal', '')
#                 },
#                 'duration': flight.get('duration', ''),
#                 'stops': flight.get('stops', flight.get('stopCount', 0)),
#                 'cabin_class': flight.get('cabinClass', 'Economy'),
#                 'baggage': {
#                     'checked': flight.get('baggage', {}).get('checked', '15kg'),
#                     'hand': flight.get('baggage', {}).get('hand', '7kg')
#                 },
#                 'refundable': flight.get('refundable', False),
#                 'source': 'Cleartrip API'
#             }
#             cleaned_flights.append(cleaned_flight)
#
#         return cleaned_flights
#
#     except Exception as e:
#         print(f"Error processing flight response: {e}")
#         return []

import re

import re
from datetime import datetime

def format_duration_from_dict(duration_dict):
    """Converts a duration dictionary to a human-readable format."""
    if not isinstance(duration_dict, dict):
        return "N/A"
    hours = duration_dict.get('hh', 0)
    minutes = duration_dict.get('mm', 0)
    return f"{int(hours)}h {int(minutes)}m"

def format_duration(duration_minutes):
    """Converts duration in minutes to a human-readable format."""
    if not isinstance(duration_minutes, (int, float)):
        return "N/A"
    hours = duration_minutes // 60
    minutes = duration_minutes % 60
    return f"{int(hours)}h {int(minutes)}m"

def transform_flight_data(flight_response):
    """
    Transforms raw flight data by checking multiple possible API response structures
    and returns a list of transformed flights.
    """
    transformed_flights = []
    try:
        if not flight_response or flight_response.get('status_code') != 200:
            print("❌ Flight response empty ya failed hai.")
            return []

        raw_data = flight_response.get('data', {})

        # -- Structure 1: Check the 'cards' section (newest format) --
        # This structure has most details together under a 'summary' key
        cards_data = raw_data.get('cards', {}).get('J1', [])
        if cards_data:
            print("✅ 'cards' structure se flight data mila.")
            for flight_card in cards_data:
                summary = flight_card.get('summary', {})
                first_departure = summary.get('firstDeparture', {}).get('airport', {})
                last_arrival = summary.get('lastArrival', {}).get('airport', {})

                transformed_flight = {
                    'id': flight_card.get('travelOptionId', 'N/A'),
                    'airline': summary.get('firstDeparture', {}).get('airlineCode', 'N/A'),
                    'departureAirport': first_departure.get('code', 'N/A'),
                    'departureTime': first_departure.get('time', 'N/A'),
                    'arrivalAirport': last_arrival.get('code', 'N/A'),
                    'arrivalTime': last_arrival.get('time', 'N/A'),
                    'totalDuration': format_duration_from_dict(summary.get('totalDuration', {})),
                    'stops': summary.get('stops', 0),
                    'legs': summary.get('flights', []),
                    'price': flight_card.get('price', {}).get('amount', 'N/A')
                }
                transformed_flights.append(transformed_flight)
            return transformed_flights

        # -- Structure 2: Fallback to 'flights' and 'fares' maps (older format) --
        # This structure requires joining two dictionaries
        flights_map = raw_data.get('flights', {})
        fares_map = raw_data.get('fares', {})

        if flights_map and fares_map:
            print("✅ 'flights' aur 'fares' map se data mila.")
            for fare_id, fare_data in fares_map.items():
                fare_pricing = fare_data.get('pricing', {})
                flight_ids_list = fare_data.get('travelOptionIds', [])

                flight_legs = []
                for flight_id in flight_ids_list:
                    flight_legs.append(flights_map.get(flight_id, {}))

                if flight_legs:
                    first_leg = flight_legs[0]
                    last_leg = flight_legs[-1]

                    transformed_flight = {
                        'id': fare_id,
                        'airline': first_leg.get('airlineCode', 'N/A'),
                        'departureAirport': first_leg.get('from', 'N/A'),
                        'departureTime': first_leg.get('depTime', 'N/A'),
                        'arrivalAirport': last_leg.get('to', 'N/A'),
                        'arrivalTime': last_leg.get('arrTime', 'N/A'),
                        'totalDuration': format_duration(fare_data.get('duration', 0)),
                        'stops': len(flight_legs) - 1,
                        'legs': flight_legs,
                        'price': fare_pricing.get('fare', 0)
                    }
                    transformed_flights.append(transformed_flight)
            return transformed_flights

    except Exception as e:
        print(f"Error transforming flight data: {e}")

    return []

# def process_hotel_response(hotel_response):
#     """Extract only important fields from Cleartrip hotel response"""
#     try:
#         if not hotel_response or hotel_response.get('status_code') != 200:
#             return []
#
#         raw_data = hotel_response.get('data', {})
#         cleaned_hotels = []
#
#         # Extract hotels from Cleartrip response structure
#         # This structure may vary - adjust based on actual Cleartrip response
#         hotels = raw_data.get('hotels', []) or raw_data.get('data', []) or []
#
#         for hotel in hotels[:10]:  # Limit to top 10 hotels
#             cleaned_hotel = {
#                 'id': hotel.get('id', hotel.get('hotelId', '')),
#                 'name': hotel.get('name', hotel.get('hotelName', '')),
#                 'rating': hotel.get('rating', hotel.get('userRating', 0)),
#                 'star_rating': hotel.get('starRating', hotel.get('stars', 0)),
#                 'price': {
#                     'amount': hotel.get('price', {}).get('amount', hotel.get('fare', 0)),
#                     'currency': hotel.get('price', {}).get('currency', 'INR'),
#                     'per_night': True
#                 },
#                 'location': {
#                     'address': hotel.get('address', ''),
#                     'city': hotel.get('city', ''),
#                     'landmarks': hotel.get('landmarks', [])
#                 },
#                 'amenities': hotel.get('amenities', hotel.get('facilities', [])),
#                 'images': hotel.get('images', []),
#                 'description': hotel.get('description', ''),
#                 'cancellation_policy': hotel.get('cancellationPolicy', ''),
#                 'source': 'Cleartrip API'
#             }
#             cleaned_hotels.append(cleaned_hotel)
#
#         return cleaned_hotels
#
#     except Exception as e:
#         print(f"Error processing hotel response: {e}")
#         return []

import json

import json

def find_hotel_list_recursively(data):
    """
    Recursively searches for a list of hotels.
    Returns the first list of dictionaries found where each dict
    contains a key named 'hotelInfo'.
    """
    if isinstance(data, list) and data:
        if isinstance(data[0], dict) and 'hotelInfo' in data[0]:
            return data
        for item in data:
            result = find_hotel_list_recursively(item)
            if result is not None:
                return result
    elif isinstance(data, dict):
        for value in data.values():
            result = find_hotel_list_recursively(value)
            if result is not None:
                return result
    return None

def transform_hotel_data(hotel_response):
    """
    Transforms raw Cleartrip hotel data into desired format.
    Ismein price ko dhoondhne ke liye robust logic daala gaya hai.
    """
    transformed_hotels = []
    try:
        if not hotel_response or hotel_response.get('status_code') != 200:
            print("❌ Hotel response empty ya failed hai.")
            return []

        raw_data = hotel_response.get('data', {})
        hotel_list = find_hotel_list_recursively(raw_data)

        if hotel_list and isinstance(hotel_list, list):
            print(f"✅ Found a list of hotels with {len(hotel_list)} items.")
            for hotel in hotel_list:
                if isinstance(hotel, dict) and 'hotelInfo' in hotel:
                    hotel_info = hotel['hotelInfo']

                    # --- Naya Logic: Price ko alag-alag jagah dhoondhna ---
                    price = 'N/A' # Default value

                    # Method 1: Dhoondho 'rooms' ke andar
                    rooms = hotel.get('rooms', [])
                    if rooms and isinstance(rooms, list):
                        first_room = rooms[0]
                        rates = first_room.get('rates', [])
                        if rates and isinstance(rates, list):
                            first_rate = rates[0]
                            price = first_rate.get('pricing', {}).get('totalFare', 'N/A')

                    # Method 2: Dhoondho 'priceText' key mein
                    if price == 'N/A':
                        price_text_data = hotel.get('priceText', {}).get('data', {})
                        if price_text_data.get('text', '').replace('Sold out', '').strip():
                            price = price_text_data['text']

                    # Method 3: Seedhe 'price' key mein dhoondho
                    if price == 'N/A':
                        price = hotel.get('price', 'N/A')
                    # ----------------------------------------

                    transformed_hotel = {
                        'id': hotel_info.get('id', 'N/A'),
                        'name': hotel_info.get('name', 'N/A'),
                        'starRating': hotel_info.get('starRating', 0),
                        'city': hotel_info.get('cityName', 'N/A'),
                        'address': hotel_info.get('address', 'N/A'),
                        'images': [img.get('url') for img in hotel_info.get('images', [])],
                        'amenities': [amenity.get('name') for amenity in hotel_info.get('amenities', [])],
                        'price': price
                    }
                    transformed_hotels.append(transformed_hotel)
        else:
            print("❌ Hotel list expected format mein nahi mila.")

    except Exception as e:
        print(f"Error transforming hotel data: {e}")

    return transformed_hotels

@search_bp.route('/api/package/create', methods=['POST'])
def create_package_from_search():
    """Create travel package from selected flight and hotel"""
    try:
        data = request.get_json() or {}
        
        # Extract selected items
        selected_flight = data.get('selected_flight', {})
        selected_hotel = data.get('selected_hotel', {})
        package_info = data.get('package_info', {})
        
        # Validate required fields
        if not selected_flight or not selected_hotel:
            return jsonify({
                'success': False,
                'error': 'Both selected_flight and selected_hotel are required',
                'timestamp': datetime.now().isoformat()
            }), 400
        
        # Generate package ID
        package_id = f"PKG_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Calculate pricing
        flight_price = selected_flight.get('price', {}).get('amount', 0)
        hotel_price = selected_hotel.get('price', {}).get('amount', 0)
        total_cost = flight_price + hotel_price
        package_discount = int(total_cost * 0.15)  # 15% package discount
        final_price = total_cost - package_discount
        
        # Create complete package
        travel_package = {
            'package_id': package_id,
            'package_type': 'Flight + Hotel Package',
            'status': 'created',
            'created_at': datetime.now().isoformat(),
            'validity': '30 days',
            
            'package_info': {
                'from': package_info.get('from', ''),
                'to': package_info.get('to', ''),
                'departure_date': package_info.get('departure_date', ''),
                'return_date': package_info.get('return_date', ''),
                'adults': package_info.get('adults', 1),
                'children': package_info.get('children', 0),
                'cabin_class': package_info.get('cabin_class', 'Economy'),
                'hotel_checkin': package_info.get('hotel_checkin', ''),
                'hotel_checkout': package_info.get('hotel_checkout', ''),
                'hotel_guests': package_info.get('hotel_guests', 1)
            },
            
            'selected_flight': selected_flight,
            'selected_hotel': selected_hotel,
            
            'pricing': {
                'flight_price': flight_price,
                'hotel_price': hotel_price,
                'subtotal': total_cost,
                'package_discount': package_discount,
                'final_price': final_price,
                'currency': 'INR',
                'savings_percentage': 15
            },
            
            'package_includes': [
                'Round-trip flights',
                'Hotel accommodation',
                'Airport transfers',
                'Travel insurance',
                '24/7 customer support',
                'Free cancellation (until 24h before)',
                'Package discount'
            ],
            
            'next_steps': [
                'Review package details',
                'Add passenger information',
                'Make payment',
                'Receive confirmation',
                'Download tickets and vouchers'
            ]
        }
        
        return jsonify({
            'success': True,
            'message': 'Travel package created successfully!',
            'travel_package': travel_package,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

import re

def transform_flight_data(flight_response):
    transformed_flights = []
    try:
        raw_data = flight_response.get('data', {})
        flights_map = raw_data.get('flights', {})
        fares_map = raw_data.get('fares', {})

        if not flights_map or not fares_map:
            return []

        print(f"✅ Found {len(flights_map)} flights and {len(fares_map)} fares.")

        # Regex pattern to capture the flight segments string
        # This looks for content between '~' and the next '__'
        pattern = re.compile(r'~([^__]+)__')

        for fare_id, fare_data in fares_map.items():
            fare_pricing = fare_data.get('pricing', {})
            flight_legs = []

            # Use the regex pattern to find the flight segment string
            match = pattern.search(fare_id)
            if not match:
                print(f"⚠️ Fare {fare_id} does not match expected flight string format. Skipping.")
                continue

            flight_details_str = match.group(1)
            leg_details = flight_details_str.split(':')

            for leg in leg_details:
                parts = leg.split('^')
                if len(parts) >= 4:
                    flight_legs.append({
                        'from': parts[0],
                        'to': parts[1],
                        'airlineCode': parts[2],
                        'fltNo': parts[3]
                    })

            if flight_legs:
                first_leg = flight_legs[0]
                last_leg = flight_legs[-1]

                transformed_flight = {
                    'id': fare_id,
                    'airline': get_airline_name(first_leg.get('airlineCode', '')),
                    'departureAirport': first_leg.get('from', ''),
                    'departureTime': 'N/A', # Time is not in the fare_id string
                    'arrivalAirport': last_leg.get('to', ''),
                    'arrivalTime': 'N/A', # Time is not in the fare_id string
                    'totalDuration': format_duration(fare_data.get('duration', 0)),
                    'stops': len(flight_legs) - 1,
                    'legs': format_legs(flight_legs),
                    'price': fare_pricing.get('fare', 0)
                }
                transformed_flights.append(transformed_flight)
    except Exception as e:
        print(f"Error transforming flight data: {e}")

    print(f"✅ Final number of transformed flights: {len(transformed_flights)}")
    return transformed_flights


import json

def transform_hotel_data(hotel_response):
    transformed_hotels = []
    try:
        raw_data = hotel_response.get('data', {})
        response_data = raw_data.get('response', {})

        # The hotel list is in a key named 'slotsData' at the top level of the response
        if 'slotsData' in response_data and isinstance(response_data['slotsData'], list):
            all_slots = response_data['slotsData']

            # Iterate through all slots to find the ones that contain hotel card data
            for slot in all_slots:
                slot_data = slot.get('slotData', {})
                if slot_data.get('type') == 'UNIFIED_HOTEL_CARD':
                    hotel_card_data = slot_data.get('data', {})

                    # Extract the hotelInfo, which is now at the top level of this data object
                    name_data = hotel_card_data.get('name', {}).get('data', {})
                    rating_data = hotel_card_data.get('starRating', {}).get('data', {})
                    description_data = hotel_card_data.get('description', {}).get('data', {})

                    transformed_hotel = {
                        'id': slot_data.get('eventData', {}).get('h_hotel_id', 'N/A'),
                        'name': name_data.get('text', 'N/A'),
                        'starRating': rating_data.get('rating', 0),
                        'city': description_data.get('text', '').replace('Hotel in ', '').replace('Resort in ', ''),
                        'address': 'N/A', # The address is not available in the provided sample
                        'images': [item.get('data', {}).get('url') for item in hotel_card_data.get('carouselData', []) if item.get('type') == 'IMAGE'],
                        'amenities': [] # The amenities list isn't directly available in this specific card
                    }
                    transformed_hotels.append(transformed_hotel)
        else:
            print("❌ 'slotsData' key not found or is not a list at the expected path.")

    except Exception as e:
        print(f"Error transforming hotel data: {e}")

    print(f"✅ Final number of transformed hotels: {len(transformed_hotels)}")
    return transformed_hotels


def get_airline_name(airline_code):
    """Convert airline code to full name"""
    airline_names = {
        '6E': 'IndiGo',
        'AI': 'Air India',
        'UK': 'Vistara',
        'SG': 'SpiceJet',
        'G8': 'GoAir',
        '9W': 'Jet Airways'
    }
    return airline_names.get(airline_code, airline_code)

def format_duration(duration):
    """Format duration from {hh: X, mm: Y} to 'Xh Ym'"""
    try:
        hours = duration.get('hh', 0)
        minutes = duration.get('mm', 0)
        if hours > 0 and minutes > 0:
            return f"{hours}h {minutes}m"
        elif hours > 0:
            return f"{hours}h"
        elif minutes > 0:
            return f"{minutes}m"
        else:
            return "0h 0m"
    except:
        return "0h 0m"

def format_stop_details(stops):
    """Format stop details"""
    if not stops:
        return "Direct flight"
    elif len(stops) == 1:
        return f"1 stop"
    else:
        return f"{len(stops)} stops"

def format_legs(flight_details):
    """Format flight legs"""
    try:
        # For now, create a simple leg structure
        # You can enhance this based on actual Cleartrip data structure
        return [
            {
                'flightNumber': flight_details.get('fltNo', ''),
                'departureTerminal': flight_details.get('departure', {}).get('airport', {}).get('terminal', {}).get('name', ''),
                'arrivalTerminal': flight_details.get('arrival', {}).get('airport', {}).get('terminal', {}).get('name', '')
            }
        ]
    except:
        return []

def extract_flight_info_from_fare_id(fare_id, fare_data):
    """Extract flight information from Cleartrip fare ID and data"""
    try:
        # Example fare_id: "REGULAR__DEL|BOM|1755801000000|1|0|0|ECONOMY|IN||||REGULAR|production_IN_book_indigo_newskies_1430772_new_url~DEL^BOM^6E^449__INDIGO__C0IP__R__RETAIL__REGULAR__false__DOMESTIC"
        
        # Split fare_id to extract flight details
        parts = fare_id.split('|')
        if len(parts) < 7:
            return None
            
        # Extract basic route info
        route_info = parts[1].split('|')[0] if '|' in parts[1] else parts[1]  # DEL|BOM
        if '|' in route_info:
            from_airport, to_airport = route_info.split('|')[:2]
        else:
            return None
            
        # Look for flight details in the fare_id
        flight_details = {}
        
        # Try to extract airline and flight number from the detailed part
        if '~' in fare_id:
            flight_part = fare_id.split('~')[1] if len(fare_id.split('~')) > 1 else ''
            if '^' in flight_part:
                flight_segments = flight_part.split('^')
                if len(flight_segments) >= 4:
                    # Format: DEL^BOM^6E^449
                    flight_details['departureAirport'] = flight_segments[0]
                    flight_details['arrivalAirport'] = flight_segments[1] 
                    flight_details['airlineCode'] = flight_segments[2]
                    flight_details['flightNumber'] = flight_segments[3].split('__')[0]
        
        # If we couldn't extract from fare_id, use the parts we have
        if not flight_details.get('departureAirport'):
            flight_details['departureAirport'] = from_airport
            flight_details['arrivalAirport'] = to_airport
            
        # Extract pricing information
        pricing_info = fare_data.get('pricing', {}).get('totalPricing', {})
        flight_details['price'] = pricing_info.get('totalPrice', 0)
        flight_details['currency'] = 'INR'
        
        # Extract brand/fare type
        flight_details['fareType'] = fare_data.get('displayText', {}).get('displayTitle', '')
        
        # Add unique ID
        flight_details['id'] = fare_id
        
        # Add default values for missing fields
        flight_details['departureTime'] = f"2025-08-22T{6 + len(flight_details['id']) % 12:02d}:00:00.000+05:30"
        flight_details['arrivalTime'] = f"2025-08-22T{8 + len(flight_details['id']) % 12:02d}:00:00.000+05:30"
        flight_details['duration'] = {'hh': 2, 'mm': 0}
        flight_details['stops'] = []
        
        return flight_details
    
    except Exception as e:
        print(f"Error extracting flight info from fare_id: {e}")
        return None
