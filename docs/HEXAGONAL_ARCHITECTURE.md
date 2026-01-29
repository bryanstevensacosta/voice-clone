# Hexagonal Architecture Guide

## Overview

TTS Studio uses **Hexagonal Architecture** (also known as **Ports and Adapters**) to create a clean, maintainable, and testable codebase.

**Key Principle**: Business logic (domain) is independent of external concerns (infrastructure).

---

## What is Hexagonal Architecture?

Hexagonal Architecture separates your application into layers with clear boundaries:

```
┌─────────────────────────────────────────────────────────────┐
│                     API Layer (Entry Points)                 │
│                      Python API for Tauri                    │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│                    Application Layer                         │
│                      (Use Cases)                             │
│  • CreateVoiceProfile  • GenerateAudio  • ProcessBatch      │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│                      Domain Layer                            │
│                   (Business Logic)                           │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Models     │  │    Ports     │  │   Services   │     │
│  │  (Entities)  │  │ (Interfaces) │  │   (Logic)    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│                  Infrastructure Layer                        │
│                      (Adapters)                              │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ TTS Engines  │  │    Audio     │  │ Persistence  │     │
│  │  (Qwen3,     │  │  Processing  │  │   (Files,    │     │
│  │   XTTS)      │  │  (librosa)   │  │    JSON)     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

---

## Core Concepts

### 1. Ports (Interfaces)

**Ports** are interfaces that define contracts between layers.

**Location**: `apps/core/src/domain/ports/`

**Example**:
```python
# domain/ports/tts_engine.py
from abc import ABC, abstractmethod
from pathlib import Path

class TTSEngine(ABC):
    """Port (interface) for TTS engines."""

    @abstractmethod
    def generate_audio(
        self,
        text: str,
        profile_id: str,
        output_path: Path
    ) -> Path:
        """Generate audio from text using voice profile."""
        pass

    @abstractmethod
    def validate_profile(self, profile_id: str) -> bool:
        """Validate that profile is compatible with engine."""
        pass
```

**Why Ports?**
- Define what the domain needs, not how it's implemented
- Allow swapping implementations without changing domain logic
- Enable testing with mocks

### 2. Adapters (Implementations)

**Adapters** are concrete implementations of ports.

**Location**: `apps/core/src/infra/`

**Example**:
```python
# infra/engines/qwen3/adapter.py
from domain.ports.tts_engine import TTSEngine
from pathlib import Path

class Qwen3Adapter(TTSEngine):
    """Adapter that implements TTSEngine port using Qwen3."""

    def __init__(self, config: dict):
        self.config = config
        self.model = None  # Loaded lazily

    def generate_audio(
        self,
        text: str,
        profile_id: str,
        output_path: Path
    ) -> Path:
        # Qwen3-specific implementation
        if self.model is None:
            self._load_model()

        # Generate audio using Qwen3
        audio = self.model.generate(text, profile_id)
        audio.save(output_path)
        return output_path

    def validate_profile(self, profile_id: str) -> bool:
        # Qwen3-specific validation
        return True
```

**Why Adapters?**
- Implement ports with specific technologies (Qwen3, XTTS, etc.)
- Can be swapped without changing domain or application layers
- Easy to test in isolation

### 3. Dependency Inversion

**Rule**: Dependencies point inward (toward domain).

```
API Layer ──────────> Application Layer
                            │
                            ▼
                      Domain Layer
                            ▲
                            │
Infrastructure Layer ───────┘
```

**Example**:

```python
# ✅ CORRECT: Infrastructure depends on domain
from domain.ports.tts_engine import TTSEngine  # Port (interface)

class Qwen3Adapter(TTSEngine):  # Adapter implements port
    pass

# ❌ WRONG: Domain depends on infrastructure
from infra.engines.qwen3.adapter import Qwen3Adapter  # NO!

class VoiceProfile:
    def __init__(self, engine: Qwen3Adapter):  # NO! Use port instead
        pass
```

---

## Layer Responsibilities

### Domain Layer (`apps/core/src/domain/`)

**Purpose**: Pure business logic, NO external dependencies

**Contains**:
- **Models** (`domain/models/`): Entities and value objects
  - `VoiceProfile`: Voice profile entity
  - `AudioSample`: Audio sample value object
- **Ports** (`domain/ports/`): Interfaces for external dependencies
  - `TTSEngine`: Interface for TTS engines
  - `AudioProcessor`: Interface for audio processing
  - `ProfileRepository`: Interface for storage
- **Services** (`domain/services/`): Domain logic
  - `VoiceCloningService`: Voice cloning business rules
  - `AudioGenerationService`: Audio generation logic
- **Exceptions** (`domain/exceptions.py`): Domain-specific errors

**Rules**:
- ✅ NO imports from `infra/` or `app/`
- ✅ Only Python standard library + domain code
- ✅ Defines interfaces (ports) for external dependencies
- ✅ Contains pure business logic

**Example**:
```python
# domain/services/voice_cloning.py
from domain.ports.audio_processor import AudioProcessor
from domain.models.voice_profile import VoiceProfile

