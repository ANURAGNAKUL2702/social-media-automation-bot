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
    Hash a password using SHA256 with salt.
    
    Note: In production, use bcrypt, scrypt, or argon2 for better security.
    This is a simplified implementation for demonstration.
    
    Args:
        password: Plain text password
        
    Returns:
        str: Hashed password with salt
    """
    import os
    # Generate salt
    salt = os.urandom(32).hex()
    # Hash password with salt
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    # Return salt and hash combined
    return f"{salt}${hashed.hex()}"


def verify_password(password, hashed_password):
    """
    Verify a password against a hash.
    
    Args:
        password: Plain text password
        hashed_password: Hashed password with salt
        
    Returns:
        bool: True if password matches
    """
    try:
        salt, hash_hex = hashed_password.split('$')
        # Hash the input password with the stored salt
        hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return hashed.hex() == hash_hex
    except Exception as e:
        logger.error(f"Password verification error: {str(e)}")
        return False


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


def encrypt_credentials(credentials, secret_key):
    """
    Encrypt credentials using Fernet symmetric encryption.
    
    Note: In production, use a proper key management system.
    
    Args:
        credentials: Credentials string to encrypt
        secret_key: Encryption key
        
    Returns:
        str: Encrypted credentials
    """
    try:
        from cryptography.fernet import Fernet
        import base64
        import hashlib
        
        # Create a Fernet key from the secret key
        key = base64.urlsafe_b64encode(hashlib.sha256(secret_key.encode()).digest())
        f = Fernet(key)
        
        # Encrypt the credentials
        encrypted = f.encrypt(credentials.encode())
        return encrypted.decode()
    except Exception as e:
        logger.error(f"Encryption error: {str(e)}")
        return credentials  # Fallback to unencrypted in case of error


def decrypt_credentials(encrypted_credentials, secret_key):
    """
    Decrypt credentials using Fernet symmetric encryption.
    
    Args:
        encrypted_credentials: Encrypted credentials string
        secret_key: Encryption key
        
    Returns:
        str: Decrypted credentials
    """
    try:
        from cryptography.fernet import Fernet
        import base64
        import hashlib
        
        # Create a Fernet key from the secret key
        key = base64.urlsafe_b64encode(hashlib.sha256(secret_key.encode()).digest())
        f = Fernet(key)
        
        # Decrypt the credentials
        decrypted = f.decrypt(encrypted_credentials.encode())
        return decrypted.decode()
    except Exception as e:
        logger.error(f"Decryption error: {str(e)}")
        return encrypted_credentials  # Fallback to returning as-is
