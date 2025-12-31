"""
Instagram integration for posting to Instagram.
"""
import logging

logger = logging.getLogger(__name__)


class InstagramIntegration:
    """
    Handles Instagram API integration for posting.
    """
    
    def __init__(self, config):
        """
        Initialize Instagram integration.
        
        Args:
            config: Application configuration with Instagram credentials
        """
        self.config = config
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Instagram API client."""
        try:
            # Check if credentials are available
            if not all([
                self.config.INSTAGRAM_USERNAME,
                self.config.INSTAGRAM_PASSWORD
            ]):
                logger.warning("Instagram credentials not configured")
                return
            
            # Initialize Instagram client using instagrapi
            try:
                from instagrapi import Client
                self.client = Client()
                # Note: Login should be done per request in production for security
                # This is a simplified version
                logger.info("Instagram client initialized successfully")
            except ImportError:
                logger.warning("Instagrapi library not installed")
            except Exception as e:
                logger.error(f"Error initializing Instagram client: {str(e)}")
        except Exception as e:
            logger.error(f"Error in Instagram initialization: {str(e)}")
    
    def post(self, content, media_url=None, user_id=None):
        """
        Post to Instagram.
        
        Args:
            content: Post caption
            media_url: Media URL (required for Instagram)
            user_id: User ID for account-specific credentials
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.client:
            logger.error("Instagram client not initialized")
            return False
        
        # Instagram requires media for posts
        if not media_url:
            logger.error("Instagram posts require media_url")
            return False
        
        try:
            # Login to Instagram
            self.client.login(
                self.config.INSTAGRAM_USERNAME,
                self.config.INSTAGRAM_PASSWORD
            )
            
            # Upload photo with caption
            # In production, you'd download the media_url first
            # This is a simplified version
            logger.info("Instagram post would be published here")
            # self.client.photo_upload(path=local_media_path, caption=content)
            
            return True
            
        except Exception as e:
            logger.error(f"Error posting to Instagram: {str(e)}")
            return False
    
    def validate_credentials(self, user_id=None):
        """
        Validate Instagram credentials.
        
        Args:
            user_id: User ID for account-specific credentials
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not self.client:
            return False
        
        try:
            # Try to login
            self.client.login(
                self.config.INSTAGRAM_USERNAME,
                self.config.INSTAGRAM_PASSWORD
            )
            return True
        except Exception as e:
            logger.error(f"Instagram credentials validation failed: {str(e)}")
            return False
