"""
Password Generator - Flask Application
A secure password generator with REST API
"""

from flask import Flask, render_template, jsonify, request
from datetime import datetime
import secrets
import string
import os

# Create Flask app
app = Flask(__name__)

# Configuration from environment variables
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 5000))


def generate_password(length=12, use_uppercase=True, use_lowercase=True, 
                     use_digits=True, use_symbols=True):
    """
    Generate a cryptographically secure random password
    
    Args:
        length (int): Password length (4-128 characters)
        use_uppercase (bool): Include uppercase letters (A-Z)
        use_lowercase (bool): Include lowercase letters (a-z)
        use_digits (bool): Include digits (0-9)
        use_symbols (bool): Include special symbols (!@#$%...)
    
    Returns:
        str: Generated password
    
    Example:
        >>> generate_password(12, True, True, True, False)
        'aB3xK9mNpQ2r'
    """
    # Build character pool based on options
    characters = ''
    
    if use_lowercase:
        characters += string.ascii_lowercase  # a-z
    
    if use_uppercase:
        characters += string.ascii_uppercase  # A-Z
    
    if use_digits:
        characters += string.digits  # 0-9
    
    if use_symbols:
        characters += string.punctuation  # !@#$%^&*...
    
    # Fallback: if no character type selected, use all
    if not characters:
        characters = string.ascii_letters + string.digits + string.punctuation
    
    # Generate password using secrets module (cryptographically secure)
    password = ''.join(secrets.choice(characters) for _ in range(length))
    
    return password


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
    Home page - Render HTML interface
    """
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def api_generate():
    """
    API endpoint to generate password
    
    Request (JSON):
    {
        "length": 12,
        "uppercase": true,
        "lowercase": true,
        "digits": true,
        "symbols": true
    }
    
    Response (JSON):
    {
        "success": true,
        "password": "aB3!xK9p",
        "length": 8,
        "options": {...}
    }
    """
    # Get JSON data from request (empty dict if no data)
    data = request.get_json() or {}
    
    # Extract options with defaults
    length = data.get('length', 12)
    use_uppercase = data.get('uppercase', True)
    use_lowercase = data.get('lowercase', True)
    use_digits = data.get('digits', True)
    use_symbols = data.get('symbols', True)
    
    # Validate and constrain length (4-128)
    length = int(length)
    length = max(4, min(128, length))
    
    # Generate password
    password = generate_password(
        length=length,
        use_uppercase=use_uppercase,
        use_lowercase=use_lowercase,
        use_digits=use_digits,
        use_symbols=use_symbols
    )
    
    # Return JSON response
    return jsonify({
        'success': True,
        'password': password,
        'length': len(password),
        'options': {
            'uppercase': use_uppercase,
            'lowercase': use_lowercase,
            'digits': use_digits,
            'symbols': use_symbols
        }
    }), 200


# Run application
if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)
