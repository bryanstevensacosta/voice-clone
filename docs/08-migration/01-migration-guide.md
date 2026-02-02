# Migration Guide - TTS Studio v1.0.0

## Overview

This guide helps you migrate from the old CLI-based voice cloning tool to the new TTS Studio with hexagonal architecture and Python API.

**Major Changes**:
- ❌ CLI removed (no more `voice-clone` commands)
- ❌ Gradio UI removed
- ✅ Python API added (programmatic access)
- ✅ Hexagonal architecture (clean, testable, maintainable)
- ✅ Monorepo structure (`apps/core/` for Python library)
- ✅ Desktop app coming soon (Tauri)

---

## Breaking Changes

### 1. No More CLI

**Before (v0.x)**:
```bash
# Old CLI commands
voice-clone validate-samples --dir ./data/samples
voice-clone prepare --samples ./data/samples --output profile.json
voice-clone generate --profile profile.json --text "Hello world"
voice-clone batch --profile profile.json --input script.txt
```

**After (v1.0.0)**:
```python
# New Python API
from api.studio import TTSStudio

# Initialize API
studio = TTSStudio()

# Validate samples
result = studio.validate_samples(['./data/samples/sample1.wav'])

# Create profile
profile = studio.create_voice_profile(
    name='my_voice',
    sample_paths=['./data/samples/sample1.wav']
)

# Generate audio
audio = studio.generate_audio(
    profile_id='my_voice',
    text='Hello world',
    output_path='./output.wav'
)
```

### 2. No More Gradio UI

**Before (v0.x)**:
```bash
# Old Gradio UI
voice-clone ui
# Opens web interface at http://localhost:7860
```

**After (v1.0.0)**:
- Gradio UI removed
- Desktop app coming soon (Tauri-based)
- Use Python API for programmatic access

### 3. Package Structure Changed

**Before (v0.x)**:
```
voice-clone/
├── src/voice_clone/
│   ├── cli.py
│   ├── audio/
│   ├── model/
│   └── batch/
└── tests/
```

**After (v1.0.0)**:
```
tts-studio/
├── apps/core/              # Python library
│   ├── src/
│   │   ├── domain/         # Business logic
│   │   ├── app/            # Use cases
│   │   ├── infra/          # Adapters
│   │   └── api/            # Python API
│   └── tests/
└── apps/ui/           # Tauri app (coming soon)
```

### 4. Import Paths Changed

**Before (v0.x)**:
```python
from voice_clone.audio.processor import AudioProcessor
from voice_clone.model.generator import VoiceGenerator
```

**After (v1.0.0)**:
```python
# Use the high-level API instead
from api.studio import TTSStudio

# Or use specific layers if needed
from domain.models.voice_profile import VoiceProfile
from infra.engines.qwen3.adapter import Qwen3Adapter
from app.use_cases.create_voice_profile import CreateVoiceProfileUseCase
```

---

## Migration Steps

### Step 1: Update Installation

```bash
# Uninstall old version
pip uninstall voice-clone-cli

# Install new version
cd apps/core
pip install -e .
```

### Step 2: Update Your Code

#### Example 1: Create Voice Profile

**Before**:
```bash
voice-clone prepare \
  --samples ./data/samples \
  --output ./data/my_voice.json \
  --name "my_voice"
```

**After**:
```python
from api.studio import TTSStudio
from pathlib import Path

studio = TTSStudio()

# Create profile
result = studio.create_voice_profile(
    name='my_voice',
    sample_paths=[
        './data/samples/sample1.wav',
        './data/samples/sample2.wav'
    ]
)

if result['status'] == 'success':
    print(f"Profile created: {result['profile']['id']}")
else:
    print(f"Error: {result['error']}")
```

#### Example 2: Generate Audio

**Before**:
```bash
voice-clone generate \
  --profile ./data/my_voice.json \
  --text "Hello world" \
  --output ./output.wav
```

