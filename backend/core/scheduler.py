"""
Scheduler module for automating social media posts.
Uses APScheduler for scheduling posts at optimal times.
"""
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
import logging

logger = logging.getLogger(__name__)


class PostScheduler:
    """
    Handles scheduling and execution of social media posts.
    """
    
    def __init__(self, db, post_handler):
        """
        Initialize the scheduler.
        
        Args:
            db: Database instance
            post_handler: Handler for posting to social media platforms
        """
        self.db = db
        self.post_handler = post_handler
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        logger.info("Post scheduler initialized")
    
    def schedule_post(self, post_id, scheduled_time):
        """
        Schedule a post for future publication.
        
        Args:
            post_id: ID of the scheduled post
            scheduled_time: datetime when the post should be published
        """
        try:
            # Add job to scheduler
            job = self.scheduler.add_job(
                func=self._execute_post,
                trigger=DateTrigger(run_date=scheduled_time),
                args=[post_id],
                id=f'post_{post_id}',
                replace_existing=True
            )
            logger.info(f"Scheduled post {post_id} for {scheduled_time}")
            return True
        except Exception as e:
            logger.error(f"Error scheduling post {post_id}: {str(e)}")
            return False
    
    def cancel_post(self, post_id):
        """
        Cancel a scheduled post.
        
        Args:
            post_id: ID of the post to cancel
        """
        try:
            self.scheduler.remove_job(f'post_{post_id}')
            logger.info(f"Cancelled scheduled post {post_id}")
            return True
        except Exception as e:
            logger.error(f"Error cancelling post {post_id}: {str(e)}")
            return False
    
    def _execute_post(self, post_id):
        """
        Execute a scheduled post by publishing to social media platforms.
        
        Args:
            post_id: ID of the post to execute
        """
        from backend.models.database import ScheduledPost
        
        try:
            post = self.db.session.query(ScheduledPost).get(post_id)
            if not post:
                logger.error(f"Post {post_id} not found")
                return
            
            platforms = post.platforms.split(',') if post.platforms else []
            success = True
            
            for platform in platforms:
                platform = platform.strip()
                result = self.post_handler.post_to_platform(
                    platform=platform,
                    content=post.content,
                    media_url=post.media_url,
                    user_id=post.user_id
                )
                if not result:
                    success = False
                    logger.error(f"Failed to post to {platform} for post {post_id}")
            
            # Update post status
            post.status = 'posted' if success else 'failed'
            post.posted_at = datetime.utcnow()
            self.db.session.commit()
            
            logger.info(f"Executed post {post_id} with status: {post.status}")
            
        except Exception as e:
            logger.error(f"Error executing post {post_id}: {str(e)}")
            # Update post status to failed
            try:
                post = self.db.session.query(ScheduledPost).get(post_id)
                if post:
                    post.status = 'failed'
                    self.db.session.commit()
            except:
                pass
    
    def get_scheduled_jobs(self):
        """Get all scheduled jobs."""
        jobs = self.scheduler.get_jobs()
        return [{
            'job_id': job.id,
            'next_run_time': job.next_run_time.isoformat() if job.next_run_time else None
        } for job in jobs]
    
    def shutdown(self):
        """Shutdown the scheduler."""
        self.scheduler.shutdown()
        logger.info("Scheduler shut down")
