# Contributing to NECTA Analysis Dashboard

Thank you for your interest in contributing to the NECTA Analysis Dashboard! This document provides guidelines and instructions for contributing.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Submitting Changes](#submitting-changes)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)

## Code of Conduct

### Our Pledge
We are committed to providing a welcoming and inclusive experience for everyone. We expect all contributors to:
- Be respectful and considerate
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards others

### Unacceptable Behavior
- Harassment or discriminatory language
- Trolling or insulting comments
- Publishing others' private information
- Any conduct that would be inappropriate in a professional setting

## How to Contribute

### Types of Contributions We Welcome

1. **Bug Reports** - Help us identify and fix issues
2. **Feature Suggestions** - Ideas for new functionality
3. **Code Contributions** - Bug fixes, new features, optimizations
4. **Documentation** - Improvements to guides and comments
5. **Testing** - Help test new features and report issues
6. **Translations** - Help make the app accessible to more users

## Development Setup

### Prerequisites
- Python 3.8 or higher
- Git
- Basic understanding of Streamlit and web scraping

### Setting Up Development Environment

1. **Fork the repository** (if hosted on GitHub)
   ```bash
   # Fork via GitHub UI, then clone your fork
   git clone https://github.com/YOUR-USERNAME/necta-analysis-dashboard.git
   cd necta-analysis-dashboard
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   
   # On Linux/Mac:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a development branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

5. **Run the application**
   ```bash
   streamlit run necta_analysis_app.py
   ```

## Coding Standards

### Python Style Guide
We follow PEP 8 with some flexibility:
- Use 4 spaces for indentation
- Maximum line length: 100 characters (flexible for readability)
- Use descriptive variable names
- Add docstrings to functions and classes

### Code Structure
```python
def function_name(param1, param2):
    """
    Brief description of what the function does.
    
    Args:
        param1 (type): Description of param1
        param2 (type): Description of param2
    
    Returns:
        type: Description of return value
    """
    # Implementation
    pass
```

### Best Practices
- Write clear, self-documenting code
- Add comments for complex logic
- Keep functions focused and small
- Use type hints where beneficial
- Handle exceptions appropriately
- Validate user inputs

## Submitting Changes

### Before Submitting
- [ ] Test your changes thoroughly
- [ ] Update documentation if needed
- [ ] Add comments to complex code
- [ ] Ensure code follows style guidelines
- [ ] Test with both Quick and Full Analysis modes
- [ ] Verify download functionality works

### Pull Request Process

1. **Update your branch**
   ```bash
   git fetch origin
   git rebase origin/main
   ```

2. **Commit your changes**
   ```bash
   git add .
   git commit -m "Brief description of changes"
   ```
   
   **Good commit messages:**
   - "Add regional filter to subject analysis"
   - "Fix GPA calculation for schools with no Division I"
   - "Update documentation for installation on Windows"
   
   **Bad commit messages:**
   - "Fixed stuff"
   - "Update"
   - "Changes"

3. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

4. **Create a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Fill in the PR template with:
     - Description of changes
     - Related issue number (if applicable)
     - Screenshots (if UI changes)
     - Testing performed

### Pull Request Template
```markdown
## Description
Brief description of changes

## Related Issue
Fixes #(issue number)

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing Performed
- [ ] Tested with Quick Analysis
- [ ] Tested with Full Analysis
- [ ] Tested downloads
- [ ] Tested filters
- [ ] Verified visualizations

## Screenshots (if applicable)
Add screenshots here

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have added comments to complex code
- [ ] I have updated the documentation
- [ ] My changes don't break existing functionality
```

## Reporting Bugs

### Before Reporting
1. Check if the bug has already been reported
2. Try to reproduce the bug consistently
3. Test with the latest version

### Bug Report Template
```markdown
## Bug Description
Clear description of what's wrong

## Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See error

## Expected Behavior
What you expected to happen

## Actual Behavior
What actually happened

## Screenshots
If applicable, add screenshots

## Environment
- OS: [e.g., Windows 10, Ubuntu 20.04]
- Python Version: [e.g., 3.9.5]
- Browser: [e.g., Chrome 96]
- App Version/Commit: [e.g., main branch]

## Additional Context
Any other relevant information
```

## Suggesting Features

### Feature Request Template
```markdown
## Feature Description
Clear description of the proposed feature

## Problem It Solves
What problem does this feature address?

## Proposed Solution
How should this feature work?

## Alternative Solutions
Other approaches you've considered

## Use Cases
Who would benefit and how?

## Additional Context
Mockups, examples, or references
```

### Good Feature Suggestions
- Align with project goals
- Are clearly described
- Solve real user problems
- Are technically feasible
- Consider user experience

## Development Guidelines

### Adding New Features

1. **Plan the feature**
   - Define scope clearly
   - Consider edge cases
   - Think about user experience
   - Plan for error handling

2. **Implement incrementally**
   - Start with core functionality
   - Add features step by step
   - Test each step

3. **Add tests**
   - Test normal cases
   - Test edge cases
   - Test error conditions

4. **Update documentation**
   - Update README if needed
   - Update USER_GUIDE
   - Add inline comments

### Working with Web Scraping

**Important Considerations:**
- Respect NECTA's servers - implement rate limiting
- Handle network errors gracefully
- Cache data when appropriate
- Don't overload the server with requests
- Follow robots.txt guidelines

**Rate Limiting:**
```python
import time

# Add delay between requests
time.sleep(0.5)  # 500ms delay
```

### Working with Visualizations

**Best Practices:**
- Keep charts simple and clear
- Use consistent color schemes
- Add descriptive titles and labels
- Make charts responsive
- Consider color-blind accessibility

## Areas for Contribution

### Current Priorities
1. Performance optimization for large datasets
2. Additional visualization types
3. Export format improvements
4. Mobile responsiveness
5. Error handling improvements

### Easy Issues for Beginners
Look for issues labeled:
- `good first issue`
- `documentation`
- `help wanted`

### Advanced Contributions
- Database integration for caching
- Advanced statistical analysis
- Machine learning predictions
- API development
- Mobile app version

## Testing

### Manual Testing Checklist
- [ ] Quick Analysis mode works
- [ ] Full Analysis mode works
- [ ] Custom Selection works
- [ ] All tabs display correctly
- [ ] Filters function properly
- [ ] Downloads work (CSV and Excel)
- [ ] Charts are interactive
- [ ] Error messages are clear
- [ ] Progress indicators work

### Testing Different Scenarios
- Test with slow internet
- Test with many schools selected
- Test with filters applied
- Test download with large datasets
- Test on different browsers
- Test on different screen sizes

## Community

### Getting Help
- Review existing documentation first
- Check closed issues for similar problems
- Ask clear, specific questions
- Provide context and examples

### Staying Updated
- Watch the repository for updates
- Read commit messages
- Check the changelog
- Participate in discussions

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing to making education data more accessible in Tanzania! 🇹🇿

## Questions?

If you have questions about contributing, feel free to:
- Open an issue with the `question` label
- Check existing documentation
- Reach out to maintainers

---

**Remember:** Every contribution, no matter how small, is valuable and appreciated! 🎉
