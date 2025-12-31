"""
Main Flask application for Social Media Automation Bot.
"""
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import logging
import os

from backend.config import config
from backend.models.database import db, User, ScheduledPost, SocialAccount, Analytics
from backend.core.scheduler import PostScheduler
from backend.core.post_handler import PostHandler
from backend.core.analytics import AnalyticsTracker
from backend.utils.helpers import (
    hash_password, verify_password, generate_token, 
    require_auth, format_error_response, format_success_response,
    validate_subscription
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app(config_name='default'):
    """Create and configure the Flask application."""
    # Get the base directory
    basedir = os.path.abspath(os.path.dirname(__file__))
    
    app = Flask(__name__, 
                static_folder=os.path.join(basedir, 'frontend/static'),
                template_folder=os.path.join(basedir, 'frontend/templates'))
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Enable CORS
    CORS(app)
    
    # Initialize database
    db.init_app(app)
    
    # Initialize scheduler and post handler
    with app.app_context():
        db.create_all()
        post_handler = PostHandler(app.config)
        scheduler = PostScheduler(db, post_handler)
        analytics_tracker = AnalyticsTracker(db)
        
        # Store in app context
        app.scheduler = scheduler
        app.post_handler = post_handler
        app.analytics_tracker = analytics_tracker
    
    # Register routes
    register_routes(app)
    
    logger.info(f"Application created with config: {config_name}")
    
    return app


def register_routes(app):
    """Register all API routes."""
    
    @app.route('/')
    def index():
        """Home page."""
        return render_template('index.html')
    
    @app.route('/api/health')
    def health():
        """Health check endpoint."""
        return jsonify({'status': 'healthy'})
    
    # Authentication routes
    @app.route('/api/auth/register', methods=['POST'])
    def register():
        """Register a new user."""
        data = request.json
        
        if not all(k in data for k in ['username', 'email', 'password']):
            return format_error_response("Missing required fields")
        
        # Check if user exists
        if User.query.filter_by(username=data['username']).first():
            return format_error_response("Username already exists")
        
        if User.query.filter_by(email=data['email']).first():
            return format_error_response("Email already exists")
        
        # Create user
        user = User(
            username=data['username'],
            email=data['email'],
            password_hash=hash_password(data['password']),
            subscription_plan=data.get('subscription_plan', 'basic')
        )
        
        db.session.add(user)
        db.session.commit()
        
        token = generate_token(user.id, app.config['JWT_SECRET_KEY'])
        
        return format_success_response({
            'user': user.to_dict(),
            'token': token
        }, "User registered successfully")
    
    @app.route('/api/auth/login', methods=['POST'])
    def login():
        """Login user."""
        data = request.json
        
        if not all(k in data for k in ['username', 'password']):
            return format_error_response("Missing username or password")
        
        user = User.query.filter_by(username=data['username']).first()
        
        if not user or not verify_password(data['password'], user.password_hash):
            return format_error_response("Invalid credentials", 401)
        
        token = generate_token(user.id, app.config['JWT_SECRET_KEY'])
        
        return format_success_response({
            'user': user.to_dict(),
            'token': token
        })
    
    # Post management routes
    @app.route('/api/posts', methods=['GET'])
    @require_auth
    def get_posts():
        """Get all scheduled posts for the user."""
        posts = ScheduledPost.query.filter_by(user_id=request.user_id).all()
        return format_success_response([post.to_dict() for post in posts])
    
    @app.route('/api/posts', methods=['POST'])
    @require_auth
    def create_post():
        """Schedule a new post."""
        data = request.json
        
        if not all(k in data for k in ['content', 'platforms', 'scheduled_time']):
            return format_error_response("Missing required fields")
        
        # Validate user subscription
        user = User.query.get(request.user_id)
        is_valid, message = validate_subscription(user)
        if not is_valid:
            return format_error_response(message, 403)
        
        from datetime import datetime
        scheduled_time = datetime.fromisoformat(data['scheduled_time'])
        
        # Create post
        post = ScheduledPost(
            user_id=request.user_id,
            content=data['content'],
            platforms=','.join(data['platforms']),
            scheduled_time=scheduled_time,
            media_url=data.get('media_url')
        )
        
        db.session.add(post)
        db.session.commit()
        
        # Schedule the post
        app.scheduler.schedule_post(post.id, scheduled_time)
        
        return format_success_response(post.to_dict(), "Post scheduled successfully")
    
    @app.route('/api/posts/<int:post_id>', methods=['DELETE'])
    @require_auth
    def delete_post(post_id):
        """Cancel and delete a scheduled post."""
        post = ScheduledPost.query.filter_by(id=post_id, user_id=request.user_id).first()
        
        if not post:
            return format_error_response("Post not found", 404)
        
        # Cancel scheduled job
        app.scheduler.cancel_post(post_id)
        
        # Delete post
        db.session.delete(post)
        db.session.commit()
        
        return format_success_response(None, "Post deleted successfully")
    
    # Analytics routes
    @app.route('/api/analytics/summary', methods=['GET'])
    @require_auth
    def get_analytics_summary():
        """Get analytics summary for the user."""
        days = request.args.get('days', 30, type=int)
        summary = app.analytics_tracker.get_user_analytics(request.user_id, days)
        
        if not summary:
            return format_error_response("Failed to retrieve analytics")
        
        return format_success_response(summary)
    
    @app.route('/api/analytics/best-times', methods=['GET'])
    @require_auth
    def get_best_times():
        """Get recommended posting times."""
        recommendations = app.analytics_tracker.get_best_posting_times(request.user_id)
        return format_success_response(recommendations)
    
    @app.route('/api/analytics/post/<int:post_id>', methods=['GET'])
    @require_auth
    def get_post_analytics(post_id):
        """Get analytics for a specific post."""
        analytics = app.analytics_tracker.get_post_analytics(post_id)
        return format_success_response(analytics)
    
    # Social account management
    @app.route('/api/accounts', methods=['GET'])
    @require_auth
    def get_social_accounts():
        """Get all connected social accounts."""
        accounts = SocialAccount.query.filter_by(user_id=request.user_id).all()
        return format_success_response([acc.to_dict() for acc in accounts])
    
    @app.route('/api/accounts', methods=['POST'])
    @require_auth
    def add_social_account():
        """Connect a new social media account."""
        data = request.json
        
        if not all(k in data for k in ['platform', 'account_name', 'credentials']):
            return format_error_response("Missing required fields")
        
        account = SocialAccount(
            user_id=request.user_id,
            platform=data['platform'],
            account_name=data['account_name'],
            credentials=data['credentials']  # Should be encrypted in production
        )
        
        db.session.add(account)
        db.session.commit()
        
        return format_success_response(account.to_dict(), "Account connected successfully")
    
    # User profile
    @app.route('/api/user/profile', methods=['GET'])
    @require_auth
    def get_profile():
        """Get user profile."""
        user = User.query.get(request.user_id)
        if not user:
            return format_error_response("User not found", 404)
        return format_success_response(user.to_dict())
    
    @app.route('/api/user/subscription', methods=['PUT'])
    @require_auth
    def update_subscription():
        """Update user subscription plan."""
        data = request.json
        
        if 'subscription_plan' not in data:
            return format_error_response("Missing subscription_plan")
        
        user = User.query.get(request.user_id)
        if not user:
            return format_error_response("User not found", 404)
        
        user.subscription_plan = data['subscription_plan']
        db.session.commit()
        
        return format_success_response(user.to_dict(), "Subscription updated successfully")


if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    app.run(host='0.0.0.0', port=5000, debug=True)
