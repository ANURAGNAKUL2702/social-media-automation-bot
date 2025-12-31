"""
Database models for the Social Media Automation Bot.
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """User model for authentication and subscription management."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    subscription_plan = db.Column(db.String(50), default='basic')
    subscription_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    posts = db.relationship('ScheduledPost', backref='user', lazy=True, cascade='all, delete-orphan')
    social_accounts = db.relationship('SocialAccount', backref='user', lazy=True, cascade='all, delete-orphan')
    analytics = db.relationship('Analytics', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert user object to dictionary."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'subscription_plan': self.subscription_plan,
            'subscription_active': self.subscription_active,
            'created_at': self.created_at.isoformat()
        }


class SocialAccount(db.Model):
    """Social media account credentials."""
    __tablename__ = 'social_accounts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    platform = db.Column(db.String(50), nullable=False)  # twitter, facebook, instagram
    account_name = db.Column(db.String(100), nullable=False)
    credentials = db.Column(db.Text, nullable=False)  # Encrypted credentials
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert social account to dictionary."""
        return {
            'id': self.id,
            'platform': self.platform,
            'account_name': self.account_name,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat()
        }


class ScheduledPost(db.Model):
    """Scheduled posts for social media platforms."""
    __tablename__ = 'scheduled_posts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    platforms = db.Column(db.String(200))  # Comma-separated list
    scheduled_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, posted, failed
    media_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    posted_at = db.Column(db.DateTime)
    
    def to_dict(self):
        """Convert scheduled post to dictionary."""
        return {
            'id': self.id,
            'content': self.content,
            'platforms': self.platforms.split(',') if self.platforms else [],
            'scheduled_time': self.scheduled_time.isoformat(),
            'status': self.status,
            'media_url': self.media_url,
            'created_at': self.created_at.isoformat(),
            'posted_at': self.posted_at.isoformat() if self.posted_at else None
        }


class Analytics(db.Model):
    """Analytics data for posts."""
    __tablename__ = 'analytics'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('scheduled_posts.id'))
    platform = db.Column(db.String(50), nullable=False)
    likes = db.Column(db.Integer, default=0)
    shares = db.Column(db.Integer, default=0)
    comments = db.Column(db.Integer, default=0)
    reach = db.Column(db.Integer, default=0)
    engagement_rate = db.Column(db.Float, default=0.0)
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert analytics to dictionary."""
        return {
            'id': self.id,
            'post_id': self.post_id,
            'platform': self.platform,
            'likes': self.likes,
            'shares': self.shares,
            'comments': self.comments,
            'reach': self.reach,
            'engagement_rate': self.engagement_rate,
            'recorded_at': self.recorded_at.isoformat()
        }
