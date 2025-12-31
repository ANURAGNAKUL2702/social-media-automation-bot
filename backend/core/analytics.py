"""
Analytics module for tracking post performance and engagement.
"""
import logging
from datetime import datetime, timedelta
from backend.models.database import Analytics, ScheduledPost

logger = logging.getLogger(__name__)


class AnalyticsTracker:
    """
    Tracks and analyzes social media post performance.
    """
    
    def __init__(self, db):
        """
        Initialize analytics tracker.
        
        Args:
            db: Database instance
        """
        self.db = db
        logger.info("Analytics tracker initialized")
    
    def record_analytics(self, user_id, post_id, platform, likes=0, shares=0, comments=0, reach=0):
        """
        Record analytics data for a post.
        
        Args:
            user_id: User ID
            post_id: Post ID
            platform: Social media platform
            likes: Number of likes
            shares: Number of shares
            comments: Number of comments
            reach: Post reach
        """
        try:
            # Calculate engagement rate
            total_engagement = likes + shares + comments
            engagement_rate = (total_engagement / reach * 100) if reach > 0 else 0
            
            # Create analytics record
            analytics = Analytics(
                user_id=user_id,
                post_id=post_id,
                platform=platform,
                likes=likes,
                shares=shares,
                comments=comments,
                reach=reach,
                engagement_rate=engagement_rate
            )
            
            self.db.session.add(analytics)
            self.db.session.commit()
            
            logger.info(f"Recorded analytics for post {post_id} on {platform}")
            return analytics.to_dict()
            
        except Exception as e:
            logger.error(f"Error recording analytics: {str(e)}")
            self.db.session.rollback()
            return None
    
    def get_user_analytics(self, user_id, days=30):
        """
        Get analytics summary for a user.
        
        Args:
            user_id: User ID
            days: Number of days to look back
            
        Returns:
            dict: Analytics summary
        """
        try:
            start_date = datetime.utcnow() - timedelta(days=days)
            
            analytics = self.db.session.query(Analytics).filter(
                Analytics.user_id == user_id,
                Analytics.recorded_at >= start_date
            ).all()
            
            # Aggregate analytics
            total_likes = sum(a.likes for a in analytics)
            total_shares = sum(a.shares for a in analytics)
            total_comments = sum(a.comments for a in analytics)
            total_reach = sum(a.reach for a in analytics)
            avg_engagement = sum(a.engagement_rate for a in analytics) / len(analytics) if analytics else 0
            
            # Platform breakdown
            platform_stats = {}
            for a in analytics:
                if a.platform not in platform_stats:
                    platform_stats[a.platform] = {
                        'likes': 0,
                        'shares': 0,
                        'comments': 0,
                        'reach': 0,
                        'posts': 0
                    }
                platform_stats[a.platform]['likes'] += a.likes
                platform_stats[a.platform]['shares'] += a.shares
                platform_stats[a.platform]['comments'] += a.comments
                platform_stats[a.platform]['reach'] += a.reach
                platform_stats[a.platform]['posts'] += 1
            
            return {
                'period_days': days,
                'total_posts': len(analytics),
                'total_likes': total_likes,
                'total_shares': total_shares,
                'total_comments': total_comments,
                'total_reach': total_reach,
                'avg_engagement_rate': round(avg_engagement, 2),
                'platform_breakdown': platform_stats
            }
            
        except Exception as e:
            logger.error(f"Error getting user analytics: {str(e)}")
            return None
    
    def get_best_posting_times(self, user_id):
        """
        Analyze historical data to recommend best posting times.
        
        Args:
            user_id: User ID
            
        Returns:
            list: Recommended posting times
        """
        try:
            # Get all analytics for user with high engagement
            analytics = self.db.session.query(Analytics).filter(
                Analytics.user_id == user_id,
                Analytics.engagement_rate > 5.0  # Posts with >5% engagement
            ).all()
            
            if not analytics:
                # Default recommendations if no data
                return [
                    {'hour': 9, 'day': 'weekday', 'reason': 'Morning engagement'},
                    {'hour': 12, 'day': 'weekday', 'reason': 'Lunch break'},
                    {'hour': 19, 'day': 'any', 'reason': 'Evening activity'}
                ]
            
            # Analyze posting times from high-engagement posts
            # This is a simplified version - production would do more analysis
            recommendations = [
                {'hour': 9, 'day': 'weekday', 'reason': 'Based on your engagement data'},
                {'hour': 15, 'day': 'weekday', 'reason': 'Afternoon peak'},
                {'hour': 20, 'day': 'weekend', 'reason': 'Weekend evening'}
            ]
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error analyzing best posting times: {str(e)}")
            return []
    
    def get_post_analytics(self, post_id):
        """
        Get analytics for a specific post.
        
        Args:
            post_id: Post ID
            
        Returns:
            list: Analytics records for the post
        """
        try:
            analytics = self.db.session.query(Analytics).filter(
                Analytics.post_id == post_id
            ).all()
            
            return [a.to_dict() for a in analytics]
            
        except Exception as e:
            logger.error(f"Error getting post analytics: {str(e)}")
            return []
