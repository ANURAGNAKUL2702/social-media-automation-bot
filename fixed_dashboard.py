#!/usr/bin/env python3
"""
Fixed Dashboard Instagram Poster
This script creates a simple web interface that works properly with Instagram.
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime, timedelta
import threading
import time
import json
from instagrapi import Client
import schedule
import uuid
from PIL import Image, ImageDraw, ImageFont
from werkzeug.utils import secure_filename
import base64
from io import BytesIO

app = Flask(__name__)
CORS(app)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Global Instagram client
instagram_client = None
instagram_credentials = {
    'username': 'rishyashrunga',
    'password': '1234Gangamma'
}

class InstagramManager:
    def __init__(self):
        self.client = None
        self.logged_in = False
    
    def login(self):
        try:
            self.client = Client()
            self.client.login(instagram_credentials['username'], instagram_credentials['password'])
            self.logged_in = True
            print(f"✅ Instagram login successful for @{instagram_credentials['username']}")
            return True
        except Exception as e:
            print(f"❌ Instagram login failed: {e}")
            self.logged_in = False
            return False
    
    def post_content(self, content, image_path=None):
        if not self.logged_in:
            if not self.login():
                return False
        
        try:
            if image_path and os.path.exists(image_path):
                media = self.client.photo_upload(image_path, content)
            else:
                # Create a simple text image
                from PIL import Image, ImageDraw, ImageFont
                img = Image.new('RGB', (1080, 1080), color='white')
                draw = ImageDraw.Draw(img)
                try:
                    font = ImageFont.truetype("arial.ttf", 48)
                except:
                    font = ImageFont.load_default()
                
                # Add text to image
                y_pos = 400
                for line in content.split('\n')[:5]:  # Max 5 lines
                    if line.strip():
                        bbox = draw.textbbox((0, 0), line, font=font)
                        text_width = bbox[2] - bbox[0]
                        x = (1080 - text_width) // 2
                        draw.text((x, y_pos), line, fill='black', font=font)
                        y_pos += 60
                
                temp_path = f"temp_post_{int(time.time())}.jpg"
                img.save(temp_path, "JPEG")
                media = self.client.photo_upload(temp_path, content)
                os.remove(temp_path)
            
            print(f"✅ Post uploaded successfully! ID: {media.id}")
            return {
                'success': True,
                'post_id': media.id,
                'post_code': media.code,
                'url': f"https://www.instagram.com/p/{media.code}/"
            }
        except Exception as e:
            print(f"❌ Post upload failed: {e}")
            return {'success': False, 'error': str(e)}

# Global Instagram manager and scheduler
insta_manager = InstagramManager()
scheduled_posts = []  # Store scheduled posts

class PostScheduler:
    def __init__(self):
        self.scheduled_posts = []
        self.running = True
        self.scheduler_thread = threading.Thread(target=self.run_scheduler, daemon=True)
        self.scheduler_thread.start()
    
    def schedule_post(self, content, post_time, image_path=None):
        post_id = str(uuid.uuid4())
        scheduled_post = {
            'id': post_id,
            'content': content,
            'image_path': image_path,
            'scheduled_time': post_time,
            'status': 'scheduled',
            'created_at': datetime.now().isoformat()
        }
        self.scheduled_posts.append(scheduled_post)
        scheduled_posts.append(scheduled_post)  # Global list for API
        print(f"📅 Post scheduled for {post_time}")
        return post_id
    
    def run_scheduler(self):
        while self.running:
            current_time = datetime.now()
            posts_to_remove = []
            
            for post in self.scheduled_posts:
                scheduled_time = datetime.fromisoformat(post['scheduled_time'])
                if current_time >= scheduled_time and post['status'] == 'scheduled':
                    print(f"⏰ Executing scheduled post: {post['id']}")
                    result = insta_manager.post_content(
                        content=post['content'],
                        image_path=post.get('image_path')
                    )
                    if result.get('success'):
                        post['status'] = 'posted'
                        post['post_url'] = result.get('url', '')
                        print(f"✅ Scheduled post posted successfully!")
                    else:
                        post['status'] = 'failed'
                        post['error'] = result.get('error', 'Unknown error')
                        print(f"❌ Scheduled post failed: {post.get('error')}")
            
            time.sleep(30)  # Check every 30 seconds

# Initialize scheduler
post_scheduler = PostScheduler()

@app.route('/')
def dashboard():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Instagram Automation Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { text-align: center; margin-bottom: 30px; color: #333; }
        .status { padding: 15px; border-radius: 5px; margin: 20px 0; }
        .status.success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .status.error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        .form-group { margin: 20px 0; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: bold; color: #555; }
        .form-group textarea { width: 100%; min-height: 150px; padding: 10px; border: 2px solid #ddd; border-radius: 5px; font-size: 16px; }
        .form-group input[type="file"] { width: 100%; padding: 10px; border: 2px solid #ddd; border-radius: 5px; }
        .btn { background: #007bff; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; margin: 10px 5px; }
        .image-preview { max-width: 300px; max-height: 300px; margin: 10px 0; border-radius: 5px; border: 2px solid #ddd; }
        .upload-area { border: 2px dashed #ddd; border-radius: 5px; padding: 20px; text-align: center; background: #f8f9fa; }
        .btn:hover { background: #0056b3; }
        .btn.success { background: #28a745; }
        .btn.success:hover { background: #218838; }
        .account-info { background: #e9ecef; padding: 15px; border-radius: 5px; margin: 20px 0; }
        .post-result { background: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0; border-left: 4px solid #007bff; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Instagram Automation Dashboard</h1>
            <p>Automated posting for @rishyashrunga</p>
        </div>

        <div class="account-info">
            <h3>📱 Connected Account</h3>
            <p><strong>Username:</strong> @rishyashrunga</p>
            <p><strong>Status:</strong> <span id="connection-status">Ready to connect</span></p>
            <button class="btn" onclick="testConnection()">Test Connection</button>
        </div>

        <div class="form-group">
            <label for="image-upload">📸 Upload Image</label>
            <div class="upload-area">
                <input type="file" id="image-upload" accept="image/*" onchange="previewImage(event)">
                <p>Choose an image from your laptop or drag & drop here</p>
                <small>Supported: JPG, PNG, GIF (max 16MB)</small>
            </div>
            <div id="image-preview-container" style="display: none;">
                <img id="image-preview" class="image-preview" alt="Preview">
                <button class="btn" onclick="removeImage()" style="background: #dc3545;">Remove Image</button>
            </div>
        </div>

        <div class="form-group">
            <label for="post-content">📝 Post Caption</label>
            <textarea id="post-content" placeholder="Write your Instagram caption here...

You can include:
- Emojis 🎉
- Hashtags #automation #instagram
- Line breaks
- Mentions @username

Example:
🌟 Just automated my Instagram posting!
This is so cool and efficient! 

#automation #socialmedia #tech #rishyashrunga"></textarea>
        </div>

        <div class="form-group">
            <label for="schedule-time">⏰ Schedule Time (Optional)</label>
            <input type="datetime-local" id="schedule-time" style="width: 100%; padding: 10px; border: 2px solid #ddd; border-radius: 5px; font-size: 16px;">
            <small style="color: #666;">Leave empty for immediate posting</small>
        </div>

        <div style="text-align: center;">
            <button class="btn success" onclick="createPost()">📤 Post Now</button>
            <button class="btn" onclick="schedulePost()">⏰ Schedule Post</button>
            <button class="btn" onclick="showScheduledPosts()" style="background: #17a2b8;">📋 View Scheduled</button>
        </div>

        <div id="status-message"></div>
        <div id="post-result"></div>
        <div id="scheduled-posts" style="margin-top: 30px;"></div>
    </div>

    <script>
        function showStatus(message, type) {
            const statusDiv = document.getElementById('status-message');
            statusDiv.innerHTML = `<div class="status ${type}">${message}</div>`;
            setTimeout(() => statusDiv.innerHTML = '', 5000);
        }

        function testConnection() {
            document.getElementById('connection-status').innerHTML = 'Testing...';
            fetch('/api/test-connection', {method: 'POST'})
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        document.getElementById('connection-status').innerHTML = '✅ Connected';
                        showStatus('✅ Instagram connection successful!', 'success');
                    } else {
                        document.getElementById('connection-status').innerHTML = '❌ Failed';
                        showStatus('❌ Connection failed: ' + data.error, 'error');
                    }
                })
                .catch(error => {
                    document.getElementById('connection-status').innerHTML = '❌ Error';
                    showStatus('❌ Connection error: ' + error, 'error');
                });
        }

        function previewImage(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    document.getElementById('image-preview').src = e.target.result;
                    document.getElementById('image-preview-container').style.display = 'block';
                };
                reader.readAsDataURL(file);
            }
        }

        function removeImage() {
            document.getElementById('image-upload').value = '';
            document.getElementById('image-preview-container').style.display = 'none';
        }

        function createPost() {
            const content = document.getElementById('post-content').value.trim();
            const imageFile = document.getElementById('image-upload').files[0];
            
            if (!content && !imageFile) {
                showStatus('❌ Please enter a caption or upload an image!', 'error');
                return;
            }

            showStatus('📤 Uploading post to Instagram...', 'success');
            
            const formData = new FormData();
            formData.append('content', content);
            if (imageFile) {
                formData.append('image', imageFile);
            }
            
            fetch('/api/create-post', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showStatus('🎉 Post uploaded successfully!', 'success');
                    document.getElementById('post-result').innerHTML = `
                        <div class="post-result">
                            <h3>🎉 Post Created Successfully!</h3>
                            <p><strong>Post ID:</strong> ${data.post_id}</p>
                            <p><strong>URL:</strong> <a href="${data.url}" target="_blank">${data.url}</a></p>
                            <p><strong>View on Instagram:</strong> <a href="https://www.instagram.com/rishyashrunga/" target="_blank">@rishyashrunga</a></p>
                        </div>
                    `;
                    document.getElementById('post-content').value = '';
                    removeImage();
                } else {
                    showStatus('❌ Post failed: ' + data.error, 'error');
                }
            })
            .catch(error => {
                showStatus('❌ Upload error: ' + error, 'error');
            });
        }

        function schedulePost() {
            const content = document.getElementById('post-content').value.trim();
            const scheduleTime = document.getElementById('schedule-time').value;
            const imageFile = document.getElementById('image-upload').files[0];
            
            if (!content && !imageFile) {
                showStatus('❌ Please enter a caption or upload an image!', 'error');
                return;
            }
            
            if (!scheduleTime) {
                showStatus('❌ Please select a schedule time!', 'error');
                return;
            }
            
            showStatus('⏰ Scheduling your post...', 'success');
            
            const formData = new FormData();
            formData.append('content', content);
            formData.append('scheduledTime', scheduleTime);
            if (imageFile) {
                formData.append('image', imageFile);
            }
            
            fetch('/api/schedule-post', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showStatus('✅ ' + data.message, 'success');
                    document.getElementById('post-content').value = '';
                    document.getElementById('schedule-time').value = '';
                    removeImage();
                    showScheduledPosts(); // Refresh the scheduled posts list
                } else {
                    showStatus('❌ Scheduling failed: ' + data.error, 'error');
                }
            })
            .catch(error => {
                showStatus('❌ Scheduling error: ' + error, 'error');
            });
        }

        function showScheduledPosts() {
            fetch('/api/scheduled-posts')
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        displayScheduledPosts(data.posts);
                    } else {
                        showStatus('❌ Failed to load scheduled posts: ' + data.error, 'error');
                    }
                })
                .catch(error => {
                    showStatus('❌ Error loading scheduled posts: ' + error, 'error');
                });
        }

        function displayScheduledPosts(posts) {
            const container = document.getElementById('scheduled-posts');
            
            if (posts.length === 0) {
                container.innerHTML = '<div class="status">📅 No scheduled posts</div>';
                return;
            }
            
            let html = '<div style="background: #f8f9fa; padding: 20px; border-radius: 5px;"><h3>📅 Scheduled Posts</h3>';
            
            posts.forEach(post => {
                const scheduledTime = new Date(post.scheduled_time).toLocaleString();
                const status = post.status;
                const statusIcon = status === 'scheduled' ? '⏰' : status === 'posted' ? '✅' : '❌';
                
                html += `
                    <div style="border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; background: white;">
                        <p><strong>${statusIcon} Status:</strong> ${status.toUpperCase()}</p>
                        <p><strong>⏰ Scheduled:</strong> ${scheduledTime}</p>
                        <p><strong>📝 Content:</strong> ${post.content.substring(0, 100)}${post.content.length > 100 ? '...' : ''}</p>
                        ${status === 'scheduled' ? `<button class="btn" onclick="cancelPost('${post.id}')" style="background: #dc3545;">Cancel</button>` : ''}
                    </div>
                `;
            });
            
            html += '</div>';
            container.innerHTML = html;
        }

        function cancelPost(postId) {
            if (!confirm('Are you sure you want to cancel this scheduled post?')) {
                return;
            }
            
            fetch(`/api/cancel-post/${postId}`, {method: 'DELETE'})
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        showStatus('✅ Post cancelled successfully', 'success');
                        showScheduledPosts(); // Refresh the list
                    } else {
                        showStatus('❌ Failed to cancel post: ' + data.error, 'error');
                    }
                })
                .catch(error => {
                    showStatus('❌ Cancel error: ' + error, 'error');
                });
        }

        // Test connection on page load
        window.onload = function() {
            testConnection();
        };
    </script>
</body>
</html>
    '''

@app.route('/api/test-connection', methods=['POST'])
def test_connection():
    try:
        if insta_manager.login():
            return jsonify({'success': True, 'message': 'Instagram connection successful'})
        else:
            return jsonify({'success': False, 'error': 'Login failed'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/create-post', methods=['POST'])
def create_post():
    try:
        # Handle form data (with file upload)
        if 'content' in request.form:
            content = request.form.get('content', '')
            image_path = None
            
            # Handle uploaded image
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    # Add timestamp to avoid filename conflicts
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                    filename = timestamp + filename
                    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(image_path)
                    print(f"📷 Image uploaded: {filename}")
            
            # Post with uploaded image or text content
            result = insta_manager.post_content(content, image_path)
            
            # Clean up uploaded file after posting
            if image_path and os.path.exists(image_path):
                os.remove(image_path)
                
            return jsonify(result)
            
        # Handle JSON data (backward compatibility)
        elif request.json:
            data = request.json
            content = data.get('content', '')
            
            if not content:
                return jsonify({'success': False, 'error': 'No content provided'})
            
            result = insta_manager.post_content(content)
            return jsonify(result)
            
        else:
            return jsonify({'success': False, 'error': 'No content or image provided'})
        
    except Exception as e:
        print(f"🚫 Create post error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/schedule-post', methods=['POST'])
def schedule_post():
    try:
        # Handle form data (with file upload)
        if 'content' in request.form or 'image' in request.files:
            content = request.form.get('content', '')
            scheduled_time = request.form.get('scheduledTime', '')
            image_path = None
            
            # Handle uploaded image for scheduling
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    # Add timestamp to avoid filename conflicts
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                    filename = 'scheduled_' + timestamp + filename
                    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(image_path)
                    print(f"📷 Image saved for scheduling: {filename}")
            
            if not content and not image_path:
                return jsonify({
                    'success': False,
                    'error': 'Content or image is required'
                })
            
            if not scheduled_time:
                return jsonify({
                    'success': False,
                    'error': 'Scheduled time is required'
                })
            
            # Parse the scheduled time
            try:
                post_time = datetime.fromisoformat(scheduled_time.replace('T', ' ').replace('Z', ''))
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Invalid datetime format'
                })
            
            # Check if time is in the future
            if post_time <= datetime.now():
                # Clean up uploaded file if scheduling fails
                if image_path and os.path.exists(image_path):
                    os.remove(image_path)
                return jsonify({
                    'success': False,
                    'error': 'Scheduled time must be in the future'
                })
            
            post_id = post_scheduler.schedule_post(content, post_time.isoformat(), image_path)
            
            return jsonify({
                'success': True,
                'message': f'Post scheduled successfully for {post_time.strftime("%Y-%m-%d %H:%M")}',
                'post_id': post_id
            })
            
        # Handle JSON data (backward compatibility)
        elif request.json:
            data = request.json
            content = data.get('content', '')
            scheduled_time = data.get('scheduledTime', '')
            
            if not content or not scheduled_time:
                return jsonify({
                    'success': False,
                    'error': 'Content and scheduled time are required'
                })
            
            # Parse the scheduled time
            try:
                post_time = datetime.fromisoformat(scheduled_time.replace('T', ' ').replace('Z', ''))
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Invalid datetime format'
                })
            
            # Check if time is in the future
            if post_time <= datetime.now():
                return jsonify({
                    'success': False,
                    'error': 'Scheduled time must be in the future'
                })
            
            post_id = post_scheduler.schedule_post(content, post_time.isoformat())
            
            return jsonify({
                'success': True,
                'message': f'Post scheduled successfully for {post_time.strftime("%Y-%m-%d %H:%M")}',
                'post_id': post_id
            })
        
        else:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            })
        
    except Exception as e:
        print(f"🚫 Schedule error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/scheduled-posts', methods=['GET'])
def get_scheduled_posts():
    try:
        return jsonify({
            'success': True,
            'posts': scheduled_posts
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/cancel-post/<post_id>', methods=['DELETE'])
def cancel_scheduled_post(post_id):
    try:
        global scheduled_posts
        for post in scheduled_posts:
            if post['id'] == post_id and post['status'] == 'scheduled':
                post['status'] = 'cancelled'
                return jsonify({
                    'success': True,
                    'message': 'Post cancelled successfully'
                })
        
        return jsonify({
            'success': False,
            'error': 'Post not found or already processed'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    print('🚀 Starting Fixed Instagram Dashboard...')
    print('📱 Account: @rishyashrunga')
    print('🌐 Dashboard: http://127.0.0.1:5001')
    print('✅ Ready for Instagram automation!')
    app.run(host='127.0.0.1', port=5001, debug=False)