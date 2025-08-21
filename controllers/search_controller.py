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
            'flights': transformed_flights,
            'hotels': transformed_hotels,
            'original_flight_data': flight_data  # Pass through the original flight data including departure date
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
        print(f"🔍 DEBUG: Flight data received: {flight_data}")

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

            # Add detailed debugging for the response structure
            if isinstance(response_data, dict):
                print(f"🔍 DEBUG: Response has 'data' key: {'data' in response_data}")
                if 'data' in response_data:
                    data = response_data['data']
                    print(f"🔍 DEBUG: Data keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")

                    if isinstance(data, dict):
                        print(f"🔍 DEBUG: Has 'flights': {'flights' in data}")
                        print(f"🔍 DEBUG: Has 'subTravelOptions': {'subTravelOptions' in data}")
                        print(f"🔍 DEBUG: Has 'fares': {'fares' in data}")

                        # Show sample of first few items
                        if 'flights' in data and isinstance(data['flights'], dict):
                            flight_keys = list(data['flights'].keys())[:3]
                            print(f"🔍 DEBUG: Sample flight keys: {flight_keys}")
                            if flight_keys:
                                sample_flight = data['flights'][flight_keys[0]]
                                print(f"🔍 DEBUG: Sample flight structure: {list(sample_flight.keys()) if isinstance(sample_flight, dict) else 'Not a dict'}")

                        if 'subTravelOptions' in data and isinstance(data['subTravelOptions'], dict):
                            option_keys = list(data['subTravelOptions'].keys())[:3]
                            print(f"🔍 DEBUG: Sample travel option keys: {option_keys}")
                            if option_keys:
                                sample_option = data['subTravelOptions'][option_keys[0]]
                                print(f"🔍 DEBUG: Sample travel option structure: {list(sample_option.keys()) if isinstance(sample_option, dict) else 'Not a dict'}")
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

from datetime import datetime

def format_duration(duration_minutes):
    """Converts duration in minutes to a human-readable format."""
    if not isinstance(duration_minutes, (int, float)):
        return "N/A"
    hours = duration_minutes // 60
    minutes = duration_minutes % 60
    return f"{int(hours)}h {int(minutes)}m"

def transform_flight_data(flight_response):
    """
    Transforms raw flight data from Cleartrip API response.
    The actual structure has 'cards', 'subTravelOptions', 'flights', and 'fares'.
    """
    transformed_flights = []
    try:
        if not flight_response or flight_response.get('status_code') != 200:
            print("❌ Flight response empty ya failed hai.")
            return []

        # The actual Cleartrip API structure - data is at the top level, not nested under 'data'
        raw_data = flight_response.get('data', flight_response)
        cards = raw_data.get('cards', {})
        sub_travel_options = raw_data.get('subTravelOptions', {})
        flights_map = raw_data.get('flights', {})
        fares_map = raw_data.get('fares', {})

        print(f"🔍 DEBUG: Raw data keys: {list(raw_data.keys())}")
        print(f"🔍 DEBUG: Cards count: {len(cards.get('J1', [])) if cards.get('J1') else 'Not found'}")
        print(f"🔍 DEBUG: Fares count: {len(fares_map) if isinstance(fares_map, dict) else 'Not a dict'}")
        print(f"🔍 DEBUG: Sample fare keys: {list(fares_map.keys())[:3] if isinstance(fares_map, dict) and fares_map else 'No fares'}")

        if not cards or 'J1' not in cards:
            print("❌ Cards data API response mein nahi mila.")
            return []

        # Iterate through each card (flight option)
        for card in cards.get('J1', []):
            try:
                travel_option_id = card.get('travelOptionId', '')
                summary = card.get('summary', {})

                if not summary:
                    continue

                # Extract flight information from summary
                first_departure = summary.get('firstDeparture', {})
                last_arrival = summary.get('lastArrival', {})
                total_duration = summary.get('totalDuration', {})
                stops = summary.get('stops', 0)

                # Get airline code from flights array
                airline_code = 'N/A'
                flights_summary = summary.get('flights', [])
                if flights_summary:
                    airline_code = flights_summary[0].get('airlineCode', 'N/A')

                # Get price from fares (if available)
                price = 'N/A'

                # The travel_option_id doesn't directly match fare keys, so we need to search for it
                # The fare keys contain flight info after the '~' symbol
                matching_fare_key = None

                # Simple fare matching logic
                for fare_key in fares_map.keys():
                    if '~' in fare_key:
                        # Extract the flight part after '~'
                        flight_part = fare_key.split('~')[1] if len(fare_key.split('~')) > 1 else ''

                        # Parse travel_option_id components
                        try:
                            travel_parts = travel_option_id.split('-')
                            airline_code = travel_parts[0]  # 6E
                            flight_number = travel_parts[1]  # 2766
                            from_airport = travel_parts[2]  # DEL
                            to_airport = travel_parts[3]  # BOM

                            # Check if our travel_option_id components are in the flight part
                            if (airline_code in flight_part and
                                    flight_number in flight_part and
                                    from_airport in flight_part and
                                    to_airport in flight_part):
                                matching_fare_key = fare_key
                                break
                        except IndexError:
                            continue

                if matching_fare_key:
                    fare_data = fares_map[matching_fare_key]
                    if 'pricing' in fare_data:
                        pricing = fare_data['pricing']
                        if 'totalPricing' in pricing:
                            total_pricing = pricing['totalPricing']
                            price = total_pricing.get('totalPrice', 'N/A')

                # Format departure and arrival times
                departure_time = 'N/A'
                if first_departure and 'airport' in first_departure and 'time' in first_departure['airport']:
                    departure_time = first_departure['airport']['time']

                arrival_time = 'N/A'
                if last_arrival and 'airport' in last_arrival and 'time' in last_arrival['airport']:
                    arrival_time = last_arrival['airport']['time']

                # Format duration
                duration_text = 'N/A'
                if total_duration:
                    hours = total_duration.get('hh', 0)
                    minutes = total_duration.get('mm', 0)
                    if hours or minutes:
                        duration_text = f"{hours}h {minutes}m"

                # Get detailed flight legs
                flight_legs = []
                if travel_option_id in sub_travel_options:
                    sub_option = sub_travel_options[travel_option_id]
                    if 'sequenceToFlightIdMap' in sub_option:
                        sequence_map = sub_option['sequenceToFlightIdMap']
                        for sequence, flight_id in sorted(sequence_map.items()):
                            if flight_id in flights_map:
                                flight_legs.append(flights_map[flight_id])

                # Create transformed flight object
                transformed_flight = {
                    'id': travel_option_id,
                    'airline': airline_code,
                    'departureAirport': first_departure.get('airport', {}).get('code', 'N/A'),
                    'departureTime': departure_time,
                    'arrivalAirport': last_arrival.get('airport', {}).get('code', 'N/A'),
                    'arrivalTime': arrival_time,
                    'totalDuration': duration_text,
                    'stops': stops,
                    'legs': flight_legs,
                    'price': price
                }

                transformed_flights.append(transformed_flight)

            except Exception as e:
                print(f"Error processing card {card.get('cardId', 'unknown')}: {e}")
                continue

    except Exception as e:
        print(f"Error transforming flight data: {e}")

    return transformed_flights

