from flask import Blueprint, jsonify, request
from datetime import datetime
import random

main_bp = Blueprint('main', __name__)

@main_bp.route('/test/hello')
def test_hello():
    """Test endpoint that returns a simple hello message"""
    return jsonify({
        'message': 'Hello from TripVoice Controller!',
        'endpoint': '/test/hello',
        'timestamp': datetime.now().isoformat()
    })

@main_bp.route('/test/echo', methods=['POST'])
def test_echo():
    """Test endpoint that echoes back the request data"""
    data = request.get_json() or {}
    return jsonify({
        'message': 'Echo response from controller',
        'received_data': data,
        'method': request.method,
        'timestamp': datetime.now().isoformat()
    })

@main_bp.route('/test/random')
def test_random():
    """Test endpoint that returns random data"""
    return jsonify({
        'random_number': random.randint(1, 100),
        'random_float': round(random.uniform(0, 1), 4),
        'message': 'Random data generated successfully',
        'timestamp': datetime.now().isoformat()
    })

@main_bp.route('/test/status/<status_code>')
def test_status(status_code):
    """Test endpoint that returns different HTTP status codes"""
    try:
        status = int(status_code)
        if status in [200, 201, 400, 401, 404, 500]:
            return jsonify({
                'message': f'Test status code: {status}',
                'status_code': status,
                'timestamp': datetime.now().isoformat()
            }), status
        else:
            return jsonify({
                'error': 'Invalid status code. Use: 200, 201, 400, 401, 404, 500',
                'timestamp': datetime.now().isoformat()
            }), 400
    except ValueError:
        return jsonify({
            'error': 'Status code must be a number',
            'timestamp': datetime.now().isoformat()
        }), 400

@main_bp.route('/test/headers')
def test_headers():
    """Test endpoint that shows request headers"""
    return jsonify({
        'message': 'Request headers received',
        'headers': dict(request.headers),
        'user_agent': request.headers.get('User-Agent', 'Not provided'),
        'timestamp': datetime.now().isoformat()
    })

@main_bp.route('/test/params')
def test_params():
    """Test endpoint that shows query parameters"""
    return jsonify({
        'message': 'Query parameters received',
        'params': dict(request.args),
        'param_count': len(request.args),
        'timestamp': datetime.now().isoformat()
    }) 