#!/usr/bin/env python3
"""
Social Media Scheduler - Example Script
Demonstrates how to schedule posts for specific social media accounts.
"""

import requests
import json
from datetime import datetime, timedelta

class SocialMediaScheduler:
    def __init__(self, base_url="http://127.0.0.1:5000"):
        self.base_url = base_url
        self.token = None
    
    def register_user(self, username, email, password):
        """Register a new user and get authentication token."""
        url = f"{self.base_url}/api/auth/register"
        data = {
            "username": username,
            "email": email,
            "password": password,
            "subscription_plan": "basic"
        }
        
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            self.token = result['data']['token']
            print(f"✅ User registered successfully! Token: {self.token[:20]}...")
            return True
        else:
            print(f"❌ Registration failed: {response.json()}")
            return False
    
    def login(self, username, password):
        """Login and get authentication token."""
        url = f"{self.base_url}/api/auth/login"
        data = {
            "username": username,
            "password": password
        }
        
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            self.token = result['data']['token']
            print(f"✅ Login successful! Token: {self.token[:20]}...")
            return True
        else:
            print(f"❌ Login failed: {response.json()}")
            return False
    
    def add_social_account(self, platform, account_name, credentials):
        """Connect a social media account."""
        if not self.token:
            print("❌ Please login first!")
            return False
        
        url = f"{self.base_url}/api/accounts"
        headers = {"Authorization": f"Bearer {self.token}"}
        data = {
            "platform": platform,
            "account_name": account_name,
            "credentials": credentials
        }
        
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            print(f"✅ {platform.title()} account '{account_name}' connected successfully!")
            return True
        else:
            print(f"❌ Failed to connect {platform} account: {response.json()}")
            return False
    
    def schedule_post(self, content, platforms, scheduled_time, media_url=None):
        """Schedule a post for specific social media platforms."""
        if not self.token:
            print("❌ Please login first!")
            return False
        
        url = f"{self.base_url}/api/posts"
        headers = {"Authorization": f"Bearer {self.token}"}
        data = {
            "content": content,
            "platforms": platforms,
            "scheduled_time": scheduled_time.isoformat(),
        }
        
        if media_url:
            data["media_url"] = media_url
        
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            post_id = result['data']['id']
            print(f"✅ Post scheduled successfully! Post ID: {post_id}")
            print(f"📅 Scheduled for: {scheduled_time}")
            print(f"📱 Platforms: {', '.join(platforms)}")
            return post_id
        else:
            print(f"❌ Failed to schedule post: {response.json()}")
            return None
    
    def get_scheduled_posts(self):
        """Get all scheduled posts."""
        if not self.token:
            print("❌ Please login first!")
            return []
        
        url = f"{self.base_url}/api/posts"
        headers = {"Authorization": f"Bearer {self.token}"}
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            posts = response.json()['data']
            print(f"📝 You have {len(posts)} scheduled posts:")
            for post in posts:
                print(f"  - ID: {post['id']}, Content: {post['content'][:50]}...")
                print(f"    Platforms: {', '.join(post['platforms'])}")
                print(f"    Scheduled: {post['scheduled_time']}")
                print(f"    Status: {post['status']}")
                print()
            return posts
        else:
            print(f"❌ Failed to get posts: {response.json()}")
            return []
    
    def cancel_post(self, post_id):
        """Cancel a scheduled post."""
        if not self.token:
            print("❌ Please login first!")
            return False
        
        url = f"{self.base_url}/api/posts/{post_id}"
        headers = {"Authorization": f"Bearer {self.token}"}
        
        response = requests.delete(url, headers=headers)
        if response.status_code == 200:
            print(f"✅ Post {post_id} cancelled successfully!")
            return True
        else:
            print(f"❌ Failed to cancel post: {response.json()}")
            return False


# Example usage
def example_usage():
    """Example of how to use the scheduler."""
    scheduler = SocialMediaScheduler()
    
    # Step 1: Register or login
    username = "demo_user"
    email = "demo@example.com"
    password = "demo_password123"
    
    print("🚀 Starting Social Media Scheduler Demo")
    print("=" * 50)
    
    # Try to login first, if it fails, register
    if not scheduler.login(username, password):
        print("🔧 User doesn't exist, registering...")
        scheduler.register_user(username, email, password)
    
    print("\n" + "=" * 50)
    
    # Step 2: Add social media accounts
    print("📱 Adding social media accounts...")
    
    # Add Instagram account (demo credentials - replace with real ones)
    instagram_creds = {
        "username": "your_instagram_username",
        "password": "your_instagram_password"
    }
    scheduler.add_social_account("instagram", "my_insta_account", instagram_creds)
    
    # Add Facebook account (demo credentials - replace with real ones)
    facebook_creds = {
        "access_token": "your_facebook_access_token",
        "page_id": "your_page_id"
    }
    scheduler.add_social_account("facebook", "my_facebook_page", facebook_creds)
    
    print("\n" + "=" * 50)
    
    # Step 3: Schedule posts
    print("📅 Scheduling posts...")
    
    # Schedule a post for 1 hour from now
    future_time = datetime.now() + timedelta(hours=1)
    post_id1 = scheduler.schedule_post(
        content="Hello world! This is my first automated post! 🤖 #automation #socialmedia",
        platforms=["instagram", "facebook"],
        scheduled_time=future_time
    )
    
    # Schedule another post for tomorrow
    tomorrow = datetime.now() + timedelta(days=1)
    post_id2 = scheduler.schedule_post(
        content="Good morning! Starting the day with positive vibes! ☀️ #motivation #goodmorning",
        platforms=["instagram"],
        scheduled_time=tomorrow,
        media_url="https://example.com/sunrise.jpg"
    )
    
    print("\n" + "=" * 50)
    
    # Step 4: View scheduled posts
    print("📋 Viewing scheduled posts...")
    scheduler.get_scheduled_posts()
    
    print("\n" + "=" * 50)
    print("✨ Demo completed! Check the web interface at http://127.0.0.1:5000")
    print("💡 To cancel a post, use: scheduler.cancel_post(post_id)")


if __name__ == "__main__":
    example_usage()