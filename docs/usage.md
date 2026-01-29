# Usage Guide

This guide covers how to use TTS Studio Python API for voice cloning and text-to-speech synthesis.

## Quick Start

```python
from api.studio import TTSStudio

# Initialize the API
studio = TTSStudio()

# Create a voice profile from audio samples
profile = studio.create_voice_profile(
    name="my_voice",
    sample_paths=["./data/samples/neutral_01.wav", "./data/samples/happy_01.wav"],
    language="es"
)

# Generate speech from text
result = studio.generate_audio(
    profile_id=profile["profile"]["id"],
    text="Hola, esta es una prueba de mi voz clonada.",
    output_path="./data/outputs/output.wav"
)

print(f"Audio generated: {result['output_path']}")
```

## API Overview

TTS Studio provides a Python API with the following main methods:

- `create_voice_profile()` - Create a voice profile from audio samples
- `generate_audio()` - Generate speech from text using a voice profile
- `list_voice_profiles()` - List all available voice profiles
- `delete_voice_profile()` - Delete a voice profile
- `validate_samples()` - Validate audio samples before creating a profile

## Creating a Voice Profile

### Basic Profile Creation

```python
from api.studio import TTSStudio

studio = TTSStudio()

# Create profile from audio samples
profile = studio.create_voice_profile(
    name="my_voice",
    sample_paths=[
        "./data/samples/neutral_01.wav",
        "./data/samples/happy_01.wav"
    ],
    language="es"
)

if profile["status"] == "success":
    print(f"Profile created: {profile['profile']['id']}")
else:
    print(f"Error: {profile['error']}")
```

### Profile Creation Options

```python
# Create profile with all options
profile = studio.create_voice_profile(
    name="my_voice",
    sample_paths=[
        "./data/samples/neutral_01.wav",
        "./data/samples/happy_01.wav",
        "./data/samples/serious_01.wav"
    ],
    language="es",  # Language code (es, en, fr, de, etc.)
    reference_text="Hola, esta es una muestra de mi voz para clonación."
)
```

**Parameters**:
- `name`: Name for the voice profile (required)
- `sample_paths`: List of paths to audio sample files (required)
- `language`: Language code (default: "es")
- `reference_text`: Optional text describing the samples

### Audio Sample Requirements

For best results:
- **Duration**: 3-30 seconds per sample
- **Quantity**: 1-3 samples (Qwen3-TTS requires fewer samples)
- **Quality**: Clear audio, minimal background noise
- **Format**: WAV, 12000 Hz, mono, 16-bit (or will be converted)
- **Content**: Natural speech, varied intonation
- **Consistency**: Same speaker, similar recording conditions

### Example Profile Creation Workflow

```python
from api.studio import TTSStudio
from pathlib import Path

studio = TTSStudio()

# 1. Prepare audio samples
samples_dir = Path("./data/samples/my_voice")
sample_files = list(samples_dir.glob("*.wav"))

# 2. Validate samples first (optional but recommended)
validation = studio.validate_samples([str(f) for f in sample_files])

if validation["all_valid"]:
    # 3. Create the profile
    profile = studio.create_voice_profile(
        name="my_voice",
        sample_paths=[str(f) for f in sample_files],
        language="es"
    )

    if profile["status"] == "success":
        print(f"Profile created: {profile['profile']['id']}")
        print(f"Total duration: {profile['profile']['total_duration']}s")
    else:
        print(f"Error: {profile['error']}")
else:
    print("Some samples are invalid:")
    for result in validation["results"]:
        if not result["valid"]:
            print(f"  - {result['path']}: {result['error']}")
```

## Generating Speech

### Basic Speech Generation

```python
from api.studio import TTSStudio

studio = TTSStudio()

# Generate speech from text
result = studio.generate_audio(
    profile_id="my_voice_20240115_143022",
    text="Hola, esta es una prueba de mi voz clonada.",
    output_path="./data/outputs/output.wav"
)

if result["status"] == "success":
    print(f"Audio generated: {result['output_path']}")
    print(f"Duration: {result['duration']}s")
else:
    print(f"Error: {result['error']}")
```

### Generation Options

