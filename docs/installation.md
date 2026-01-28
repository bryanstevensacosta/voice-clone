# Installation Guide

This guide covers the installation process for Voice Clone CLI.

## Prerequisites

- Python 3.10 or 3.11 (3.10 recommended)
- pip package manager
- Git
- 4GB+ RAM recommended
- CUDA-compatible GPU (optional, for faster processing)

## System Requirements

### Operating Systems

- Linux (Ubuntu 20.04+, Debian 11+)
- macOS (10.15+)
- Windows 10/11 (with WSL2 recommended)

### Hardware

- **CPU**: Modern multi-core processor
- **RAM**: Minimum 4GB, 8GB+ recommended
- **Storage**: 2GB+ free space for models and dependencies
- **GPU**: NVIDIA GPU with CUDA support (optional, improves performance)

## Installation Methods

### Method 1: Install from Source (Recommended)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/voice-clone-cli.git
   cd voice-clone-cli
   ```

2. **Run the automated setup script**:
   ```bash
   ./setup.sh
   ```

   This script will:
   - Check Python version compatibility
   - Create a virtual environment
   - Install all dependencies
   - Set up pre-commit hooks
   - Verify the installation

3. **Activate the virtual environment**:
   ```bash
   source venv/bin/activate
   ```

4. **Verify installation**:
   ```bash
   voice-clone --version
   ```

### Method 2: Manual Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/voice-clone-cli.git
   cd voice-clone-cli
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
   ```bash
   voice-clone --version
   ```

### Method 3: Install with Development Dependencies

For contributors and developers:

```bash
# Clone and navigate to repository
git clone https://github.com/yourusername/voice-clone-cli.git
cd voice-clone-cli

# Create and activate virtual environment
python3.10 -m venv venv
source venv/bin/activate

# Install with development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
pre-commit install --hook-type commit-msg
pre-commit install --hook-type pre-push
```

## GPU Support (Optional)

To enable GPU acceleration with CUDA:

1. **Install CUDA Toolkit** (11.8 or compatible version):
   - Download from [NVIDIA CUDA Toolkit](https://developer.nvidia.com/cuda-downloads)
   - Follow platform-specific installation instructions

2. **Install PyTorch with CUDA support**:
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```

3. **Verify GPU availability**:
   ```bash
   python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
   ```

## Troubleshooting

### Common Issues

**Issue**: `python3.10: command not found`
- **Solution**: Install Python 3.10 using your system package manager or from [python.org](https://www.python.org/downloads/)

**Issue**: `pip install` fails with permission errors
- **Solution**: Use a virtual environment (recommended) or add `--user` flag to pip install

**Issue**: CUDA out of memory errors
- **Solution**: Reduce batch size or use CPU mode by setting `CUDA_VISIBLE_DEVICES=""`

**Issue**: Audio library errors (librosa, soundfile)
- **Solution**: Install system audio libraries:
  - Ubuntu/Debian: `sudo apt-get install libsndfile1 ffmpeg`
  - macOS: `brew install libsndfile ffmpeg`

### Getting Help

- Check the [FAQ](../README.md#faq) in the README
- Search [existing issues](https://github.com/yourusername/voice-clone-cli/issues)
- Open a [new issue](https://github.com/yourusername/voice-clone-cli/issues/new) with details

## Next Steps

After installation, proceed to:
- [Usage Guide](usage.md) - Learn how to use the CLI
- [Development Guide](development.md) - Set up for development
- [API Documentation](api.md) - Explore the API

## Uninstallation

To remove Voice Clone CLI:

```bash
# Deactivate virtual environment
deactivate

# Remove the project directory
cd ..
rm -rf voice-clone-cli
```

Or if installed globally:

```bash
pip uninstall voice-clone-cli
```
