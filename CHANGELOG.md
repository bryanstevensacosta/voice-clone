# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security

## [1.0.0] - 2026-01-29

### Added
- **Hexagonal Architecture**: Clean architecture with ports & adapters pattern
- **Monorepo Structure**: Separate apps for core library (`apps/core/`) and desktop app (`apps/desktop/`)
- **Python API**: Programmatic access via `TTSStudio` class
- **Domain Layer**: Pure business logic with no external dependencies
- **Application Layer**: Use cases for orchestrating workflows
- **Infrastructure Layer**: Adapters for TTS engines, audio processing, and storage
- **API Layer**: Entry point with dependency injection
- **Integration Tests**: End-to-end workflow tests
- **Property-Based Tests**: Hypothesis-based tests for domain invariants
- **Hexagonal Architecture Tests**: Verify architectural boundaries
- **Documentation**:
  - `MIGRATION.md` - Migration guide from v0.x to v1.0.0
  - `HEXAGONAL_ARCHITECTURE.md` - Architecture guide
  - Updated `development.md` with monorepo and testing guidelines
- **DTOs**: Data transfer objects for clean API boundaries
- **Ports**: Interfaces for TTS engines, audio processors, and repositories
- **Adapters**: Qwen3 TTS engine, librosa audio processor, file repository

### Changed
- **BREAKING**: Removed CLI (`voice-clone` commands)
- **BREAKING**: Removed Gradio UI
- **BREAKING**: Package structure changed to monorepo
- **BREAKING**: Import paths changed (use `api.studio.TTSStudio`)
- **BREAKING**: Configuration structure updated for hexagonal architecture
- Project renamed from `voice-clone-cli` to `tts-studio`
- All business logic moved to domain layer
- All infrastructure moved to adapters
- Test structure reorganized by architecture layers
- Documentation updated for Python API usage
- Steering files updated with hexagonal architecture

### Deprecated
- `docs/ui-guide.md` - Replaced with Python API usage
- `docs/SVELTE_UI_SPECIFICATION.md` - Tauri chosen instead

### Removed
- **CLI**: All `voice-clone` commands removed
- **Gradio UI**: Web interface removed
- `src/cli/` directory and all CLI code
- `src/gradio_ui/` directory and all Gradio code
- `click` dependency (CLI framework)
- `gradio` dependency (UI framework)
- CLI entry points from `setup.py`
- Old test files for CLI and Gradio

### Fixed
- Improved testability with dependency inversion
- Better separation of concerns
- Cleaner error handling with domain exceptions
- More maintainable codebase with hexagonal architecture

### Security
- Domain layer isolated from external dependencies
- Better validation with domain services
- Cleaner boundaries between layers

### Migration Notes

**From v0.x to v1.0.0**:

1. **Uninstall old package**:
   ```bash
   pip uninstall voice-clone-cli
   ```

2. **Install new package**:
   ```bash
   cd apps/core
   pip install -e .
   ```

3. **Update code to use Python API**:
   ```python
   from api.studio import TTSStudio

   studio = TTSStudio()
   result = studio.create_voice_profile(
       name='my_voice',
       sample_paths=['./data/samples/sample1.wav']
   )
   ```

4. **See `docs/MIGRATION.md` for detailed migration guide**

### Architecture

**Hexagonal Architecture Layers**:
- **Domain**: Pure business logic (NO external dependencies)
- **Application**: Use cases (orchestration)
- **Infrastructure**: Adapters (implementations)
- **API**: Entry points (dependency injection)

**Benefits**:
- Easy to test (mock adapters)
- Easy to swap implementations (Qwen3 → XTTS)
- Easy to extend (add new engines, processors, storage)
- Clean, maintainable codebase

**See `docs/HEXAGONAL_ARCHITECTURE.md` for detailed architecture guide**

## [0.2.0] - 2026-01-24

### Added
- Qwen3-TTS integration for voice cloning
- MPS (Apple Silicon) support with Metal Performance Shaders
- Automated migration script (`scripts/migrate_to_qwen3.sh`)
- Comprehensive migration guide (`MIGRATION.md`)
- Property-based tests for migration verification
- System cleanup tests for Coqui TTS removal
- Voice profile migration utilities
- Support for 1-3 voice samples (reduced from 6-10)
- `ref_text` field in voice profiles for better cloning

### Changed
- **BREAKING**: Migrated from Coqui TTS (XTTS-v2) to Qwen3-TTS
- **BREAKING**: Sample rate changed from 22050 Hz to 12000 Hz
- **BREAKING**: Device configuration changed from CUDA to MPS/CPU
- **BREAKING**: Minimum sample duration reduced from 6s to 3s
- Updated all CLI commands to use Qwen3-TTS
- Updated configuration files for Qwen3-TTS
- Updated all documentation for Qwen3-TTS
- Updated steering files with Qwen3-TTS specifications
- Model cache directory: `./data/models`
- Dtype configuration now requires `float32` for MPS

### Removed
- Coqui TTS (XTTS-v2) dependency
- Old model manager (`src/voice_clone/model/manager.py`)
- Old generator (`src/voice_clone/model/generator.py`)
- TTS.api imports and references
- XTTS-v2 specific code and tests
- Old test files for Coqui TTS

### Fixed
- Audio processor validation for 12000 Hz sample rate
- Batch processor compatibility with Qwen3-TTS
- Configuration validation for new model format

### Security
- Removed deprecated Coqui TTS package
- Updated to actively maintained Qwen3-TTS

## Version Format

Versions follow [Semantic Versioning](https://semver.org/):

- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality additions
- **PATCH** version for backwards-compatible bug fixes

### Version Examples

- `1.0.0` - First stable release
- `1.1.0` - Added new feature (backwards-compatible)
- `1.1.1` - Fixed bug (backwards-compatible)
- `2.0.0` - Breaking change (not backwards-compatible)

## Change Categories

- **Added** - New features
- **Changed** - Changes in existing functionality
- **Deprecated** - Soon-to-be removed features
- **Removed** - Removed features
- **Fixed** - Bug fixes
- **Security** - Security vulnerability fixes

## How to Update This File

When making changes to the project:

1. Add your changes under the `[Unreleased]` section
2. Use the appropriate category (Added, Changed, Fixed, etc.)
3. Write clear, user-focused descriptions
4. Link to relevant issues/PRs when applicable

### Example Entry

```markdown
## [Unreleased]

### Added
- Voice cloning functionality using XTTS-v2 (#42)
- Interactive mode for real-time synthesis (#45)

### Fixed
- Audio processing bug with stereo files (#38)
- Memory leak in model loading (#40)
```

When releasing a new version:

1. Move items from `[Unreleased]` to a new version section
2. Add the release date
3. Update the version comparison links at the bottom

### Example Release

```markdown
## [1.0.0] - 2026-01-23

### Added
- Voice cloning functionality using XTTS-v2 (#42)
- Interactive mode for real-time synthesis (#45)

### Fixed
- Audio processing bug with stereo files (#38)
- Memory leak in model loading (#40)
```

## Links

[Unreleased]: https://github.com/bryanstevensacosta/tts-studio/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/bryanstevensacosta/tts-studio/compare/v0.2.0...v1.0.0
[0.2.0]: https://github.com/bryanstevensacosta/tts-studio/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/bryanstevensacosta/tts-studio/releases/tag/v0.1.0
