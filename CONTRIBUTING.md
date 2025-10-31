# Contributing to GitPeek

Thank you for your interest in contributing to GitPeek! This document provides guidelines and instructions for contributing.

## 🤝 Code of Conduct

Be respectful, inclusive, and professional in all interactions.

## 🚀 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/GitPeek.git
   cd GitPeek
   ```
3. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 💻 Development Setup

Follow the setup instructions in [README.md](README.md) to get your development environment running.

## 📝 Making Changes

### Backend Changes

1. Follow PEP 8 style guide
2. Add type hints to all functions
3. Write tests for new features
4. Update docstrings
5. Run tests: `pytest --cov=app`
6. Lint code: `ruff check app/`

### Frontend Changes

1. Follow the existing code style
2. Use TypeScript types properly
3. Write tests for components
4. Run tests: `npm test`
5. Lint code: `npm run lint`
6. Build to verify: `npm run build`

## 🧪 Testing

- **Backend:** Maintain 90%+ test coverage
- **Frontend:** Write tests for new components and features
- All tests must pass before submitting PR

## 📤 Submitting Changes

1. **Commit your changes:**
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```

2. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create a Pull Request** on GitHub

### PR Guidelines

- Provide a clear description of changes
- Reference any related issues
- Include screenshots for UI changes
- Ensure all tests pass
- Maintain or improve test coverage

## 🎯 Commit Message Format

Use conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

Example: `feat: add user profile page`

## 🐛 Reporting Bugs

1. Check if the bug is already reported in [Issues](https://github.com/yourusername/GitPeek/issues)
2. If not, create a new issue with:
   - Clear title
   - Detailed description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Environment details (OS, browser, etc.)

## 💡 Feature Requests

1. Check [Issues](https://github.com/yourusername/GitPeek/issues) for similar requests
2. Create a new issue describing:
   - The feature you'd like to see
   - Why it would be useful
   - Possible implementation approach

## 📚 Documentation

- Update README.md for user-facing changes
- Add docstrings for new functions/classes
- Update API documentation if endpoints change

## ⚡ Quick Tips

- Keep PRs focused on a single feature/fix
- Update tests when changing functionality
- Run the full test suite before submitting
- Ask questions if anything is unclear

## 📞 Questions?

Open an issue or reach out to the maintainers.

Thank you for contributing! 🎉

