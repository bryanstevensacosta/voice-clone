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
- Add XTTS-v2 model integration
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

## Gradio Hot Reload (Fast Development) 🔥

### What is Hot Reload?

Gradio's hot reload mode automatically reloads your UI when you make code changes, eliminating the need to manually stop and restart the server. This dramatically speeds up development.

### How to Use Hot Reload

Instead of running your app with Python:
```bash
# ❌ Old way (manual restart required)
python src/gradio_ui/app.py
```

Use the Gradio CLI:
```bash
# ✅ New way (automatic reload)
gradio src/gradio_ui/app.py

# Or with custom demo name
gradio src/gradio_ui/app.py --demo-name=app

# With custom port
gradio src/gradio_ui/app.py --server-port 8080
```

### What Gets Reloaded

When you save changes to any of these files, Gradio automatically reloads:
- `src/gradio_ui/app.py` - Main application
- `src/gradio_ui/handlers/*.py` - Event handlers
- `src/gradio_ui/utils/*.py` - Utilities
- Any imported modules

### Controlling Reload Behavior

Some code should only run once (like loading ML models). Use `gr.NO_RELOAD` to prevent re-execution:

```python
import gradio as gr
from voice_clone.model.generator import VoiceGenerator

# This code runs only once, not on every reload
if gr.NO_RELOAD:
    print("Loading model (one time only)...")
    generator = VoiceGenerator()
    print("Model loaded!")

def create_app():
    with gr.Blocks() as app:
        # UI code here - this WILL reload
        pass
    return app
```

**Use cases for `gr.NO_RELOAD`:**
- Loading ML models (Qwen3-TTS)
- Initializing database connections
- Loading large datasets
- Importing libraries with C/Rust extensions (numpy, tiktoken)

### Development Workflow with Hot Reload

1. **Start the app in reload mode**
   ```bash
   gradio src/gradio_ui/app.py
   ```

2. **Open in browser**
   ```
   http://localhost:7860
   ```

3. **Make changes to code**
   - Edit handlers, components, or layout
   - Save the file (Cmd+S / Ctrl+S)

4. **See changes instantly**
   - Gradio detects the change
   - Automatically reloads the app
   - Browser refreshes with new version

5. **Iterate quickly**
   - No need to stop/restart server
   - Focus on coding, not process management

### Watching Multiple Files

Gradio watches the directory containing your main file and automatically reloads when any Python file changes:

```
src/gradio_ui/
├── app.py                    # Watched ✓
├── handlers/
│   ├── sample_handler.py     # Watched ✓
│   ├── profile_handler.py    # Watched ✓
│   └── generation_handler.py # Watched ✓
└── utils/
    └── audio_viz.py          # Watched ✓
```

### Troubleshooting Hot Reload

**Problem**: Changes not reloading

**Solution**: Make sure you're using `gradio` command, not `python`:
```bash
# ❌ Won't hot reload
python src/gradio_ui/app.py

# ✅ Will hot reload
gradio src/gradio_ui/app.py
```

**Problem**: Demo not found error

**Solution**: Specify the demo name if it's not called `demo`:
```bash
# If your app variable is named 'app' instead of 'demo'
gradio src/gradio_ui/app.py --demo-name=app
```

**Problem**: Encoding errors

**Solution**: Specify encoding if not UTF-8:
```bash
gradio src/gradio_ui/app.py --encoding cp1252
```

**Problem**: Model reloads on every change (slow)

**Solution**: Wrap model loading in `if gr.NO_RELOAD:` block

### Jupyter Notebook Development

If you prefer Jupyter notebooks, use Gradio's magic command:

```python
# Load extension at top of notebook
%load_ext gradio

# In your demo cell
%%blocks
import gradio as gr

with gr.Blocks() as demo:
    gr.Markdown("# My Demo")
    # ... rest of your UI
```

Changes take effect when you re-run the cell.

### Vibe Mode (Experimental)

Gradio also offers "Vibe Mode" - an AI assistant that can edit your code:

```bash
gradio --vibe src/gradio_ui/app.py
```

**⚠️ Warning**: Vibe Mode allows arbitrary code execution. Use only for local development.

### Performance Tips

1. **Use `gr.NO_RELOAD` for expensive operations**
   - Model loading
   - Database connections
   - Large file reads

2. **Keep UI code separate from business logic**
   - Handlers in separate files
   - Easy to reload without affecting models

3. **Test with small changes first**
   - Verify reload is working
   - Then make larger changes

### Comparison: Manual vs Hot Reload

**Manual Restart (Old Way):**
```bash
# 1. Stop server (Ctrl+C)
# 2. Edit code
# 3. Save file
# 4. Restart server
python src/gradio_ui/app.py
# 5. Wait for model to load (~30s)
# 6. Refresh browser
# 7. Test changes
# Total time: ~45 seconds per change
```

**Hot Reload (New Way):**
```bash
# 1. Edit code
# 2. Save file
# 3. Gradio auto-reloads (~2s)
# 4. Test changes
# Total time: ~5 seconds per change
```

**Time saved**: ~40 seconds per change = ~10 minutes per hour of development!

### Integration with CLI

The CLI command `voice-clone ui` can also use hot reload:

```python
# In src/voice_clone/cli.py
@cli.command()
@click.option("--port", default=7860, help="Port to run the UI")
@click.option("--reload", is_flag=True, help="Enable hot reload")
def ui(port: int, reload: bool):
    """Launch the Gradio web interface."""
    if reload:
        import subprocess
        subprocess.run([
            "gradio",
            "src/gradio_ui/app.py",
            "--server-port", str(port)
        ])
    else:
        from gradio_ui.app import main
        main(server_port=port)
```

Usage:
```bash
# Normal mode
voice-clone ui

# Hot reload mode
voice-clone ui --reload
```

## Best Practices

1. **Always use virtual environment** - Never install packages globally
2. **Use hot reload during development** - Save time with automatic reloads
3. **Commit often** - Small, focused commits are better
4. **Write tests first** - TDD helps design better code
5. **Run pre-commit before pushing** - Catch issues early
6. **Keep dependencies minimal** - Only add what you need
7. **Document as you go** - Update docs with code changes
8. **Review your own PR** - Catch obvious issues before review
9. **Wrap expensive operations in `gr.NO_RELOAD`** - Prevent unnecessary reloading

## Resources

- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- [Gradio Hot Reload Guide](https://www.gradio.app/guides/developing-faster-with-reload-mode)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Black Documentation](https://black.readthedocs.io/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [MyPy Documentation](https://mypy.readthedocs.io/)
- [pytest Documentation](https://docs.pytest.org/)
- [Pre-commit Documentation](https://pre-commit.com/)
