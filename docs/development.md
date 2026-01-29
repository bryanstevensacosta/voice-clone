# Development Guide

This guide covers the development setup and workflow for the Voice Clone CLI project.

## Table of Contents

- [Environment Setup](#environment-setup)
- [Development Workflow](#development-workflow)
- [Code Quality Tools](#code-quality-tools)
- [Testing](#testing)
- [Git Workflow](#git-workflow)
- [Troubleshooting](#troubleshooting)

## Environment Setup

### Prerequisites

- Python 3.10 (recommended)
- Git
- pip (comes with Python)

### Why Virtual Environments?

We use Python's built-in `venv` for dependency isolation because:

1. **Isolation**: Keeps project dependencies separate from system Python
2. **Reproducibility**: Ensures consistent environments across developers
3. **No conflicts**: Prevents version conflicts with other Python projects
4. **Lightweight**: Native to Python, no additional tools needed
5. **Standard**: Industry standard for Python projects

### Automated Setup

The easiest way to set up your development environment:

```bash
./setup.sh
```

This script will:
1. Check Python 3.10 is installed
2. Create a virtual environment in `venv/`
3. Activate the virtual environment
4. Upgrade pip to the latest version
5. Install all development dependencies
6. Install pre-commit hooks

### Manual Setup

If you prefer to set up manually or need more control:

#### 1. Create Virtual Environment

```bash
# Using Python 3.10 (recommended)
python3.10 -m venv venv

# Or using default python3
python3 -m venv venv
```

#### 2. Activate Virtual Environment

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```cmd
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

#### 3. Upgrade pip

```bash
pip install --upgrade pip
```

#### 4. Install Development Dependencies

```bash
# Core development tools
pip install pre-commit black ruff mypy pytest pytest-cov

# Install project in editable mode (when available)
pip install -e ".[dev]"
```

#### 5. Install Pre-commit Hooks

```bash
pre-commit install
pre-commit install --hook-type commit-msg
pre-commit install --hook-type pre-push
```

### Verify Installation

```bash
# Check Python version
python --version

# Check installed packages
pip list

# Test pre-commit
pre-commit run --all-files
```

## Development Workflow

### Daily Workflow

1. **Activate virtual environment**
   ```bash
   source venv/bin/activate
   ```

2. **Pull latest changes**
   ```bash
   git pull origin master
   ```

3. **Create feature branch**
   ```bash
   git checkout -b feat/your-feature-name
   ```

4. **Make your changes**
   - Write code
   - Write tests
   - Update documentation

5. **Run quality checks**
   ```bash
   make pre-commit
   # or
   pre-commit run --all-files
   ```

6. **Run tests**
   ```bash
   make test
   # or
   pytest
   ```

7. **Commit changes**
   ```bash
   git add .
   git commit -m "feat: add your feature"
   ```

8. **Push and create PR**
   ```bash
   git push origin feat/your-feature-name
   ```

### Using Make Commands

We provide a `Makefile` with common commands:

```bash
make help          # Show all available commands
make setup         # Run automated setup
make test          # Run tests with coverage
make test-fast     # Run tests without coverage
make lint          # Run linter
make format        # Format code
make type-check    # Run type checker
make pre-commit    # Run all pre-commit hooks
make clean         # Clean generated files
```

## Code Quality Tools

### Black (Code Formatter)

Black automatically formats your code to a consistent style.

```bash
# Format all code
black src/ tests/

# Check without modifying
black --check src/ tests/

# Format specific file
black src/voice_clone/audio.py
```

**Configuration**: See `[tool.black]` in `pyproject.toml`

### Ruff (Linter)

Ruff is a fast Python linter that catches common errors and style issues.

```bash
# Lint all code
ruff check src/ tests/

# Auto-fix issues
ruff check --fix src/ tests/

# Lint specific file
ruff check src/voice_clone/audio.py
```

**Configuration**: See `[tool.ruff]` in `pyproject.toml`

### MyPy (Type Checker)

MyPy performs static type checking to catch type-related bugs.

```bash
# Type check all code
mypy src/

# Type check specific file
mypy src/voice_clone/audio.py
```

**Configuration**: See `[tool.mypy]` in `pyproject.toml`

### Pre-commit Hooks

Pre-commit hooks run automatically before commits and pushes:

**On every commit:**
- Black formatting
- Ruff linting
- MyPy type checking
- Trailing whitespace removal
- End-of-file fixing
- YAML validation
- Large file detection
- Merge conflict detection
- Private key detection

**On commit message:**
- Conventional Commits validation

**On push:**
- Full test suite with coverage

```bash
# Run all hooks manually
pre-commit run --all-files

# Run specific hook
pre-commit run black --all-files

# Update hooks to latest versions
pre-commit autoupdate

# Skip hooks (not recommended)
git commit --no-verify
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=voice_clone --cov-report=term-missing

# Run specific test file
pytest tests/test_audio.py

# Run specific test
pytest tests/test_audio.py::test_load_audio

# Run with verbose output
pytest -v

# Run and stop on first failure
pytest -x
```

### Writing Tests

Place tests in the `tests/` directory with the naming convention `test_*.py`.

```python
# tests/test_example.py
import pytest
from voice_clone.example import example_function

def test_example_function():
    """Test that example_function works correctly."""
    result = example_function("input")
    assert result == "expected_output"

def test_example_function_error():
    """Test that example_function raises error on invalid input."""
    with pytest.raises(ValueError):
        example_function(None)
```

### Coverage Requirements

- Minimum coverage: 70%
- Pre-push hook will fail if coverage is below threshold
- View coverage report: `open htmlcov/index.html`

## Git Workflow

### Branch Naming

- `feat/feature-name` - New features
- `fix/bug-description` - Bug fixes
- `docs/what-changed` - Documentation updates
- `refactor/what-changed` - Code refactoring
- `test/what-added` - Test additions

### Commit Messages

We use [Conventional Commits](https://www.conventionalcommits.org/):

**Format:**
```
type(scope): description

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `perf`: Performance improvements
- `ci`: CI/CD changes
- `build`: Build system changes

**Examples:**
```bash
git commit -m "feat: add voice cloning functionality"
git commit -m "fix: resolve audio processing bug in stereo files"
git commit -m "docs: update installation instructions for macOS"
git commit -m "test: add unit tests for audio loader"
```

**Multi-line commits:**
```bash
git commit -m "feat: add voice cloning functionality

- Implement audio sample processing
- Add Qwen3-TTS model integration
- Create CLI interface for cloning

Closes #123"
```

### Pull Request Process

1. Create feature branch from `master`
2. Make changes and commit using conventional commits
3. Push branch to remote
4. Create Pull Request on GitHub
5. Wait for CI checks to pass
6. Request review from maintainers
7. Address review feedback
8. Merge when approved

## Troubleshooting

### Virtual Environment Issues

**Problem**: `command not found: python3.10`

**Solution**: Install Python 3.10 using pyenv or your system package manager:
```bash
# Using pyenv
pyenv install 3.10
pyenv local 3.10

# Using Homebrew (macOS)
brew install python@3.10
```

**Problem**: Virtual environment not activating

**Solution**: Make sure you're in the project directory and run:
```bash
source venv/bin/activate
```

**Problem**: Wrong Python version in venv

**Solution**: Delete and recreate the virtual environment:
```bash
rm -rf venv
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Pre-commit Issues

**Problem**: Pre-commit hooks not running

**Solution**: Reinstall hooks:
```bash
pre-commit uninstall
pre-commit install
pre-commit install --hook-type commit-msg
pre-commit install --hook-type pre-push
```

**Problem**: Hook installation fails with `core.hooksPath` error

**Solution**: Unset the Git config:
```bash
git config --unset-all core.hooksPath
pre-commit install
```

**Problem**: Hooks are too slow

**Solution**: Pre-commit caches environments. First run is slow, subsequent runs are fast.

### Testing Issues

**Problem**: Tests fail with import errors

**Solution**: Install project in editable mode:
```bash
pip install -e .
```

**Problem**: Coverage below threshold

**Solution**: Add more tests or adjust threshold in `pyproject.toml`

### Dependency Issues

**Problem**: Package conflicts

**Solution**: Recreate virtual environment:
```bash
deactivate
rm -rf venv
./setup.sh
```

## Best Practices

1. **Always use virtual environment** - Never install packages globally
2. **Commit often** - Small, focused commits are better
3. **Write tests first** - TDD helps design better code
4. **Run pre-commit before pushing** - Catch issues early
5. **Keep dependencies minimal** - Only add what you need
6. **Document as you go** - Update docs with code changes
7. **Review your own PR** - Catch obvious issues before review

## Resources

- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Black Documentation](https://black.readthedocs.io/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [MyPy Documentation](https://mypy.readthedocs.io/)
- [pytest Documentation](https://docs.pytest.org/)
- [Pre-commit Documentation](https://pre-commit.com/)
