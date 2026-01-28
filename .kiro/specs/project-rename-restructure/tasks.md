# Tasks: TTS Studio - Project Rename & Restructure (Hexagonal Architecture + Monorepo)

## Overview

Implementation tasks for migrating to TTS Studio with hexagonal architecture and monorepo structure.

**Architecture**: Hexagonal (Ports & Adapters) + Monorepo
**Duration**: 9 weeks
**Approach**: Phase by phase, layer by layer

---

## Phase 1: Monorepo Setup & Hexagonal Structure (Week 1)

### 1.1 Create Monorepo Directory Structure
- [x] Create `apps/` root directory
- [x] Create `apps/core/` for Python library
- [x] Create `apps/desktop/` for Tauri app (placeholder)
- [x] Create `packages/` for shared code (optional)

### 1.2 Create Hexagonal Layer Structure
- [x] Create `apps/core/src/domain/` layer
  - [x] Create `apps/core/src/domain/models/`
  - [x] Create `apps/core/src/domain/ports/`
  - [x] Create `apps/core/src/domain/services/`
- [x] Create `apps/core/src/application/` layer
  - [x] Create `apps/core/src/application/use_cases/`
  - [x] Create `apps/core/src/application/dto/`
  - [x] Create `apps/core/src/application/services/`
- [x] Create `apps/core/src/infrastructure/` layer
  - [x] Create `apps/core/src/infrastructure/engines/qwen3/`
  - [x] Create `apps/core/src/infrastructure/audio/`
  - [x] Create `apps/core/src/infrastructure/persistence/`
  - [x] Create `apps/core/src/infrastructure/config/`
- [x] Create `apps/core/src/api/` layer
- [x] Create `apps/core/src/shared/` utilities

### 1.3 Create Test Structure
- [x] Create `apps/core/tests/domain/`
- [x] Create `apps/core/tests/application/`
- [x] Create `apps/core/tests/infrastructure/`
- [x] Create `apps/core/tests/integration/`
- [x] Create `apps/core/tests/properties/`

### 1.4 Move Configuration Files
- [x] Move `setup.py` → `apps/core/setup.py`
- [x] Move `pyproject.toml` → `apps/core/pyproject.toml`
- [x] Move `requirements.txt` → `apps/core/requirements.txt`
- [x] Move `Makefile` → `apps/core/Makefile`
- [x] Move `.python-version` → `apps/core/.python-version`

### 1.5 Update setup.py
- [x] Change package name to `tts-studio`
- [x] Update version to `1.0.0`
- [x] Remove CLI entry points
- [x] Update package discovery path
- [x] Add new dependencies (pydantic for DTOs)

### 1.6 Update .gitignore
- [x] Add monorepo-specific ignores
- [x] Update paths for `apps/core/`
- [x] Add `apps/desktop/` ignores

### 1.7 Validation
- [x] Verify directory structure matches design
- [x] Test `cd apps/core && pip install -e .`
- [x] Verify no import errors

---

## Phase 2: Domain Layer Implementation (Week 2)

**Note**: Domain models contain ONLY pure business concepts that exist independently of application use cases. Request/Result objects are DTOs and belong in the Application layer (Phase 4).

### 2.1 Domain Models
- [x] Create `apps/core/src/domain/models/__init__.py`
- [x] Create `apps/core/src/domain/models/voice_profile.py`
  - [x] Define `VoiceProfile` entity (with ID and identity)
  - [x] Add `add_sample()` method
  - [x] Add `is_valid()` method
  - [x] Add `total_duration` property
  - [x] Add `remove_sample()` method
- [x] Create `apps/core/src/domain/models/audio_sample.py`
  - [x] Define `AudioSample` value object (immutable)
  - [x] Add validation in constructor
  - [x] Add `is_valid_duration()` method
  - [x] Add `is_valid_sample_rate()` method

