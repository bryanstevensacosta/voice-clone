# Voice Clone CLI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/bryanstevensacosta/voice-clone/workflows/CI/badge.svg)](https://github.com/bryanstevensacosta/voice-clone/actions)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A personal voice cloning CLI tool powered by Qwen3-TTS. Clone any voice with just a few audio samples and generate natural-sounding speech from text.

## Features

- 🎤 **Voice Cloning**: Clone any voice using audio samples
- 🗣️ **Text-to-Speech**: Generate speech from text in the cloned voice
- 🎯 **High Quality**: Powered by Qwen3-TTS for natural-sounding results
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

# 1. Validate your audio samples
voice-clone validate-samples --dir ./data/samples

# 2. Create a voice profile
voice-clone prepare \
  --samples ./data/samples \
  --ref-text "Hola, esta es una muestra de mi voz para clonación." \
  --output ./data/voice_profile.json \
  --name "my_voice"

# 3. Generate speech from text
voice-clone generate \
  --profile ./data/voice_profile.json \
  --text "Hola, esta es una prueba de mi voz clonada." \
  --output ./output.wav

# 4. Quick test
voice-clone test --profile ./data/voice_profile.json
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

### Preparing Voice Samples

First, record 6-10 audio samples of your voice (10-20 seconds each):

```bash
# Samples should be:
# - WAV format, 12000 Hz, mono, 16-bit
# - Clear speech, no background noise
# - Different emotions/tones
# - Named: neutral_01.wav, happy_01.wav, serious_01.wav, etc.

# Place samples in data/samples/
data/samples/
├── neutral_01.wav
├── neutral_02.wav
├── happy_01.wav
├── serious_01.wav
└── calm_01.wav
```

### Validating Samples

```bash
# Validate all samples in a directory
voice-clone validate-samples --dir ./data/samples

# Output shows:
# ✓ neutral_01.wav - Valid
# ✓ happy_01.wav - Valid
# ✗ serious_01.wav - ERROR: Stereo (must be mono)
```

### Creating Voice Profile

```bash
# Create profile from validated samples
voice-clone prepare \
  --samples ./data/samples \
  --ref-text "Hola, esta es una muestra de mi voz para clonación." \
  --output ./data/voice_profile.json \
  --name "my_voice"

# Output:
# ✓ Voice profile created successfully!
# Samples: 8
# Duration: 127.3s
# Language: es
```

### Generating Speech

```bash
# Generate from text
voice-clone generate \
  --profile ./data/voice_profile.json \
  --text "Bienvenidos a este tutorial sobre inteligencia artificial." \
  --output ./intro.wav

# Generate from longer text (auto-chunking)
voice-clone generate \
  --profile ./data/voice_profile.json \
  --text "$(cat script.txt)" \
  --output ./narration.wav
```

### Batch Processing

```bash
# Create a script file with markers
cat > script.txt << 'EOF'
[INTRO]
Hola a todos, bienvenidos a este nuevo video.

[SECTION_1]
Hoy vamos a hablar sobre inteligencia artificial.

[OUTRO]
Gracias por ver este video.
EOF

# Process entire script
voice-clone batch \
  --profile ./data/voice_profile.json \
  --input ./script.txt \
  --output-dir ./data/outputs/video_001

# Output:
# ✓ Batch processing complete!
# Total segments: 3
# Successful: 3
# Failed: 0
```

### Quick Testing

```bash
# Test with default Spanish phrase
voice-clone test --profile ./data/voice_profile.json

# Test with custom text
voice-clone test \
  --profile ./data/voice_profile.json \
  --text "Esta es una prueba personalizada" \
  --output ./test.wav

# Play the result (macOS)
afplay ./test.wav
```

## Configuration

Create a `config/config.yaml` file to customize settings (see `config/config.yaml.example`):

```yaml
# Model configuration
model:
  name: "Qwen/Qwen3-TTS-12Hz-1.7B-Base"
  device: "auto"  # auto, mps (M1/M2), or cpu
  dtype: "float32"  # Required for MPS

# Generation parameters
generation:
  language: "Spanish"
  temperature: 0.75  # 0.5-1.0 (consistency vs variety)
  speed: 1.0  # 0.8-1.2 (speaking speed)
  max_new_tokens: 2048  # Maximum tokens to generate

# Audio settings
audio:
  sample_rate: 12000  # Qwen3-TTS native
  channels: 1  # Mono
  bit_depth: 16

# Paths
paths:
  samples: "./data/samples"
  outputs: "./data/outputs"
  models: "./data/models"
```

### Environment Variables

Create a `.env` file for sensitive settings:

```bash
# Optional: Custom model cache directory
QWEN_TTS_CACHE_DIR=/path/to/cache

# Optional: Logging level
LOG_LEVEL=INFO
```

## Documentation

For detailed documentation, see:

- [Installation Guide](docs/installation.md) - Detailed installation instructions
- [Usage Guide](docs/usage.md) - Comprehensive usage examples
- [Development Guide](docs/development.md) - Contributing and development setup
- [API Documentation](docs/api.md) - API reference and integration guide

## Requirements

