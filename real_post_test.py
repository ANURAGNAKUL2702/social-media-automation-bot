#!/usr/bin/env python3
"""
Real Instagram Post Test for rishyashrunga
This will make an actual post to validate everything works.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from backend.integrations.instagram_integration import InstagramIntegration

def make_test_post():
    """Make a real test post to Instagram."""
    
    print("🚀 REAL Instagram Post Test for @rishyashrunga")
    print("=" * 60)
    
    # Your credentials
    class Config:
        INSTAGRAM_USERNAME = "rishyashrunga"
        INSTAGRAM_PASSWORD = "1234Gangamma"
    
    config = Config()
    
    try:
        print("🔗 Connecting to Instagram...")
        instagram = InstagramIntegration(config)
        
        if instagram.client is None:
            print("❌ Failed to connect to Instagram")
            return False
        
        print("✅ Connected to Instagram successfully!")
        
        # Create test post content
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        test_content = f"""🧪 Social Media Bot Test Post
        
🤖 Automated posting is now LIVE!
📅 Posted on: {timestamp}
🔥 This is a validation test for the social media automation system.

#SocialMediaBot #Automation #TestPost #rishyashrunga #TechTest"""
        
        print(f"📝 Post Content:")
        print(f"{test_content}")
        print("\n🚨 WARNING: This will make a REAL post to your Instagram!")
        
        # Ask for confirmation
        while True:
            confirm = input("\n🤔 Do you want to proceed with the real post? (yes/no): ").lower().strip()
            if confirm in ['yes', 'y']:
                break
            elif confirm in ['no', 'n']:
                print("❌ Post cancelled by user.")
                return False
            else:
                print("Please enter 'yes' or 'no'")
        
        print("\n📤 Posting to Instagram...")
        
        # Make the actual post
        success = instagram.post(
            content=test_content,
            media_url=None
        )
        
        if success:
            print("🎉 SUCCESS! Post published to Instagram!")
            print("✅ Your Instagram automation is fully working!")
            print(f"📱 Check your Instagram @rishyashrunga to see the post")
            return True
        else:
            print("❌ Failed to publish post")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = make_test_post()
    
    if success:
        print("\n🎊 CONGRATULATIONS!")
        print("Your Instagram automation is 100% functional!")
        print("You can now schedule posts, automate content, and manage your account.")
    else:
        print("\n🔧 Please check your credentials and try again.")