### 2.2 Domain Ports (Interfaces)
- [x] Create `apps/core/src/domain/ports/__init__.py`
- [x] Create `apps/core/src/domain/ports/tts_engine.py`
  - [x] Define `TTSEngine` ABC
  - [x] Add `get_supported_modes()` abstract method
  - [x] Add `generate_audio()` abstract method
  - [x] Add `validate_profile()` abstract method
- [x] Create `apps/core/src/domain/ports/audio_processor.py`
  - [x] Define `AudioProcessor` ABC
  - [x] Add `validate_sample()` abstract method
  - [x] Add `process_sample()` abstract method
  - [x] Add `normalize_audio()` abstract method
- [x] Create `apps/core/src/domain/ports/profile_repository.py`
  - [x] Define `ProfileRepository` ABC
  - [x] Add `save()` abstract method
  - [x] Add `find_by_id()` abstract method
  - [x] Add `list_all()` abstract method
  - [x] Add `delete()` abstract method
- [x] Create `apps/core/src/domain/ports/config_provider.py`
  - [x] Define `ConfigProvider` ABC

### 2.3 Domain Services
- [x] Create `apps/core/src/domain/services/__init__.py`
- [x] Create `apps/core/src/domain/services/voice_cloning.py`
  - [x] Define `VoiceCloningService` class
  - [x] Inject `AudioProcessor` port in constructor
  - [x] Implement `create_profile_from_samples()` method
  - [x] Add validation logic (pure business rules)
- [x] Create `apps/core/src/domain/services/audio_generation.py`
  - [x] Define `AudioGenerationService` class
  - [x] Add generation orchestration logic

### 2.4 Domain Exceptions
- [x] Create `apps/core/src/domain/exceptions.py`
  - [x] Define `DomainException` base class
  - [x] Define `InvalidProfileException`
  - [x] Define `InvalidSampleException`
  - [x] Define `GenerationException`

### 2.5 Domain Tests
- [x] Create `apps/core/tests/domain/models/test_voice_profile.py`
  - [x] Test `VoiceProfile` creation
  - [x] Test `add_sample()` method
  - [x] Test `is_valid()` validation
- [x] Create `apps/core/tests/domain/services/test_voice_cloning.py`
  - [x] Test `create_profile_from_samples()` with mocks
  - [x] Test validation logic
  - [x] Test error handling
- [x] Verify domain tests pass without infrastructure

### 2.6 Validation
- [x] Domain layer has ZERO infrastructure dependencies
- [x] All domain tests pass with mocks only
- [x] `pytest apps/core/tests/domain/` passes
- [x] No imports from `infrastructure/` in domain

---

## Phase 3: Infrastructure Adapters (Week 3)

### 3.1 Qwen3 TTS Engine Adapter
- [x] Create `apps/core/src/infrastructure/engines/qwen3/__init__.py`
- [x] Create `apps/core/src/infrastructure/engines/qwen3/adapter.py`
  - [x] Define `Qwen3Adapter` class implementing `TTSEngine` port
  - [x] Implement `get_supported_modes()` method
  - [x] Implement `generate_audio()` method
  - [x] Implement `validate_profile()` method
- [x] Move existing Qwen3 code from `src/voice_clone/model/`
  - [x] Move `qwen3_manager.py` → `model_loader.py`
  - [x] Move `qwen3_generator.py` → `inference.py`
  - [x] Refactor to work with adapter pattern
- [x] Create `apps/core/src/infrastructure/engines/qwen3/modes/`
  - [x] Move clone mode implementation
  - [x] Move custom voice mode implementation
  - [x] Move voice design mode implementation
- [x] Create `apps/core/src/infrastructure/engines/qwen3/config.py`

### 3.2 Audio Processor Adapter
- [x] Create `apps/core/src/infrastructure/audio/__init__.py`
- [x] Create `apps/core/src/infrastructure/audio/processor_adapter.py`
  - [x] Define `LibrosaAudioProcessor` implementing `AudioProcessor` port
  - [x] Implement `validate_sample()` method
  - [x] Implement `process_sample()` method
  - [x] Implement `normalize_audio()` method
