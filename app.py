"""
Password Generator - Flask Application
A secure password generator with REST API
"""

from flask import Flask, jsonify
from datetime import datetime
import os

# Create Flask app
app = Flask(__name__)

# Configuration from environment variables
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 5000))


@app.route('/health')
def health():
    """
    Health check endpoint for monitoring
    Returns service status and timestamp
    """
    return jsonify({
        'status': 'healthy',
        'service': 'password-generator',
        'timestamp': str(datetime.now())
    }), 200


@app.route('/')
def home():
    """
    Home endpoint - API information
    """
    return jsonify({
        'message': 'Password Generator API',
        'version': '1.0.0',
        'endpoints': {
            'health': '/health',
            'generate': '/api/generate (coming soon)'
        }
    }), 200


# Run application
if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)
