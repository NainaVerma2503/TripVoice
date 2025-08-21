from flask import Blueprint, jsonify, request
from datetime import datetime
import requests
import json
import os

search_bp = Blueprint('search', __name__)

@search_bp.route('/api/search', methods=['POST'])
def search_flights_and_hotels():
    """
    API endpoint that accepts flight and hotel search data and calls external APIs
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

