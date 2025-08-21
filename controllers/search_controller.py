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
        
        return jsonify({
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'flight_response': flight_response,
            'hotel_response': hotel_response
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
        # Hotel API endpoint
        url = 'https://qa2new.cleartrip.com/hotel/orchestrator/v2/search'
        
        # Headers for hotel API
        headers = {
            'Content-Type': 'application/json'
        }
        
        # Make the API call
        response = requests.post(url, json=hotel_data, headers=headers, timeout=30)
        
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
