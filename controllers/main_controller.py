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
