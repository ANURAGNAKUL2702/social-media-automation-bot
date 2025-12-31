"""
Post handler for publishing content to social media platforms.
"""
import logging
from backend.integrations.twitter_integration import TwitterIntegration
from backend.integrations.facebook_integration import FacebookIntegration
from backend.integrations.instagram_integration import InstagramIntegration

logger = logging.getLogger(__name__)


class PostHandler:
    """
    Handles posting content to various social media platforms.
    """
    
    def __init__(self, config):
        """
        Initialize post handler with platform integrations.
        
        Args:
            config: Application configuration
        """
        self.config = config
        self.platforms = {
            'twitter': TwitterIntegration(config),
            'facebook': FacebookIntegration(config),
            'instagram': InstagramIntegration(config)
        }
        logger.info("Post handler initialized with platforms: " + ", ".join(self.platforms.keys()))
    
    def post_to_platform(self, platform, content, media_url=None, user_id=None):
        """
        Post content to a specific platform.
        
        Args:
            platform: Platform name (twitter, facebook, instagram)
            content: Post content/text
            media_url: Optional media URL
            user_id: User ID for account-specific credentials
            
        Returns:
            bool: True if successful, False otherwise
        """
        platform = platform.lower()
        
        if platform not in self.platforms:
            logger.error(f"Unsupported platform: {platform}")
            return False
        
        try:
            integration = self.platforms[platform]
            result = integration.post(content=content, media_url=media_url, user_id=user_id)
            
            if result:
                logger.info(f"Successfully posted to {platform}")
                return True
            else:
                logger.error(f"Failed to post to {platform}")
                return False
                
        except Exception as e:
            logger.error(f"Error posting to {platform}: {str(e)}")
            return False
    
    def validate_credentials(self, platform, user_id=None):
        """
        Validate credentials for a platform.
        
        Args:
            platform: Platform name
            user_id: User ID for account-specific credentials
            
        Returns:
            bool: True if credentials are valid, False otherwise
        """
        platform = platform.lower()
        
        if platform not in self.platforms:
            return False
        
        try:
            integration = self.platforms[platform]
            return integration.validate_credentials(user_id=user_id)
        except Exception as e:
            logger.error(f"Error validating credentials for {platform}: {str(e)}")
            return False
