# Project Structure Explanation

## Directory Layout

```
voice-clone/
├── src/
│   ├── voice_clone/              # ← Main Python package
│   │   ├── __init__.py
│   │   ├── cli.py
│   │   ├── audio/
│   │   ├── model/
│   │   └── utils/
│   └── voice_clone_cli.egg-info/ # ← Auto-generated metadata (gitignored)
├── tests/
├── data/
├── config/
└── pyproject.toml
```

## Why `src/voice_clone/` instead of `src/`?

This project uses the **"src layout"** pattern, which is a Python packaging best practice.

### The Problem with Flat Layout

**Flat layout** (NOT recommended):
```
project/
├── voice_clone/
│   ├── __init__.py
│   └── cli.py
├── tests/
└── setup.py
```

**Issues**:
1. ❌ Can import code without installing it
2. ❌ Tests might pass locally but fail after installation
3. ❌ Confusing namespace (is it installed or local?)
4. ❌ Hard to distinguish package code from project files

### The Solution: src Layout

**src layout** (RECOMMENDED):
```
project/
├── src/
│   └── voice_clone/
│       ├── __init__.py
│       └── cli.py
├── tests/
└── pyproject.toml
```

**Benefits**:
1. ✅ **Forces proper installation**: Can't import without `pip install -e .`
2. ✅ **Tests are realistic**: Tests run against installed package
3. ✅ **Clear separation**: Package code is isolated in `src/`
4. ✅ **Correct namespace**: Import as `voice_clone`, not `src.voice_clone`
5. ✅ **Industry standard**: Used by major Python projects

### How It Works

#### Installation
```bash
# Install in development mode
pip install -e .

# This creates:
# - src/voice_clone_cli.egg-info/ (metadata)
# - Links package to site-packages
```

#### Importing
```python
# After installation, you can import:
from voice_clone.cli import cli
from voice_clone.audio.processor import AudioProcessor

# NOT:
from src.voice_clone.cli import cli  # ❌ Wrong!
```

#### Package Configuration

In `pyproject.toml`:
```toml
[project]
name = "voice-clone-cli"  # Package name on PyPI

[project.scripts]
voice-clone = "voice_clone.cli:cli"  # CLI entry point
```

The package name (`voice-clone-cli`) is different from the import name (`voice_clone`):
- **Package name**: Used for `pip install voice-clone-cli`
- **Import name**: Used for `import voice_clone`

## What is `voice_clone_cli.egg-info/`?

This directory contains **package metadata** generated during installation.

### Contents

```
voice_clone_cli.egg-info/
├── PKG-INFO              # Package information (name, version, author)
├── SOURCES.txt           # List of all package files
├── dependency_links.txt  # External dependency links
├── entry_points.txt      # CLI commands (voice-clone)
└── top_level.txt         # Top-level modules (voice_clone)
```

### When It's Created

Generated automatically when you run:
```bash
pip install -e .          # Development mode
pip install .             # Regular install
python -m build           # Build package
```

### Should It Be Committed?

**NO!** ❌

This directory should be in `.gitignore` because:
1. It's auto-generated (like `__pycache__`)
2. It's specific to your local installation
3. It changes every time you install
4. Other developers will generate their own

Our `.gitignore` already covers it:
```gitignore
*.egg-info/
```

## Package vs Module Names

### Package Name (for pip)
```bash
pip install voice-clone-cli
```
- Defined in `pyproject.toml` as `name = "voice-clone-cli"`
- Used for distribution (PyPI, pip)
- Can contain hyphens

### Module Name (for import)
```python
import voice_clone
```
- Defined by directory name: `src/voice_clone/`
- Used in Python code
- Must be valid Python identifier (no hyphens)

### CLI Command Name
```bash
voice-clone --help
```
- Defined in `pyproject.toml` as `voice-clone = "voice_clone.cli:cli"`
- Can contain hyphens
- Maps to Python function

## Directory Structure Best Practices

### ✅ Good Structure (Current)
```
voice-clone/
├── src/
│   └── voice_clone/          # Package code
│       ├── __init__.py
│       ├── cli.py
│       ├── audio/
│       │   ├── __init__.py
│       │   ├── processor.py
│       │   └── validator.py
│       ├── model/
│       │   ├── __init__.py
│       │   ├── manager.py
│       │   └── generator.py
│       └── utils/
│           ├── __init__.py
│           ├── logger.py
│           └── helpers.py
├── tests/                    # Test code
│   ├── test_audio.py
│   ├── test_model.py
│   └── test_cli.py
├── data/                     # Data files (gitignored)
├── config/                   # Configuration
├── scripts/                  # Utility scripts
├── docs/                     # Documentation
└── pyproject.toml           # Package configuration
```

### ❌ Bad Structure (Avoid)
```
voice-clone/
├── voice_clone/              # Package at root (flat layout)
│   ├── __init__.py
│   └── cli.py
├── test_audio.py            # Tests mixed with code
├── data/                    # Data at root
└── setup.py
```

## Common Questions

### Q: Why not just `src/cli.py`?

**A**: Because you need a package (directory with `__init__.py`) to:
- Organize code into modules
- Create proper namespace
- Support subpackages (audio/, model/, utils/)
- Enable relative imports

### Q: Can I have multiple packages in `src/`?

**A**: Yes! For example:
```
src/
├── voice_clone/          # Main package
│   └── ...
└── voice_clone_tools/    # Additional package
    └── ...
```

### Q: What if I want to rename the package?

**A**: You need to:
1. Rename `src/voice_clone/` to `src/new_name/`
2. Update `pyproject.toml`:
   ```toml
   [project.scripts]
   voice-clone = "new_name.cli:cli"
   ```
3. Update all imports in code
4. Reinstall: `pip install -e .`

### Q: How do I verify the structure is correct?

**A**: After `pip install -e .`:
```bash
# Should work:
python -c "import voice_clone; print(voice_clone.__file__)"
# Output: /path/to/src/voice_clone/__init__.py

# Should work:
voice-clone --help

# Should NOT work (if it does, structure is wrong):
python -c "import src.voice_clone"  # Should fail
```

## References

- [Python Packaging User Guide - src layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/)
- [Setuptools - Package Discovery](https://setuptools.pypa.io/en/latest/userguide/package_discovery.html)
- [PEP 517 - Build System](https://peps.python.org/pep-0517/)
- [PEP 518 - pyproject.toml](https://peps.python.org/pep-0518/)

## Summary

| Aspect | Value | Purpose |
|--------|-------|---------|
| **Package directory** | `src/voice_clone/` | Contains Python code |
| **Package name** | `voice-clone-cli` | For pip install |
| **Import name** | `voice_clone` | For Python imports |
| **CLI command** | `voice-clone` | For terminal |
| **Metadata dir** | `voice_clone_cli.egg-info/` | Auto-generated, gitignored |
| **Layout pattern** | src layout | Best practice |

The structure is correct and follows Python packaging best practices! 🎉