**After**:
```python
from api.studio import TTSStudio

studio = TTSStudio()

# Generate audio
result = studio.generate_audio(
    profile_id='my_voice',
    text='Hello world',
    output_path='./output.wav'
)

if result['status'] == 'success':
    print(f"Audio generated: {result['output_path']}")
else:
    print(f"Error: {result['error']}")
```

#### Example 3: Batch Processing

**Before**:
```bash
voice-clone batch \
  --profile ./data/my_voice.json \
  --input ./script.txt \
  --output-dir ./outputs
```

**After**:
```python
from api.studio import TTSStudio

studio = TTSStudio()

# Read script
with open('./script.txt', 'r') as f:
    script = f.read()

# Process batch (split by paragraphs)
segments = script.split('\n\n')
for i, segment in enumerate(segments):
    result = studio.generate_audio(
        profile_id='my_voice',
        text=segment,
        output_path=f'./outputs/segment_{i:03d}.wav'
    )
    print(f"Segment {i}: {result['status']}")
```

### Step 3: Update Configuration

**Before (v0.x)**:
```yaml
# config/config.yaml
model:
  name: "Qwen/Qwen3-TTS-12Hz-1.7B-Base"
  device: "mps"
```

**After (v1.0.0)**:
```yaml
# config/config.yaml (same location)
engines:
  qwen3:
    model_name: "Qwen/Qwen3-TTS-12Hz-1.7B-Base"
    device: "mps"
    dtype: "float32"

audio:
  sample_rate: 12000
  format: "wav"

paths:
  samples: "./data/samples"
  outputs: "./data/outputs"
  profiles: "./data/profiles"
```

### Step 4: Update Tests

**Before**:
```python
from voice_clone.audio.processor import AudioProcessor

def test_audio_processing():
    processor = AudioProcessor()
    result = processor.validate_sample('sample.wav')
    assert result.is_valid
```

**After**:
```python
from api.studio import TTSStudio

def test_audio_processing():
    studio = TTSStudio()
    result = studio.validate_samples(['sample.wav'])
    assert result['status'] == 'success'
```

---

## New Features

### 1. Hexagonal Architecture

The new architecture separates concerns into layers:

```
┌─────────────────────────────────────────┐
│           API Layer                     │
│       (Python API for Tauri)            │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│       Application Layer                 │
│         (Use Cases)                     │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│         Domain Layer                    │
│      (Business Logic)                   │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│      Infrastructure Layer               │
│         (Adapters)                      │
└─────────────────────────────────────────┘
```

**Benefits**:
- Clean separation of concerns
- Easy to test (mock adapters)
- Easy to swap implementations (e.g., Qwen3 → XTTS)
- Maintainable and scalable

### 2. Python API

Direct programmatic access to all functionality:

```python
from api.studio import TTSStudio

studio = TTSStudio()

# All operations return JSON-like dicts
result = studio.create_voice_profile(...)
# {'status': 'success', 'profile': {...}}

result = studio.generate_audio(...)
# {'status': 'success', 'output_path': '...'}
```

### 3. Better Error Handling

```python
result = studio.generate_audio(
    profile_id='nonexistent',
    text='Hello'
)

if result['status'] == 'error':
    print(f"Error type: {result['error_type']}")
    print(f"Error message: {result['error']}")
```

### 4. Monorepo Structure

```
tts-studio/
├── apps/core/          # Python library
├── apps/ui/       # Tauri desktop app (coming soon)
└── packages/           # Shared code (optional)
```

---

## FAQ

### Q: Can I still use the CLI?

**A**: No, the CLI has been removed. Use the Python API instead. If you need a command-line interface, you can create a simple wrapper script:

```python
#!/usr/bin/env python3
# my_cli.py
import sys
from api.studio import TTSStudio

studio = TTSStudio()

if sys.argv[1] == 'generate':
    result = studio.generate_audio(
        profile_id=sys.argv[2],
        text=sys.argv[3],
        output_path=sys.argv[4]
    )
    print(result)
```

### Q: What happened to the Gradio UI?

**A**: The Gradio UI has been removed. A new desktop app (Tauri-based) is coming soon. In the meantime, use the Python API.

