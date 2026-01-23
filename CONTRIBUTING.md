# Contributing to Voice Clone CLI

Thank you for your interest in contributing to Voice Clone CLI! This document provides guidelines and instructions for contributing to this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Commit Message Format](#commit-message-format)
- [Pull Request Process](#pull-request-process)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)

## Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow. Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing.

## How Can I Contribute?

### Reporting Bugs

Before creating a bug report, please check the [issue tracker](https://github.com/yourusername/voice-clone-cli/issues) to avoid duplicates.

When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the issue
- **Expected behavior** vs actual behavior
- **System information**:
  - OS (macOS, Linux, Windows)
  - Python version
  - Package versions (`pip list`)
- **Error messages** and stack traces
- **Sample files** if relevant (audio samples, config files)

**Example bug report:**

```markdown
**Bug**: Audio processing fails with stereo files

**Steps to reproduce:**
1. Run `voice-clone train --samples data/stereo/`
2. Observe error

**Expected**: Should process stereo files
**Actual**: Crashes with "ValueError: expected mono audio"

**System**: macOS 13.0, Python 3.10.8
**Error**: [paste full error here]
```

### Suggesting Features

Feature suggestions are welcome! Please:

1. Check if the feature already exists or is planned
2. Open an issue with the "feature request" label
3. Describe the feature and its use case
4. Explain why it would be valuable to users
5. Provide examples of how it would work

### Contributing Code

We welcome code contributions! Here's how:

1. **Fork** the repository
2. **Create** a feature branch
3. **Make** your changes
4. **Test** your changes
5. **Commit** using conventional commits
6. **Push** to your fork
7. **Open** a Pull Request

## Development Setup

### Prerequisites

- Python 3.9, 3.10, or 3.11
- Git
- pip (comes with Python)

### Quick Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/voice-clone-cli.git
cd voice-clone-cli

# Add upstream remote
git remote add upstream https://github.com/yourusername/voice-clone-cli.git

# Run automated setup
./setup.sh
```

### Manual Setup

```bash
# Create virtual environment
python3.10 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
pre-commit install --hook-type commit-msg
pre-commit install --hook-type pre-push
```

### Verify Setup

```bash
# Check Python version
python --version

# Run pre-commit checks
pre-commit run --all-files

# Run tests
pytest
```

## Coding Standards

### Code Style

We use automated tools to maintain consistent code style:

- **Black** (code formatter) - Line length: 88 characters
- **Ruff** (linter) - Fast Python linter
- **MyPy** (type checker) - Static type checking

These tools run automatically via pre-commit hooks.

### Python Style Guidelines

```python
# Good: Type hints, docstrings, clear names
def process_audio(file_path: str, sample_rate: int = 22050) -> np.ndarray:
    """
    Process audio file and return normalized waveform.

    Args:
        file_path: Path to audio file
        sample_rate: Target sample rate in Hz

    Returns:
        Normalized audio waveform as numpy array

    Raises:
        FileNotFoundError: If audio file doesn't exist
        ValueError: If audio format is unsupported
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Audio file not found: {file_path}")

    # Load and process audio
    waveform = load_audio(file_path, sample_rate)
    return normalize_audio(waveform)


# Bad: No types, no docstring, unclear names
def proc(f, sr=22050):
    w = load(f, sr)
    return norm(w)
```

### Best Practices

1. **Type hints**: Use type hints for all function signatures
2. **Docstrings**: Write clear docstrings for public functions/classes
3. **Error handling**: Handle errors gracefully with informative messages
4. **Logging**: Use logging instead of print statements
5. **Constants**: Use UPPER_CASE for constants
6. **Naming**: Use descriptive names (no single letters except loop counters)
7. **Functions**: Keep functions small and focused (single responsibility)
8. **Comments**: Write comments for complex logic, not obvious code

### Code Organization

```python
# Standard library imports
import os
import sys
from pathlib import Path
from typing import List, Optional

# Third-party imports
import numpy as np
import torch
from TTS.api import TTS

# Local imports
from voice_clone.audio import load_audio
from voice_clone.config import Config
```

## Commit Message Format

We use [Conventional Commits](https://www.conventionalcommits.org/) for clear commit history.

### Format

```
type(scope): description

[optional body]

[optional footer]
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, missing semicolons, etc.)
- `refactor`: Code refactoring (no functional changes)
- `test`: Adding or updating tests
- `chore`: Maintenance tasks (dependencies, build, etc.)
- `perf`: Performance improvements
- `ci`: CI/CD changes
- `build`: Build system changes

### Scope (Optional)

The scope specifies what part of the codebase is affected:

- `audio`: Audio processing
- `model`: Model management
- `cli`: CLI interface
- `config`: Configuration
- `tests`: Test suite

### Examples

```bash
# Simple feature
git commit -m "feat: add voice cloning functionality"

# Bug fix with scope
git commit -m "fix(audio): resolve stereo to mono conversion issue"

# Documentation update
git commit -m "docs: update installation instructions for Windows"

# Multi-line commit with body
git commit -m "feat(cli): add interactive mode

- Implement REPL interface
- Add command history
- Support multi-line input

Closes #42"

# Breaking change
git commit -m "feat(api)!: change synthesize function signature

BREAKING CHANGE: synthesize() now requires model_path as first argument"
```

### Commit Message Rules

- **Subject line**: 50 characters or less
- **Body lines**: 72 characters or less
- **Imperative mood**: "add feature" not "added feature"
- **No period**: Don't end subject with a period
- **Capitalize**: Start subject with capital letter

The commit-msg hook will validate your commit messages automatically.

## Pull Request Process

### Before Submitting

1. **Update from upstream**:
   ```bash
   git fetch upstream
   git rebase upstream/master
   ```

2. **Run all checks**:
   ```bash
   make pre-commit  # or: pre-commit run --all-files
   make test
   ```

3. **Update documentation** if needed

4. **Add tests** for new features

### Creating a Pull Request

1. **Push to your fork**:
   ```bash
   git push origin feat/your-feature
   ```

2. **Open PR** on GitHub

3. **Fill out PR template**:
   - Description of changes
   - Related issues
   - Type of change (feature, bugfix, etc.)
   - Testing performed
   - Checklist completion

### PR Title Format

Use conventional commit format:

```
feat: add voice cloning functionality
fix: resolve audio processing bug
docs: update contributing guidelines
```

### PR Description Template

```markdown
## Description
Brief description of what this PR does.

## Related Issues
Closes #123
Relates to #456

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] All tests passing
- [ ] Manual testing performed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests added that prove fix/feature works
- [ ] Dependent changes merged
```

### Review Process

1. **Automated checks** must pass (CI, linting, tests)
2. **Code review** by maintainers
3. **Address feedback** if requested
4. **Approval** from at least 1 maintainer
5. **Merge** by maintainers (squash merge)

### After Merge

1. **Delete your branch**:
   ```bash
   git branch -d feat/your-feature
   git push origin --delete feat/your-feature
   ```

2. **Update your fork**:
   ```bash
   git checkout master
   git pull upstream master
   git push origin master
   ```

## Testing Guidelines

### Writing Tests

Place tests in `tests/` directory with `test_*.py` naming:

```python
# tests/test_audio.py
import pytest
import numpy as np
from voice_clone.audio import load_audio, normalize_audio


def test_load_audio_mono():
    """Test loading mono audio file."""
    waveform = load_audio("tests/fixtures/mono.wav")
    assert waveform.ndim == 1
    assert len(waveform) > 0


def test_load_audio_stereo_converts_to_mono():
    """Test that stereo audio is converted to mono."""
    waveform = load_audio("tests/fixtures/stereo.wav")
    assert waveform.ndim == 1


def test_normalize_audio():
    """Test audio normalization."""
    audio = np.array([0.5, 1.0, -0.5, -1.0])
    normalized = normalize_audio(audio)
    assert normalized.max() <= 1.0
    assert normalized.min() >= -1.0


def test_load_audio_invalid_file():
    """Test that invalid file raises appropriate error."""
    with pytest.raises(FileNotFoundError):
        load_audio("nonexistent.wav")


@pytest.fixture
def sample_audio():
    """Fixture providing sample audio for tests."""
    return np.random.randn(22050)  # 1 second at 22050 Hz


def test_with_fixture(sample_audio):
    """Test using fixture."""
    normalized = normalize_audio(sample_audio)
    assert len(normalized) == len(sample_audio)
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=voice_clone --cov-report=term-missing

# Run specific test file
pytest tests/test_audio.py

# Run specific test
pytest tests/test_audio.py::test_load_audio_mono

# Run with verbose output
pytest -v

# Run and stop on first failure
pytest -x

# Run only failed tests from last run
pytest --lf
```

### Test Coverage

- **Minimum coverage**: 70%
- **Target coverage**: 80%+
- Pre-push hook will fail if coverage is below 70%

### What to Test

✅ **Do test**:
- Core functionality
- Edge cases
- Error conditions
- Input validation
- Integration points

❌ **Don't test**:
- Third-party libraries
- Trivial getters/setters
- Private implementation details

## Documentation

### Docstring Format

Use Google-style docstrings:

```python
def synthesize_speech(
    text: str,
    model_path: str,
    output_path: str,
    speed: float = 1.0,
    temperature: float = 0.7,
) -> None:
    """
    Synthesize speech from text using trained voice model.

    This function generates audio from input text using a pre-trained
    voice cloning model. The output is saved as a WAV file.

    Args:
        text: Input text to synthesize
        model_path: Path to trained voice model directory
        output_path: Path where output audio will be saved
        speed: Speech speed multiplier (default: 1.0)
        temperature: Sampling temperature for generation (default: 0.7)
            Higher values (>1.0) increase randomness
            Lower values (<1.0) make output more deterministic

    Returns:
        None. Audio is saved to output_path.

    Raises:
        FileNotFoundError: If model_path doesn't exist
        ValueError: If text is empty or speed/temperature out of range
        RuntimeError: If synthesis fails

    Example:
        >>> synthesize_speech(
        ...     text="Hello, world!",
        ...     model_path="models/my_voice",
        ...     output_path="output.wav",
        ...     speed=1.2
        ... )
    """
    pass
```

### Updating Documentation

When making changes, update relevant documentation:

- **README.md**: For user-facing changes
- **docs/**: For detailed guides
- **Docstrings**: For API changes
- **CHANGELOG.md**: For all changes

## Questions?

- 💬 Open a [Discussion](https://github.com/yourusername/voice-clone-cli/discussions)
- 🐛 Create an [Issue](https://github.com/yourusername/voice-clone-cli/issues)
- 📧 Email: bryanstevensacosta@gmail.com

## Recognition

Contributors will be recognized in:
- GitHub contributors page
- CHANGELOG.md for significant contributions
- README.md for major features

Thank you for contributing! 🎉
