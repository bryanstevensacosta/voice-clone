# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project setup
- Git repository initialization
- Pre-commit hooks configuration
- MIT License
- Open source documentation (README, CONTRIBUTING, CODE_OF_CONDUCT)
- Development environment configuration
- Project structure and tooling

### Changed

### Deprecated

### Removed

### Fixed

### Security

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

[Unreleased]: https://github.com/yourusername/voice-clone-cli/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/yourusername/voice-clone-cli/releases/tag/v0.1.0