### Q: How do I migrate my existing voice profiles?

**A**: Voice profiles are stored as JSON files in `data/profiles/`. They should work with the new version without changes. If you encounter issues, recreate the profile using the new API.

### Q: Can I still use Qwen3-TTS?

**A**: Yes! Qwen3-TTS is still the default engine. The new architecture makes it easier to add support for other engines in the future.

### Q: How do I test my code?

**A**: Use pytest with the new test structure:

```bash
cd apps/core
pytest tests/
```

### Q: Where is the documentation?

**A**: Documentation is in the `docs/` directory:
- `docs/api.md` - Python API reference
- `docs/HEXAGONAL_ARCHITECTURE.md` - Architecture guide
- `docs/development.md` - Development guide
- `docs/usage.md` - Usage examples

### Q: How do I contribute?

**A**: See `CONTRIBUTING.md` for contribution guidelines. The new architecture makes it easier to contribute:
- Add new TTS engines by implementing the `TTSEngine` port
- Add new audio processors by implementing the `AudioProcessor` port
- Add new storage backends by implementing the `ProfileRepository` port

### Q: What about the desktop app?

**A**: The desktop app (Tauri-based) is in development. It will provide a modern, native UI for all platforms (macOS, Windows, Linux). The Python API is the foundation for the desktop app.

---

## Troubleshooting

### Issue: Import errors after upgrade

**Problem**:
```python
ImportError: No module named 'voice_clone'
```

**Solution**:
```bash
# Uninstall old package
pip uninstall voice-clone-cli

# Install new package
cd apps/core
pip install -e .

# Update imports
from api.studio import TTSStudio  # New import
```

### Issue: Config file not found

**Problem**:
```
FileNotFoundError: config/config.yaml not found
```

**Solution**:
```bash
# Copy example config
cp config/config.yaml.example config/config.yaml

# Or create from scratch
cat > config/config.yaml << 'EOF'
engines:
  qwen3:
    model_name: "Qwen/Qwen3-TTS-12Hz-1.7B-Base"
    device: "mps"
    dtype: "float32"
EOF
```

### Issue: Voice profiles not found

**Problem**:
```python
result = studio.generate_audio(profile_id='my_voice', ...)
# {'status': 'error', 'error': 'Profile not found'}
```

**Solution**:
```python
# List available profiles
result = studio.list_voice_profiles()
print(result['profiles'])

# Or create a new profile
result = studio.create_voice_profile(
    name='my_voice',
    sample_paths=['./data/samples/sample1.wav']
)
```

### Issue: Tests failing

**Problem**:
```bash
pytest tests/
# ImportError or test failures
```

**Solution**:
```bash
# Install in development mode
cd apps/core
pip install -e .

# Install test dependencies
pip install pytest pytest-cov hypothesis

# Run tests
pytest tests/ -v
```

---

## Support

- **Issues**: https://github.com/bryanstevensacosta/tts-studio/issues
- **Discussions**: https://github.com/bryanstevensacosta/tts-studio/discussions
- **Documentation**: https://github.com/bryanstevensacosta/tts-studio/tree/master/docs

---

## Timeline

- **v0.x**: CLI + Gradio UI
- **v1.0.0**: Python API + Hexagonal Architecture (current)
- **v1.1.0**: Desktop app (Tauri) - coming soon
- **v1.2.0**: Additional TTS engines (XTTS, etc.) - planned

---

## Summary

**What's Removed**:
- ❌ CLI (`voice-clone` commands)
- ❌ Gradio UI

**What's New**:
- ✅ Python API (programmatic access)
- ✅ Hexagonal architecture (clean, testable)
- ✅ Monorepo structure
- ✅ Better error handling
- ✅ Easier to extend (add new engines, processors, etc.)

**Migration Path**:
1. Uninstall old package
2. Install new package from `apps/core/`
3. Update imports to use `api.studio.TTSStudio`
4. Update code to use Python API instead of CLI
5. Update tests
6. Enjoy the new architecture!

For detailed examples, see `examples/api_usage.py`.
