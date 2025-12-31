# Social Media Automation Bot 🤖

A comprehensive social media automation platform that simplifies posting and scheduling across multiple platforms including Instagram, Twitter, and Facebook.

## Features ✨

- **Multi-Platform Support**: Automate posts across Instagram, Twitter, and Facebook
- **Smart Scheduling**: Schedule posts at optimal times for maximum engagement
- **Analytics Dashboard**: Track likes, shares, comments, and engagement rates
- **Engagement Tracking**: Monitor post performance across all platforms
- **Best Time Recommendations**: AI-powered suggestions for optimal posting times
- **User-Friendly Interface**: Intuitive web dashboard for managing all activities
- **Subscription Management**: Flexible pricing plans (Basic, Premium, Enterprise)
- **Secure Authentication**: JWT-based authentication system
- **API Integration Ready**: Modular architecture for easy third-party integrations

## Architecture 🏗️

The bot uses a modular architecture with the following components:

- **Backend (Python/Flask)**: RESTful API for all operations
- **Database (SQLAlchemy)**: User management, post scheduling, analytics storage
- **Scheduler (APScheduler)**: Background job scheduling for automated posting
- **Platform Integrations**: Modular connectors for social media platforms
- **Analytics Engine**: Performance tracking and insights generation
- **Frontend (HTML/CSS/JS)**: Interactive dashboard for user interactions

## Installation 🚀

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/ANURAGNAKUL2702/social-media-automation-bot.git
   cd social-media-automation-bot
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` file with your credentials:
   - Set your social media API credentials
   - Configure database settings
   - Set JWT secret keys

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the dashboard**
   Open your browser and navigate to `http://localhost:5000`

## Configuration ⚙️

### Environment Variables

Configure the following in your `.env` file:

```env
# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key

# Database
DATABASE_URL=sqlite:///social_media_bot.db

# Twitter API
TWITTER_API_KEY=your-twitter-api-key
TWITTER_API_SECRET=your-twitter-api-secret
TWITTER_ACCESS_TOKEN=your-access-token
TWITTER_ACCESS_SECRET=your-access-secret

# Facebook API
FACEBOOK_ACCESS_TOKEN=your-facebook-token
FACEBOOK_PAGE_ID=your-page-id

# Instagram
INSTAGRAM_USERNAME=your-username
INSTAGRAM_PASSWORD=your-password

# JWT
JWT_SECRET_KEY=your-jwt-secret
JWT_EXPIRATION_HOURS=24
```

## Usage 📖

### 1. Register an Account
- Navigate to the registration page
- Choose a subscription plan (Basic, Premium, or Enterprise)
- Complete the registration form

### 2. Connect Social Media Accounts
- Go to the "Accounts" section
- Add your social media account credentials
- Verify the connection

### 3. Schedule Posts
- Navigate to "Schedule Post"
- Enter your post content
- Select target platforms
- Choose the scheduled time
- Add media (optional)
- Click "Schedule Post"

### 4. View Analytics
- Access the "Analytics" dashboard
- View performance metrics
- Check platform breakdown
- Get best posting time recommendations

## API Documentation 📚

### Authentication

#### Register User
```
POST /api/auth/register
Body: {
  "username": "string",
  "email": "string",
  "password": "string",
  "subscription_plan": "basic|premium|enterprise"
}
```

#### Login
```
POST /api/auth/login
Body: {
  "username": "string",
  "password": "string"
}
```

### Posts

#### Schedule Post
```
POST /api/posts
Headers: Authorization: Bearer <token>
Body: {
  "content": "string",
  "platforms": ["twitter", "facebook", "instagram"],
  "scheduled_time": "ISO8601 datetime",
  "media_url": "string (optional)"
}
```

#### Get All Posts
```
GET /api/posts
Headers: Authorization: Bearer <token>
```

#### Delete Post
```
DELETE /api/posts/<post_id>
Headers: Authorization: Bearer <token>
```

### Analytics

#### Get Analytics Summary
```
GET /api/analytics/summary?days=30
Headers: Authorization: Bearer <token>
```

#### Get Best Posting Times
```
GET /api/analytics/best-times
Headers: Authorization: Bearer <token>
```

### Accounts

#### Get Connected Accounts
```
GET /api/accounts
Headers: Authorization: Bearer <token>
```

#### Add Account
```
POST /api/accounts
Headers: Authorization: Bearer <token>
Body: {
  "platform": "twitter|facebook|instagram",
  "account_name": "string",
  "credentials": "string (JSON)"
}
```

## Subscription Plans 💳

### Basic ($9.99/month)
- 100 posts per month
- 2 platforms
- Basic analytics
- Email support

### Premium ($29.99/month)
- 500 posts per month
- 5 platforms
- Advanced analytics
- Priority support
- Best time recommendations

### Enterprise ($99.99/month)
- Unlimited posts
- Unlimited platforms
- Full analytics suite
- 24/7 support
- Custom integrations
- API access

## Technology Stack 💻

- **Backend**: Python, Flask
- **Database**: SQLAlchemy (SQLite/PostgreSQL)
- **Scheduler**: APScheduler
- **Authentication**: JWT (PyJWT)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **API Integration**: Tweepy, Facebook SDK, Instagrapi

## Project Structure 📁

```
social-media-automation-bot/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
├── backend/
│   ├── config.py              # Configuration management
│   ├── core/
│   │   ├── scheduler.py       # Post scheduling engine
│   │   ├── post_handler.py    # Post publishing handler
│   │   └── analytics.py       # Analytics tracking
│   ├── integrations/
│   │   ├── twitter_integration.py
│   │   ├── facebook_integration.py
│   │   └── instagram_integration.py
│   ├── models/
│   │   └── database.py        # Database models
│   └── utils/
│       └── helpers.py         # Utility functions
└── frontend/
    ├── static/
    │   ├── css/
    │   │   └── styles.css     # Styling
    │   └── js/
    │       └── app.js         # Frontend logic
    └── templates/
        └── index.html         # Main dashboard

```

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## Security 🔒

- Never commit your `.env` file or sensitive credentials
- Use strong passwords and API keys
- Enable 2FA on your social media accounts
- Regularly update dependencies
- Review security advisories

## License 📄

This project is licensed under the MIT License.

## Support 💬

For support, please email support@example.com or create an issue in the GitHub repository.

## Roadmap 🗺️

- [ ] Add support for LinkedIn and TikTok
- [ ] Implement content recommendation system
- [ ] Add image editing integration (Canva)
- [ ] Mobile app development
- [ ] Advanced AI-powered analytics
- [ ] Team collaboration features
- [ ] Webhook support for external integrations

## Acknowledgments 🙏

Built with ❤️ for content creators, businesses, and social media managers worldwide.