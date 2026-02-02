---
inclusion: always
---

# Technology Stack - TTS Studio

## Project Architecture

### Monorepo Structure
- **Architecture**: Monorepo with separate apps
- **Apps**: `apps/core/` (Python library), `apps/ui/` (Tauri app)
- **Build System**: Independent builds per app
- **CI/CD**: Separate workflows per technology (Python, Rust, TypeScript)

### Core Library Architecture (Hexagonal)
- **Pattern**: Hexagonal Architecture (Ports & Adapters)
- **Layers**: Domain → Application → Infrastructure → API
- **Dependency Direction**: All dependencies point inward (toward domain)
- **Testability**: Domain testable without infrastructure

## Core Technologies

### Python Core Library (`apps/core/`)
- **TTS Engine**: `Qwen/Qwen3-TTS-12Hz-1.7B-Base` - Primary TTS engine
- **Python Version**: `3.10-3.11` (optimal for Qwen3-TTS and type hints)
- **Architecture**: Hexagonal (Ports & Adapters)

### Python Dependencies

#### Core Dependencies
```python
# TTS Engine
qwen-tts>=1.0.0          # Qwen3-TTS framework
torch>=2.0.0             # PyTorch for model inference
torchaudio>=2.0.0        # Audio processing
transformers>=4.30.0     # Hugging Face transformers

# Audio Processing
librosa>=0.10.0          # Audio analysis and manipulation
soundfile>=0.12.0        # Audio I/O
scipy>=1.10.0            # Signal processing
numpy>=1.24.0            # Numerical operations

# Configuration & Utilities
pyyaml>=6.0              # YAML configuration
python-dotenv>=1.0.0     # Environment variables
pydantic>=2.0.0          # Data validation (for DTOs)
```

#### Development Dependencies
```python
# Testing
pytest>=7.4.0            # Testing framework
pytest-cov>=4.0.0        # Coverage reporting
hypothesis>=6.0.0        # Property-based testing

# Code Quality
black>=23.0.0            # Code formatter
ruff>=0.1.0              # Fast linter
mypy>=1.0.0              # Type checker

# Pre-commit
pre-commit>=3.0.0        # Git hooks
```

### Desktop App Technologies (`apps/ui/`)

#### Rust Backend (Tauri)
```toml
# Cargo.toml
[dependencies]
tauri = "1.5"            # Desktop app framework
serde = "1.0"            # Serialization
serde_json = "1.0"       # JSON support
tokio = "1.0"            # Async runtime
rusqlite = "0.30"        # SQLite database
```

#### TypeScript Frontend (React)
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "@tauri-apps/api": "^1.5.0",
    "zustand": "^4.4.0",
    "react-router-dom": "^6.20.0",
    "tailwindcss": "^3.3.0",
    "shadcn/ui": "latest"
  },
  "devDependencies": {
    "typescript": "^5.2.0",
    "vite": "^5.0.0",
    "@vitejs/plugin-react": "^4.2.0",
    "eslint": "^8.55.0",
    "prettier": "^3.1.0"
  }
}
```

## Hexagonal Architecture Principles

### Layer Responsibilities

#### Domain Layer (`apps/core/src/domain/`)
- **Purpose**: Pure business logic, NO external dependencies
- **Contains**: Entities, Value Objects, Domain Services, Ports (interfaces)
- **Rules**:
  - NO imports from infrastructure
  - NO framework dependencies
  - Only Python standard library + domain code
  - Defines interfaces (ports) for external dependencies

#### Application Layer (`apps/core/src/app/`)
- **Purpose**: Orchestrate use cases, coordinate domain logic
- **Contains**: Use Cases, DTOs, Application Services
- **Rules**:
  - Uses domain layer
  - Uses ports (interfaces), NOT adapters (implementations)
  - NO direct infrastructure dependencies

#### Infrastructure Layer (`apps/core/src/infra/`)
- **Purpose**: Implement ports with concrete adapters
- **Contains**: TTS engine adapters, audio processors, repositories, config providers
- **Rules**:
  - Implements ports defined in domain
  - Can use external libraries (Qwen3, librosa, etc.)
  - Depends on domain (via ports)

#### API Layer (`apps/core/src/api/`)
- **Purpose**: Entry points for external consumers
- **Contains**: Python API for Tauri backend
- **Rules**:
  - Wires everything together (dependency injection)
  - Uses application layer (use cases)
  - Provides clean API for Tauri backend

### Dependency Inversion

```python
# ✅ CORRECT: Infrastructure depends on domain
from domain.ports.tts_engine import TTSEngine  # Port (interface)