```python
# Generate with all options
result = studio.generate_audio(
    profile_id="my_voice_20240115_143022",
    text="Hola, ¿cómo estás?",
    output_path="./data/outputs/output.wav",
    temperature=0.75,  # Sampling temperature (0.5-1.0)
    speed=1.0,  # Speaking speed multiplier (0.8-1.2)
    language="es",  # Language code
    mode="clone"  # Generation mode
)
```

**Parameters**:
- `profile_id`: ID of the voice profile to use (required)
- `text`: Text to convert to speech (required)
- `output_path`: Path to save audio (auto-generated if None)
- `temperature`: Sampling temperature (0.5-1.0, default: 0.75)
- `speed`: Speaking speed multiplier (0.8-1.2, default: 1.0)
- `language`: Language code (default: from config)
- `mode`: Generation mode (default: "clone")

### Temperature and Speed

**Temperature** controls synthesis randomness:
- Lower (0.5-0.6): More consistent, less expressive
- Medium (0.7-0.8): Balanced, natural-sounding (recommended)
- Higher (0.9-1.0): More varied, potentially less stable

**Speed** controls speech rate:
- Slower (0.8-0.9): Clearer, more deliberate
- Normal (1.0): Natural pace
- Faster (1.1-1.2): Quicker, may reduce clarity

### Batch Processing

Process multiple texts:

```python
from api.studio import TTSStudio

studio = TTSStudio()

# List of texts to generate
texts = [
    "Hola, esta es la primera oración.",
    "Esta es la segunda oración.",
    "Y esta es la tercera."
]

# Generate each text
for i, text in enumerate(texts):
    result = studio.generate_audio(
        profile_id="my_voice_20240115_143022",
        text=text,
        output_path=f"./data/outputs/output_{i:03d}.wav"
    )

    if result["status"] == "success":
        print(f"Generated {i+1}/{len(texts)}: {result['output_path']}")
    else:
        print(f"Error {i+1}/{len(texts)}: {result['error']}")
```

## Managing Voice Profiles

### List All Profiles

```python
from api.studio import TTSStudio

studio = TTSStudio()

# List all available profiles
profiles = studio.list_voice_profiles()

if profiles["status"] == "success":
    print(f"Found {profiles['count']} profiles:")
    for profile in profiles["profiles"]:
        print(f"  - {profile['name']} ({profile['id']})")
        print(f"    Samples: {profile['num_samples']}, Duration: {profile['total_duration']}s")
else:
    print(f"Error: {profiles['error']}")
```

### Delete a Profile

```python
# Delete a profile by ID
result = studio.delete_voice_profile(profile_id="my_voice_20240115_143022")

if result["status"] == "success":
    print("Profile deleted successfully")
else:
    print(f"Error: {result['error']}")
```

### Validate Audio Samples

```python
# Validate samples before creating a profile
validation = studio.validate_samples([
    "./data/samples/neutral_01.wav",
    "./data/samples/happy_01.wav"
])

if validation["status"] == "success":
    print(f"Valid samples: {validation['valid_samples']}/{validation['total_samples']}")
    print(f"Total duration: {validation['total_duration']}s")

    for result in validation["results"]:
        if result["valid"]:
            print(f"✓ {result['path']}: {result['duration']}s, {result['sample_rate']}Hz")
        else:
            print(f"✗ {result['path']}: {result['error']}")
else:
    print(f"Error: {validation['error']}")
```

## Configuration

### Using Configuration Files

Create a `config/config.yaml` file for default settings:

```yaml
# config/config.yaml
model:
  name: "Qwen/Qwen3-TTS-12Hz-1.7B-Base"
  device: "auto"  # auto, mps (M1/M2), or cpu
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

paths:
  samples: "./data/samples"
  outputs: "./data/outputs"
  profiles: "./data/profiles"
  models_cache: "./data/models"
```

### Loading Custom Configuration

```python
from api.studio import TTSStudio
from pathlib import Path

# Load with custom config file
studio = TTSStudio(config_path=Path("./config/my_config.yaml"))

# Or with config dictionary (for testing)
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

## Complete Examples

### Example 1: Personal Voice Assistant

```python
from api.studio import TTSStudio

studio = TTSStudio()

