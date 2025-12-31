"""
Twitter integration for posting tweets.
"""
import logging

logger = logging.getLogger(__name__)


class TwitterIntegration:
    """
    Handles Twitter API integration for posting tweets.
    """
    
    def __init__(self, config):
        """
        Initialize Twitter integration.
        
        Args:
            config: Application configuration with Twitter API credentials
        """
        self.config = config
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Twitter API client."""
        try:
            # Check if credentials are available
            if not all([
                self.config.TWITTER_API_KEY,
                self.config.TWITTER_API_SECRET,
                self.config.TWITTER_ACCESS_TOKEN,
                self.config.TWITTER_ACCESS_SECRET
            ]):
                logger.warning("Twitter credentials not configured")
                return
            
            # Initialize tweepy client (requires tweepy library)
            try:
                import tweepy
                auth = tweepy.OAuthHandler(
                    self.config.TWITTER_API_KEY,
                    self.config.TWITTER_API_SECRET
                )
                auth.set_access_token(
                    self.config.TWITTER_ACCESS_TOKEN,
                    self.config.TWITTER_ACCESS_SECRET
                )
                self.client = tweepy.API(auth)
                logger.info("Twitter client initialized successfully")
            except ImportError:
                logger.warning("Tweepy library not installed")
            except Exception as e:
                logger.error(f"Error initializing Twitter client: {str(e)}")
        except Exception as e:
            logger.error(f"Error in Twitter initialization: {str(e)}")
    
    def post(self, content, media_url=None, user_id=None):
        """
        Post a tweet to Twitter.
        
        Args:
            content: Tweet content
            media_url: Optional media URL
            user_id: User ID for account-specific credentials
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.client:
            logger.error("Twitter client not initialized")
            return False
        
        try:
            # Post tweet with or without media
            if media_url:
                # Download and upload media
                # This is a simplified version - production would handle media properly
                self.client.update_status(status=content)
            else:
                self.client.update_status(status=content)
            
            logger.info("Tweet posted successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error posting tweet: {str(e)}")
            return False
    
    def validate_credentials(self, user_id=None):
        """
        Validate Twitter credentials.
        
        Args:
            user_id: User ID for account-specific credentials
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not self.client:
            return False
        
        try:
            self.client.verify_credentials()
            return True
        except Exception as e:
            logger.error(f"Twitter credentials validation failed: {str(e)}")
            return False
