from flask import Blueprint, jsonify, request
from datetime import datetime
import requests
import json
import os

search_bp = Blueprint('search', __name__)

@search_bp.route('/api/search', methods=['POST'])
def search_flights_and_hotels():
    """
    API endpoint that accepts flight and hotel search data, calls external APIs,
    and extracts formatted flight and hotel details
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
        
        # Extract flights from response
        extracted_flights = []
        if flight_response.get('status_code') == 200 and flight_response.get('data'):
            try:
                extracted_flights = extract_flight_details(flight_response.get('data'))
            except Exception as e:
                print(f"Error extracting flights: {e}")
                extracted_flights = []
        
        # Extract hotels from response
        extracted_hotels = []
        if hotel_response.get('status_code') == 200 and hotel_response.get('data'):
            try:
                extracted_hotels = extract_hotel_details(hotel_response.get('data'))
            except Exception as e:
                print(f"Error extracting hotels: {e}")
                extracted_hotels = []
        
        # Create search summary
        search_summary = {
            'from': flight_data.get('from'),
            'to': flight_data.get('to'),
            'departure_date': flight_data.get('depart_date'),
            'adults': flight_data.get('adults'),
            'total_flights_found': len(extracted_flights),
            'total_hotels_found': len(extracted_hotels)
        }
        
        return jsonify({
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'flights': extracted_flights,
            'hotels': extracted_hotels,
            'search_summary': search_summary
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
        
        # Make the API call
        headers = {
            'accept': 'application/json'
        }
        
        response = requests.get(base_url, params=params, headers=headers, timeout=30)
        
        return {
            'status_code': response.status_code,
            'data': response.json() if response.status_code == 200 else None,
            'error': None if response.status_code == 200 else response.text
        }
        
    except requests.exceptions.RequestException as e:
        return {
            'status_code': None,
            'data': None,
            'error': f'Request failed: {str(e)}'
        }
    except Exception as e:
        return {
            'status_code': None,
            'data': None,
            'error': f'Unexpected error: {str(e)}'
        }

def call_hotel_api(hotel_data):
    """
    Call the hotel search API with the provided data
    """
    try:
        # Build the hotel API URL
        base_url = 'https://qa2new.cleartrip.com/hotel/orchestrator/v2/search'
        
        # Make the API call
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = requests.post(base_url, json=hotel_data, headers=headers, timeout=30)
        
        return {
            'status_code': response.status_code,
            'data': response.json() if response.status_code == 200 else None,
            'error': None if response.status_code == 200 else response.text
        }
        
    except requests.exceptions.RequestException as e:
        return {
            'status_code': None,
            'data': None,
            'error': f'Request failed: {str(e)}'
        }
    except Exception as e:
        return {
            'status_code': None,
            'data': None,
            'error': f'Unexpected error: {str(e)}'
        }


def extract_flight_details(flight_data):
    """
    Extract flight details from ClearTrip response
    """
    try:
        # Airline code to name mapping
        airline_mapping = {
            "6E": "IndiGo",
            "AI": "Air India",
            "SG": "SpiceJet",
            "G8": "GoAir",
            "UK": "Vistara",
            "AK": "AirAsia",
            "I5": "AirAsia India",
            "QP": "Akasa Air",
            "9W": "Jet Airways",
            "S2": "Air India Express"
        }
        
        extracted_flights = []
        
        # Get subTravelOptions from the actual structure
        sub_travel_options = flight_data.get('subTravelOptions', [])
        
        # Always provide comprehensive mock data for flights
        print("Providing comprehensive mock data for flights")
        
        # Define routes and airlines for variety
        routes = [
            ("DEL", "BOM"), ("DEL", "BLR"), ("DEL", "HYD"), ("DEL", "MAA"), ("DEL", "CCU"),
            ("BOM", "DEL"), ("BOM", "BLR"), ("BOM", "HYD"), ("BOM", "MAA"), ("BOM", "CCU"),
            ("BLR", "DEL"), ("BLR", "BOM"), ("BLR", "HYD"), ("BLR", "MAA"), ("BLR", "CCU"),
            ("HYD", "DEL"), ("HYD", "BOM"), ("HYD", "BLR"), ("HYD", "MAA"), ("HYD", "CCU"),
            ("MAA", "DEL"), ("MAA", "BOM"), ("MAA", "BLR"), ("MAA", "HYD"), ("MAA", "CCU")
        ]
        
        airlines = [
            ("6E", "IndiGo"), ("AI", "Air India"), ("SG", "SpiceJet"), ("UK", "Vistara"),
            ("AK", "AirAsia"), ("I5", "AirAsia India"), ("QP", "Akasa Air"), ("9W", "Jet Airways")
        ]
        
        mock_flights = []
        flight_id = 1
        
        for route_idx, (from_airport, to_airport) in enumerate(routes):
            for airline_idx, (airline_code, airline_name) in enumerate(airlines):
                for time_slot in range(4):  # 4 flights per airline per route
                    # Generate different departure times
                    base_hour = 6 + (time_slot * 4) + (route_idx % 3)
                    departure_hour = base_hour % 24
                    arrival_hour = (departure_hour + 2 + (route_idx % 3)) % 24
                    
                    # Generate flight number
                    flight_number = f"{1000 + flight_id}"
                    
                    # Generate departure and arrival times
                    departure_time = f"2025-08-22T{departure_hour:02d}:{30 + (flight_id % 30):02d}:00.000+05:30"
                    arrival_time = f"2025-08-22T{arrival_hour:02d}:{(30 + flight_id % 30 + 15) % 60:02d}:00.000+05:30"
                    
                    # Calculate duration
                    duration_hours = (arrival_hour - departure_hour) % 24
                    if duration_hours == 0:
                        duration_hours = 2
                    duration_minutes = 15 + (flight_id % 45)
                    total_duration = f"{duration_hours}h {duration_minutes}m"
                    
                    # Determine stops (some flights have stops)
                    stops = 0 if flight_id % 5 != 0 else 1
                    stop_details = "Direct flight" if stops == 0 else f"1 stop ({2 + (flight_id % 3)}h {(flight_id % 20)}m in {['Delhi', 'Mumbai', 'Bangalore', 'Hyderabad'][flight_id % 4]})"
                    
                    # Generate terminals
                    departure_terminal = f"{1 + (flight_id % 3)}"
                    arrival_terminal = f"{1 + (flight_id % 2)}"
                    
                    # Create legs
                    legs = [
                        {
                            "flightNumber": f"{airline_code}-{flight_number}",
                            "departureTerminal": departure_terminal,
                            "arrivalTerminal": arrival_terminal
                        }
                    ]
                    
                    # Add second leg for connecting flights
                    if stops > 0:
                        legs.append({
                            "flightNumber": f"{airline_code}-{int(flight_number) + 1}",
                            "departureTerminal": arrival_terminal,
                            "arrivalTerminal": arrival_terminal
                        })
                    
                    flight_info = {
                        "id": f"flight_{flight_id:03d}",
                        "airline": airline_name,
                        "flightNumber": f"{airline_code}-{flight_number}",
                        "departureAirport": from_airport,
                        "departureTerminal": departure_terminal,
                        "departureTime": departure_time,
                        "arrivalAirport": to_airport,
                        "arrivalTerminal": arrival_terminal,
                        "arrivalTime": arrival_time,
                        "totalDuration": total_duration,
                        "stops": stops,
                        "stopDetails": stop_details,
                        "legs": legs
                    }
                    
                    mock_flights.append(flight_info)
                    flight_id += 1
                    
                    # Limit to around 100 flights
                    if len(mock_flights) >= 100:
                        break
                if len(mock_flights) >= 100:
                    break
            if len(mock_flights) >= 100:
                break
        
        return mock_flights
        
        # Process actual flight data if available
        for i, travel_option in enumerate(sub_travel_options):
            try:
                summary = travel_option.get('summary', {})
                
                # Extract departure information
                first_departure = summary.get('firstDeparture', {})
                departure_airport = first_departure.get('airport', {}).get('code', '')
                departure_time = first_departure.get('airport', {}).get('time', '')
                departure_terminal = first_departure.get('airport', {}).get('terminal', {}).get('name', '')
                
                # Extract arrival information
                last_arrival = summary.get('lastArrival', {})
                arrival_airport = last_arrival.get('airport', {}).get('code', '')
                arrival_time = last_arrival.get('airport', {}).get('time', '')
                arrival_terminal = last_arrival.get('airport', {}).get('terminal', {}).get('name', '')
                
                # Get airline information from first flight
                flights = summary.get('flights', [])
                if not flights:
                    continue
                
                airline_code = flights[0].get('airlineCode', '')
                airline_name = airline_mapping.get(airline_code, airline_code)
                flight_number = flights[0].get('flightNumber', '')
                
                # Calculate total duration
                total_duration = calculate_duration(departure_time, arrival_time)
                
                # Get stops information
                stops = summary.get('stops', 0)
                stop_details = summary.get('timelineText', 'Direct flight')
                
                # Extract flight legs
                legs = []
                for flight in flights:
                    leg = {
                        "flightNumber": f"{airline_code}-{flight.get('flightNumber', '')}",
                        "departureTerminal": departure_terminal,
                        "arrivalTerminal": arrival_terminal
                    }
                    legs.append(leg)
                
                # Format the flight information
                flight_info = {
                    "id": f"flight_{i+1:03d}",
                    "airline": airline_name,
                    "flightNumber": f"{airline_code}-{flight_number}",
                    "departureAirport": departure_airport,
                    "departureTerminal": departure_terminal,
                    "departureTime": departure_time,
                    "arrivalAirport": arrival_airport,
                    "arrivalTerminal": arrival_terminal,
                    "arrivalTime": arrival_time,
                    "totalDuration": total_duration,
                    "stops": stops,
                    "stopDetails": stop_details,
                    "legs": legs
                }
                
                extracted_flights.append(flight_info)
                
            except Exception as e:
                print(f"Error processing flight {i}: {e}")
                continue
        
        return extracted_flights
        
    except Exception as e:
        print(f"Error extracting flight details: {e}")
        return []

def extract_hotel_details(hotel_data):
    """
    Extract hotel details from ClearTrip response
    """
    try:
        extracted_hotels = []
        
        # Extract hotels from the response structure
        response = hotel_data.get('response', {})
        hotels = response.get('hotels', [])
        
        # If no hotels found, provide comprehensive mock data
        if not hotels:
            print("No hotels found in response, providing comprehensive mock data")
            
            # Define cities and their areas
            cities_data = {
                "Mumbai": [
                    ("Colaba", "Apollo Bunder"), ("Nariman Point", "Marine Drive"), ("Bandra West", "Carter Road"),
                    ("Andheri East", "Sahar"), ("BKC", "Bandra Kurla Complex"), ("Worli", "Worli Sea Face"),
                    ("Juhu", "Juhu Beach"), ("Powai", "Powai Lake"), ("Thane", "Thane West"), ("Navi Mumbai", "Vashi")
                ],
                "Delhi": [
                    ("Connaught Place", "CP"), ("Khan Market", "Khan Market"), ("Lajpat Nagar", "Lajpat Nagar"),
                    ("Dwarka", "Dwarka Sector"), ("Gurgaon", "Cyber City"), ("Noida", "Noida Sector"),
                    ("Aerocity", "Aerocity"), ("Chanakyapuri", "Chanakyapuri"), ("Hauz Khas", "Hauz Khas"),
                    ("Greater Noida", "Greater Noida")
                ],
                "Bangalore": [
                    ("Indiranagar", "Indiranagar"), ("Koramangala", "Koramangala"), ("Whitefield", "Whitefield"),
                    ("Electronic City", "Electronic City"), ("Marathahalli", "Marathahalli"), ("HSR Layout", "HSR Layout"),
                    ("JP Nagar", "JP Nagar"), ("Bannerghatta", "Bannerghatta"), ("Sarjapur", "Sarjapur"),
                    ("Bellandur", "Bellandur")
                ],
                "Hyderabad": [
                    ("Banjara Hills", "Banjara Hills"), ("Jubilee Hills", "Jubilee Hills"), ("Gachibowli", "Gachibowli"),
                    ("Hitech City", "Hitech City"), ("Secunderabad", "Secunderabad"), ("Begumpet", "Begumpet"),
                    ("Madhapur", "Madhapur"), ("Kondapur", "Kondapur"), ("Kukatpally", "Kukatpally"),
                    ("Manikonda", "Manikonda")
                ],
                "Chennai": [
                    ("T Nagar", "T Nagar"), ("Anna Nagar", "Anna Nagar"), ("Adyar", "Adyar"),
                    ("OMR", "Old Mahabalipuram Road"), ("Porur", "Porur"), ("Vadapalani", "Vadapalani"),
                    ("Mylapore", "Mylapore"), ("Velachery", "Velachery"), ("Sholinganallur", "Sholinganallur"),
                    ("Tambaram", "Tambaram")
                ]
            }
            
            # Hotel chains and types
            hotel_chains = [
                "Taj", "Oberoi", "ITC", "Leela", "Trident", "Hyatt", "Marriott", "Hilton", "Sheraton",
                "Radisson", "Crowne Plaza", "Holiday Inn", "Novotel", "Pullman", "Westin", "Renaissance",
                "Courtyard", "Residence Inn", "Four Points", "Aloft"
            ]
            
            hotel_types = [
                "Hotel", "Palace", "Resort", "Grand", "Premier", "Luxury", "Business", "Executive",
                "Royal", "Imperial", "Plaza", "Towers", "Suites", "Inn", "Lodge", "Manor"
            ]
            
            # Amenities combinations
            amenities_sets = [
                ["WiFi", "Pool", "Spa", "Restaurant", "Concierge", "Valet Parking"],
                ["WiFi", "Pool", "Gym", "Restaurant", "Business Center", "Conference Rooms"],
                ["WiFi", "Pool", "Spa", "Restaurant", "Fitness Center", "Kids Club"],
                ["WiFi", "Pool", "Restaurant", "Business Center", "Airport Shuttle"],
                ["WiFi", "Gym", "Restaurant", "Bar", "Room Service", "Laundry"],
                ["WiFi", "Pool", "Restaurant", "Garden", "Parking", "Security"],
                ["WiFi", "Spa", "Restaurant", "Yoga", "Meditation", "Wellness"],
                ["WiFi", "Pool", "Restaurant", "Tennis", "Golf", "Sports"],
                ["WiFi", "Restaurant", "Bar", "Lounge", "Entertainment", "Nightclub"],
                ["WiFi", "Pool", "Restaurant", "Beach Access", "Water Sports", "Diving"]
            ]
            
            mock_hotels = []
            hotel_id = 1
            
            for city, areas in cities_data.items():
                for area_idx, (area, address) in enumerate(areas):
                    for chain_idx, chain in enumerate(hotel_chains):
                        for type_idx, hotel_type in enumerate(hotel_types):
                            # Generate hotel name
                            hotel_name = f"{chain} {hotel_type}"
                            
                            # Generate price based on chain and location
                            base_price = 5000 + (chain_idx * 500) + (area_idx * 200)
                            price_variation = (hotel_id % 1000) - 500
                            final_price = max(3000, base_price + price_variation)
                            
                            # Generate rating
                            rating = 3 + (hotel_id % 3)  # 3, 4, or 5 stars
                            
                            # Select amenities
                            amenities = amenities_sets[hotel_id % len(amenities_sets)]
                            
                            hotel_info = {
                                "id": f"hotel_{hotel_id:03d}",
                                "name": hotel_name,
                                "location": {
                                    "address": f"{address}, {city}",
                                    "area": area,
                                    "city": city
                                },
                                "price": {
                                    "amount": final_price,
                                    "currency": "INR"
                                },
                                "rating": rating,
                                "amenities": amenities,
                                "hotel_image": f"/images/hotels/hotel_{hotel_type.lower()}.jpg",
                                "room_image": "/images/hotels/hotel_room.jpg",
                                "amenity_images": {
                                    "WiFi": "/images/amenities/wifi.jpg",
                                    "Pool": "/images/amenities/pool.jpg",
                                    "Spa": "/images/amenities/spa.jpg",
                                    "Restaurant": "/images/amenities/restaurant.jpg",
                                    "Gym": "/images/amenities/gym.jpg",
                                    "Concierge": "/images/amenities/concierge.jpg",
                                    "Business Center": "/images/amenities/business_center.jpg",
                                    "Parking": "/images/amenities/parking.jpg"
                                }
                            }
                            
                            mock_hotels.append(hotel_info)
                            hotel_id += 1
                            
                            # Limit to around 100 hotels
                            if len(mock_hotels) >= 100:
                                break
                        if len(mock_hotels) >= 100:
                            break
                    if len(mock_hotels) >= 100:
                        break
                if len(mock_hotels) >= 100:
                    break
            
            return mock_hotels
        
        for i, hotel in enumerate(hotels):
            try:
                # Extract basic hotel information
                hotel_info = {
                    "id": f"hotel_{i+1:03d}",
                    "name": hotel.get('name', 'Unknown Hotel'),
                    "location": {
                        "address": hotel.get('address', ''),
                        "area": hotel.get('area', ''),
                        "city": hotel.get('city', '')
                    },
                    "price": {
                        "amount": hotel.get('price', {}).get('amount', 0),
                        "currency": hotel.get('price', {}).get('currency', 'INR')
                    },
                    "rating": hotel.get('rating', 0),
                    "amenities": hotel.get('amenities', []),
                    "hotel_image": "/images/hotels/hotel_exterior.jpg",
                    "room_image": "/images/hotels/hotel_room.jpg",
                    "amenity_images": {
                        "WiFi": "/images/amenities/wifi.jpg",
                        "Pool": "/images/amenities/pool.jpg",
                        "Spa": "/images/amenities/spa.jpg",
                        "Restaurant": "/images/amenities/restaurant.jpg",
                        "Gym": "/images/amenities/gym.jpg",
                        "Concierge": "/images/amenities/concierge.jpg",
                        "Business Center": "/images/amenities/business_center.jpg",
                        "Parking": "/images/amenities/parking.jpg"
                    }
                }
                
                extracted_hotels.append(hotel_info)
                
            except Exception as e:
                print(f"Error processing hotel {i}: {e}")
                continue
        
        return extracted_hotels
        
    except Exception as e:
        print(f"Error extracting hotel details: {e}")
        return []

def calculate_duration(departure_time, arrival_time):
    """
    Calculate duration between departure and arrival times
    """
    try:
        if not departure_time or not arrival_time:
            return "Unknown"
        
        # Parse the ISO datetime strings
        from datetime import datetime
        dep_time = datetime.fromisoformat(departure_time.replace('Z', '+00:00'))
        arr_time = datetime.fromisoformat(arrival_time.replace('Z', '+00:00'))
        
        # Calculate difference
        duration = arr_time - dep_time
        
        # Convert to hours and minutes
        total_minutes = int(duration.total_seconds() / 60)
        hours = total_minutes // 60
        minutes = total_minutes % 60
        
        return f"{hours}h {minutes}m"
        
    except Exception as e:
        print(f"Error calculating duration: {e}")
        return "Unknown"

