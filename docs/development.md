# Development Guide

This guide covers the development setup and workflow for TTS Studio.

## Table of Contents

- [Project Structure](#project-structure)
- [Environment Setup](#environment-setup)
- [Development Workflow](#development-workflow)
- [Code Quality Tools](#code-quality-tools)
- [Testing](#testing)
- [Git Workflow](#git-workflow)
- [Troubleshooting](#troubleshooting)

## Project Structure

TTS Studio uses a **monorepo** structure with **hexagonal architecture**:

```
tts-studio/
├── apps/
│   ├── core/              # Python library (hexagonal architecture)
│   │   ├── src/
│   │   │   ├── domain/    # Business logic (NO external dependencies)
│   │   │   ├── app/       # Use cases (orchestration)
│   │   │   ├── infra/     # Adapters (implementations)
│   │   │   └── api/       # Python API (entry point)
│   │   ├── tests/
│   │   │   ├── domain/    # Domain tests (mocks only)
│   │   │   ├── app/       # Application tests (mocked ports)
│   │   │   ├── infra/     # Infrastructure tests (real adapters)
│   │   │   ├── integration/  # End-to-end tests
│   │   │   └── pbt/       # Property-based tests
│   │   ├── setup.py
│   │   ├── pyproject.toml
│   │   └── requirements.txt
│   └── desktop/           # Tauri desktop app (coming soon)
├── config/                # Configuration files
├── data/                  # Data directory (gitignored)
├── docs/                  # Documentation
└── examples/              # Usage examples
```

### Hexagonal Architecture Layers

**Domain Layer** (`apps/core/src/domain/`):
- Pure business logic
- NO external dependencies
- Defines ports (interfaces)
- Contains models, services, exceptions

**Application Layer** (`apps/core/src/app/`):
- Use cases (orchestration)
- DTOs (data transfer objects)
- Uses ports, NOT adapters

**Infrastructure Layer** (`apps/core/src/infra/`):
- Adapters (implementations)
- TTS engines (Qwen3, XTTS, etc.)
- Audio processing (librosa)
- Storage (files, databases)

**API Layer** (`apps/core/src/api/`):
- Entry points
- Dependency injection
- Python API for Tauri backend

For more details, see [HEXAGONAL_ARCHITECTURE.md](HEXAGONAL_ARCHITECTURE.md).

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

#### 1. Navigate to Core Library

```bash
cd apps/core
```

#### 2. Create Virtual Environment

```bash
# Using Python 3.10 (recommended)
python3.10 -m venv venv

# Or using default python3
python3 -m venv venv
```

#### 3. Activate Virtual Environment

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```cmd
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

#### 4. Upgrade pip

```bash
pip install --upgrade pip
```

#### 5. Install Development Dependencies

```bash
# Install from requirements.txt
pip install -r requirements.txt

# Install project in editable mode
pip install -e .
```

#### 6. Install Pre-commit Hooks

```bash
# Navigate back to repo root
cd ../..

# Install hooks
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

# Run tests
cd apps/core
pytest tests/ -v
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

### Test Structure

Tests are organized by hexagonal architecture layers:

```
apps/core/tests/
├── domain/          # Domain tests (NO infrastructure)
│   ├── models/      # Test entities and value objects
│   └── services/    # Test domain services with mocks
├── app/             # Application tests (mocked ports)
│   └── use_cases/   # Test use cases with mocked adapters
├── infra/           # Infrastructure tests (real adapters)
│   ├── engines/     # Test TTS engine adapters
│   ├── audio/       # Test audio processing adapters
│   └── persistence/ # Test storage adapters
├── integration/     # End-to-end tests
│   ├── test_end_to_end.py
│   └── test_hexagonal_architecture.py
└── pbt/             # Property-based tests
    ├── test_domain_properties.py
    └── test_use_case_properties.py
```

### Running Tests

```bash
# Navigate to core library
cd apps/core

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=term-missing

# Run specific layer
pytest tests/domain/          # Domain tests only
pytest tests/app/             # Application tests only
pytest tests/infra/           # Infrastructure tests only
pytest tests/integration/     # Integration tests only
pytest tests/pbt/             # Property-based tests only

# Run specific test file
pytest tests/domain/models/test_voice_profile.py

# Run specific test
pytest tests/domain/models/test_voice_profile.py::test_voice_profile_creation

# Run with verbose output
pytest -v

# Run and stop on first failure
pytest -x

# Run tests matching pattern
pytest -k "test_voice"
```

### Writing Tests

#### Domain Tests (Pure)

Test business logic without infrastructure:

```python
# tests/domain/services/test_voice_cloning.py
from unittest.mock import Mock
from domain.ports.audio_processor import AudioProcessor
from domain.services.voice_cloning import VoiceCloningService

def test_create_profile_from_samples():
    """Test domain service with mocked port."""
    # Mock the audio processor port
    mock_processor = Mock(spec=AudioProcessor)
    mock_processor.validate_sample.return_value = True
    mock_processor.process_sample.return_value = AudioSample(...)

    # Test domain service
    service = VoiceCloningService(mock_processor)
    profile = service.create_profile_from_samples("test", [Path("sample.wav")])

    assert profile.name == "test"
    assert len(profile.samples) == 1
```

#### Application Tests (Mocked Ports)

Test use cases with mocked adapters:

```python
# tests/app/use_cases/test_create_voice_profile.py
from unittest.mock import Mock
from app.use_cases.create_voice_profile import CreateVoiceProfileUseCase

def test_create_voice_profile_use_case():
    """Test use case with mocked ports."""
    mock_processor = Mock(spec=AudioProcessor)
    mock_repository = Mock(spec=ProfileRepository)

    uc = CreateVoiceProfileUseCase(mock_processor, mock_repository)
    result = uc.execute("test", [Path("sample.wav")])

    assert result.name == "test"
    mock_repository.save.assert_called_once()
```

#### Infrastructure Tests (Real Adapters)

Test adapters with real implementations:

```python
# tests/infra/engines/test_qwen3_adapter.py
from infra.engines.qwen3.adapter import Qwen3Adapter

def test_qwen3_adapter_generates_audio():
    """Test adapter with real Qwen3."""
    config = {'model_name': 'Qwen/Qwen3-TTS-12Hz-1.7B-Base'}
    adapter = Qwen3Adapter(config)

    output = adapter.generate_audio(
        text="Hello world",
        profile_id="test_profile",
        output_path=Path("test_output.wav")
    )

    assert output.exists()
    assert output.stat().st_size > 0
```

#### Integration Tests (End-to-End)

Test complete workflows:

```python
# tests/integration/test_end_to_end.py
from api.studio import TTSStudio

def test_create_profile_and_generate_audio():
    """Test complete workflow."""
    studio = TTSStudio()

    # Create profile
    profile_result = studio.create_voice_profile(
        name='test_voice',
        sample_paths=['data/samples/sample1.wav']
    )
    assert profile_result['status'] == 'success'

    # Generate audio
    audio_result = studio.generate_audio(
        profile_id='test_voice',
        text='Hello world',
        output_path='output.wav'
    )
    assert audio_result['status'] == 'success'
```

#### Property-Based Tests

Test properties that should always hold:

```python
# tests/pbt/test_domain_properties.py
from hypothesis import given, strategies as st
from domain.models.voice_profile import VoiceProfile

@given(st.text(min_size=1, max_size=50))
def test_voice_profile_name_preserved(name):
    """Test that profile name is always preserved."""
    profile = VoiceProfile(id=name, name=name, samples=[])
    assert profile.name == name

@given(st.lists(st.floats(min_value=0.1, max_value=30.0), min_size=1, max_size=10))
def test_voice_profile_duration_sum(durations):
    """Test that total duration equals sum of sample durations."""
    samples = [AudioSample(duration=d, ...) for d in durations]
    profile = VoiceProfile(id="test", name="test", samples=samples)
    assert abs(profile.total_duration - sum(durations)) < 0.01
```

### Coverage Requirements

- Minimum coverage: 80%
- Pre-push hook will fail if coverage is below threshold
- View coverage report: `pytest --cov=src --cov-report=html && open htmlcov/index.html`

### Testing Best Practices

1. **Domain tests**: Use mocks for all ports, test pure business logic
2. **Application tests**: Mock infrastructure, test orchestration
3. **Infrastructure tests**: Use real implementations, test integration
4. **Integration tests**: Test complete workflows end-to-end
5. **Property-based tests**: Test invariants that should always hold
6. **Test naming**: Use descriptive names that explain what is being tested
7. **Test isolation**: Each test should be independent
8. **Test data**: Use fixtures for common test data
9. **Test coverage**: Aim for >80% coverage, but focus on critical paths

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
