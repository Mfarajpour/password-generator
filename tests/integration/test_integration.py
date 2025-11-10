import requests
import pytest
import os

BASE_URL = os.getenv('TEST_URL', 'http://localhost:5000')

class TestIntegration:
    
    def test_health_endpoint(self):
        response = requests.get(f'{BASE_URL}/health', timeout=10)
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'healthy'
        assert 'version' in data
    
    def test_version_endpoint(self):
        response = requests.get(f'{BASE_URL}/version', timeout=10)
        assert response.status_code == 200
        data = response.json()
        assert 'version' in data
        
        if 'localhost' not in BASE_URL and '127.0.0.1' not in BASE_URL:
            assert data['version'] != 'unknown', "Production should have version set"
    
    def test_password_generation_api(self):
        response = requests.post(f'{BASE_URL}/api/generate',
            json={'length': 20, 'uppercase': True, 'digits': True},
            timeout=10)
        assert response.status_code == 200
        data = response.json()
        assert data['success'] == True
        assert len(data['password']) == 20
    
    def test_password_length_limits(self):
        response = requests.post(f'{BASE_URL}/api/generate',
            json={'length': 1}, timeout=10)
        assert response.status_code == 200
        assert len(response.json()['password']) >= 4
        
        response = requests.post(f'{BASE_URL}/api/generate',
            json={'length': 500}, timeout=10)
        assert response.status_code == 200
        assert len(response.json()['password']) <= 128
    
    def test_service_handles_multiple_requests(self):
        for i in range(10):
            response = requests.post(f'{BASE_URL}/api/generate',
                json={'length': 16}, timeout=10)
            assert response.status_code == 200
            assert response.json()['success'] == True
    
    def test_home_page(self):
        response = requests.get(f'{BASE_URL}/', timeout=10)
        assert response.status_code == 200
        assert 'text/html' in response.headers.get('Content-Type', '')
