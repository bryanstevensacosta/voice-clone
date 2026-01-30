# Quick Start Guide

Get up and running with TTS Studio in 5 minutes.

## Installation

```bash
git clone https://github.com/bryanstevensacosta/tts-studio.git
cd tts-studio/apps/core
./setup.sh
source venv/bin/activate
```

## Basic Usage

### 1. Create a Voice Profile

```python
from api.studio import TTSStudio

# Initialize
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

print(f"Profile created: {profile['profile']['id']}")
```

### 2. Generate Speech

```python
# Generate audio from text
result = studio.generate_audio(
    profile_id="my_voice",
    text="Hola, esta es una prueba de mi voz clonada.",
    output_path="./data/outputs/output.wav"
)

print(f"Audio generated: {result['output_path']}")
```

### 3. Complete Example

```python
from api.studio import TTSStudio
from pathlib import Path

# Initialize
studio = TTSStudio()

# Validate samples first (optional)
validation = studio.validate_samples([
    "./data/samples/neutral_01.wav",
    "./data/samples/happy_01.wav"
])

if validation["all_valid"]:
    # Create profile
    profile = studio.create_voice_profile(
        name="my_voice",
        sample_paths=[
            "./data/samples/neutral_01.wav",
            "./data/samples/happy_01.wav"
        ],
        language="es"
    )

    # Generate audio
    result = studio.generate_audio(
        profile_id=profile["profile"]["id"],
        text="Hola, ¿cómo estás?",
        output_path="./data/outputs/greeting.wav"
    )

    print(f"✓ Audio generated: {result['output_path']}")
else:
    print("✗ Some samples are invalid")
```

## Audio Sample Requirements

For best results:
- **Duration**: 3-30 seconds per sample
- **Quantity**: 1-3 samples
- **Quality**: Clear audio, minimal background noise
- **Format**: WAV, 12000 Hz, mono, 16-bit (or will be converted)

## Next Steps

- [Configuration Guide](03-configuration.md) - Configure TTS Studio
- [Recording Samples](../03-user-guides/01-recording-samples.md) - Learn how to record quality samples
- [API Reference](../04-api-reference/01-python-api.md) - Explore the full API
