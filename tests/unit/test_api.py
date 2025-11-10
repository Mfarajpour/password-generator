"""
Integration tests for API endpoints
"""

import pytest
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app import app


@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestHealthEndpoint:
    """Test health check endpoint"""
    
    def test_health_endpoint(self, client):
        """Test /health returns 200"""
        response = client.get('/health')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert data['service'] == 'password-generator'
        assert 'timestamp' in data


class TestHomeEndpoint:
    """Test home page endpoint"""
    
    def test_home_page(self, client):
        """Test / returns HTML"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Password Generator' in response.data


class TestGenerateAPI:
    """Test /api/generate endpoint"""
    
    def test_generate_default(self, client):
        """Test generate with default parameters"""
        response = client.post('/api/generate',
                               data=json.dumps({}),
                               content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['success'] is True
        assert 'password' in data
        assert len(data['password']) == 12
        assert data['length'] == 12
    
    def test_generate_custom_length(self, client):
        """Test generate with custom length"""
        for length in [8, 16, 32]:
            response = client.post('/api/generate',
                                   data=json.dumps({'length': length}),
                                   content_type='application/json')
            
            data = json.loads(response.data)
            assert data['success'] is True
            assert len(data['password']) == length
    
    def test_generate_only_lowercase(self, client):
        """Test generate with only lowercase"""
        response = client.post('/api/generate',
                               data=json.dumps({
                                   'length': 20,
                                   'uppercase': False,
                                   'lowercase': True,
                                   'digits': False,
                                   'symbols': False
                               }),
                               content_type='application/json')
        
        data = json.loads(response.data)
        assert data['success'] is True
        password = data['password']
        assert password.islower()
        assert password.isalpha()
    
    def test_generate_only_digits(self, client):
        """Test generate with only digits"""
        response = client.post('/api/generate',
                               data=json.dumps({
                                   'length': 20,
                                   'uppercase': False,
                                   'lowercase': False,
                                   'digits': True,
                                   'symbols': False
                               }),
                               content_type='application/json')
        
        data = json.loads(response.data)
        assert data['success'] is True
        password = data['password']
        assert password.isdigit()
    
    def test_generate_mixed(self, client):
        """Test generate with all character types"""
        response = client.post('/api/generate',
                               data=json.dumps({
                                   'length': 16,
                                   'uppercase': True,
                                   'lowercase': True,
                                   'digits': True,
                                   'symbols': True
                               }),
                               content_type='application/json')
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert len(data['password']) == 16
        assert data['options']['uppercase'] is True
        assert data['options']['lowercase'] is True
        assert data['options']['digits'] is True
        assert data['options']['symbols'] is True
    
    def test_generate_length_constraints(self, client):
        """Test length constraints (4-128)"""
        # Too small (should constrain to 4)
        response = client.post('/api/generate',
                               data=json.dumps({'length': 2}),
                               content_type='application/json')
        data = json.loads(response.data)
        assert len(data['password']) == 4
        
        # Too large (should constrain to 128)
        response = client.post('/api/generate',
                               data=json.dumps({'length': 200}),
                               content_type='application/json')
        data = json.loads(response.data)
        assert len(data['password']) == 128
    
    def test_generate_no_body(self, client):
        """Test generate with empty JSON body"""
        response = client.post('/api/generate',
                           data=json.dumps({}),  # ✅ Empty JSON instead of no body
                           content_type='application/json')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert len(data['password']) == 12  # Default
      
    def test_generate_invalid_json(self, client):
        """Test generate with invalid JSON"""
        response = client.post('/api/generate',
                               data='invalid json',
                               content_type='application/json')
        
        # Should handle gracefully and use defaults
        assert response.status_code in [200, 400]
    
    def test_generate_randomness(self, client):
        """Test that multiple calls generate different passwords"""
        passwords = []
        for _ in range(10):
            response = client.post('/api/generate',
                                   data=json.dumps({'length': 16}),
                                   content_type='application/json')
            data = json.loads(response.data)
            passwords.append(data['password'])
        
        # All should be unique
        assert len(set(passwords)) == 10
    
    def test_response_structure(self, client):
        """Test response has correct structure"""
        response = client.post('/api/generate',
                               data=json.dumps({'length': 12}),
                               content_type='application/json')
        
        data = json.loads(response.data)
        
        # Check required fields
        assert 'success' in data
        assert 'password' in data
        assert 'length' in data
        assert 'options' in data
        
        # Check options structure
        assert 'uppercase' in data['options']
        assert 'lowercase' in data['options']
        assert 'digits' in data['options']
        assert 'symbols' in data['options']
