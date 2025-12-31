#!/usr/bin/env python3
"""
Instagram Direct Post Script for rishyashrunga
Create and post directly to Instagram without the dashboard.
"""

from instagrapi import Client
from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime

def create_instagram_post():
    """Create and post to Instagram directly"""
    
    print("🚀 Instagram Direct Posting for @rishyashrunga")
    print("=" * 50)
    
    # Instagram credentials
    username = "rishyashrunga"
    password = "1234Gangamma"
    
    print(f"📱 Connecting to Instagram account: @{username}")
    
    try:
        # Initialize Instagram client
        client = Client()
        
        # Login to Instagram
        print("🔑 Logging in...")
        client.login(username, password)
        print("✅ Login successful!")
        
        # Create post content
        caption = f"""🎉 New Year's Eve 2025! 

Ready to make 2026 absolutely amazing! 
Excited for all the new opportunities and adventures ahead! 

#NewYear2026 #Goals #MotivatedLife #Success #2025Memories #Grateful
#rishyashrunga #NewBeginnings #Inspiration

Posted automatically on: {datetime.now().strftime('%Y-%m-%d at %H:%M')}"""
        
        print("🎨 Creating post image...")
        
        # Create a beautiful New Year image
        img_width, img_height = 1080, 1080
        image = Image.new('RGB', (img_width, img_height), color='#1a1a2e')  # Dark blue
        draw = ImageDraw.Draw(image)
        
        # Try to use a nice font, fallback to default
        try:
            title_font = ImageFont.truetype("arial.ttf", 72)
            subtitle_font = ImageFont.truetype("arial.ttf", 48)
            date_font = ImageFont.truetype("arial.ttf", 36)
        except:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            date_font = ImageFont.load_default()
        
        # Add gradient-like effect
        for i in range(img_height):
            color_val = int(26 + (i / img_height) * 50)  # Gradient from dark to lighter
            draw.line([(0, i), (img_width, i)], fill=(color_val, color_val, min(color_val + 20, 100)))
        
        # Add text content
        texts = [
            ("🎉 HAPPY NEW YEAR! 🎉", title_font, "#FFD700", 200),
            ("2026 Here We Come!", subtitle_font, "#FFFFFF", 320),
            ("Ready for New Adventures", subtitle_font, "#87CEEB", 420),
            ("& Amazing Opportunities!", subtitle_font, "#87CEEB", 520),
            ("", None, None, 600),
            ("@rishyashrunga", date_font, "#FFD700", 700),
            (datetime.now().strftime("%B %d, %Y"), date_font, "#CCCCCC", 780),
        ]
        
        for text, font, color, y_pos in texts:
            if text and font and color:
                # Get text dimensions for centering
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                x = (img_width - text_width) // 2
                draw.text((x, y_pos), text, fill=color, font=font)
        
        # Add decorative elements
        # Stars
        for star_x, star_y in [(200, 150), (880, 180), (150, 850), (900, 820), (500, 100)]:
            draw.text((star_x, star_y), "⭐", fill="#FFD700", font=subtitle_font)
        
        # Save the image
        temp_path = "new_year_2026_post.jpg"
        image.save(temp_path, "JPEG", quality=95)
        print(f"✅ Image created: {temp_path}")
        
        # Upload to Instagram
        print("📤 Uploading to Instagram...")
        print(f"📝 Caption preview: {caption[:100]}...")
        
        # Confirm before posting
        confirm = input("\n🤔 Do you want to post this to Instagram? (y/N): ").lower().strip()
        
        if confirm in ['y', 'yes']:
            media = client.photo_upload(temp_path, caption=caption)
            
            print(f"\n🎉 SUCCESS! Post uploaded to Instagram!")
            print(f"📱 Post ID: {media.id}")
            print(f"🔗 Post URL: https://www.instagram.com/p/{media.code}/")
            print(f"👀 View your post at: https://www.instagram.com/{username}/")
            
            # Clean up
            os.remove(temp_path)
            print(f"🧹 Temporary file cleaned up")
            
        else:
            print("🛑 Post cancelled by user")
            os.remove(temp_path)
            print(f"🧹 Temporary file cleaned up")
        
        # Logout
        client.logout()
        print("🔐 Logged out from Instagram")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\n💡 Possible solutions:")
        print("   1. Check if username and password are correct")
        print("   2. Check if Instagram account has two-factor authentication")
        print("   3. Try logging in manually to Instagram first")
        
        # Clean up on error
        if 'temp_path' in locals() and os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == "__main__":
    create_instagram_post()