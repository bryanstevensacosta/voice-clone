# API Documentation

This document provides API reference for Voice Clone CLI's Python modules and functions.

## Overview

Voice Clone CLI is organized into modular components:

- **cli.py** - Command-line interface and argument parsing
- **audio.py** - Audio processing and manipulation utilities
- **model.py** - Model management and loading
- **synthesizer.py** - Text-to-speech synthesis logic

## Module: voice_clone.cli

Command-line interface implementation.

### Functions

#### `cli()`

Main CLI entry point using Click framework.

**Returns**: None

**Example**:
```python
from voice_clone.cli import cli

if __name__ == "__main__":
    cli()
```

---

## Module: voice_clone.audio

Audio processing utilities for loading, normalizing, and converting audio files.

### Functions

#### `load_audio(file_path: str, sample_rate: int = 22050) -> np.ndarray`

Load an audio file and return as numpy array.

**Parameters**:
- `file_path` (str): Path to audio file (WAV, MP3, FLAC)
- `sample_rate` (int, optional): Target sample rate in Hz. Default: 22050

**Returns**:
- `np.ndarray`: Audio data as 1D numpy array (mono)

**Raises**:
- `FileNotFoundError`: If audio file doesn't exist
- `ValueError`: If audio file format is unsupported
- `RuntimeError`: If audio loading fails

**Example**:
```python
from voice_clone.audio import load_audio

audio = load_audio("sample.wav", sample_rate=22050)
print(f"Audio shape: {audio.shape}")
print(f"Duration: {len(audio) / 22050:.2f} seconds")
```

#### `normalize_audio(audio: np.ndarray, target_level: float = -20.0) -> np.ndarray`

Normalize audio to target dB level.

**Parameters**:
- `audio` (np.ndarray): Input audio array
- `target_level` (float, optional): Target level in dB. Default: -20.0

**Returns**:
- `np.ndarray`: Normalized audio array

**Example**:
```python
from voice_clone.audio import load_audio, normalize_audio

audio = load_audio("sample.wav")
normalized = normalize_audio(audio, target_level=-20.0)
```

#### `convert_to_mono(audio: np.ndarray) -> np.ndarray`

Convert stereo audio to mono by averaging channels.

**Parameters**:
- `audio` (np.ndarray): Input audio (1D for mono, 2D for stereo)

**Returns**:
- `np.ndarray`: Mono audio as 1D array

**Example**:
```python
from voice_clone.audio import load_audio, convert_to_mono

audio = load_audio("stereo.wav")
mono = convert_to_mono(audio)
```

#### `save_audio(audio: np.ndarray, file_path: str, sample_rate: int = 22050) -> None`

Save audio array to file.

**Parameters**:
- `audio` (np.ndarray): Audio data to save
- `file_path` (str): Output file path
- `sample_rate` (int, optional): Sample rate in Hz. Default: 22050

**Returns**: None

**Raises**:
- `ValueError`: If audio data is invalid
- `IOError`: If file cannot be written

**Example**:
```python
from voice_clone.audio import save_audio
import numpy as np

audio = np.random.randn(22050)  # 1 second of noise
save_audio(audio, "output.wav", sample_rate=22050)
```

#### `get_audio_duration(audio: np.ndarray, sample_rate: int) -> float`

Calculate audio duration in seconds.

**Parameters**:
- `audio` (np.ndarray): Audio data
- `sample_rate` (int): Sample rate in Hz

**Returns**:
- `float`: Duration in seconds

**Example**:
```python
from voice_clone.audio import load_audio, get_audio_duration

audio = load_audio("sample.wav", sample_rate=22050)
duration = get_audio_duration(audio, 22050)
print(f"Duration: {duration:.2f} seconds")
```

---

## Module: voice_clone.model

Model management and loading for Qwen3-TTS.

### Classes

#### `VoiceModel`

Represents a trained voice model.

**Attributes**:
- `model_path` (str): Path to model directory
- `language` (str): Model language code
- `sample_rate` (int): Model sample rate

**Methods**:

##### `__init__(model_path: str, language: str = "en")`

Initialize voice model.

**Parameters**:
- `model_path` (str): Path to model directory
- `language` (str, optional): Language code. Default: "en"

