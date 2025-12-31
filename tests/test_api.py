"""
Test suite for Social Media Automation Bot
Run with: python -m pytest tests/
"""
import json
import pytest
from app import create_app
from backend.models.database import db


@pytest.fixture
def app():
    """Create and configure a test application instance."""
    app = create_app('development')
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()


class TestAuthentication:
    """Test authentication endpoints."""
    
    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get('/api/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'healthy'
    
    def test_registration(self, client):
        """Test user registration."""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'subscription_plan': 'basic'
        }
        response = client.post('/api/auth/register',
                              data=json.dumps(data),
                              content_type='application/json')
        assert response.status_code == 200
        result = response.get_json()
        assert result['success'] is True
        assert 'token' in result['data']
    
    def test_duplicate_registration(self, client):
        """Test registration with duplicate username."""
        data = {
            'username': 'testuser',
            'email': 'test1@example.com',
            'password': 'password123'
        }
        # First registration
        client.post('/api/auth/register',
                   data=json.dumps(data),
                   content_type='application/json')
        
        # Duplicate registration
        response = client.post('/api/auth/register',
                              data=json.dumps(data),
                              content_type='application/json')
        assert response.status_code == 400
    
    def test_login(self, client):
        """Test user login."""
        # Register first
        register_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123'
        }
        client.post('/api/auth/register',
                   data=json.dumps(register_data),
                   content_type='application/json')
        
        # Login
        login_data = {
            'username': 'testuser',
            'password': 'password123'
        }
        response = client.post('/api/auth/login',
                              data=json.dumps(login_data),
                              content_type='application/json')
        assert response.status_code == 200
        result = response.get_json()
        assert result['success'] is True
        assert 'token' in result['data']
    
    def test_invalid_login(self, client):
        """Test login with invalid credentials."""
        data = {
            'username': 'nonexistent',
            'password': 'wrongpassword'
        }
        response = client.post('/api/auth/login',
                              data=json.dumps(data),
                              content_type='application/json')
        assert response.status_code == 401


class TestPosts:
    """Test post management endpoints."""
    
    def get_auth_token(self, client):
        """Helper to get authentication token."""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123'
        }
        response = client.post('/api/auth/register',
                              data=json.dumps(data),
                              content_type='application/json')
        return response.get_json()['data']['token']
    
    def test_get_posts_without_auth(self, client):
        """Test getting posts without authentication."""
        response = client.get('/api/posts')
        assert response.status_code == 401
    
    def test_get_posts_with_auth(self, client):
        """Test getting posts with authentication."""
        token = self.get_auth_token(client)
        response = client.get('/api/posts',
                             headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 200
        result = response.get_json()
        assert result['success'] is True
        assert isinstance(result['data'], list)
    
    def test_schedule_post(self, client):
        """Test scheduling a new post."""
        token = self.get_auth_token(client)
        from datetime import datetime, timedelta
        
        data = {
            'content': 'Test post content',
            'platforms': ['twitter', 'facebook'],
            'scheduled_time': (datetime.utcnow() + timedelta(hours=1)).isoformat()
        }
        response = client.post('/api/posts',
                              data=json.dumps(data),
                              content_type='application/json',
                              headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 200
        result = response.get_json()
        assert result['success'] is True


class TestAnalytics:
    """Test analytics endpoints."""
    
    def get_auth_token(self, client):
        """Helper to get authentication token."""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123'
        }
        response = client.post('/api/auth/register',
                              data=json.dumps(data),
                              content_type='application/json')
        return response.get_json()['data']['token']
    
    def test_get_analytics_summary(self, client):
        """Test getting analytics summary."""
        token = self.get_auth_token(client)
        response = client.get('/api/analytics/summary?days=30',
                             headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 200
        result = response.get_json()
        assert result['success'] is True
    
    def test_get_best_posting_times(self, client):
        """Test getting best posting times."""
        token = self.get_auth_token(client)
        response = client.get('/api/analytics/best-times',
                             headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 200
        result = response.get_json()
        assert result['success'] is True


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