def find_hotel_list_recursively(data):
    """
    Recursively searches for a list of hotels in the API response.
    Returns the first list of dictionaries found where each dict
    contains a key named 'slotData' with a 'UNIFIED_HOTEL_CARD' type.
    """
    if isinstance(data, list) and data:
        # Check if this list contains hotel card data
        if isinstance(data[0], dict) and data[0].get('slotData', {}).get('type') == 'UNIFIED_HOTEL_CARD':
            return data
        # If not, search recursively within each item of the list
        for item in data:
            result = find_hotel_list_recursively(item)
            if result is not None:
                return result
    elif isinstance(data, dict):
        # Search recursively within each value of the dictionary
        for value in data.values():
            result = find_hotel_list_recursively(value)
            if result is not None:
                return result
    return None

def transform_hotel_data(hotel_response):
    """
    Transforms raw Cleartrip hotel data into desired format.
    Includes robust logic to find the price and amenities.
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
            for hotel_card in hotel_list:
                slot_data = hotel_card.get('slotData', {})
                hotel_info_data = slot_data.get('data', {})

                # --- Price ko dhoondhne ka naya, robust logic ---
                price = 'N/A' # Default value

                # Method 1: Check for price in eventData (sabse reliable)
                price_from_event = slot_data.get('eventData', {}).get('h_total_amount')
                if price_from_event is not None and price_from_event > 0:
                    price = price_from_event

                # Method 2: Check for 'priceText' in the card itself
                elif hotel_info_data.get('priceText', {}).get('data', {}).get('text'):
                    price_text = hotel_info_data['priceText']['data']['text']
                    if price_text.lower() == 'sold out':
                        price = 'Sold out'
                    else:
                        # Clean up the price string (e.g., "₹5,500" -> "5500")
                        price = price_text.replace('₹', '').replace(',', '').strip()

                # --- Amenities ko dhoondhne ka logic ---
                amenities = []
                # 'highlights' list mein amenities ho sakte hain
                highlights = hotel_info_data.get('highlights', [])
                if highlights:
                    amenities.extend([h.get('text') for h in highlights if h.get('text')])

                # 'amenities' key in hotelInfo
                hotel_info = hotel_info_data.get('hotelInfo', {})
                if hotel_info and hotel_info.get('amenities'):
                    amenities.extend([a.get('name') for a in hotel_info['amenities'] if a.get('name')])

                # Ensure unique amenities
                amenities = list(set(amenities))

                transformed_hotel = {
                    'id': slot_data.get('eventData', {}).get('h_hotel_id', 'N/A'),
                    'name': hotel_info_data.get('name', {}).get('data', {}).get('text', 'N/A'),
                    'starRating': hotel_info_data.get('starRating', {}).get('data', {}).get('rating', 0),
                    'city': slot_data.get('eventData', {}).get('h_search_destination_city', 'N/A'),
                    'address': hotel_info_data.get('description', {}).get('data', {}).get('text', 'N/A'),
                    'images': [item.get('data', {}).get('url') for item in hotel_info_data.get('carouselData', []) if item.get('type') == 'IMAGE'],
                    'amenities': amenities,
                    'price': price,
                    'isSoldOut': slot_data.get('hotelSoldOut', False)
                }
                transformed_hotels.append(transformed_hotel)
        else:
            print("❌ Hotel list expected format mein nahi mila.")

    except Exception as e:
        print(f"Error transforming hotel data: {e}")

    return transformed_hotels