- [x] Move existing audio code from `src/voice_clone/audio/`
  - [x] Move `processor.py` logic to adapter
  - [x] Move `validator.py` logic to adapter
- [x] Create `apps/core/src/infrastructure/audio/converter.py`
- [x] Create `apps/core/src/infrastructure/audio/effects.py`

### 3.3 Profile Repository Adapter
- [x] Create `apps/core/src/infrastructure/persistence/__init__.py`
- [x] Create `apps/core/src/infrastructure/persistence/file_profile_repository.py`
  - [x] Define `FileProfileRepository` implementing `ProfileRepository` port
  - [x] Implement `save()` method (JSON serialization)
  - [x] Implement `find_by_id()` method
  - [x] Implement `list_all()` method
  - [x] Implement `delete()` method
- [ ] Create `apps/core/src/infrastructure/persistence/json_serializer.py`
  - [x] Implement serialization logic
  - [x] Implement deserialization logic

### 3.4 Config Provider Adapter
- [x] Create `apps/core/src/infrastructure/config/__init__.py`
- [x] Create `apps/core/src/infrastructure/config/yaml_config.py`
  - [x] Define `YAMLConfigProvider` implementing `ConfigProvider` port
  - [x] Implement config loading from YAML
  - [x] Implement config merging (defaults + user)
- [x] Create `apps/core/src/infrastructure/config/env_config.py`
  - [x] Support environment variables

### 3.5 Infrastructure Tests
- [x] Create `apps/core/tests/infrastructure/engines/test_qwen3_adapter.py`
  - [x] Test adapter implements port correctly
  - [x] Test `generate_audio()` with real Qwen3
  - [x] Test mode switching
- [x] Create `apps/core/tests/infrastructure/audio/test_processor_adapter.py`
  - [x] Test audio validation
  - [x] Test audio processing
  - [x] Test normalization
- [x] Create `apps/core/tests/infrastructure/persistence/test_file_repository.py`
  - [x] Test save/load profiles
  - [x] Test JSON serialization
  - [x] Test file operations

### 3.6 Validation
- [x] All adapters implement their respective ports
- [x] `pytest apps/core/tests/infrastructure/` passes
- [x] Qwen3 adapter can generate audio
- [x] Audio processor can validate samples
- [x] Repository can save/load profiles

---

## Phase 4: Application Layer (Week 4)

### 4.1 DTOs (Data Transfer Objects)
- [x] Create `apps/core/src/application/dto/__init__.py`
- [x] Create `apps/core/src/application/dto/voice_profile_dto.py`
  - [x] Define `VoiceProfileDTO` dataclass
  - [x] Add `from_entity()` class method
  - [x] Add `to_dict()` method
- [x] Create `apps/core/src/application/dto/generation_dto.py`
  - [x] Define `GenerationRequestDTO` dataclass
  - [x] Define `GenerationResultDTO` dataclass
  - [x] Add serialization methods
- [x] Create `apps/core/src/application/dto/batch_dto.py`
  - [x] Define `BatchRequestDTO` dataclass
  - [x] Define `BatchResultDTO` dataclass

### 4.2 Use Cases
- [x] Create `apps/core/src/application/use_cases/__init__.py`
- [x] Create `apps/core/src/application/use_cases/create_voice_profile.py`
  - [x] Define `CreateVoiceProfileUseCase` class
  - [x] Inject `AudioProcessor` and `ProfileRepository` ports
  - [x] Implement `execute()` method
  - [x] Use `VoiceCloningService` from domain
  - [x] Return `VoiceProfileDTO`
- [x] Create `apps/core/src/application/use_cases/generate_audio.py`
  - [x] Define `GenerateAudioUseCase` class
  - [x] Inject `TTSEngine` and `ProfileRepository` ports
  - [x] Implement `execute()` method
  - [x] Return `GenerationResultDTO`
