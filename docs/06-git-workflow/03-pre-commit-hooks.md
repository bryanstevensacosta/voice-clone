# Pre-commit Hooks Configuration Guide

## Overview
This document describes the complete pre-commit and pre-push hooks configuration for the TTS Studio monorepo, including solutions to common issues with Mypy, pytest, and formatting tools.

## Architecture

### Hook Types
- **Pre-commit hooks**: Run before each commit (fast checks, auto-fixes)
- **Pre-push hooks**: Run before pushing to remote (slower checks like tests)

### Monorepo Considerations
- Hooks are scoped to `apps/core/` (Python library)
- Hooks run in the project's virtualenv (not pre-commit's isolated env)
- Configuration is consistent between local and CI/CD

## Complete Configuration

### .pre-commit-config.yaml

```yaml
repos:
  # Ruff - Fast linting, import sorting, and formatting
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.9
    hooks:
      - id: ruff
        args: ['--fix', '--exit-non-zero-on-fix']  # Fail if fixes needed
        files: ^apps/core/
      - id: ruff-format
        files: ^apps/core/

  # Mypy - Type checking (custom local hook for monorepo)
  - repo: local
    hooks:
      - id: mypy
        name: mypy
        entry: bash -c 'cd apps/core && if [ -d "venv" ]; then source venv/bin/activate; elif [ -d ".venv" ]; then source .venv/bin/activate; fi && python -m mypy src --config-file=pyproject.toml'
        language: system
        types: [python]
        files: ^apps/core/src/
        exclude: '^apps/core/src/domain/'
        pass_filenames: false
        require_serial: true

  # Pytest - Run tests on pre-push
  - repo: local
    hooks:
      - id: pytest-check
        name: pytest
        entry: bash -c 'cd apps/core && if [ -d "venv" ]; then source venv/bin/activate; elif [ -d ".venv" ]; then source .venv/bin/activate; fi && python -m pytest tests/domain tests/app -q --tb=short'
        language: system
        pass_filenames: false
        always_run: true
        stages: [pre-push]

  # Pre-commit hooks for common issues
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: ['--maxkb=1000']
      - id: check-merge-conflict
      - id: check-case-conflict
      - id: mixed-line-ending
        args: ['--fix=lf']

  # Branch protection hooks
  - repo: local
    hooks:
      - id: check-branch-before-commit
        name: Check branch before commit
        entry: bash scripts/check-branch-before-commit.sh
        language: system
        pass_filenames: false
        always_run: true
        stages: [pre-commit]

      - id: check-merge-to-protected
        name: Check merge to protected branch
        entry: bash scripts/check-merge-to-protected.sh
        language: system
        pass_filenames: false
        always_run: true
        stages: [pre-commit]

# Configuration
default_language_version:
  python: python3.11

default_install_hook_types: [pre-commit, pre-push]
default_stages: [pre-commit, pre-push]
fail_fast: true
minimum_pre_commit_version: '3.0.0'
```

### apps/core/pyproject.toml (Mypy Configuration)

```toml
[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
explicit_package_bases = true
mypy_path = "$MYPY_CONFIG_FILE_DIR/src"  # Relative to config file
namespace_packages = true
warn_unused_ignores = false

[[tool.mypy.overrides]]
module = ["tests.*", "examples.*"]
ignore_errors = true

[[tool.mypy.overrides]]
module = ["qwen_tts.*", "librosa.*", "numpy.*", "soundfile.*", "torch.*"]
ignore_missing_imports = true
```

## Key Design Decisions

### 1. Custom Local Hooks for Mypy and Pytest

**Problem**: Pre-commit runs hooks in isolated virtualenvs that don't have access to local packages (domain, app, infra).

**Solution**: Use `language: system` with custom bash scripts that:
- Change to the correct directory (`apps/core/`)
- Activate the project's virtualenv (checks for `venv` or `.venv`)
- Run the tool with the project's Python interpreter

**Why this works**:
- Mypy can resolve local imports (domain, app, infra)
- Pytest can import test dependencies (soundfile, librosa, etc.)
- Works consistently across different developer setups

### 2. Mypy Path Configuration

**Problem**: Mypy couldn't find local modules when run from repository root.

**Solution**: Use `$MYPY_CONFIG_FILE_DIR/src` in `mypy_path`:
- `$MYPY_CONFIG_FILE_DIR` expands to the directory containing `pyproject.toml`
- Makes paths relative to the config file, not the working directory
- Works both locally and in CI

### 3. Virtualenv Detection

**Problem**: Different developers use different virtualenv names (`venv`, `.venv`, etc.).

**Solution**: Check for common virtualenv locations:
```bash
if [ -d "venv" ]; then
  source venv/bin/activate
elif [ -d ".venv" ]; then
  source .venv/bin/activate
fi
```

**Fallback**: If no virtualenv is found, uses system Python (works in CI where dependencies are installed globally).

### 4. Ruff Configuration

**Why `--exit-non-zero-on-fix`**:
- Ensures that if Ruff fixes issues, the hook fails
- Forces developer to review and commit the fixes
- Prevents auto-fixed code from being committed without review
- Consistent with strict pre-commit philosophy

