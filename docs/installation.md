# Installation Guide

This guide covers the installation process for TTS Studio Python library.

## Prerequisites

- Python 3.10 or 3.11 (3.10 recommended)
- pip package manager
- Git
- 8GB+ RAM (16GB recommended for M1 Pro)
- GPU optional (MPS for Apple Silicon, CUDA for NVIDIA)

## System Requirements

### Operating Systems

- Linux (Ubuntu 20.04+, Debian 11+)
- macOS (10.15+, M1/M2 recommended)
- Windows 10/11 (with WSL2 recommended)

### Hardware

- **CPU**: Modern multi-core processor
- **RAM**: Minimum 8GB, 16GB+ recommended
- **Storage**: 10GB+ free space (for models and cache)
- **GPU**:
  - Apple Silicon M1/M2 with MPS (recommended for macOS)
  - NVIDIA GPU with CUDA support (optional for Linux/Windows)

## Installation Methods

### Method 1: Automated Setup (Recommended)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/bryanstevensacosta/tts-studio.git
   cd tts-studio
   ```

2. **Navigate to core library**:
   ```bash
   cd apps/core
   ```

3. **Run the automated setup script**:
   ```bash
   ./setup.sh
   ```

   This script will:
   - Check Python version compatibility
   - Create a virtual environment
   - Install all dependencies
   - Set up pre-commit hooks (for development)
   - Verify the installation

4. **Activate the virtual environment**:
   ```bash
   source venv/bin/activate
   ```

5. **Verify installation**:
   ```python
   python -c "from api.studio import TTSStudio; print('TTS Studio installed successfully!')"
   ```

### Method 2: Manual Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/bryanstevensacosta/tts-studio.git
   cd tts-studio/apps/core
   ```

2. **Create a virtual environment**:
   ```bash
   python3.10 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Upgrade pip**:
   ```bash
   pip install --upgrade pip
   ```

4. **Install the package**:
   ```bash
   pip install -e .
   ```

5. **Verify installation**:
   ```python
   python -c "from api.studio import TTSStudio; print('Installation successful!')"
   ```

### Method 3: Install with Development Dependencies

For contributors and developers:

```bash
# Clone and navigate to core library
git clone https://github.com/bryanstevensacosta/tts-studio.git
cd tts-studio/apps/core

# Create and activate virtual environment
python3.10 -m venv venv
source venv/bin/activate

# Install with development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
pre-commit install --hook-type commit-msg
pre-commit install --hook-type pre-push

# Verify installation
make test
```

## GPU Support (Optional)

### Apple Silicon (M1/M2/M3) - MPS

For Apple Silicon Macs, MPS (Metal Performance Shaders) is automatically supported:

1. **Verify MPS availability**:
   ```python
   import torch
   print(f"MPS available: {torch.backends.mps.is_available()}")
   ```

2. **Configure for MPS** in `config/config.yaml`:
   ```yaml
   model:
     device: "mps"  # or "auto" for automatic detection
     dtype: "float32"  # Required for MPS stability
   ```

3. **Performance**: M1 Pro generates ~15-25 seconds per minute of audio

### NVIDIA GPU - CUDA

To enable GPU acceleration with CUDA (Linux/Windows):

1. **Install CUDA Toolkit** (11.8 or compatible version):
   - Download from [NVIDIA CUDA Toolkit](https://developer.nvidia.com/cuda-downloads)
   - Follow platform-specific installation instructions

2. **Install PyTorch with CUDA support**:
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```

3. **Verify GPU availability**:
   ```python
   import torch
   print(f"CUDA available: {torch.cuda.is_available()}")
   print(f"GPU: {torch.cuda.get_device_name(0)}")
   ```

4. **Configure for CUDA** in `config/config.yaml`:
   ```yaml
   model:
     device: "cuda"  # or "auto"
     dtype: "float32"
   ```

### CPU-Only Mode

If no GPU is available, TTS Studio will automatically use CPU:

```yaml
# config/config.yaml
model:
  device: "cpu"
  dtype: "float32"
```

**Note**: CPU-only mode is significantly slower (~2-3 minutes per minute of audio).

## Model Download

The Qwen3-TTS model (~3.4GB) downloads automatically on first use:

```python
from api.studio import TTSStudio

# First initialization downloads the model
studio = TTSStudio()  # Downloads model to apps/core/data/models/

# Subsequent initializations use cached model
studio = TTSStudio()  # Fast, uses cached model
```

**Download location**: `apps/core/data/models/Qwen3-TTS-12Hz-1.7B-Base/`

**Note**: Ensure you have:
- Stable internet connection
- At least 10GB free disk space
- Patience (first download takes 10-15 minutes)

## Desktop Application (Coming Soon)

A native desktop application with modern UI is in development. The desktop app will:

- Download models on-demand (not included in installer)
- Store models in OS-specific user directories:
  - macOS: `~/Library/Application Support/TTS Studio/models/`
  - Windows: `%LOCALAPPDATA%\TTS Studio\models\`
  - Linux: `~/.local/share/tts-studio/models/`
- Allow users to manage models (download, delete, re-download)
- Provide visual interface for all features

Stay tuned for updates!

## Troubleshooting

### Common Issues

**Issue**: `python3.10: command not found`
- **Solution**: Install Python 3.10 using your system package manager or from [python.org](https://www.python.org/downloads/)

**Issue**: `pip install` fails with permission errors
- **Solution**: Use a virtual environment (recommended) or add `--user` flag to pip install

**Issue**: Model download fails
- **Solution**: Ensure stable internet connection and at least 10GB free disk space. The model (~3.4GB) downloads automatically on first use.

**Issue**: MPS/CUDA out of memory errors
- **Solution**: Use CPU mode by setting `device: "cpu"` in config.yaml, or close other applications

**Issue**: Audio library errors (librosa, soundfile)
- **Solution**: Install system audio libraries:
  - Ubuntu/Debian: `sudo apt-get install libsndfile1 ffmpeg`
  - macOS: `brew install libsndfile ffmpeg`

**Issue**: Import errors after installation
- **Solution**: Ensure virtual environment is activated: `source venv/bin/activate`

### Getting Help

- Check the [FAQ](../README.md#faq) in the README
- Search [existing issues](https://github.com/bryanstevensacosta/tts-studio/issues)
- Open a [new issue](https://github.com/bryanstevensacosta/tts-studio/issues/new) with details

## Next Steps

After installation, proceed to:
- [Usage Guide](usage.md) - Learn how to use the Python API
- [API Documentation](api.md) - Explore the API reference
- [Development Guide](development.md) - Set up for development
- [Examples](../examples/api_usage.py) - See complete usage examples

## Uninstallation

To remove TTS Studio:

```bash
# Deactivate virtual environment
deactivate

# Remove the project directory
cd ../..
rm -rf tts-studio
```

Or if you want to keep the repository but remove the virtual environment:

```bash
cd apps/core
rm -rf venv
```
