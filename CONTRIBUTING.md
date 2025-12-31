# Contributing to Social Media Automation Bot

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Report any inappropriate behavior

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version)
   - Screenshots if applicable

### Suggesting Features

1. Check existing issues for similar suggestions
2. Create a new issue with:
   - Clear description of the feature
   - Use case and benefits
   - Possible implementation approach

### Code Contributions

1. **Fork the Repository**
   ```bash
   git clone https://github.com/ANURAGNAKUL2702/social-media-automation-bot.git
   cd social-media-automation-bot
   ```

2. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Your Changes**
   - Follow existing code style
   - Add comments for complex logic
   - Update documentation if needed
   - Add tests for new features

4. **Test Your Changes**
   ```bash
   # Run existing tests
   python -m pytest tests/
   
   # Test manually
   python app.py
   ```

5. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "Add: brief description of changes"
   ```

6. **Push and Create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then create a PR on GitHub

## Development Guidelines

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Keep functions small and focused
- Add docstrings to functions and classes

### Project Structure

```
backend/
├── core/          # Core functionality (scheduler, analytics)
├── integrations/  # Platform integrations
├── models/        # Database models
└── utils/         # Helper functions

frontend/
├── static/        # CSS, JS, images
└── templates/     # HTML templates
```

### Adding New Platform Integration

1. Create new file in `backend/integrations/`
2. Follow existing integration patterns
3. Implement required methods:
   - `__init__()`: Initialize client
   - `post()`: Post content
   - `validate_credentials()`: Check credentials
4. Update `post_handler.py` to include new platform
5. Add configuration in `config.py`
6. Update frontend UI to support platform

### Testing

- Write tests for new features
- Ensure existing tests pass
- Test with different configurations
- Test error handling

## Pull Request Process

1. Update README.md if needed
2. Update documentation
3. Add entry to CHANGELOG (if exists)
4. Ensure CI/CD passes
5. Request review from maintainers
6. Address review feedback
7. Wait for approval and merge

## Areas Needing Contribution

Current priorities:
- [ ] LinkedIn integration
- [ ] TikTok integration
- [ ] Content recommendation system
- [ ] Image editing features
- [ ] Mobile responsive improvements
- [ ] Performance optimizations
- [ ] Additional analytics metrics
- [ ] Webhook support
- [ ] Team collaboration features

## Questions?

- Open an issue for questions
- Join discussions in existing issues
- Contact maintainers

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Acknowledged in README

Thank you for helping improve the Social Media Automation Bot! 🙏