class VoiceCloningService:
    """Domain service for voice cloning logic."""

    def __init__(self, audio_processor: AudioProcessor):
        # Depends on port, not adapter
        self._audio_processor = audio_processor

    def create_profile_from_samples(
        self,
        name: str,
        sample_paths: list[Path]
    ) -> VoiceProfile:
        # Pure business logic
        samples = []
        for path in sample_paths:
            if not self._audio_processor.validate_sample(path):
                raise ValueError(f"Invalid sample: {path}")
            samples.append(self._audio_processor.process_sample(path))

        profile = VoiceProfile(
            id=self._generate_id(name),
            name=name,
            samples=samples
        )

        if not profile.is_valid():
            raise ValueError("Profile does not meet requirements")

        return profile
```

### Application Layer (`apps/core/src/app/`)

**Purpose**: Orchestrate use cases, coordinate domain logic

**Contains**:
- **Use Cases** (`app/use_cases/`): Application logic
  - `CreateVoiceProfileUseCase`: Create profile workflow
  - `GenerateAudioUseCase`: Generate audio workflow
  - `ListVoiceProfilesUseCase`: List profiles workflow
- **DTOs** (`app/dto/`): Data transfer objects
  - `VoiceProfileDTO`: Profile data for API
  - `GenerationRequestDTO`: Generation request data
  - `GenerationResultDTO`: Generation result data

**Rules**:
- ✅ Uses domain layer
- ✅ Uses ports (interfaces), NOT adapters (implementations)
- ✅ NO direct infrastructure dependencies
- ✅ Orchestrates workflows

**Example**:
```python
# app/use_cases/create_voice_profile.py
from domain.ports.audio_processor import AudioProcessor
from domain.ports.profile_repository import ProfileRepository
from domain.services.voice_cloning import VoiceCloningService
from app.dto.voice_profile_dto import VoiceProfileDTO

class CreateVoiceProfileUseCase:
    """Use case for creating voice profiles."""

    def __init__(
        self,
        audio_processor: AudioProcessor,  # Port
        profile_repository: ProfileRepository  # Port
    ):
        self._voice_cloning = VoiceCloningService(audio_processor)
        self._repository = profile_repository

    def execute(self, name: str, sample_paths: list[Path]) -> VoiceProfileDTO:
        # 1. Use domain service
        profile = self._voice_cloning.create_profile_from_samples(
            name, sample_paths
        )

        # 2. Use repository
        self._repository.save(profile)

        # 3. Return DTO
        return VoiceProfileDTO.from_entity(profile)
```

### Infrastructure Layer (`apps/core/src/infra/`)

**Purpose**: Implement ports with concrete adapters

**Contains**:
- **Engines** (`infra/engines/`): TTS engine adapters
  - `Qwen3Adapter`: Qwen3-TTS implementation
  - Future: `XTTSAdapter`, `ElevenLabsAdapter`, etc.
- **Audio** (`infra/audio/`): Audio processing adapters
  - `LibrosaAudioProcessor`: Librosa implementation
- **Persistence** (`infra/persistence/`): Storage adapters
  - `FileProfileRepository`: File-based storage
  - Future: `SQLiteRepository`, `PostgreSQLRepository`, etc.
- **Config** (`infra/config/`): Configuration adapters
  - `YAMLConfigProvider`: YAML config implementation

**Rules**:
- ✅ Implements ports defined in domain
- ✅ Can use external libraries (Qwen3, librosa, etc.)
- ✅ Depends on domain (via ports)
- ✅ NO business logic (only technical implementation)

**Example**:
```python
# infra/audio/processor_adapter.py
from domain.ports.audio_processor import AudioProcessor
from domain.models.audio_sample import AudioSample
import librosa

class LibrosaAudioProcessor(AudioProcessor):
    """Audio processor using librosa."""

    def validate_sample(self, path: Path) -> bool:
        try:
            audio, sr = librosa.load(path, sr=None)
            return sr == 12000 and len(audio.shape) == 1
        except Exception:
            return False

    def process_sample(self, path: Path) -> AudioSample:
        audio, sr = librosa.load(path, sr=12000, mono=True)
        duration = len(audio) / sr
        return AudioSample(
            path=path,
            duration=duration,
            sample_rate=sr,
            channels=1
        )
