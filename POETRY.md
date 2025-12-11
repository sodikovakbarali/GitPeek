# Poetry Setup Guide

This guide covers using Poetry for Python dependency management in GitPeek.

## 📦 What is Poetry?

Poetry is a modern dependency management and packaging tool for Python that:
- ✅ Resolves dependencies deterministically
- ✅ Creates reproducible builds
- ✅ Manages virtual environments automatically
- ✅ Replaces pip + virtualenv + requirements.txt

## 🚀 Installation

### Install Poetry

```bash
# Via official installer (recommended)
curl -sSL https://install.python-poetry.org | python3 -

# Via pip
pip install poetry

# Via homebrew (macOS)
brew install poetry
```

### Verify Installation

```bash
poetry --version
```

## 🏃 Quick Start

### 1. Navigate to Backend

```bash
cd backend
```

### 2. Install Dependencies

```bash
# Install all dependencies
poetry install

# Install only production dependencies
poetry install --only main

# Install with dev dependencies
poetry install --with dev
```

### 3. Activate Virtual Environment

```bash
# Activate the virtualenv
poetry shell

# Or run commands without activating
poetry run uvicorn app.main:app --reload
```

### 4. Run the Application

```bash
# Inside poetry shell
uvicorn app.main:app --reload

# Or without activating shell
poetry run uvicorn app.main:app --reload
```

## 📝 Common Commands

### Managing Dependencies

```bash
# Add a package
poetry add fastapi

# Add a dev dependency
poetry add --group dev pytest

# Add with version constraint
poetry add "requests>=2.28.0,<3.0.0"

# Remove a package
poetry remove httpx

# Update all packages
poetry update

# Update specific package
poetry update fastapi
```

### Working with Virtual Environments

```bash
# Show virtualenv info
poetry env info

# List all virtualenvs
poetry env list

# Remove virtualenv
poetry env remove python3.11

# Use specific Python version
poetry env use python3.11
```

### Lock File Management

```bash
# Update lock file without installing
poetry lock

# Update lock file and install
poetry lock --no-update

# Install from lock file
poetry install --no-root
```

### Running Commands

```bash
# Run Python script
poetry run python script.py

# Run tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=app

# Run linter
poetry run ruff check app/
```

### Exporting Dependencies

```bash
# Export to requirements.txt (for compatibility)
poetry export -f requirements.txt --output requirements.txt

# Export without hashes
poetry export -f requirements.txt --output requirements.txt --without-hashes

# Export dev dependencies too
poetry export -f requirements.txt --with dev --output requirements-dev.txt
```

## 🔧 Configuration

### pyproject.toml Structure

```toml
[tool.poetry]
name = "gitpeek-backend"
version = "1.0.0"
description = "GitPeek backend API"
authors = ["Your Name <you@example.com>"]

[tool.poetry.dependencies]
python = "^3.11"
fastapi = "0.109.0"
# ... more dependencies

[tool.poetry.group.dev.dependencies]
pytest = "7.4.4"
pytest-cov = "4.1.0"
# ... more dev dependencies

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

### Poetry Configuration

```bash
# Don't create virtualenv (useful in Docker)
poetry config virtualenvs.create false

# Create virtualenv in project directory
poetry config virtualenvs.in-project true

# Show configuration
poetry config --list
```

## 🐳 Using Poetry with Docker

Our Dockerfile already handles Poetry:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install poetry
RUN pip install poetry==1.7.1

# Configure poetry
RUN poetry config virtualenvs.create false

# Copy poetry files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install --no-interaction --no-ansi --only main

# Copy application
COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🔄 Migrating from requirements.txt

Already done! But here's how it works:

### 1. Create pyproject.toml from requirements.txt

```bash
# Install poetry
pip install poetry

# Initialize Poetry project
poetry init

# Add all dependencies from requirements.txt
cat requirements.txt | xargs -I {} poetry add {}
```

### 2. Organize Dependencies

```toml
[tool.poetry.dependencies]
python = "^3.11"
# Production dependencies here

