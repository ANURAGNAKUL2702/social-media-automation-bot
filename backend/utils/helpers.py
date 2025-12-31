"""
Utility functions for the Social Media Automation Bot.
"""
import hashlib
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
import logging

logger = logging.getLogger(__name__)


def hash_password(password):
    """
    Hash a password using SHA256.
    
    Args:
        password: Plain text password
        
    Returns:
        str: Hashed password
    """
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password, hashed_password):
    """
    Verify a password against a hash.
    
    Args:
        password: Plain text password
        hashed_password: Hashed password
        
    Returns:
        bool: True if password matches
    """
    return hash_password(password) == hashed_password


def generate_token(user_id, secret_key, expiration_hours=24):
    """
    Generate a JWT token for a user.
    
    Args:
        user_id: User ID
        secret_key: JWT secret key
        expiration_hours: Token expiration in hours
        
    Returns:
        str: JWT token
    """
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=expiration_hours),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, secret_key, algorithm='HS256')


def decode_token(token, secret_key):
    """
    Decode and verify a JWT token.
    
    Args:
        token: JWT token
        secret_key: JWT secret key
        
    Returns:
        dict: Decoded payload or None if invalid
    """
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        logger.warning("Token has expired")
        return None
    except jwt.InvalidTokenError:
        logger.warning("Invalid token")
        return None


def require_auth(f):
    """
    Decorator to require authentication for routes.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'No token provided'}), 401
        
        # Remove 'Bearer ' prefix if present
        if token.startswith('Bearer '):
            token = token[7:]
        
        from flask import current_app
        payload = decode_token(token, current_app.config['JWT_SECRET_KEY'])
        
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Add user_id to request context
        request.user_id = payload['user_id']
        
        return f(*args, **kwargs)
    
    return decorated_function


def validate_subscription(user, required_plan=None):
    """
    Validate user subscription and limits.
    
    Args:
        user: User object
        required_plan: Required subscription plan
        
    Returns:
        tuple: (is_valid, message)
    """
    if not user.subscription_active:
        return False, "Subscription is not active"
    
    if required_plan:
        plans_hierarchy = ['basic', 'premium', 'enterprise']
        user_plan_level = plans_hierarchy.index(user.subscription_plan) if user.subscription_plan in plans_hierarchy else -1
        required_plan_level = plans_hierarchy.index(required_plan) if required_plan in plans_hierarchy else -1
        
        if user_plan_level < required_plan_level:
            return False, f"Requires {required_plan} plan or higher"
    
    return True, "Valid subscription"


def format_error_response(message, status_code=400):
    """
    Format error response.
    
    Args:
        message: Error message
        status_code: HTTP status code
        
    Returns:
        tuple: JSON response and status code
    """
    return jsonify({'error': message}), status_code


def format_success_response(data, message=None):
    """
    Format success response.
    
    Args:
        data: Response data
        message: Optional success message
        
    Returns:
        dict: JSON response
    """
    response = {'success': True, 'data': data}
    if message:
        response['message'] = message
    return jsonify(response)
