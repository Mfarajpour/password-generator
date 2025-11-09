"""
Password Generator - Flask Application
A secure password generator with REST API
"""

from flask import Flask, render_template, jsonify, request
from datetime import datetime
import secrets
import string
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 5000))

APP_VERSION = os.getenv('APP_VERSION', 'unknown')


def generate_password(length=12, use_uppercase=True, use_lowercase=True,
                     use_digits=True, use_symbols=True):
    characters = ''
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation
    if not characters:
        characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password


@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'password-generator',
        'version': APP_VERSION,
        'timestamp': str(datetime.now())
    }), 200


@app.route('/version')
def version():
    return jsonify({
        'version': APP_VERSION,
        'service': 'password-generator',
        'environment': os.getenv('FLASK_ENV', 'development'),
        'timestamp': str(datetime.now())
    }), 200


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/generate', methods=['POST'])
def api_generate():
    data = request.get_json() or {}
    length = data.get('length', 12)
    use_uppercase = data.get('uppercase', True)
    use_lowercase = data.get('lowercase', True)
    use_digits = data.get('digits', True)
    use_symbols = data.get('symbols', True)

    length = int(length)
    length = max(4, min(128, length))

    password = generate_password(
        length=length,
        use_uppercase=use_uppercase,
        use_lowercase=use_lowercase,
        use_digits=use_digits,
        use_symbols=use_symbols
    )

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


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)