[tool.poetry.group.dev.dependencies]
# Development dependencies here
```

### 3. Generate Lock File

```bash
poetry lock
```

### 4. Test Installation

```bash
poetry install
poetry run pytest
```

## 🎯 Best Practices

### 1. Always Commit poetry.lock

```bash
git add pyproject.toml poetry.lock
git commit -m "Update dependencies"
```

### 2. Use Version Constraints Wisely

```toml
# Exact version
package = "1.2.3"

# Compatible version (^)
package = "^1.2.3"  # >=1.2.3 <2.0.0

# Approximate version (~)
package = "~1.2.3"  # >=1.2.3 <1.3.0

# Wildcard
package = "1.2.*"   # >=1.2.0 <1.3.0
```

### 3. Separate Dev Dependencies

```bash
# Add to dev group
poetry add --group dev pytest pytest-cov ruff black

# Install without dev dependencies in production
poetry install --only main
```

### 4. Regular Updates

```bash
# Check for outdated packages
poetry show --outdated

# Update all packages
poetry update

# Update specific package
poetry update fastapi
```

### 5. Use Scripts

Add to `pyproject.toml`:

```toml
[tool.poetry.scripts]
start = "uvicorn app.main:app --reload"
test = "pytest --cov=app"
lint = "ruff check app/"
```

Then run:

```bash
poetry run start
poetry run test
poetry run lint
```

## 🐛 Troubleshooting

### Poetry Not Found

```bash
# Add to PATH (add to ~/.bashrc or ~/.zshrc)
export PATH="$HOME/.local/bin:$PATH"
```

### Lock File Out of Sync

```bash
# Regenerate lock file
poetry lock --no-update

# Or force update
poetry lock
```

### Dependency Conflicts

```bash
# Show dependency tree
poetry show --tree

# Update resolver
poetry update --lock
```

### Virtual Environment Issues

```bash
# Remove and recreate virtualenv
poetry env remove python3.11
poetry install
```

### Slow Dependency Resolution

```bash
# Use faster installer
poetry config installer.max-workers 10

# Clear cache
poetry cache clear pypi --all
```

## 📊 Comparison: requirements.txt vs Poetry

| Feature | requirements.txt | Poetry |
|---------|-----------------|--------|
| Dependency resolution | Manual | Automatic |
| Lock file | No | Yes (poetry.lock) |
| Dev dependencies | Separate file | Built-in groups |
| Version constraints | Basic | Advanced |
| Virtual env management | External | Built-in |
| Build system | setup.py | pyproject.toml |
| Reproducibility | Low | High |
| Speed | Fast install | Slower resolve, fast install |

## 🔗 Integration with Other Tools

### VS Code

Install Python extension and configure:

```json
{
  "python.poetryPath": "poetry",
  "python.terminal.activateEnvironment": true
}
```

### PyCharm

1. Go to Settings → Project → Python Interpreter
2. Click gear icon → Add
3. Select "Poetry Environment"
4. Choose existing environment or create new

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: poetry-check
        name: poetry-check
        entry: poetry check
        language: system
        pass_filenames: false
```

## 📚 Resources

- [Poetry Documentation](https://python-poetry.org/docs/)
- [Poetry GitHub](https://github.com/python-poetry/poetry)
- [PEP 518 – pyproject.toml](https://peps.python.org/pep-0518/)
- [Poetry Cheat Sheet](https://gist.github.com/CarlosDomingues/b88df15749af23a463148bd2c2b9b3fb)

## 💡 Tips

1. **Poetry is slower on first run** - it resolves all dependencies, but subsequent runs are fast
2. **Use `poetry.lock`** - commit it to git for reproducible builds
3. **Organize dependencies** - use groups for dev, test, docs, etc.
4. **Export for compatibility** - generate requirements.txt for tools that need it
5. **Update regularly** - run `poetry update` weekly to get security patches

---

**Need help?** Check the [main README](README.md) or open an issue on GitHub.