**Example**:
```python
from voice_clone.model import VoiceModel

model = VoiceModel("data/models/my_voice", language="en")
```

##### `load() -> None`

Load model into memory.

**Returns**: None

**Raises**:
- `FileNotFoundError`: If model files don't exist
- `RuntimeError`: If model loading fails

**Example**:
```python
model = VoiceModel("data/models/my_voice")
model.load()
```

##### `is_loaded() -> bool`

Check if model is loaded.

**Returns**:
- `bool`: True if model is loaded, False otherwise

**Example**:
```python
if not model.is_loaded():
    model.load()
```

### Functions

#### `train_model(samples_dir: str, output_path: str, language: str = "en", **kwargs) -> VoiceModel`

Train a new voice model from audio samples.

**Parameters**:
- `samples_dir` (str): Directory containing audio samples
- `output_path` (str): Output path for trained model
- `language` (str, optional): Language code. Default: "en"
- `**kwargs`: Additional training parameters

**Returns**:
- `VoiceModel`: Trained voice model instance

**Raises**:
- `FileNotFoundError`: If samples directory doesn't exist
- `ValueError`: If insufficient samples provided
- `RuntimeError`: If training fails

**Example**:
```python
from voice_clone.model import train_model

model = train_model(
    samples_dir="data/samples/my_voice",
    output_path="data/models/my_voice",
    language="en",
    min_duration=1.0,
    max_duration=10.0
)
```

#### `load_model(model_path: str, language: str = "en") -> VoiceModel`

Load an existing voice model.

**Parameters**:
- `model_path` (str): Path to model directory
- `language` (str, optional): Language code. Default: "en"

**Returns**:
- `VoiceModel`: Loaded voice model instance

**Raises**:
- `FileNotFoundError`: If model doesn't exist
- `RuntimeError`: If model loading fails

**Example**:
```python
from voice_clone.model import load_model

model = load_model("data/models/my_voice", language="en")
```

---

## Module: voice_clone.synthesizer

Text-to-speech synthesis functionality.

### Classes

#### `Synthesizer`

Text-to-speech synthesizer using Qwen3-TTS.

**Attributes**:
- `model` (VoiceModel): Voice model to use
- `sample_rate` (int): Output sample rate (12000 Hz for Qwen3-TTS)
- `temperature` (float): Synthesis temperature
- `speed` (float): Speech speed multiplier

**Methods**:

##### `__init__(model: VoiceModel, sample_rate: int = 22050)`

Initialize synthesizer with voice model.

**Parameters**:
- `model` (VoiceModel): Voice model instance
- `sample_rate` (int, optional): Output sample rate. Default: 22050

**Example**:
```python
from voice_clone.model import load_model
from voice_clone.synthesizer import Synthesizer

model = load_model("data/models/my_voice")
synthesizer = Synthesizer(model, sample_rate=22050)
```

##### `synthesize(text: str, temperature: float = 0.7, speed: float = 1.0) -> np.ndarray`

Synthesize speech from text.

**Parameters**:
- `text` (str): Text to synthesize
- `temperature` (float, optional): Synthesis temperature (0.1-1.0). Default: 0.7
- `speed` (float, optional): Speech speed multiplier (0.5-2.0). Default: 1.0

**Returns**:
- `np.ndarray`: Synthesized audio as numpy array

**Raises**:
- `ValueError`: If parameters are out of range
- `RuntimeError`: If synthesis fails

**Example**:
```python
synthesizer = Synthesizer(model)
audio = synthesizer.synthesize(
    text="Hello, world!",
    temperature=0.7,
    speed=1.0
)
```

##### `synthesize_to_file(text: str, output_path: str, temperature: float = 0.7, speed: float = 1.0) -> None`

Synthesize speech and save to file.

**Parameters**:
- `text` (str): Text to synthesize
- `output_path` (str): Output file path
- `temperature` (float, optional): Synthesis temperature. Default: 0.7
- `speed` (float, optional): Speech speed multiplier. Default: 1.0

**Returns**: None

**Example**:
```python
synthesizer.synthesize_to_file(
    text="Hello, world!",
    output_path="output.wav",
    temperature=0.7,
    speed=1.0
)
```

### Functions

#### `synthesize_text(model: VoiceModel, text: str, **kwargs) -> np.ndarray`