class Qwen3Adapter(TTSEngine):  # Adapter implements port
    def generate_audio(self, text: str, profile_id: str) -> Path:
        # Qwen3-specific implementation
        pass

# ❌ WRONG: Domain depends on infrastructure
from infrastructure.engines.qwen3.adapter import Qwen3Adapter  # NO!

class VoiceProfile:
    def __init__(self, engine: Qwen3Adapter):  # NO! Use port instead
        pass
```

### Ports & Adapters Pattern

**Ports** (Interfaces in `domain/ports/`):
- `TTSEngine` - Interface for TTS engines
- `AudioProcessor` - Interface for audio processing
- `ProfileRepository` - Interface for profile storage
- `ConfigProvider` - Interface for configuration

**Adapters** (Implementations in `infra/`):
- `Qwen3Adapter` - Implements `TTSEngine` for Qwen3
- `LibrosaAudioProcessor` - Implements `AudioProcessor` with librosa
- `FileProfileRepository` - Implements `ProfileRepository` with files
- `YAMLConfigProvider` - Implements `ConfigProvider` with YAML

### Dependency Injection

```python
# apps/core/src/api/python_api.py
class TTSStudioAPI:
    def __init__(self, config: Dict[str, Any]):
        # Initialize adapters (infrastructure)
        audio_processor = LibrosaAudioProcessor()
        profile_repository = FileProfileRepository(Path(config['paths']['profiles']))
        tts_engine = Qwen3Adapter(config['engines']['qwen3'])

        # Initialize use cases (application)
        self._create_profile_uc = CreateVoiceProfileUseCase(
            audio_processor=audio_processor,
            profile_repository=profile_repository
        )
        self._generate_audio_uc = GenerateAudioUseCase(
            tts_engine=tts_engine,
            profile_repository=profile_repository
        )

    def create_voice_profile(self, name: str, sample_paths: List[str]) -> Dict[str, Any]:
        """Public API method."""
        paths = [Path(p) for p in sample_paths]
        profile_dto = self._create_profile_uc.execute(name, paths)
        return profile_dto.to_dict()
```

## Desktop App Architecture (FSD)

### Feature-Sliced Design Layers

#### 1. App Layer (`apps/ui/src/app/`)
- Application initialization
- Global providers (theme, router, store)
- Global styles
- Root-level configuration

#### 2. Pages Layer (`apps/ui/src/pages/`)
- Route components
- Page-level layouts
- Composition of widgets

#### 3. Widgets Layer (`apps/ui/src/widgets/`)
- Complex, self-contained UI blocks
- Combine multiple features and entities
- Business logic for widget behavior

#### 4. Features Layer (`apps/ui/src/features/`)
- User interactions (actions)
- Business logic for specific features
- Reusable across pages

#### 5. Entities Layer (`apps/ui/src/entities/`)
- Business entities (Profile, Sample, Generation, Model)
- Entity state management (Zustand)
- Tauri API calls for entities
- Entity UI components

#### 6. Shared Layer (`apps/ui/src/shared/`)
- Reusable UI components (shadcn/ui)
- Utilities, hooks, types
- No business logic

### Desktop-First Principles

**Offline-First**:
- Everything works without internet (except model downloads)
- Models downloaded once, stored locally
- SQLite for local storage (profiles, history, config)
- No authentication or registration
- No external API calls (everything local)

**No Redundant Suffixes**:
```typescript
// ❌ WRONG
services/VoiceCloningService.ts
hooks/useVoiceProfilesHook.ts
components/ProfileCardComponent.tsx

