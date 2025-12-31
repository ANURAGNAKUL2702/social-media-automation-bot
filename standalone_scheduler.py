#!/usr/bin/env python3
"""
Standalone Instagram Post Scheduler
Works without Flask server - Direct Instagram posting and scheduling.
"""

import sys
import os
import json
import sqlite3
from datetime import datetime, timedelta
from threading import Timer
import time

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.integrations.instagram_integration import InstagramIntegration

class StandaloneScheduler:
    def __init__(self):
        self.db_path = "standalone_scheduler.db"
        self.init_database()
        
        # Your Instagram credentials
        class Config:
            INSTAGRAM_USERNAME = "rishyashrunga"
            INSTAGRAM_PASSWORD = "1234Gangamma"
        
        self.config = Config()
        self.instagram = InstagramIntegration(self.config)
        
    def init_database(self):
        """Initialize SQLite database for storing scheduled posts."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scheduled_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                scheduled_time TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                posted_at TEXT
            )
        ''')
        conn.commit()
        conn.close()
        
    def schedule_post(self, content, scheduled_time):
        """Schedule a post for future posting."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO scheduled_posts (content, scheduled_time) VALUES (?, ?)",
            (content, scheduled_time.isoformat())
        )
        post_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Calculate delay
        delay = (scheduled_time - datetime.now()).total_seconds()
        if delay > 0:
            timer = Timer(delay, self.execute_post, [post_id])
            timer.start()
            print(f"✅ Post scheduled for {scheduled_time}")
            print(f"📝 Content: {content[:50]}...")
            print(f"🆔 Post ID: {post_id}")
        else:
            print("❌ Cannot schedule posts in the past")
            
        return post_id
    
    def execute_post(self, post_id):
        """Execute a scheduled post."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get post details
        cursor.execute("SELECT content FROM scheduled_posts WHERE id = ? AND status = 'pending'", (post_id,))
        result = cursor.fetchone()
        
        if not result:
            print(f"❌ Post {post_id} not found or already posted")
            conn.close()
            return
        
        content = result[0]
        
        try:
            print(f"📤 Posting to Instagram... (Post ID: {post_id})")
            success = self.instagram.post(content)
            
            if success:
                # Update status
                cursor.execute(
                    "UPDATE scheduled_posts SET status = 'posted', posted_at = ? WHERE id = ?",
                    (datetime.now().isoformat(), post_id)
                )
                print(f"✅ Successfully posted to Instagram! Post ID: {post_id}")
            else:
                cursor.execute(
                    "UPDATE scheduled_posts SET status = 'failed' WHERE id = ?",
                    (post_id,)
                )
                print(f"❌ Failed to post to Instagram. Post ID: {post_id}")
                
        except Exception as e:
            print(f"❌ Error posting: {str(e)}")
            cursor.execute(
                "UPDATE scheduled_posts SET status = 'failed' WHERE id = ?",
                (post_id,)
            )
        
        conn.commit()
        conn.close()
    
    def list_posts(self):
        """List all scheduled posts."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM scheduled_posts ORDER BY scheduled_time")
        posts = cursor.fetchall()
        conn.close()
        
        if not posts:
            print("📋 No scheduled posts found.")
            return
        
        print("📋 Scheduled Posts:")
        print("=" * 60)
        for post in posts:
            id, content, scheduled_time, status, created_at, posted_at = post
            print(f"🆔 ID: {id}")
            print(f"📝 Content: {content[:50]}...")
            print(f"⏰ Scheduled: {scheduled_time}")
            print(f"📊 Status: {status}")
            if posted_at:
                print(f"✅ Posted: {posted_at}")
            print("-" * 40)
    
    def cancel_post(self, post_id):
        """Cancel a scheduled post."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM scheduled_posts WHERE id = ? AND status = 'pending'", (post_id,))
        if cursor.rowcount > 0:
            print(f"✅ Post {post_id} cancelled successfully")
        else:
            print(f"❌ Post {post_id} not found or already processed")
        conn.commit()
        conn.close()

def main():
    """Main interactive function."""
    print("🚀 Standalone Instagram Scheduler for @rishyashrunga")
    print("=" * 60)
    print("✅ No Flask server required!")
    print("📱 Direct Instagram posting")
    print("=" * 60)
    
    scheduler = StandaloneScheduler()
    
    if scheduler.instagram.client is None:
        print("❌ Failed to connect to Instagram. Please check your credentials.")
        return
    
    print("✅ Connected to Instagram successfully!")
    
    while True:
        print("\n📱 Instagram Scheduler Menu:")
        print("1. Schedule a post")
        print("2. Schedule immediate post (test)")
        print("3. List scheduled posts")
        print("4. Cancel a post")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            content = input("📝 Enter post content: ")
            
            print("\n⏰ When to schedule?")
            print("1. In 1 minute (test)")
            print("2. In 1 hour")
            print("3. Tomorrow at 9 AM")
            print("4. Custom date/time")
            
            time_choice = input("Choose option (1-4): ").strip()
            
            if time_choice == "1":
                scheduled_time = datetime.now() + timedelta(minutes=1)
            elif time_choice == "2":
                scheduled_time = datetime.now() + timedelta(hours=1)
            elif time_choice == "3":
                tomorrow = datetime.now() + timedelta(days=1)
                scheduled_time = tomorrow.replace(hour=9, minute=0, second=0, microsecond=0)
            elif time_choice == "4":
                date_str = input("Enter date/time (YYYY-MM-DD HH:MM): ")
                try:
                    scheduled_time = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
                except ValueError:
                    print("❌ Invalid date format")
                    continue
            else:
                print("❌ Invalid choice")
                continue
            
            scheduler.schedule_post(content, scheduled_time)
            
        elif choice == "2":
            content = input("📝 Enter post content: ")
            post_time = datetime.now() + timedelta(seconds=5)
            scheduler.schedule_post(content, post_time)
            print("🧪 Test post will be published in 5 seconds!")
            
        elif choice == "3":
            scheduler.list_posts()
            
        elif choice == "4":
            scheduler.list_posts()
            try:
                post_id = int(input("Enter post ID to cancel: "))
                scheduler.cancel_post(post_id)
            except ValueError:
                print("❌ Invalid post ID")
                
        elif choice == "5":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1-5.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Scheduler stopped by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")