**Alternative approach** (auto-fix without failing):
```yaml
- id: ruff
  args: ['--fix']  # Auto-fix without failing
```
Use this if you prefer seamless auto-correction.

## Common Issues and Solutions

### Issue 1: Mypy "import-not-found" Errors

**Symptom**:
```
error: Cannot find implementation or library stub for module named "domain"
error: Cannot find implementation or library stub for module named "app"
```

**Cause**: Mypy running in isolated environment without access to local packages.

**Solution**: Use custom local hook with `language: system` (see configuration above).

### Issue 2: Pytest "ModuleNotFoundError"

**Symptom**:
```
ModuleNotFoundError: No module named 'soundfile'
```

**Cause**: Pytest running with system Python that doesn't have project dependencies.

**Solution**: Activate virtualenv before running pytest (see configuration above).

### Issue 3: Hooks Pass Locally but Fail in CI

**Symptom**: All hooks pass locally, but CI fails with lint/type-check errors.

**Cause**: Inconsistent configuration between local hooks and CI workflows.

**Solution**: Ensure CI workflows match local hook configuration:

```yaml
# .github/workflows/ci-python.yml
- name: Lint and format with Ruff
  run: |
    cd apps/core
    ruff check src/ tests/ --exit-non-zero-on-fix
    ruff format --check src/ tests/

- name: Type check with MyPy
  run: |
    cd apps/core
    mypy src --config-file=pyproject.toml
```

### Issue 4: Hooks Too Slow

**Symptom**: Pre-commit hooks take >10 seconds to run.

**Cause**: Running too many checks or checking too many files.

**Solution**:
- Move slow checks (pytest) to pre-push hooks
- Use `files:` patterns to limit scope
- Use `pass_filenames: false` for tools that check entire codebase

## Testing Hooks

### Test All Pre-commit Hooks
```bash
python3 -m pre_commit run --all-files
```

### Test Pre-push Hooks
```bash
python3 -m pre_commit run --hook-stage pre-push --all-files
```

### Test Specific Hook
```bash
python3 -m pre_commit run mypy --all-files
python3 -m pre_commit run pytest-check --all-files
```

### Reinstall Hooks
```bash
python3 -m pre_commit uninstall
python3 -m pre_commit install --install-hooks
```

## CI/CD Integration

### GitHub Actions Workflow

Ensure CI workflows match local configuration:

```yaml
lint:
  steps:
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        cd apps/core
        pip install -e ".[dev]"

    - name: Lint and format with Ruff
      run: |
        cd apps/core
        ruff check src/ tests/ --exit-non-zero-on-fix
        ruff format --check src/ tests/

type-check:
  steps:
    - name: Type check with MyPy
      run: |
        cd apps/core
        mypy src --config-file=pyproject.toml

test:
  steps:
    - name: Run tests with pytest
      run: |
        cd apps/core
        pytest tests/ --cov=src --cov-report=xml
```

## Best Practices

### Do's ✅
- Use `language: system` for hooks that need project dependencies
- Activate virtualenv in custom hooks
- Use `$MYPY_CONFIG_FILE_DIR` for relative paths in mypy config
- Test hooks locally before pushing
- Keep pre-commit hooks fast (<5 seconds)
- Move slow checks to pre-push hooks
- Ensure CI matches local configuration

### Don'ts ❌
- Don't use `language: python` for hooks that need local packages
- Don't hardcode virtualenv paths (check for common names)
- Don't use absolute paths in configuration
- Don't skip testing hooks before committing
- Don't run full test suite in pre-commit (use pre-push instead)
- Don't have inconsistent configuration between local and CI

## Troubleshooting

### Hooks Not Running
```bash
# Check if hooks are installed
ls -la .git/hooks/

# Reinstall hooks
python3 -m pre_commit install --install-hooks
```

### Mypy Still Can't Find Modules
```bash
# Test mypy directly
cd apps/core
source venv/bin/activate
python -m mypy src --config-file=pyproject.toml

# Check mypy_path
python -c "import tomli; print(tomli.load(open('apps/core/pyproject.toml', 'rb'))['tool']['mypy']['mypy_path'])"
```

### Pytest Fails with Import Errors
```bash
# Test pytest directly
cd apps/core
source venv/bin/activate
python -m pytest tests/domain tests/app -v

# Check if dependencies are installed
pip list | grep soundfile
```

## References

- [Pre-commit Documentation](https://pre-commit.com/)
- [Mypy Configuration](https://mypy.readthedocs.io/en/stable/config_file.html)
- [Running Mypy in Pre-commit](https://jaredkhan.com/blog/mypy-pre-commit)
- [Ruff Documentation](https://docs.astral.sh/ruff/)

## Summary

**Key Takeaways**:
- ✅ Use custom local hooks for tools that need project dependencies
- ✅ Activate virtualenv in custom hooks for consistent environment
- ✅ Use `$MYPY_CONFIG_FILE_DIR` for relative paths in mypy config
- ✅ Keep pre-commit fast, move slow checks to pre-push
- ✅ Ensure CI configuration matches local hooks
- 🎯 Goal: Strict, consistent checks that catch errors before they reach CI

---

**Last Updated**: January 30, 2026