- [x] Create `apps/core/src/application/use_cases/list_voice_profiles.py`
  - [x] Define `ListVoiceProfilesUseCase` class
  - [x] Inject `ProfileRepository` port
  - [x] Implement `execute()` method
- [x] Create `apps/core/src/application/use_cases/validate_audio_samples.py`
  - [x] Define `ValidateAudioSamplesUseCase` class
  - [x] Inject `AudioProcessor` port
  - [x] Implement `execute()` method
- [x] Create `apps/core/src/application/use_cases/process_batch.py`
  - [x] Define `ProcessBatchUseCase` class
  - [x] Inject necessary ports
  - [x] Implement batch processing logic

### 4.3 Application Services (SKIPPED - YAGNI)
**Decision**: Application Services are not needed at this time because:
- All use cases are self-contained and well-defined
- `ProcessBatchUseCase` already handles the orchestration we need
- No complex transactions requiring coordination
- API layer can call use cases directly
- Following YAGNI principle - will add if needed in future

- [x]* Create `apps/core/src/app/services/__init__.py` (skipped)
- [x]* Create `apps/core/src/app/services/orchestrator.py` (skipped)
  - [x]* Define `ApplicationOrchestrator` class (skipped)
  - [x]* Coordinate multiple use cases if needed (skipped)

### 4.4 Application Tests
- [x] Create `apps/core/tests/app/use_cases/test_create_voice_profile.py`
  - [x] Test use case with mocked ports
  - [x] Test orchestration logic
  - [x] Test error handling
- [x] Create `apps/core/tests/app/use_cases/test_generate_audio.py`
  - [x] Test use case with mocked ports
  - [x] Test profile loading
  - [x] Test generation flow
- [x] Create `apps/core/tests/app/use_cases/test_list_voice_profiles.py`
  - [x] Test listing profiles
  - [x] Test empty repository
  - [x] Test DTO conversion
- [x] Create `apps/core/tests/app/use_cases/test_validate_audio_samples.py`
  - [x] Test validation with valid samples
  - [x] Test validation with invalid samples
  - [x] Test validation summary
- [x] Create `apps/core/tests/app/use_cases/test_process_batch.py`
  - [x] Test batch processing logic
  - [x] Test error handling per segment
  - [x] Test partial failures

### 4.5 Validation
- [x] Use cases orchestrate domain and infrastructure correctly
- [x] `pytest apps/core/tests/application/` passes
- [x] Use cases work with mocked adapters
- [x] DTOs serialize/deserialize correctly

---

## Phase 5: API Layer (Week 5)

### 5.1 Python API Implementation
- [ ] Create `apps/core/src/api/__init__.py`
- [ ] Create `apps/core/src/api/python_api.py`
  - [ ] Define `TTSStudioAPI` class
  - [ ] Initialize all adapters in `__init__()`
  - [ ] Initialize all use cases
  - [ ] Implement `create_voice_profile()` method
  - [ ] Implement `generate_audio()` method
  - [ ] Implement `list_voice_profiles()` method
  - [ ] Implement `delete_voice_profile()` method
  - [ ] Implement `validate_samples()` method
  - [ ] Add error handling (try/except with status dict)
  - [ ] Add logging

### 5.2 CLI Interface for Subprocess (Tauri Bridge)
- [ ] Create `apps/core/src/api/cli.py`
  - [ ] Add argparse CLI for subprocess calls
  - [ ] Add `generate` command
  - [ ] Add `list-profiles` command
  - [ ] Add `create-profile` command
  - [ ] Output JSON for Tauri to parse
  - [ ] Add `if __name__ == '__main__'` block

### 5.3 API Tests
- [ ] Create `apps/core/tests/api/test_python_api.py`
  - [ ] Test API initialization
  - [ ] Test `create_voice_profile()` with real adapters
  - [ ] Test `generate_audio()` with real adapters
  - [ ] Test error handling
  - [ ] Test JSON response format
- [ ] Create `apps/core/tests/api/test_cli.py`
  - [ ] Test CLI commands
  - [ ] Test JSON output
  - [ ] Test subprocess invocation

