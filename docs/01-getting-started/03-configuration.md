# Configuration Guide

Learn how to configure TTS Studio for your needs.

## Configuration File

TTS Studio uses YAML configuration files located in `apps/core/config/`.

### Default Configuration

```yaml
# config/config.yaml
engines:
  qwen3:
    model_name: "Qwen/Qwen3-TTS-12Hz-1.7B-Base"
    device: "auto"  # auto, mps (M1/M2), cuda, or cpu
    dtype: "float32"  # Required for MPS

generation:
  language: "Spanish"
  temperature: 0.75
  speed: 1.0
  max_new_tokens: 2048

audio:
  sample_rate: 12000
  channels: 1
  bit_depth: 16
  format: "wav"

paths:
  samples: "./data/samples"
  outputs: "./data/outputs"
  profiles: "./data/profiles"
  models_cache: "./data/models"
```

## Configuration Options

### Engine Configuration

```yaml
engines:
  qwen3:
    model_name: "Qwen/Qwen3-TTS-12Hz-1.7B-Base"
    device: "auto"  # Device selection
    dtype: "float32"  # Data type
    cache_dir: "./data/models"  # Model cache location
```

**Device Options**:
- `auto`: Automatically detect best device (MPS > CUDA > CPU)
- `mps`: Apple Silicon Metal Performance Shaders
- `cuda`: NVIDIA GPU
- `cpu`: CPU only (slower)

### Generation Configuration

```yaml
generation:
  language: "Spanish"  # Language code
  temperature: 0.75  # Sampling temperature (0.5-1.0)
  speed: 1.0  # Speaking speed (0.8-1.2)
  max_new_tokens: 2048  # Maximum tokens per generation
```

**Temperature**: Controls randomness
- Lower (0.5-0.6): More consistent, less expressive
- Medium (0.7-0.8): Balanced (recommended)
- Higher (0.9-1.0): More varied, potentially less stable

**Speed**: Controls speech rate
- Slower (0.8-0.9): Clearer, more deliberate
- Normal (1.0): Natural pace
- Faster (1.1-1.2): Quicker, may reduce clarity

### Audio Configuration

```yaml
audio:
  sample_rate: 12000  # Hz (Qwen3-TTS native)
  channels: 1  # Mono (required)
  bit_depth: 16  # 16-bit (standard)
  format: "wav"  # Output format
```

### Path Configuration

```yaml
paths:
  samples: "./data/samples"  # Input samples directory
  outputs: "./data/outputs"  # Generated audio directory
  profiles: "./data/profiles"  # Voice profiles directory
  models_cache: "./data/models"  # Model cache directory
```

## Loading Configuration

### From File

```python
from api.studio import TTSStudio
from pathlib import Path

# Load custom config file
studio = TTSStudio(config_path=Path("./config/my_config.yaml"))
```

### From Dictionary

```python
# For testing or dynamic configuration
config_dict = {
    "model": {"device": "cpu"},
    "generation": {"temperature": 0.8}
}
studio = TTSStudio(config_dict=config_dict)
```

### Accessing Configuration

```python
# Get configuration values
device = studio.get_config("model.device", default="cpu")
temperature = studio.get_config("generation.temperature", default=0.75)

# Reload configuration
result = studio.reload_config()
if result["status"] == "success":
    print("Configuration reloaded")
```

## Environment-Specific Configuration

### Development

```yaml
# config/dev.yaml
engines:
  qwen3:
    device: "cpu"  # Use CPU for development

paths:
  models_cache: "./data/models_dev"
```

### Production

```yaml
# config/prod.yaml
engines:
  qwen3:
    device: "auto"  # Use best available device

paths:
  models_cache: "/var/lib/tts-studio/models"
```

## Platform-Specific Configuration

### macOS (Apple Silicon)

```yaml
engines:
  qwen3:
    device: "mps"
    dtype: "float32"  # Required for MPS
```

### Linux (NVIDIA GPU)

```yaml
engines:
  qwen3:
    device: "cuda"
    dtype: "float32"
```

### Windows

```yaml
engines:
  qwen3:
    device: "cpu"  # Or "cuda" if NVIDIA GPU available
```

## Next Steps

- [Recording Samples](../03-user-guides/01-recording-samples.md) - Learn how to record quality samples
- [Creating Profiles](../03-user-guides/02-creating-profiles.md) - Create voice profiles
- [API Reference](../04-api-reference/01-python-api.md) - Explore the full API