// ✅ CORRECT
services/voice-cloning.ts
hooks/use-profiles.ts
ui/profile-card.tsx
```

### Tauri Backend (Rust)

**Python Bridge**:
- Subprocess management for Python core library
- Calls Python API via subprocess
- Handles Python process lifecycle

**Local Storage**:
- SQLite database for profiles, history, settings
- File system for audio samples and outputs
- Model registry for installed models

**Model Management**:
- Download models from Hugging Face on-demand (only time internet needed)
- Install models in OS-specific user directories:
  - macOS: `~/Library/Application Support/TTS Studio/models/`
  - Windows: `%LOCALAPPDATA%\TTS Studio\models\`
  - Linux: `~/.local/share/tts-studio/models/`
- Delete models from UI to free disk space
- List installed models
- Models NOT included in installer (downloaded separately by user)

## Hardware Requirements

### Minimum (CPU Only)
- **CPU**: 4+ cores
- **RAM**: 8GB
- **Storage**: 10GB free
- **Generation Speed**: ~2-3 min por minuto de audio

### Recommended (MPS - Apple Silicon)
- **GPU**: Apple M1/M2/M3 Pro
- **RAM**: 16GB unified memory
- **Storage**: 10GB free
- **Generation Speed**: ~15-30 seg por minuto de audio

### Optimal
- **GPU**: Apple M1/M2/M3 Max (32GB+ unified memory)
- **RAM**: 32GB unified memory
- **Storage**: SSD con 20GB+ free
- **Generation Speed**: ~10-20 seg por minuto de audio

## MPS Setup (Apple Silicon)
```bash
# Verificar MPS disponible
python -c "import torch; print(torch.backends.mps.is_available())"

# PyTorch con MPS viene incluido en instalación estándar
pip install torch torchaudio

# Configurar dtype para MPS (requerido)
# En config.yaml: dtype: "float32"
```

## Environment Setup

### Python Environment Manager
- **Tool**: `venv` (built-in Python) o `conda`
- **Why**: Aislamiento de dependencias, evitar conflictos

### Recommended: venv
```bash
python3.10 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

## Directory Structure for Data

### Development Environment (apps/core/)
```
apps/core/data/          # Development only, gitignored
├── samples/             # Test audio samples
├── outputs/             # Generated test audio
├── models/              # Downloaded models for testing
│   └── Qwen3-TTS-12Hz-1.7B-Base/
└── cache/               # Temporary cache
```

### Production Desktop App (User Directories)
```
# macOS
~/Library/Application Support/TTS Studio/
├── models/              # Downloaded TTS models
│   └── Qwen3-TTS-12Hz-1.7B-Base/
├── profiles/            # User voice profiles
├── samples/             # User audio samples
├── outputs/             # Generated audio
└── cache/               # Temporary cache

# Windows
%LOCALAPPDATA%\TTS Studio\
├── models\
├── profiles\
├── samples\
├── outputs\
└── cache\

# Linux
~/.local/share/tts-studio/
├── models/
├── profiles/
├── samples/
├── outputs/
└── cache/
```

### Model Storage Strategy
- **Development**: Models in `apps/core/data/models/` (gitignored)
- **Production**: Models in OS-specific user directories
- **Installer**: Does NOT include models (~50-100MB installer)
- **First Launch**: User downloads models on-demand via UI
- **User Control**: Can delete models to free space, re-download anytime
## Audio Format Standards

### Input Samples (Reference Voice)
- **Format**: WAV (uncompressed)
- **Sample Rate**: 12000 Hz (nativo de Qwen3-TTS)
- **Channels**: Mono (1 channel)
- **Bit Depth**: 16-bit
- **Duration**: 3-30 segundos por sample
- **Quality**: Sin ruido de fondo, voz clara

### Output Generated Audio
- **Format**: WAV (default) o MP3 (para videos)
- **Sample Rate**: 12000 Hz (matching training)
- **Channels**: Mono
- **Bit Depth**: 16-bit
- **Export**: Convertible a MP3/AAC para edición de video

## Model Specifications

### Qwen3-TTS Details
- **Size**: ~3.4GB (model weights)
- **Languages**: Soporte nativo para español y múltiples idiomas
- **Context Length**: ~2048 tokens máximo por generación
- **Reference Audio**: Usa 1-3 samples por inferencia para mejor calidad
- **Loading Time**: 30-60 seg primera carga (MPS), 2-3 min (CPU)

### Model Download Strategy