# Create your voice profile
profile = studio.create_voice_profile(
    name="my_voice",
    sample_paths=[
        "./data/samples/neutral_01.wav",
        "./data/samples/happy_01.wav"
    ],
    language="es"
)

# Generate reminder
result = studio.generate_audio(
    profile_id=profile["profile"]["id"],
    text="Tu reunión comienza en 5 minutos.",
    output_path="./data/outputs/reminder.wav"
)

print(f"Reminder generated: {result['output_path']}")
```

### Example 2: Audiobook Narration

```python
from api.studio import TTSStudio
from pathlib import Path

studio = TTSStudio()

# Create narrator profile
profile = studio.create_voice_profile(
    name="narrator",
    sample_paths=list(Path("./data/samples/narrator").glob("*.wav")),
    language="es"
)

# Read chapter text
with open("chapter1.txt", "r", encoding="utf-8") as f:
    chapter_text = f.read()

# Generate chapter audio
result = studio.generate_audio(
    profile_id=profile["profile"]["id"],
    text=chapter_text,
    output_path="./data/outputs/chapter1.wav",
    speed=0.9  # Slightly slower for clarity
)

print(f"Chapter audio generated: {result['output_path']}")
```

### Example 3: Multi-Language Support

```python
from api.studio import TTSStudio

studio = TTSStudio()

# Create multilingual profile
profile = studio.create_voice_profile(
    name="multilingual_voice",
    sample_paths=["./data/samples/sample_01.wav"],
    language="es"
)

# Generate in Spanish
result_es = studio.generate_audio(
    profile_id=profile["profile"]["id"],
    text="Hola, ¿cómo estás?",
    language="es",
    output_path="./data/outputs/hello_es.wav"
)

# Generate in English
result_en = studio.generate_audio(
    profile_id=profile["profile"]["id"],
    text="Hello, how are you?",
    language="en",
    output_path="./data/outputs/hello_en.wav"
)

print(f"Spanish: {result_es['output_path']}")
print(f"English: {result_en['output_path']}")
```

## Best Practices

### For Profile Creation
- Use high-quality audio recordings (12000 Hz, mono, 16-bit WAV)
- Ensure consistent recording environment
- Include varied speech patterns and emotions (1-3 samples)
- Remove long silences and background noise
- Use 3-30 seconds per sample

### For Speech Generation
- Start with default parameters (temperature=0.75, speed=1.0)
- Use temperature 0.7-0.8 for balanced results
- Keep text length reasonable (<500 characters per generation)
- Test different speeds for optimal clarity
- Use appropriate language code

### For Production Use
- Always obtain proper consent before cloning voices
- Respect voice rights and ethical guidelines
- Test thoroughly before deploying
- Monitor output quality regularly
- Validate samples before creating profiles

## Troubleshooting

### Poor Voice Quality
- Increase number of training samples (use 2-3 instead of 1)
- Improve audio sample quality (remove noise, ensure clarity)
- Adjust temperature (try 0.6-0.8)
- Check for background noise in samples
- Ensure samples are 12000 Hz, mono, 16-bit

### Slow Processing
- Enable GPU support (MPS for M1/M2, CUDA for NVIDIA)
- First generation is slower (model loading)
- Process shorter text segments
- Check device configuration in config.yaml

### Out of Memory Errors
- Use CPU mode: set `device: "cpu"` in config
- Process shorter audio segments
- Close other applications
- Consider upgrading RAM

### Voice Sounds Robotic
- Add more samples with emotional variety
- Ensure samples are high quality and natural
- Try adjusting temperature (0.7-0.9)
- Record samples with natural expression
- Avoid monotone samples

## Desktop Application

A native desktop application with a modern UI is coming soon. The desktop app will provide:

- Visual interface for profile management
- Real-time audio generation preview
- Batch processing with progress tracking
- Model management (download, install, delete)
- Export options for video editing

Stay tuned for updates!

## Next Steps

- Explore [API Documentation](api.md) for detailed API reference
- Check [Installation Guide](installation.md) for setup instructions
- Review [README](../README.md) for project overview
- See [examples/api_usage.py](../examples/api_usage.py) for more examples

## Getting Help

- Check [GitHub Issues](https://github.com/bryanstevensacosta/tts-studio/issues)
- Read [FAQ](../README.md#faq)
- Open a new issue with details and examples
