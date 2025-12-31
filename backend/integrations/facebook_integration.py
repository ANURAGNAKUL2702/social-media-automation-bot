"""
Facebook integration for posting to Facebook pages.
"""
import logging

logger = logging.getLogger(__name__)


class FacebookIntegration:
    """
    Handles Facebook API integration for posting to pages.
    """
    
    def __init__(self, config):
        """
        Initialize Facebook integration.
        
        Args:
            config: Application configuration with Facebook API credentials
        """
        self.config = config
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Facebook API client."""
        try:
            # Check if credentials are available
            if not all([
                self.config.FACEBOOK_ACCESS_TOKEN,
                self.config.FACEBOOK_PAGE_ID
            ]):
                logger.warning("Facebook credentials not configured")
                return
            
            # Initialize Facebook SDK client
            try:
                import facebook
                self.client = facebook.GraphAPI(access_token=self.config.FACEBOOK_ACCESS_TOKEN)
                logger.info("Facebook client initialized successfully")
            except ImportError:
                logger.warning("Facebook SDK library not installed")
            except Exception as e:
                logger.error(f"Error initializing Facebook client: {str(e)}")
        except Exception as e:
            logger.error(f"Error in Facebook initialization: {str(e)}")
    
    def post(self, content, media_url=None, user_id=None):
        """
        Post to Facebook page.
        
        Args:
            content: Post content
            media_url: Optional media URL
            user_id: User ID for account-specific credentials
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.client:
            logger.error("Facebook client not initialized")
            return False
        
        try:
            page_id = self.config.FACEBOOK_PAGE_ID
            
            # Post with or without media
            if media_url:
                # Post with photo
                self.client.put_photo(
                    image=media_url,
                    message=content,
                    album_path=f"{page_id}/photos"
                )
            else:
                # Post text only
                self.client.put_object(
                    parent_object=page_id,
                    connection_name="feed",
                    message=content
                )
            
            logger.info("Facebook post published successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error posting to Facebook: {str(e)}")
            return False
    
    def validate_credentials(self, user_id=None):
        """
        Validate Facebook credentials.
        
        Args:
            user_id: User ID for account-specific credentials
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not self.client:
            return False
        
        try:
            # Try to get page info
            self.client.get_object(id=self.config.FACEBOOK_PAGE_ID)
            return True
        except Exception as e:
            logger.error(f"Facebook credentials validation failed: {str(e)}")
            return False
