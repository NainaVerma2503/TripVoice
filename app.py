from flask import Flask, jsonify
from datetime import datetime
from controllers.main_controller import main_bp
from controllers.search_controller import search_bp
from controllers.package_controller import package_bp
from controllers.smart_package_controller import smart_package_bp
from controllers.image_controller import image_bp

app = Flask(__name__)

# Register the controller blueprints
app.register_blueprint(main_bp)
app.register_blueprint(search_bp)
app.register_blueprint(package_bp)
app.register_blueprint(smart_package_bp)
app.register_blueprint(image_bp)

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
            '/api/search',
            '/api/package/create',
            '/api/package/create-from-search',
            '/api/smart-package/create'
        ],
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 