#!/usr/bin/env python3
"""
Instagram Post Validation Script for rishyashrunga
This script will register your account, add Instagram credentials, and test posting.
"""

import requests
import json
from datetime import datetime, timedelta

class InstagramValidator:
    def __init__(self, base_url="http://127.0.0.1:5000"):
        self.base_url = base_url
        self.token = None
        self.username = "rishyashrunga_bot"  # Bot account name
        self.email = "rishyashrunga@example.com"
        self.password = "secure_bot_password123"
        
        # Your Instagram credentials
        self.instagram_username = "rishyashrunga"
        self.instagram_password = "1234Gangamma"
    
    def register_and_login(self):
        """Register bot account and get token."""
        print("🔑 Setting up your bot account...")
        
        # Try to register
        register_url = f"{self.base_url}/api/auth/register"
        register_data = {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "subscription_plan": "basic"
        }
        
        response = requests.post(register_url, json=register_data)
        
        if response.status_code == 200:
            result = response.json()
            self.token = result['data']['token']
            print(f"✅ Bot account registered successfully!")
            return True
        else:
            # Try to login if registration failed (user might already exist)
            print("🔄 Account exists, trying to login...")
            login_url = f"{self.base_url}/api/auth/login"
            login_data = {
                "username": self.username,
                "password": self.password
            }
            
            response = requests.post(login_url, json=login_data)
            if response.status_code == 200:
                result = response.json()
                self.token = result['data']['token']
                print(f"✅ Login successful!")
                return True
            else:
                print(f"❌ Login failed: {response.json()}")
                return False
    
    def add_instagram_account(self):
        """Add your Instagram account to the bot."""
        if not self.token:
            print("❌ Please login first!")
            return False
        
        print("📱 Adding your Instagram account...")
        
        url = f"{self.base_url}/api/accounts"
        headers = {"Authorization": f"Bearer {self.token}"}
        data = {
            "platform": "instagram",
            "account_name": f"{self.instagram_username}_account",
            "credentials": {
                "username": self.instagram_username,
                "password": self.instagram_password
            }
        }
        
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            print(f"✅ Instagram account '{self.instagram_username}' connected successfully!")
            return True
        else:
            print(f"❌ Failed to connect Instagram account: {response.json()}")
            return False
    
    def schedule_test_post(self):
        """Schedule a test post to validate Instagram posting."""
        if not self.token:
            print("❌ Please login first!")
            return False
        
        print("🧪 Scheduling test post...")
        
        # Schedule post for 2 minutes from now to test quickly
        test_time = datetime.now() + timedelta(minutes=2)
        
        url = f"{self.base_url}/api/posts"
        headers = {"Authorization": f"Bearer {self.token}"}
        data = {
            "content": "🧪 Test post from Social Media Bot! This is automated posting validation. #SocialMediaBot #TestPost #Automation",
            "platforms": ["instagram"],
            "scheduled_time": test_time.isoformat()
        }
        
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            post_id = result['data']['id']
            print(f"✅ Test post scheduled successfully!")
            print(f"📅 Post ID: {post_id}")
            print(f"⏰ Scheduled for: {test_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"📱 Platform: Instagram")
            print(f"📝 Content: Test post from Social Media Bot!")
            return post_id
        else:
            print(f"❌ Failed to schedule test post: {response.json()}")
            return None
    
    def check_scheduled_posts(self):
        """Check all scheduled posts."""
        if not self.token:
            print("❌ Please login first!")
            return []
        
        url = f"{self.base_url}/api/posts"
        headers = {"Authorization": f"Bearer {self.token}"}
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            posts = response.json()['data']
            print(f"📋 You have {len(posts)} scheduled posts:")
            for post in posts:
                print(f"  • ID: {post['id']}")
                print(f"    Content: {post['content'][:50]}...")
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

def main():
    """Main validation workflow."""
    print("🚀 Instagram Posting Validation for rishyashrunga")
    print("=" * 60)
    
    validator = InstagramValidator()
    
    # Step 1: Register and login
    if not validator.register_and_login():
        print("❌ Failed to setup bot account. Exiting.")
        return
    
    print("\n" + "=" * 60)
    
    # Step 2: Add Instagram account
    if not validator.add_instagram_account():
        print("❌ Failed to connect Instagram account. Exiting.")
        return
    
    print("\n" + "=" * 60)
    
    # Step 3: Schedule test post
    post_id = validator.schedule_test_post()
    if not post_id:
        print("❌ Failed to schedule test post. Exiting.")
        return
    
    print("\n" + "=" * 60)
    
    # Step 4: Show all scheduled posts
    print("📋 Current scheduled posts:")
    validator.check_scheduled_posts()
    
    print("\n" + "=" * 60)
    print("🎉 Validation Complete!")
    print("✅ Your Instagram account is connected and ready for posting")
    print("⏰ Test post scheduled for 2 minutes from now")
    print("🌐 Monitor progress at: http://127.0.0.1:5000")
    print("\n💡 Commands you can try:")
    print(f"   • Cancel test post: validator.cancel_post({post_id})")
    print("   • Check post status: validator.check_scheduled_posts()")
    
    # Interactive menu
    print("\n" + "=" * 60)
    while True:
        choice = input("\nChoose an option:\n1. Check posts\n2. Cancel test post\n3. Schedule another post\n4. Exit\nEnter choice (1-4): ")
        
        if choice == "1":
            validator.check_scheduled_posts()
        elif choice == "2":
            validator.cancel_post(post_id)
        elif choice == "3":
            content = input("Enter post content: ")
            minutes = int(input("Schedule in how many minutes? "))
            schedule_time = datetime.now() + timedelta(minutes=minutes)
            
            url = f"{validator.base_url}/api/posts"
            headers = {"Authorization": f"Bearer {validator.token}"}
            data = {
                "content": content,
                "platforms": ["instagram"],
                "scheduled_time": schedule_time.isoformat()
            }
            
            response = requests.post(url, json=data, headers=headers)
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Post scheduled! ID: {result['data']['id']}")
            else:
                print(f"❌ Failed: {response.json()}")
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1-4.")

if __name__ == "__main__":
    main()