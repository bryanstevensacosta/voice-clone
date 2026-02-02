# Creating Voice Profiles

Learn how to create voice profiles from audio samples.

## Overview

A voice profile contains the audio samples and metadata needed to clone a voice. TTS Studio uses these profiles to generate speech that sounds like the original speaker.

## Basic Profile Creation

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

## Profile Creation Options

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

## Audio Sample Requirements

For best results:
- **Duration**: 3-30 seconds per sample
- **Quantity**: 1-3 samples (Qwen3-TTS requires fewer samples)
- **Quality**: Clear audio, minimal background noise
- **Format**: WAV, 12000 Hz, mono, 16-bit (or will be converted)
- **Content**: Natural speech, varied intonation
- **Consistency**: Same speaker, similar recording conditions

## Validating Samples

Before creating a profile, validate your samples:

```python
# Validate samples first (optional but recommended)
validation = studio.validate_samples([
    "./data/samples/neutral_01.wav",
    "./data/samples/happy_01.wav"
])

if validation["all_valid"]:
    print(f"✓ All samples valid")
    print(f"Total duration: {validation['total_duration']}s")
else:
    print("✗ Some samples are invalid:")
    for result in validation["results"]:
        if not result["valid"]:
            print(f"  - {result['path']}: {result['error']}")
```

## Complete Workflow

```python
from api.studio import TTSStudio
from pathlib import Path

studio = TTSStudio()

# 1. Prepare audio samples
samples_dir = Path("./data/samples/my_voice")
sample_files = list(samples_dir.glob("*.wav"))

# 2. Validate samples first
validation = studio.validate_samples([str(f) for f in sample_files])

if validation["all_valid"]:
    # 3. Create the profile
    profile = studio.create_voice_profile(
        name="my_voice",
        sample_paths=[str(f) for f in sample_files],
        language="es"
    )

    if profile["status"] == "success":
        print(f"✓ Profile created: {profile['profile']['id']}")
        print(f"  Samples: {profile['profile']['num_samples']}")
        print(f"  Duration: {profile['profile']['total_duration']}s")
    else:
        print(f"✗ Error: {profile['error']}")
else:
    print("✗ Fix invalid samples before creating profile")
```

## Managing Profiles

### List All Profiles

```python
# List all available profiles
profiles = studio.list_voice_profiles()

if profiles["status"] == "success":
    print(f"Found {profiles['count']} profiles:")
    for profile in profiles["profiles"]:
        print(f"  - {profile['name']} ({profile['id']})")
        print(f"    Samples: {profile['num_samples']}, Duration: {profile['total_duration']}s")
```

### Delete a Profile

```python
# Delete a profile by ID
result = studio.delete_voice_profile(profile_id="my_voice_20240115_143022")

if result["status"] == "success":
    print("✓ Profile deleted successfully")
else:
    print(f"✗ Error: {result['error']}")
```

## Best Practices

### For Profile Creation
- Use high-quality audio recordings (12000 Hz, mono, 16-bit WAV)
- Ensure consistent recording environment
- Include varied speech patterns and emotions (1-3 samples)
- Remove long silences and background noise
- Use 3-30 seconds per sample

### Sample Variety
- Include different emotions (neutral, happy, serious)
- Vary sentence structures (statements, questions)
- Include different speaking speeds
- Maintain consistent voice quality

## Troubleshooting

### Poor Voice Quality
- Increase number of training samples (use 2-3 instead of 1)
- Improve audio sample quality (remove noise, ensure clarity)
- Check for background noise in samples
- Ensure samples are 12000 Hz, mono, 16-bit

### Profile Creation Fails
- Validate samples first using `validate_samples()`
- Check sample format (WAV, 12000 Hz, mono)
- Ensure samples are 3-30 seconds each
- Verify file paths are correct

## Next Steps

- [Generating Audio](03-generating-audio.md) - Generate speech from text
- [Recording Samples](01-recording-samples.md) - Learn how to record quality samples
- [API Reference](../04-api-reference/01-python-api.md) - Explore the full API
