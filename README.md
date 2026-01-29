# TTS Studio - AI Voice Cloning

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/bryanstevensacosta/tts-studio/workflows/CI/badge.svg)](https://github.com/bryanstevensacosta/tts-studio/actions)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Professional voice cloning and text-to-speech system with hexagonal architecture, powered by Qwen3-TTS. Clone any voice with just a few audio samples and generate natural-sounding speech from text.

**Desktop application coming soon!** The core Python library is production-ready and can be integrated into your applications today.

## Features

- 🎤 **Voice Cloning**: Clone any voice using 1-3 audio samples
- 🗣️ **Text-to-Speech**: Generate speech from text in the cloned voice
- 🎯 **High Quality**: Powered by Qwen3-TTS for natural-sounding results
- ⚡ **Fast Processing**: Optimized for Apple Silicon (MPS) and CUDA GPUs
- 📦 **Batch Processing**: Process multiple text segments at once
- 🏗️ **Hexagonal Architecture**: Clean, testable, maintainable code
- 🔧 **Python API**: Easy-to-use Python library for integration
- 🖥️ **Desktop App**: Native Tauri desktop application (coming soon)
- 📥 **Model Management**: Download and manage TTS models on-demand
- 🔒 **Privacy-First**: Everything runs locally, no cloud required

## Architecture

TTS Studio uses a **monorepo structure** with **hexagonal architecture** (Ports & Adapters):

```
tts-studio/
├── apps/
│   ├── core/          # Python core library (hexagonal architecture)
│   │   ├── src/
│   │   │   ├── domain/      # Business logic (pure, no dependencies)
│   │   │   ├── app/         # Use cases and orchestration
│   │   │   ├── infra/       # Adapters (Qwen3, audio, storage)
│   │   │   ├── api/         # Python API entry point
│   │   │   └── shared/      # Shared utilities
│   │   └── tests/           # Comprehensive test suite
│   └── desktop/       # Tauri desktop app (coming soon)
├── config/            # Shared configuration
├── data/              # Data directory (gitignored)
└── docs/              # Documentation
```

### Hexagonal Architecture

The core library follows hexagonal architecture principles for maximum flexibility and testability:

- **Domain Layer**: Pure business logic with zero external dependencies
  - Entities (VoiceProfile, AudioSample)
  - Ports (interfaces for TTS engines, audio processors, storage)
  - Domain services (voice cloning logic)

- **Application Layer**: Use cases that orchestrate domain logic
  - CreateVoiceProfile, GenerateAudio, ValidateSamples
  - DTOs for data transfer
  - No business logic, only coordination

- **Infrastructure Layer**: Concrete implementations (adapters)
  - Qwen3 TTS engine adapter
  - Librosa audio processor adapter
  - File-based profile repository
  - YAML configuration provider

- **API Layer**: Entry point for external consumers
  - TTSStudio class (main Python API)
  - Dependency injection and wiring

This architecture makes the code:
- ✅ **Easy to test**: Domain logic testable without infrastructure
- ✅ **Easy to maintain**: Clear separation of concerns
- ✅ **Easy to extend**: Swap TTS engines without changing business logic
- ✅ **Easy to understand**: Follows SOLID principles

See [docs/HEXAGONAL_ARCHITECTURE.md](docs/HEXAGONAL_ARCHITECTURE.md) for detailed architecture documentation.

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/bryanstevensacosta/tts-studio.git
cd tts-studio

# Navigate to core library
cd apps/core

# Run the automated setup script
./setup.sh
```

The setup script will:
- Create a Python virtual environment
- Install all dependencies
- Set up pre-commit hooks for development

### Model Download

TTS Studio uses an on-demand model download system. Models are **not** included in the installation to keep the package size small.

**First-time setup:**

```python
from api.studio import TTSStudio

# Initialize the API (will prompt for model download if needed)
studio = TTSStudio()

# The Qwen3-TTS model (~3.4GB) will download automatically on first use
# This happens once and takes 10-15 minutes depending on your connection
```

**Model storage locations:**
- macOS: `~/Library/Application Support/TTS Studio/models/`
- Windows: `%LOCALAPPDATA%\TTS Studio\models\`
- Linux: `~/.local/share/tts-studio/models/`

You can delete models anytime to free disk space and re-download them later.

### Python API Usage

```python
from api.studio import TTSStudio

# Initialize the API
studio = TTSStudio()

# 1. Validate audio samples
validation = studio.validate_samples(
    sample_paths=["./data/samples/neutral_01.wav", "./data/samples/happy_01.wav"]
)

if validation["all_valid"]:
    # 2. Create voice profile
    profile = studio.create_voice_profile(
        name="my_voice",
        sample_paths=["./data/samples/neutral_01.wav", "./data/samples/happy_01.wav"],
        language="es"
    )

    if profile["status"] == "success":
        # 3. Generate audio from text
        result = studio.generate_audio(
            profile_id=profile["profile"]["id"],
            text="Hola, esta es una prueba de mi voz clonada.",
            temperature=0.75,
            speed=1.0
        )

        if result["status"] == "success":
            print(f"Audio generated: {result['output_path']}")
```

See [examples/api_usage.py](examples/api_usage.py) for complete examples.

## Installation Options

### Option 1: Automated Setup (Recommended)

```bash
cd apps/core
./setup.sh
```

### Option 2: Manual Setup

```bash
cd apps/core

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

## Python API Reference

### TTSStudio Class

Main API entry point for TTS Studio.

#### Methods

**`create_voice_profile(name, sample_paths, language="es", reference_text="")`**
- Creates a voice profile from audio samples
- Returns: `{"status": "success|error", "profile": {...}, "error": None|str}`

**`generate_audio(profile_id, text, temperature=0.75, speed=1.0, mode="clone")`**
- Generates audio from text using a voice profile
- Returns: `{"status": "success|error", "output_path": str, "duration": float, ...}`

**`list_voice_profiles()`**
- Lists all available voice profiles
- Returns: `{"status": "success|error", "profiles": [...], "count": int, ...}`

**`delete_voice_profile(profile_id)`**
- Deletes a voice profile
- Returns: `{"status": "success|error", "deleted": bool, ...}`

**`validate_samples(sample_paths)`**
- Validates audio samples for quality
- Returns: `{"status": "success|error", "results": [...], "all_valid": bool, ...}`

See [docs/api.md](docs/api.md) for complete API documentation.

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
  profiles: "./data/profiles"
  models: "./data/models"
```

## Documentation

For detailed documentation, see:

- [Installation Guide](docs/installation.md) - Detailed installation instructions
- [Usage Guide](docs/usage.md) - Comprehensive usage examples
- [Development Guide](docs/development.md) - Contributing and development setup
- [API Documentation](docs/api.md) - API reference and integration guide
- [Hexagonal Architecture](docs/HEXAGONAL_ARCHITECTURE.md) - Architecture overview

## Requirements

- Python 3.10 or 3.11
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

## Development

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Development Setup

```bash
# Clone and setup
git clone https://github.com/bryanstevensacosta/tts-studio.git
cd tts-studio/apps/core
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

This project enforces a strict rebase workflow to maintain a clean, linear history. See [docs/git-workflow.md](docs/git-workflow.md) for details.

## Project Structure

```
tts-studio/
├── apps/
│   ├── core/                    # Python core library
│   │   ├── src/
│   │   │   ├── domain/         # Domain layer (business logic)
│   │   │   ├── app/            # Application layer (use cases)
│   │   │   ├── infra/          # Infrastructure layer (adapters)
│   │   │   ├── api/            # API layer (entry points)
│   │   │   └── shared/         # Shared utilities
│   │   ├── tests/              # Test suite
│   │   ├── setup.py            # Package setup
│   │   └── requirements.txt    # Dependencies
│   └── desktop/                 # Tauri desktop app (coming soon)
├── config/                      # Configuration files
├── data/                        # Data directory (gitignored)
│   ├── samples/                # Audio samples
│   ├── profiles/               # Voice profiles
│   ├── models/                 # Cached models
│   └── outputs/                # Generated audio
├── docs/                        # Documentation
└── examples/                    # Usage examples
```

## Troubleshooting

### Common Issues

**Import errors**: Make sure you've activated the virtual environment:
```bash
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows
```

**Model download fails**: The Qwen3-TTS model (~3.4GB) downloads automatically on first use. Ensure you have:
- Stable internet connection
- At least 10GB free disk space
- Patience (first download takes 10-15 minutes)

**Model storage**: Models are stored in OS-specific directories:
- macOS: `~/Library/Application Support/TTS Studio/models/`
- Windows: `%LOCALAPPDATA%\TTS Studio\models\`
- Linux: `~/.local/share/tts-studio/models/`

You can delete models to free space and re-download them later.

**Audio quality issues**: Ensure your input samples are:
- 12000 Hz sample rate (or will be converted)
- Mono (single channel)
- 16-bit depth
- Clear speech without background noise
- 3-30 seconds duration each
- At least 1 sample (1-3 recommended)

**Generation is slow**:
- First generation is slower (model loading ~30-60 seconds)
- CPU-only mode is significantly slower than GPU
- For M1/M2 Mac: Ensure PyTorch has MPS support and dtype is set to float32
- For NVIDIA GPU: Ensure CUDA is properly installed

**Voice sounds robotic**:
- Add more samples with emotional variety
- Ensure samples are high quality
- Try adjusting temperature (0.7-0.9)
- Record samples with natural expression

**"Out of memory" errors**:
- Close other applications
- Reduce batch size
- Use shorter text chunks
- Consider upgrading RAM (16GB recommended)

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
- 🐛 [Issue Tracker](https://github.com/bryanstevensacosta/tts-studio/issues)
- 💬 [Discussions](https://github.com/bryanstevensacosta/tts-studio/discussions)

## Roadmap

- [x] Core voice cloning with Qwen3-TTS
- [x] Hexagonal architecture implementation
- [x] Python API for integration
- [x] Audio validation and conversion
- [x] Batch processing for scripts
- [x] Voice profile management
- [x] Comprehensive test suite (206 tests, 99% passing)
- [ ] **Model management system** (download models on-demand)
- [ ] **Tauri desktop application** (native UI for all platforms)
- [ ] Post-processing (normalization, fade effects)
- [ ] Format export (MP3, AAC, platform-specific)
- [ ] Streaming audio generation
- [ ] Real-time voice conversion (future)
- [ ] Multi-speaker support (future)
- [ ] Additional TTS engines (XTTS, ElevenLabs)

---

**Note**: This is a personal project for educational and research purposes. Please respect voice rights and obtain proper consent before cloning someone's voice.
