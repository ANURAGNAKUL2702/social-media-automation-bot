# Quick Start Guide

## Get Started in 5 Minutes!

### 1. Clone the Repository
```bash
git clone https://github.com/ANURAGNAKUL2702/social-media-automation-bot.git
cd social-media-automation-bot
```

### 2. Run Setup Script (Recommended)
```bash
chmod +x setup.sh
./setup.sh
```

### 3. Configure API Keys
Edit `.env` file with your social media API credentials:
```bash
nano .env  # or use your preferred editor
```

### 4. Start the Application
```bash
python app.py
```

### 5. Access the Dashboard
Open your browser and navigate to:
```
http://localhost:5000
```

## First Time User Guide

### Creating Your Account
1. Click "Register" on the login page
2. Fill in your details
3. Choose a subscription plan:
   - **Basic**: $9.99/month - Perfect for individuals
   - **Premium**: $29.99/month - Great for small businesses
   - **Enterprise**: $99.99/month - For agencies and large teams

### Connecting Social Media Accounts
1. Navigate to "Accounts" section
2. Click "+ Connect New Account"
3. Select platform (Twitter, Facebook, or Instagram)
4. Enter your credentials
5. Click "Connect"

### Scheduling Your First Post
1. Go to "Schedule Post"
2. Write your content
3. Select platforms (can select multiple)
4. Choose date and time
5. Add media URL (optional)
6. Click "Schedule Post"

### Viewing Analytics
1. Navigate to "Analytics" section
2. View your performance metrics:
   - Total likes, shares, and comments
   - Engagement rates
   - Platform breakdown
3. Check "Best Posting Times" for recommendations

## Troubleshooting

### Common Issues

**Application won't start**
- Ensure Python 3.8+ is installed
- Check if all dependencies are installed: `pip install -r requirements.txt`
- Verify .env file exists and has correct format

**Can't connect social media accounts**
- Verify API credentials in .env file
- Check if APIs are enabled in respective developer portals
- Ensure credentials have necessary permissions

**Posts not being scheduled**
- Check if scheduled time is in the future
- Verify connected accounts are active
- Check application logs for errors

### Getting Help

- Read full documentation in README.md
- Check GitHub issues
- Contact support (if using paid plan)

## Tips for Success

1. **Start Small**: Begin with scheduling 1-2 posts to test the system
2. **Use Best Times**: Follow the AI recommendations for optimal engagement
3. **Track Analytics**: Review performance weekly to improve strategy
4. **Keep Credentials Secure**: Never share your .env file
5. **Regular Updates**: Keep the application updated for best performance

## Next Steps

Once you're comfortable with basic features:

1. Explore advanced scheduling options
2. Set up recurring posts
3. Integrate with third-party tools (coming soon)
4. Use analytics to optimize content strategy
5. Upgrade plan if you need more features

---

Happy Automating! 🚀