Convenience function to synthesize text with a model.

**Parameters**:
- `model` (VoiceModel): Voice model to use
- `text` (str): Text to synthesize
- `**kwargs`: Additional synthesis parameters

**Returns**:
- `np.ndarray`: Synthesized audio

**Example**:
```python
from voice_clone.model import load_model
from voice_clone.synthesizer import synthesize_text

model = load_model("data/models/my_voice")
audio = synthesize_text(model, "Hello, world!", temperature=0.7)
```

---

## Configuration

### Config Class

Configuration management for Voice Clone CLI.

#### `Config`

Application configuration.

**Attributes**:
- `model_path` (str): Default model path
- `output_dir` (str): Default output directory
- `sample_rate` (int): Default sample rate
- `language` (str): Default language
- `temperature` (float): Default temperature
- `speed` (float): Default speed

**Methods**:

##### `load_from_file(config_path: str) -> Config`

Load configuration from YAML file.

**Parameters**:
- `config_path` (str): Path to config file

**Returns**:
- `Config`: Configuration instance

**Example**:
```python
from voice_clone.config import Config

config = Config.load_from_file("config/config.yaml")
```

---

## Type Definitions

### Common Types

```python
from typing import Union, Optional, List
import numpy as np
from pathlib import Path

# Audio data type
AudioArray = np.ndarray

# File path type
FilePath = Union[str, Path]

# Language code type
LanguageCode = str  # ISO 639-1 codes: "en", "es", "fr", etc.

# Sample rate type
SampleRate = int  # Hz, typically 16000, 22050, or 44100
```

---

## Error Handling

### Custom Exceptions

#### `VoiceCloneError`

Base exception for Voice Clone CLI errors.

#### `ModelNotFoundError`

Raised when model files cannot be found.

#### `AudioProcessingError`

Raised when audio processing fails.

#### `SynthesisError`

Raised when speech synthesis fails.

**Example**:
```python
from voice_clone.exceptions import ModelNotFoundError

try:
    model = load_model("nonexistent/path")
except ModelNotFoundError as e:
    print(f"Model not found: {e}")
```

---

## Usage Examples

### Complete Workflow Example

```python
from voice_clone.model import train_model, load_model
from voice_clone.synthesizer import Synthesizer
from voice_clone.audio import save_audio

# Train a model
model = train_model(
    samples_dir="data/samples/my_voice",
    output_path="data/models/my_voice",
    language="en"
)

# Or load existing model
model = load_model("data/models/my_voice")

# Create synthesizer
synthesizer = Synthesizer(model, sample_rate=22050)

# Synthesize speech
audio = synthesizer.synthesize(
    text="Hello, this is a test of voice cloning.",
    temperature=0.7,
    speed=1.0
)

# Save to file
save_audio(audio, "output.wav", sample_rate=22050)
```

### Batch Processing Example

```python
from voice_clone.model import load_model
from voice_clone.synthesizer import Synthesizer

model = load_model("data/models/my_voice")
synthesizer = Synthesizer(model)

texts = [
    "First sentence to synthesize.",
    "Second sentence to synthesize.",
    "Third sentence to synthesize."
]

for i, text in enumerate(texts):
    synthesizer.synthesize_to_file(
        text=text,
        output_path=f"output_{i}.wav"
    )
```

---

## Performance Considerations

### GPU Acceleration

Voice Clone CLI automatically uses GPU if available:

```python
import torch

# Check GPU availability
if torch.cuda.is_available():
    print(f"Using GPU: {torch.cuda.get_device_name(0)}")
else:
    print("Using CPU")
```

### Memory Management

For large batch processing:

```python
# Process in smaller batches
batch_size = 10
for i in range(0, len(texts), batch_size):
    batch = texts[i:i+batch_size]
    # Process batch
    torch.cuda.empty_cache()  # Clear GPU memory
```

---

## Contributing

To add new API functionality:

1. Add function/class to appropriate module
2. Include type hints for all parameters and returns
3. Write comprehensive docstrings
4. Add unit tests
5. Update this API documentation
6. Run `make pre-commit` to validate

---

## See Also

- [Usage Guide](usage.md) - CLI usage examples
- [Development Guide](development.md) - Development setup
- [Installation Guide](installation.md) - Installation instructions