### 5.4 Example Usage
- [ ] Create `examples/api_usage.py`
  - [ ] Show basic API usage
  - [ ] Show profile creation
  - [ ] Show audio generation
  - [ ] Show error handling
- [ ] Create `examples/subprocess_usage.py`
  - [ ] Show how Tauri will call Python

### 5.5 Validation
- [ ] API can be called from Python
- [ ] API returns proper JSON responses
- [ ] `pytest apps/core/tests/api/` passes
- [ ] CLI subprocess calls work
- [ ] Examples run successfully

---

## Phase 6: Delete CLI and Gradio (Week 6)

### 6.1 Delete CLI Code
- [ ] Delete `src/cli/` directory completely
- [ ] Delete `tests/cli/` directory completely
- [ ] Delete `examples/test_validation_handler.py`
- [ ] Remove CLI entry points from `apps/core/setup.py`
- [ ] Remove `click` from `apps/core/requirements.txt`

### 6.2 Delete Gradio Code
- [ ] Delete `src/gradio_ui/` directory completely
- [ ] Delete `tests/gradio_ui/` directory completely
- [ ] Remove `gradio` from `apps/core/requirements.txt`
- [ ] Remove any Gradio-related dependencies

### 6.3 Update Documentation
- [ ] Update `README.md`
  - [ ] Remove CLI usage examples
  - [ ] Remove Gradio UI references
  - [ ] Add Python API usage
  - [ ] Add Tauri desktop app reference
- [ ] Update `docs/usage.md`
  - [ ] Remove CLI commands
  - [ ] Add Python API examples
  - [ ] Add desktop app usage
- [ ] Update `docs/installation.md`
  - [ ] Remove CLI installation
  - [ ] Add Python library installation
  - [ ] Add desktop app installation
- [ ] Update `docs/api.md`
  - [ ] Document new Python API
  - [ ] Document hexagonal architecture
  - [ ] Add adapter examples

### 6.4 Update Steering Files
- [ ] Update `.kiro/steering/product.md`
  - [ ] Remove CLI/Gradio references
  - [ ] Add desktop app features
  - [ ] Update architecture description
- [ ] Update `.kiro/steering/tech.md`
  - [ ] Add hexagonal architecture
  - [ ] Remove CLI/Gradio tech
  - [ ] Add Tauri tech stack
- [ ] Update `.kiro/steering/structure.md`
  - [ ] Document monorepo structure
  - [ ] Document hexagonal layers
  - [ ] Update file organization

### 6.5 Clean Up Tests
- [ ] Remove CLI test imports
- [ ] Remove Gradio test imports
- [ ] Fix any broken test imports
- [ ] Update test fixtures
- [ ] Update conftest.py

### 6.6 Validation
- [ ] No CLI or Gradio code remains
- [ ] All remaining tests pass
- [ ] No broken imports
- [ ] Documentation is consistent
- [ ] `pytest apps/core/` passes

---

## Phase 7: Testing & Documentation (Week 7)

### 7.1 Integration Tests
- [ ] Create `apps/core/tests/integration/test_end_to_end.py`
  - [ ] Test complete workflow: create profile → generate audio
  - [ ] Test with real infrastructure (Qwen3, librosa, files)
  - [ ] Test error scenarios
- [ ] Create `apps/core/tests/integration/test_hexagonal_architecture.py`
  - [ ] Test dependency inversion
  - [ ] Test adapter swapping
  - [ ] Test port implementations

### 7.2 Property-Based Tests
- [ ] Create `apps/core/tests/properties/test_domain_properties.py`
  - [ ] Test domain invariants
  - [ ] Test voice profile properties
  - [ ] Test audio sample properties
- [ ] Create `apps/core/tests/properties/test_use_case_properties.py`
  - [ ] Test use case properties
  - [ ] Test idempotency where applicable

