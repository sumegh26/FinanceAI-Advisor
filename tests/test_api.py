"""
API Tests for FinanceAI-Advisor

This module contains unit tests for the Flask API endpoints.
"""

import pytest
import json
from app import create_app
from datetime import datetime


@pytest.fixture
def client():
    """Create test client"""
    app = create_app()
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        yield client


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert data['service'] == 'FinanceAI-Advisor'


def test_create_transaction(client):
    """Test creating a new transaction"""
    transaction_data = {
        'amount': 1000.0,
        'category': 'salary',
        'description': 'Monthly salary payment',
        'transaction_type': 'income'
    }
    
    response = client.post('/api/v1/transactions', 
                          data=json.dumps(transaction_data),
                          content_type='application/json')
    
    assert response.status_code == 201
    
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['data']['amount'] == 1000.0
    assert data['data']['category'] == 'salary'


def test_get_transactions(client):
    """Test retrieving transactions"""
    response = client.get('/api/v1/transactions')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'data' in data
    assert 'count' in data


def test_create_invalid_transaction(client):
    """Test creating transaction with invalid data"""
    invalid_data = {
        'amount': 'invalid',  # Should be number
        'category': '',       # Should not be empty
    }
    
    response = client.post('/api/v1/transactions',
                          data=json.dumps(invalid_data),
                          content_type='application/json')
    
    assert response.status_code == 400
    
    data = json.loads(response.data)
    assert data['success'] is False
    assert 'errors' in data