- Python 3.9, 3.10, or 3.11
- 8GB+ RAM (16GB recommended for M1 Pro)
- GPU recommended for faster processing:
  - NVIDIA GPU with CUDA (Linux/Windows)
  - Apple Silicon M1/M2 with MPS (macOS)
  - CPU-only mode supported (slower)

### Hardware Performance

| Hardware | Generation Speed | Notes |
|----------|-----------------|-------|
| M1 Pro (16GB) | ~15-25s per minute | Native MPS acceleration |
| RTX 3060 (12GB) | ~10-20s per minute | CUDA acceleration |
| Intel i7 (CPU) | ~2-3 min per minute | CPU-only, slower |

## Audio Sample Requirements

For best results, your audio samples should be:

- **Format**: WAV, 12000 Hz, mono, 16-bit
- **Duration**: 3-30 seconds per sample
- **Quantity**: 1-3 samples (Qwen3-TTS requires fewer samples)
- **Quality**: Clear speech, no background noise
- **Variety**: Different emotions and tones
- **Content**: Natural speech, complete sentences

### Sample Recording Tips

1. **Environment**: Record in a quiet room
2. **Microphone**: Use a decent quality mic (built-in MacBook mic is acceptable)
3. **Distance**: 15-20cm from microphone
4. **Volume**: Natural speaking volume (not whispering or shouting)
5. **Emotions**: Include neutral, happy, serious, calm tones
6. **Avoid**: Background noise, echo, mouth clicks, breathing sounds

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
├── src/voice_clone/        # Main package
│   ├── cli.py             # CLI interface
│   ├── config.py          # Configuration management
│   ├── audio/             # Audio processing
│   │   ├── processor.py   # Audio validation & conversion
│   │   └── validator.py   # Validation results
│   ├── model/             # Model management
│   │   ├── manager.py     # Model loading & caching
│   │   ├── generator.py   # TTS generation
│   │   └── profile.py     # Voice profile data
│   ├── batch/             # Batch processing
│   │   └── processor.py   # Script processing
│   └── utils/             # Utilities
│       ├── logger.py      # Logging setup
│       └── helpers.py     # Helper functions
├── tests/                 # Test suite
│   ├── unit/             # Unit tests
│   └── property/         # Property-based tests
├── docs/                  # Documentation
├── data/                  # Data directory (gitignored)
│   ├── samples/          # Audio samples
│   ├── models/           # Cached models
│   ├── outputs/          # Generated audio
│   └── scripts/          # Example scripts
├── config/                # Configuration files
│   ├── default.yaml      # Default config
│   └── config.yaml.example  # Example custom config
└── .kiro/                 # Project steering guides
    └── steering/         # Workflow documentation
```

## Troubleshooting

### Common Issues

**Import errors**: Make sure you've activated the virtual environment:
```bash
source venv/bin/activate
```

**Model download fails**: The Qwen3-TTS model (~3.4GB) downloads automatically on first use. Ensure you have:
- Stable internet connection
- At least 10GB free disk space
- Patience (first download takes 10-15 minutes)

**Audio quality issues**: Ensure your input samples are:
- 12000 Hz sample rate (or will be converted)
- Mono (single channel)
- 16-bit depth
- Clear speech without background noise
- 3-30 seconds duration each
- At least 1 sample (1-3 recommended)

**Generation is slow**:
- First generation is slower (model loading)
- CPU-only mode is significantly slower than MPS
- For M1/M2 Mac: Ensure PyTorch has MPS support and dtype is set to float32
- CUDA is not supported by Qwen3-TTS

**Voice sounds robotic**:
- Add more samples with emotional variety
- Ensure samples are high quality
- Try adjusting temperature (0.7-0.9)
- Record samples with natural expression

**"Out of memory" errors**:
- Close other applications
- Reduce batch size
- Use shorter text chunks
- Consider upgrading RAM

### Getting Help

- Check [docs/development.md](docs/development.md#troubleshooting) for detailed troubleshooting
- Review the [steering guides](.kiro/steering/) for workflow tips
- Open an issue on GitHub with:
  - Error message
  - Python version
  - Hardware specs
  - Steps to reproduce

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Qwen3-TTS](https://github.com/QwenLM/Qwen-Audio) by Alibaba Cloud
- Inspired by the open-source TTS community

## Support

- 📖 [Documentation](docs/)
- 🐛 [Issue Tracker](https://github.com/yourusername/voice-clone-cli/issues)
- 💬 [Discussions](https://github.com/yourusername/voice-clone-cli/discussions)

## Roadmap

- [x] Core voice cloning with Qwen3-TTS
- [x] CLI interface with all commands
- [x] Audio validation and conversion
- [x] Batch processing for scripts
- [x] Voice profile management
- [x] Migration from XTTS-v2 to Qwen3-TTS
- [ ] Post-processing (normalization, fade effects)
- [ ] Format export (MP3, AAC, platform-specific)
- [ ] Integration tests
- [ ] Manual testing with real samples
- [ ] Web interface (future)
- [ ] Real-time voice conversion (future)
- [ ] Multi-speaker support (future)

---

**Note**: This is a personal project for educational and research purposes. Please respect voice rights and obtain proper consent before cloning someone's voice.
