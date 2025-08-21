from flask import Flask, jsonify, request
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

from controllers.main_controller import main_bp
from controllers.search_controller import search_bp
from controllers.package_controller import package_bp
from controllers.trip_controller import trip_bp

app = Flask(__name__)

# Register the controller blueprints
app.register_blueprint(main_bp)
app.register_blueprint(search_bp)
app.register_blueprint(package_bp)
app.register_blueprint(trip_bp)

# CORS: allow localhost:3000 for browser requests (including preflight)
ALLOWED_CORS_ORIGINS = {
    'http://localhost:3000',
    'http://127.0.0.1:3000'
}

@app.before_request
def handle_preflight():
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        origin = request.headers.get('Origin')
        if origin in ALLOWED_CORS_ORIGINS:
            headers = response.headers
            headers['Access-Control-Allow-Origin'] = origin
            headers['Vary'] = 'Origin'
            headers['Access-Control-Allow-Credentials'] = 'true'
            headers['Access-Control-Allow-Headers'] = request.headers.get(
                'Access-Control-Request-Headers', 'Content-Type, Authorization, X-Requested-With'
            )
            headers['Access-Control-Allow-Methods'] = request.headers.get(
                'Access-Control-Request-Method', 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
            )
        return response

@app.after_request
def add_cors_headers(response):
    origin = request.headers.get('Origin')
    if origin in ALLOWED_CORS_ORIGINS:
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Vary'] = 'Origin'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
    return response

@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        'message': 'Welcome to TripVoice API',
        'status': 'running',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/health')
def health_check():
    """Health check endpoint to verify the service is working"""
    return jsonify({
        'status': 'healthy',
        'service': 'TripVoice',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/status')
def api_status():
    """API status endpoint"""
    return jsonify({
        'api_status': 'operational',
        'endpoints': [
            '/',
            '/health',
            '/api/status',
            '/test/hello',
            '/test/echo',
            '/test/random',
            '/test/status/<status_code>',
            '/test/headers',
            '/test/params',
            '/api/trip/plan',
            '/api/trip/health',
            '/api/trip/cities'
        ],
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6000)