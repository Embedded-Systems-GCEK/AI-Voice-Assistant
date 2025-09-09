# 🤝 Contributing to AI Voice Assistant (Cyrus)

Thank you for your interest in contributing to the AI Voice Assistant project! This guide outlines how our team members can contribute effectively based on their roles.

## 🎯 Team Structure

### 👨‍💻 Developers
**Team Members:** @Nivedh-r, @dhanashyam18, @AmayaPramod, @AbhayaGovind

**Responsibilities:**
- Core feature development and implementation
- Bug fixes and performance optimization
- Code reviews and architecture decisions
- Integration with AI services (Cohere, Ollama)
- Speech recognition and TTS implementation

### 🧪 Testers
**Team Members:** @Sneha-SJ-05, @MeenakshiPoyyil

**Responsibilities:**
- Manual and automated testing
- Bug reporting and verification
- Test case development
- Performance testing
- User acceptance testing
- Documentation testing

### 🎨 Designers
**Team Members:** @vyshnav8486, @aruncs31s

**Responsibilities:**
- User experience design
- Documentation design and formatting
- UI/UX for any visual components
- Project branding and presentation
- User interaction flow design

## 🚀 Getting Started

### Prerequisites
1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/AI-Voice-Assistant.git`
3. Set up the development environment: `python install.py`
4. Verify setup: `python test_setup.py`
5. Test basic functionality: `python demo.py`

### Development Workflow

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the coding standards below
   - Test your changes thoroughly
   - Update documentation if needed

3. **Test your changes**
   ```bash
   # Run setup verification
   python test_setup.py
   
   # Test demo mode
   python demo.py
   
   # Test full functionality (if dependencies are installed)
   python src/app.py
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "type: brief description of changes"
   ```

5. **Push and create a pull request**
   ```bash
   git push origin feature/your-feature-name
   ```

## 📝 Coding Standards

### Python Code Style
- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions small and focused
- Use type hints where appropriate

### Commit Message Format
Use conventional commit format:
```
type(scope): description

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation changes
- test: Testing improvements
- refactor: Code refactoring
- style: Code formatting
- chore: Maintenance tasks
```

### Example Commit Messages
- `feat(ai): add Ollama integration for offline responses`
- `fix(tts): resolve Piper TTS path issues on Linux`
- `docs(readme): update installation instructions`
- `test(setup): add comprehensive setup verification`

## 🐛 Bug Reporting

### For Testers
When reporting bugs, include:

1. **Environment Details**
   - Operating System (Windows/Linux/macOS)
   - Python version
   - Installation method used

2. **Steps to Reproduce**
   - Clear, numbered steps
   - Expected vs actual behavior
   - Screenshots/logs if applicable

3. **Setup Verification**
   - Run `python test_setup.py` and include results
   - Specify which components are working/failing

### Bug Report Template
Use the existing bug report template in `.github/ISSUE_TEMPLATE/bug_report.md`

## 🧪 Testing Guidelines

### For Testers
1. **Manual Testing Checklist**
   - [ ] Installation process (all methods)
   - [ ] Demo mode functionality
   - [ ] Voice recognition (if dependencies installed)
   - [ ] TTS functionality
   - [ ] AI responses (both online and offline)
   - [ ] Error handling and recovery
   - [ ] Cross-platform compatibility

2. **Test Documentation**
   - Document test cases and results
   - Report both successful tests and failures
   - Verify fixes for reported bugs

3. **Performance Testing**
   - Response time measurements
   - Memory usage monitoring
   - Resource consumption analysis

## 🎨 Design Guidelines

### For Designers
1. **Documentation Design**
   - Ensure README is clear and visually appealing
   - Use proper markdown formatting
   - Include relevant emojis and badges
   - Maintain consistent formatting style

2. **User Experience**
   - Design clear error messages
   - Plan intuitive interaction flows
   - Consider accessibility requirements
   - Focus on user-friendly setup process

3. **Branding**
   - Maintain consistent project identity
   - Design logos or visual assets if needed
   - Ensure professional presentation

## 📋 Role-Specific Contribution Areas

### Developers
- `src/` directory - Core application code
- `install.py` - Installation automation
- `requirements.txt` - Dependency management
- Integration improvements
- Performance optimizations

### Testers
- `test_setup.py` - Setup verification
- Issue reporting and verification
- Testing documentation
- Quality assurance processes

### Designers
- `README.md` - Documentation design
- Issue templates and forms
- User interaction design
- Project presentation materials

## 🔄 Review Process

1. **Pull Request Requirements**
   - Clear description of changes
   - Reference related issues
   - Include test results
   - Update documentation if needed

2. **Review Assignments**
   - Developers review code changes
   - Testers verify functionality
   - Designers review documentation/UX changes

3. **Approval Process**
   - At least one approval from relevant team
   - All tests must pass
   - No conflicts with main branch

## 🆘 Getting Help

- **GitHub Issues**: For bug reports and feature requests
- **Discussions**: For questions and general discussion
- **Team Communication**: Direct contact with team members

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project.

---

Thank you for contributing to the AI Voice Assistant project! 🎉