### 7.3 Documentation
- [ ] Create `docs/MIGRATION.md`
  - [ ] Document Python API migration
  - [ ] Show before/after code examples
  - [ ] Document hexagonal architecture
  - [ ] Add FAQ section
- [ ] Create `docs/HEXAGONAL_ARCHITECTURE.md`
  - [ ] Explain hexagonal architecture
  - [ ] Document layers (domain, application, infrastructure, API)
  - [ ] Show dependency flow
  - [ ] Add diagrams
  - [ ] Explain ports & adapters pattern
- [ ] Update `docs/development.md`
  - [ ] Document monorepo structure
  - [ ] Add development workflow
  - [ ] Add testing guidelines
- [ ] Update `CHANGELOG.md`
  - [ ] Document breaking changes
  - [ ] List new features
  - [ ] Add migration notes

### 7.4 Code Quality
- [ ] Run `black` on all Python code
- [ ] Run `ruff check` and fix issues
- [ ] Run `mypy` for type checking
- [ ] Add type hints to all public APIs
- [ ] Add docstrings to all public classes/methods
- [ ] Check code coverage (target >80%)

### 7.5 CI/CD Updates
- [ ] Update `.github/workflows/ci-python.yml`
  - [ ] Update paths to `apps/core/`
  - [ ] Add hexagonal architecture validation
  - [ ] Test on Python 3.10, 3.11
- [ ] Create `.github/workflows/ci-rust.yml` (placeholder for Tauri)
- [ ] Create `.github/workflows/ci-typescript.yml` (placeholder for Tauri)
- [ ] Update pre-commit hooks for monorepo

### 7.6 Validation
- [ ] `pytest apps/core/` passes (all tests)
- [ ] Code coverage >80%
- [ ] CI/CD green
- [ ] Documentation reviewed
- [ ] No linting errors
- [ ] Type checking passes

---

## Phase 8: Tauri Desktop App Setup (Week 8)

### 8.1 Create Tauri Structure
- [ ] `cd apps/desktop`
- [ ] Run `npm create tauri-app@latest`
- [ ] Configure project name: "TTS Studio"
- [ ] Select React + TypeScript + Vite

### 8.2 Configure Tauri Backend
- [ ] Update `apps/desktop/src-tauri/Cargo.toml`
  - [ ] Add dependencies (serde, tokio, rusqlite)
- [ ] Update `apps/desktop/src-tauri/tauri.conf.json`
  - [ ] Configure app name, version
  - [ ] Configure window settings
  - [ ] Configure permissions

### 8.3 Python Bridge Implementation
- [ ] Create `apps/desktop/src-tauri/src/python_bridge.rs`
  - [ ] Implement subprocess management
  - [ ] Add `call_python_api()` function
  - [ ] Add error handling
  - [ ] Add JSON parsing
- [ ] Create `apps/desktop/src-tauri/src/commands/`
  - [ ] Create `profiles.rs` (profile commands)
  - [ ] Create `generation.rs` (generation commands)
  - [ ] Create `samples.rs` (sample commands)
  - [ ] Create `models.rs` (model management commands)

### 8.4 Tauri Commands
- [ ] Implement `create_voice_profile` command
- [ ] Implement `list_voice_profiles` command
- [ ] Implement `generate_audio` command
- [ ] Implement `validate_samples` command
- [ ] Implement `download_model` command
- [ ] Implement `list_installed_models` command

### 8.5 Test Integration
- [ ] Test Tauri can launch
- [ ] Test Python subprocess communication
- [ ] Test Tauri commands call Python API
- [ ] Test JSON response parsing
- [ ] Test error handling

### 8.6 Validation
- [ ] Tauri app launches successfully
- [ ] Can call Python API from Rust
- [ ] Communication works bidirectionally
- [ ] Error handling works
- [ ] JSON serialization works

**Note**: Full Tauri UI implementation is in separate spec (`tauri-desktop-ui`)

---

## Phase 9: Release (Week 9)

