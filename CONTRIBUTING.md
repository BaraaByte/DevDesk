# Contributing to DevDesk

Thank you for your interest in contributing to DevDesk! We welcome contributions of all kinds.

## How to Contribute

### 1. Report Issues
Found a bug? Open an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your system info (OS, Python/Node versions)

### 2. Suggest Features
Have an idea? Open an issue with the `[FEATURE]` tag and describe:
- The feature and why it's useful
- How it would work
- Any potential implementation approaches

### 3. Improve Documentation
Documentation improvements are always welcome:
- Fix typos and unclear explanations
- Add examples and tutorials
- Improve API documentation

### 4. Create Plugins
Build and share custom widgets!
- See [PLUGIN_GUIDE.md](plugins/PLUGIN_GUIDE.md)
- Test thoroughly before submitting
- Include examples and documentation

### 5. Code Improvements
Help us improve the codebase:
- Refactor and optimize code
- Improve error handling
- Add tests
- Performance improvements

## Development Setup

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Coding Standards

### Frontend (TypeScript/React)
- Use functional components with hooks
- Follow Prettier formatting
- Add TypeScript types for everything
- Use Emotion for styling

### Backend (Python)
- Follow PEP 8
- Use type hints
- Document functions with docstrings
- Add async/await for I/O operations

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages (`git commit -m "feat: add new widget"`)
6. Push to your fork
7. Open a pull request with:
   - Clear title and description
   - Link to related issues
   - List of changes
   - Screenshots (if UI changes)

## Commit Message Format

```
<type>: <subject>

<body>
<footer>
```

Types: feat, fix, docs, style, refactor, test, chore

Example:
```
feat: add CPU temperature widget

Add real-time CPU temperature monitoring using lm_sensors.
Works on Linux systems with hwmon support.

Closes #42
```

## Questions?

Open a discussion or reach out on GitHub!

**Together, we're building something amazing! 🚀**
