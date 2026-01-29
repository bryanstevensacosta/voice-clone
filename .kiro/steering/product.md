---
inclusion: always
---

# Product Overview - TTS Studio

## Purpose
Desktop application for voice cloning and text-to-speech synthesis using Qwen3-TTS, enabling content creators to generate natural-sounding narration for YouTube, TikTok, and other social media platforms without appearing on camera.

## Target User
- **Primary User**: Content creators, YouTubers, podcasters
- **Profile**: Users who want professional voice narration without recording every time
- **Technical Level**: No technical knowledge required - desktop app with intuitive UI
- **Environment**: Desktop application (macOS, Windows, Linux)

## Core Use Case
1. **Setup**: Download and install desktop app (~50-100MB, no models included)
2. **Model Download**: On first launch, download Qwen3-TTS model (~3.4GB) from UI
3. **Profile Creation**: Upload 1-3 audio samples with different tones/emotions
4. **Voice Cloning**: App processes samples to create voice profile
5. **Generation**: Convert text to audio using cloned voice via desktop UI
6. **Export**: Download generated audio for video editing

## Key Features

### Desktop Application (Tauri + React)
- **Native UI**: Modern desktop app with intuitive interface
- **Offline-First**: Works completely offline after model download
- **No Login**: No authentication required, everything local
- **Model Management**: Download, install, and manage TTS models
- **Voice Profiles**: Create and manage multiple voice profiles
- **Audio Generation**: Generate speech from text with real-time preview
- **Batch Processing**: Process multiple text segments at once
- **Export Options**: Export to WAV, MP3, AAC for video editing

### Core Library (Python)
- **Hexagonal Architecture**: Clean, testable, maintainable code
- **Multiple Engines**: Support for Qwen3-TTS (more engines in future)
- **Audio Processing**: Validation, normalization, format conversion
- **Batch Processing**: Efficient processing of multiple segments
- **Python API**: Can be used as library for advanced users

### Quality Requirements
- **Language**: Full support for Spanish (Latin American and Castilian)
- **Audio Quality**: Minimum 12kHz, native to Qwen3-TTS
- **Naturalness**: Preserve intonation and emotions from original samples
- **Consistency**: Stable and coherent voice across generations
- **Performance**: <30 seconds for 1 minute of audio (on GPU)

## Architecture

### Monorepo Structure
- **apps/core/**: Python core library with hexagonal architecture
- **apps/desktop/**: Tauri desktop app (React + TypeScript + Rust)
- **Separation**: Clear boundaries between core logic and UI

### Hexagonal Architecture (Core Library)
- **Domain Layer**: Pure business logic, no external dependencies
- **Application Layer**: Use cases, orchestration
- **Infrastructure Layer**: TTS engines, audio processing, storage
- **API Layer**: Python API for Tauri backend

### Desktop-First Principles
- **Offline-First**: Everything works without internet (except model downloads)
- **No Login/Registration**: No authentication, everything local
- **Privacy**: All data stored locally, no cloud sync
- **Native Performance**: Fast, responsive desktop app

## Non-Features (Explicitly NOT Included)
- ❌ Authentication/Login/Registration
- ❌ REST API or GraphQL
- ❌ Web UI (browser-based)
- ❌ CLI (command-line interface)
- ❌ Database (uses SQLite locally)
- ❌ Multi-user support
- ❌ Cloud deployment
- ❌ Containerization (Docker)
- ❌ CD (Continuous Deployment)
- ✅ CI (Continuous Integration) - YES, to maintain code quality

## Technical Constraints
- **Hardware**: MPS (Apple Silicon) recommended for optimal speed, CPU supported but slower
- **Storage**:
  - App installer: ~50-100MB
  - Qwen3-TTS model: ~3.4GB (downloaded separately by user)
  - User data (samples, profiles, outputs): ~1-5GB
  - Total: ~5-10GB recommended free space
- **Python Version**: 3.10-3.11 (for core library, bundled with app)
- **OS**: macOS, Windows, Linux (Tauri supports all platforms)
- **Internet**: Required only for initial model download (~3.4GB)

## Success Metrics
- ✅ Generate coherent audio from text
- ✅ Perceptible similarity to real voice
- ✅ Reasonable generation time (<30 sec for 1 min audio on GPU)
- ✅ Audio ready for video editing without extensive post-processing
- ✅ Intuitive desktop UI that non-technical users can use
- ✅ Offline functionality after initial setup

## Project Phases

### Phase 1: Core Library Restructure (Current)
- Implement hexagonal architecture
- Restructure to monorepo with `apps/core/`
- Migrate all Python code
- Remove CLI and Gradio UI
- Update documentation

### Phase 2: Desktop UI Development
- Implement Tauri backend (Rust)
- Implement React frontend (FSD architecture)
- Python bridge for core library
- SQLite for local storage
- Model management UI

### Phase 3: Feature Completion
- Voice profile management
- Audio generation with preview
- Batch processing
- Export options
- Settings and preferences

### Phase 4: Polish & Release
- UI/UX improvements
- Performance optimization
- Testing and bug fixes
- Documentation
- Release v1.0.0

## Business Objectives
- **Efficiency**: Produce video narration without recording audio every time
- **Consistency**: Maintain same voice across all videos
- **Privacy**: Complete control of voice data (local-only)
- **Flexibility**: Easy to iterate and regenerate audio
- **Accessibility**: Desktop app accessible to non-technical users
- **Scalability**: Produce more content in less time