### 9.1 Final Testing
- [ ] Run full test suite: `pytest apps/core/`
- [ ] Manual testing of Python API
- [ ] Manual testing of Tauri integration
- [ ] Performance testing (generation speed)
- [ ] Memory usage testing
- [ ] Test on different platforms (macOS, Linux)
- [ ] Test with different Python versions (3.10, 3.11)

### 9.2 Version Update
- [ ] Update version to `1.0.0` in `apps/core/setup.py`
- [ ] Update version in `apps/core/pyproject.toml`
- [ ] Update `CHANGELOG.md` with all changes
- [ ] Create release notes

### 9.3 Build Package
- [ ] `cd apps/core`
- [ ] Clean old builds: `rm -rf dist/ build/`
- [ ] Build package: `python setup.py sdist bdist_wheel`
- [ ] Verify package: `twine check dist/*`

### 9.4 Git Release
- [ ] Commit all changes
- [ ] Create git tag: `git tag v1.0.0`
- [ ] Push tag: `git push origin v1.0.0`
- [ ] Create GitHub release with notes

### 9.5 Publish to PyPI
- [ ] Test publish to TestPyPI first
  - [ ] `twine upload --repository testpypi dist/*`
  - [ ] Test install: `pip install --index-url https://test.pypi.org/simple/ tts-studio`
- [ ] Publish to PyPI
  - [ ] `twine upload dist/*`
  - [ ] Verify on PyPI: https://pypi.org/project/tts-studio/

### 9.6 Update Documentation
- [ ] Update README badges
- [ ] Update installation instructions
- [ ] Update links to documentation
- [ ] Update examples

### 9.7 Announcement
- [ ] Create GitHub release announcement
- [ ] Update project description
- [ ] Monitor for issues
- [ ] Respond to user feedback

### 9.8 Validation
- [ ] `pip install tts-studio` works
- [ ] Package downloads successfully
- [ ] No critical issues reported
- [ ] Documentation is accessible
- [ ] Examples work

---

## Summary

| Phase | Duration | Tasks | Key Deliverable |
|-------|----------|-------|-----------------|
| 1 | Week 1 | 7 | Monorepo + hexagonal structure |
| 2 | Week 2 | 6 | Domain layer (pure business logic) |
| 3 | Week 3 | 6 | Infrastructure adapters (Qwen3, audio, persistence) |
| 4 | Week 4 | 5 | Application layer (use cases, DTOs) |
| 5 | Week 5 | 5 | API layer (Python API for Tauri) |
| 6 | Week 6 | 6 | Delete CLI/Gradio, update docs |
| 7 | Week 7 | 6 | Testing, documentation, CI/CD |
| 8 | Week 8 | 6 | Tauri setup, Python bridge |
| 9 | Week 9 | 8 | Release v1.0.0 |

**Total**: 55 task groups across 9 weeks

---

## Critical Path

1. **Phase 1-2** must be completed before Phase 3 (domain before infrastructure)
2. **Phase 3** must be completed before Phase 4 (adapters before use cases)
3. **Phase 4** must be completed before Phase 5 (use cases before API)
4. **Phase 5** must be completed before Phase 8 (API before Tauri integration)
5. **Phase 6-7** can run in parallel with Phase 8
6. **Phase 9** requires all previous phases complete

---

## Notes

- Each task should be marked as complete when done
- Tasks can be broken down further if needed
- Some tasks may be done in parallel within a phase
- Testing should be continuous throughout all phases
- Documentation should be updated as code changes
- Hexagonal architecture principles must be maintained throughout

---

## Hexagonal Architecture Validation Checklist

After each phase, verify:
- [ ] Domain layer has NO infrastructure dependencies
- [ ] All ports (interfaces) are defined in domain
- [ ] All adapters implement their respective ports
- [ ] Use cases only depend on ports, not adapters
- [ ] API layer wires everything together (dependency injection)
- [ ] Tests can use mocks for all ports
- [ ] Easy to swap implementations (e.g., Qwen3 → XTTS)
