from flask import Flask, jsonify
from datetime import datetime
from controllers.main_controller import main_bp
from controllers.search_controller import search_bp
from controllers.package_controller import package_bp

app = Flask(__name__)

# Register the controller blueprints
app.register_blueprint(main_bp)
app.register_blueprint(search_bp)
app.register_blueprint(package_bp)

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6000)