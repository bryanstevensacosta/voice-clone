# Voice Clone CLI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/yourusername/voice-clone-cli/workflows/CI/badge.svg)](https://github.com/yourusername/voice-clone-cli/actions)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A personal voice cloning CLI tool powered by XTTS-v2 (Coqui TTS). Clone any voice with just a few audio samples and generate natural-sounding speech from text.

## Features

- 🎤 **Voice Cloning**: Clone any voice using audio samples
- 🗣️ **Text-to-Speech**: Generate speech from text in the cloned voice
- 🎯 **High Quality**: Powered by XTTS-v2 for natural-sounding results
- ⚡ **Fast Processing**: Optimized for quick voice cloning and synthesis
- 🖥️ **CLI Interface**: Simple command-line interface for easy use
- 🔧 **Configurable**: Flexible configuration options for advanced users

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/voice-clone-cli.git
cd voice-clone-cli

# Run the automated setup script
./setup.sh
```

The setup script will:
- Create a Python virtual environment
- Install all dependencies
- Set up pre-commit hooks for development

### Basic Usage

```bash
# Activate the virtual environment
source venv/bin/activate

# Clone a voice from audio samples
voice-clone train --samples data/samples/speaker1/ --output data/models/speaker1

# Generate speech from text
voice-clone synthesize --model data/models/speaker1 --text "Hello, world!" --output output.wav

# Use interactive mode
voice-clone interactive --model data/models/speaker1
```

## Installation Options

### Option 1: Automated Setup (Recommended)

```bash
./setup.sh
```

### Option 2: Manual Setup

```bash
# Create virtual environment
python3.10 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -e ".[dev]"

# Install pre-commit hooks (for development)
pre-commit install
pre-commit install --hook-type commit-msg
pre-commit install --hook-type pre-push
```

## Usage Examples

### Training a Voice Model

```bash
# Train from a directory of audio samples
voice-clone train \
  --samples data/samples/my_voice/ \
  --output data/models/my_voice \
  --language en

# Train with custom parameters
voice-clone train \
  --samples data/samples/my_voice/ \
  --output data/models/my_voice \
  --language en \
  --epochs 100 \
  --batch-size 32
```

### Generating Speech

```bash
# Generate from text
voice-clone synthesize \
  --model data/models/my_voice \
  --text "This is a test of voice cloning." \
  --output output.wav

# Generate from text file
voice-clone synthesize \
  --model data/models/my_voice \
  --text-file script.txt \
  --output output.wav

# Adjust speech parameters
voice-clone synthesize \
  --model data/models/my_voice \
  --text "Hello!" \
  --output output.wav \
  --speed 1.2 \
  --temperature 0.7
```

### Interactive Mode

```bash
# Start interactive session
voice-clone interactive --model data/models/my_voice

# In interactive mode:
> Hello, how are you?
[Generates and plays audio]
> exit
```

## Configuration

Create a `config/config.yaml` file to customize settings:

```yaml
# Model settings
model:
  default_language: en
  sample_rate: 22050

# Training settings
training:
  epochs: 100
  batch_size: 32
  learning_rate: 0.001

# Output settings
output:
  format: wav
  quality: high
```

See `.env.example` for environment variable configuration options.

## Documentation

For detailed documentation, see:

- [Installation Guide](docs/installation.md) - Detailed installation instructions
- [Usage Guide](docs/usage.md) - Comprehensive usage examples
- [Development Guide](docs/development.md) - Contributing and development setup
- [API Documentation](docs/api.md) - API reference and integration guide

## Requirements

- Python 3.9, 3.10, or 3.11
- 4GB+ RAM recommended
- GPU recommended for faster processing (optional)

## Development

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Development Setup

```bash
# Clone and setup
git clone https://github.com/yourusername/voice-clone-cli.git
cd voice-clone-cli
./setup.sh

# Run tests
make test

# Run linting and formatting
make pre-commit

# See all available commands
make help
```

### Code Quality

This project uses:
- **Black** for code formatting
- **Ruff** for linting
- **MyPy** for type checking
- **pytest** for testing
- **pre-commit** for automated checks

All checks run automatically via pre-commit hooks.

### Git Workflow

This project enforces a strict rebase workflow to maintain a clean, linear history:

#### Branch Protection

The following branches are protected: `master`, `main`, `develop`
- ❌ No direct pushes allowed
- ❌ No force pushes allowed
- ✅ All changes must go through Pull Requests
- ✅ CI checks must pass before merge
- ✅ Only rebase merge is allowed (linear history)

#### Development Workflow

```bash
# 1. Create a feature branch
git checkout -b feature/my-feature

# 2. Make your changes and commit
git add .
git commit -m "feat: add new feature"

# 3. Before pushing, ensure you're up to date
make sync                    # Fetch latest changes
make rebase-master          # Rebase on master (or main/develop)

# 4. Push your branch
git push origin feature/my-feature

# 5. Create a Pull Request on GitHub
# The CI will run automatically

# 6. After PR approval, merge via GitHub
# (GitHub will automatically rebase and merge)
```

#### Pre-Push Hooks

The pre-push hook automatically checks:
- ✅ Your branch is up to date (rebased)
- ✅ You're not pushing to protected branches
- ✅ All tests pass
- ✅ Code coverage is above 70%

If your branch is behind, you'll see:
```
❌ Error: Your branch is not up to date with origin/master
To fix this, run:
  git fetch origin
  git rebase origin/master
```

#### Useful Commands

```bash
make sync              # Fetch and show status
make rebase-master     # Rebase on master
make rebase-main       # Rebase on main
make rebase-develop    # Rebase on develop
make check-branch      # Check if rebase is needed
```

#### Commit Message Convention

This project uses [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

Types:
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

Examples:
```bash
git commit -m "feat: add voice cloning feature"
git commit -m "fix: resolve audio processing bug"
git commit -m "docs: update installation guide"
git commit -m "test: add unit tests for synthesizer"
```

The commit-msg hook will validate your commit messages automatically.

## Project Structure

```
voice-clone-cli/
├── src/voice_clone/     # Main package
│   ├── cli.py          # CLI interface
│   ├── audio.py        # Audio processing
│   ├── model.py        # Model management
│   └── synthesizer.py  # Speech synthesis
├── tests/              # Test suite
├── docs/               # Documentation
├── data/               # Data directory (gitignored)
│   ├── samples/        # Audio samples
│   ├── models/         # Trained models
│   └── outputs/        # Generated audio
└── config/             # Configuration files
```

## Troubleshooting

### Common Issues

**Import errors**: Make sure you've activated the virtual environment:
```bash
source venv/bin/activate
```

**CUDA/GPU issues**: The tool works on CPU but is faster with GPU. Install PyTorch with CUDA support if needed.

**Audio quality issues**: Ensure your input samples are:
- High quality (16kHz+ sample rate)
- Clear speech without background noise
- At least 10 seconds of audio per speaker

See [docs/development.md](docs/development.md#troubleshooting) for more troubleshooting tips.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [XTTS-v2](https://github.com/coqui-ai/TTS) by Coqui AI
- Inspired by the open-source TTS community

## Support

- 📖 [Documentation](docs/)
- 🐛 [Issue Tracker](https://github.com/yourusername/voice-clone-cli/issues)
- 💬 [Discussions](https://github.com/yourusername/voice-clone-cli/discussions)

## Roadmap

- [ ] Multi-speaker support
- [ ] Real-time voice conversion
- [ ] Web interface
- [ ] Voice mixing and effects
- [ ] Cloud deployment options

---

**Note**: This is a personal project for educational and research purposes. Please respect voice rights and obtain proper consent before cloning someone's voice.