```

### API Layer (`apps/core/src/api/`)

**Purpose**: Entry points for external consumers

**Contains**:
- **Python API** (`api/studio.py`): Main API for Tauri backend

**Rules**:
- ✅ Wires everything together (dependency injection)
- ✅ Uses application layer (use cases)
- ✅ Provides clean API for external consumers
- ✅ Handles errors and returns JSON-like responses

**Example**:
```python
# api/studio.py
from app.use_cases.create_voice_profile import CreateVoiceProfileUseCase
from infra.engines.qwen3.adapter import Qwen3Adapter
from infra.audio.processor_adapter import LibrosaAudioProcessor
from infra.persistence.file_profile_repository import FileProfileRepository

class TTSStudio:
    """Main API for TTS Studio."""

    def __init__(self, config: dict = None):
        # Initialize adapters (infrastructure)
        audio_processor = LibrosaAudioProcessor()
        profile_repository = FileProfileRepository(Path('data/profiles'))
        tts_engine = Qwen3Adapter(config['engines']['qwen3'])

        # Initialize use cases (application)
        self._create_profile_uc = CreateVoiceProfileUseCase(
            audio_processor=audio_processor,
            profile_repository=profile_repository
        )

    def create_voice_profile(
        self,
        name: str,
        sample_paths: list[str]
    ) -> dict:
        """Create voice profile (public API method)."""
        try:
            paths = [Path(p) for p in sample_paths]
            profile_dto = self._create_profile_uc.execute(name, paths)
            return {
                'status': 'success',
                'profile': profile_dto.to_dict()
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
```

---

## Benefits of Hexagonal Architecture

### 1. Testability

**Domain tests** (no infrastructure):
```python
def test_voice_profile_validation():
    # Mock the audio processor port
    mock_processor = Mock(spec=AudioProcessor)
    mock_processor.validate_sample.return_value = True

    # Test domain service
    service = VoiceCloningService(mock_processor)
    profile = service.create_profile_from_samples("test", [Path("sample.wav")])

    assert profile.is_valid()
```

**Infrastructure tests** (real implementations):
```python
def test_qwen3_adapter_generates_audio():
    config = {'model_name': 'Qwen/Qwen3-TTS-12Hz-1.7B-Base'}
    adapter = Qwen3Adapter(config)

    # Test with real Qwen3
    output = adapter.generate_audio(
        text="Hello world",
        profile_id="test_profile",
        output_path=Path("test_output.wav")
    )

    assert output.exists()
```

### 2. Flexibility

**Easy to swap implementations**:
```python
# Use Qwen3
tts_engine = Qwen3Adapter(config)

# Switch to XTTS (when implemented)
tts_engine = XTTSAdapter(config)

# Use cases don't change!
generate_uc = GenerateAudioUseCase(tts_engine, repository)
```

### 3. Maintainability

**Clear separation of concerns**:
- Domain: What the business needs
- Application: How workflows are orchestrated
- Infrastructure: How things are implemented
- API: How external consumers interact

### 4. Scalability

**Easy to add new features**:
- New TTS engine? Implement `TTSEngine` port
- New storage? Implement `ProfileRepository` port
- New audio processor? Implement `AudioProcessor` port

---

## Testing Strategy

### Domain Tests (`tests/domain/`)

**Purpose**: Test business logic without infrastructure

**Approach**: Use mocks for all ports

```python
# tests/domain/services/test_voice_cloning.py
def test_create_profile_from_samples():
    # Mock audio processor
    mock_processor = Mock(spec=AudioProcessor)
    mock_processor.validate_sample.return_value = True
    mock_processor.process_sample.return_value = AudioSample(...)

    # Test domain service
    service = VoiceCloningService(mock_processor)
    profile = service.create_profile_from_samples("test", [Path("sample.wav")])

    assert profile.name == "test"
    assert len(profile.samples) == 1
```

### Application Tests (`tests/app/`)

**Purpose**: Test use cases with mocked ports

**Approach**: Mock infrastructure, test orchestration

```python
# tests/app/use_cases/test_create_voice_profile.py
def test_create_voice_profile_use_case():
    # Mock ports
    mock_processor = Mock(spec=AudioProcessor)
    mock_repository = Mock(spec=ProfileRepository)

    # Test use case
    uc = CreateVoiceProfileUseCase(mock_processor, mock_repository)
    result = uc.execute("test", [Path("sample.wav")])

    assert result.name == "test"
    mock_repository.save.assert_called_once()
```

### Infrastructure Tests (`tests/infra/`)

**Purpose**: Test adapters with real implementations

**Approach**: Use real libraries, test integration

```python
# tests/infra/engines/test_qwen3_adapter.py
def test_qwen3_adapter_generates_audio():
    config = {'model_name': 'Qwen/Qwen3-TTS-12Hz-1.7B-Base'}
    adapter = Qwen3Adapter(config)

    # Test with real Qwen3
    output = adapter.generate_audio(
        text="Hello world",
        profile_id="test_profile",
        output_path=Path("test_output.wav")
    )

    assert output.exists()
    assert output.stat().st_size > 0
```

### Integration Tests (`tests/integration/`)

**Purpose**: Test complete workflows end-to-end

**Approach**: Use real components, test full stack

```python
# tests/integration/test_end_to_end.py
def test_create_profile_and_generate_audio():
    studio = TTSStudio()

    # Create profile
    profile_result = studio.create_voice_profile(
        name='test_voice',
        sample_paths=['data/samples/sample1.wav']
    )
    assert profile_result['status'] == 'success'

    # Generate audio
    audio_result = studio.generate_audio(
        profile_id='test_voice',
        text='Hello world',
        output_path='output.wav'
    )
    assert audio_result['status'] == 'success'
```

---

## Common Patterns

### Pattern 1: Adding a New TTS Engine

1. **Define port** (if not exists):
```python
# domain/ports/tts_engine.py
class TTSEngine(ABC):
    @abstractmethod
    def generate_audio(self, text: str, profile_id: str, output: Path) -> Path:
        pass
```

2. **Implement adapter**:
```python
# infra/engines/xtts/adapter.py
class XTTSAdapter(TTSEngine):
    def generate_audio(self, text: str, profile_id: str, output: Path) -> Path:
        # XTTS-specific implementation
        pass
```

3. **Wire in API**:
```python
# api/studio.py
class TTSStudio:
    def __init__(self, config: dict):
        if config['engine'] == 'qwen3':
            tts_engine = Qwen3Adapter(config)
        elif config['engine'] == 'xtts':
            tts_engine = XTTSAdapter(config)
```

### Pattern 2: Adding a New Storage Backend

1. **Port already exists**:
```python
# domain/ports/profile_repository.py
class ProfileRepository(ABC):
    @abstractmethod
    def save(self, profile: VoiceProfile) -> None:
        pass
```

2. **Implement adapter**:
```python
# infra/persistence/sqlite_repository.py
class SQLiteProfileRepository(ProfileRepository):
    def save(self, profile: VoiceProfile) -> None:
        # SQLite-specific implementation
        pass
```

3. **Wire in API**:
```python
# api/studio.py
if config['storage'] == 'file':
    repository = FileProfileRepository(...)
elif config['storage'] == 'sqlite':
    repository = SQLiteProfileRepository(...)
```

### Pattern 3: Adding a New Use Case

1. **Define use case**:
```python
# app/use_cases/export_profile.py
class ExportProfileUseCase:
    def __init__(self, repository: ProfileRepository):
        self._repository = repository

    def execute(self, profile_id: str, format: str) -> Path:
        profile = self._repository.find_by_id(profile_id)
        # Export logic
        return export_path
```

2. **Add to API**:
```python
# api/studio.py
class TTSStudio:
    def __init__(self, config: dict):
        self._export_profile_uc = ExportProfileUseCase(repository)

    def export_profile(self, profile_id: str, format: str) -> dict:
        try:
            path = self._export_profile_uc.execute(profile_id, format)
            return {'status': 'success', 'path': str(path)}
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
```

---

## Validation Checklist

After making changes, verify:

- [ ] Domain layer has NO infra dependencies
- [ ] All ports (interfaces) are defined in domain
- [ ] All adapters implement their respective ports
- [ ] Use cases only depend on ports, not adapters
- [ ] API layer wires everything together (dependency injection)
- [ ] Tests can use mocks for all ports
- [ ] Easy to swap implementations (e.g., Qwen3 → XTTS)

---

## Resources

- **Code**: `apps/core/src/`
- **Tests**: `apps/core/tests/`
- **Examples**: `examples/api_usage.py`
- **Migration Guide**: `docs/MIGRATION.md`

---

## Summary

**Hexagonal Architecture** = Clean, testable, maintainable code

**Key Principles**:
1. **Dependency Inversion**: Dependencies point inward (toward domain)
2. **Ports & Adapters**: Domain defines interfaces, infrastructure implements them
3. **Separation of Concerns**: Each layer has a clear responsibility
4. **Testability**: Easy to test with mocks

**Benefits**:
- Easy to test (mock adapters)
- Easy to swap implementations (Qwen3 → XTTS)
- Easy to extend (add new engines, processors, storage)
- Clean, maintainable codebase

**Layers**:
- **Domain**: Pure business logic (NO external dependencies)
- **Application**: Use cases (orchestration)
- **Infrastructure**: Adapters (implementations)
- **API**: Entry points (dependency injection)

For practical examples, see `examples/api_usage.py` and the test suite.