#### Development (Core Library)
- **Auto-download**: Qwen3-TTS downloads automatically on first use from Hugging Face
- **Cache Location**: `apps/core/data/models/` (configurable, gitignored)
- **Purpose**: Testing and development only

#### Production (Desktop App)
- **On-Demand Download**: User initiates download from UI
- **Storage Location**: OS-specific user directories (see above)
- **Download Flow**:
  1. User opens app for first time
  2. UI shows "No models installed" with "Download" button
  3. User clicks "Download Qwen3-TTS (~3.4GB)"
  4. Progress bar shows download status
  5. Model extracted to user directory
  6. App ready to use
- **Model Management UI**:
  - List installed models with size
  - Download new models
  - Delete models to free space
  - Re-download if needed
- **Offline Mode**: Once downloaded, works completely offline

## Configuration Management

### Config File Format
```python
# config.yaml (usando PyYAML)
model:
  name: "Qwen/Qwen3-TTS-12Hz-1.7B-Base"
  device: "mps"  # or "cpu"
  dtype: "float32"  # Required for MPS

audio:
  sample_rate: 12000
  output_format: "wav"

paths:
  samples_dir: "./data/samples"
  output_dir: "./data/outputs"
  models_cache: "./data/qwen3_models"

generation:
  language: "Spanish"
  temperature: 0.75       # Control de variabilidad
  max_new_tokens: 2048
  speed: 1.0
```

```

## Testing Strategy

### Hexagonal Testing Approach

#### Domain Tests (`apps/core/tests/domain/`)
- Test domain logic without infrastructure
- Use mocked ports (interfaces)
- Fast, isolated unit tests
- No external dependencies

```python
# Test domain without infrastructure
def test_voice_profile_validation():
    mock_processor = Mock(spec=AudioProcessor)
    mock_processor.validate_sample.return_value = True

    service = VoiceCloningService(mock_processor)
    profile = service.create_profile_from_samples("test", [Path("sample.wav")])

    assert profile.is_valid()
```

#### Application Tests (`apps/core/tests/app/`)
- Test use cases with mocked ports
- Verify orchestration logic
- Integration between domain and application

#### Infrastructure Tests (`apps/core/tests/infra/`)
- Test adapters with real implementations
- Verify Qwen3 adapter works correctly
- Test audio processing with real files
- Test file repository with real filesystem

#### Integration Tests (`apps/core/tests/integration/`)
- End-to-end tests with real components
- Test complete workflows
- Verify all layers work together

### Desktop App Testing

#### Unit Tests (Vitest)
- Test React components
- Test hooks
- Test utilities

#### Integration Tests
- Test Tauri commands
- Test Python bridge
- Test SQLite operations

### Test Framework
```python
# Python
pytest>=7.4.0            # Testing framework
pytest-cov>=4.0.0        # Coverage
hypothesis>=6.0.0        # Property-based testing
```

```json
// TypeScript
{
  "vitest": "^1.0.0",
  "@testing-library/react": "^14.0.0"
}
```
## Performance Considerations

### Batch Processing
- **Strategy**: Process multiple texts sequentially without reloading model
- **Memory Management**: Clear cache between large batches
- **Concurrency**: Single user, sequential processing

### Caching Strategy
- **Model**: Keep in memory during session
- **Voice Profile**: Load once at startup
- **Audio Samples**: Lazy load when needed

## Known Limitations & Workarounds

### Qwen3-TTS Constraints
- **Long text**: Split texts >2048 tokens into chunks
- **Punctuation**: Critical for correct intonation
- **Speaker consistency**: Use same subset of samples for coherence
- **MPS dtype**: Requires float32 (not float16) for stability

### Platform-Specific Issues
- **Windows**: May require Microsoft C++ Build Tools
- **macOS M1/M2/M3**: Use MPS (Metal) - dtype must be float32
- **Linux**: CPU-only mode (MPS not available)

## Future Enhancements
- [ ] Voice fine-tuning with more samples
- [ ] FFmpeg integration for direct MP3 export
- [ ] Additional TTS engines (XTTS, ElevenLabs)
- [ ] Direct export to video editing formats (AAC, etc.)
- [ ] CUDA support (if Qwen3-TTS adds support)
