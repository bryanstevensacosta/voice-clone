"""Pytest configuration for core library tests.

Ensures src/ directory is prioritized in sys.path before tests/ directory
to avoid naming conflicts between test directories (tests/app/, tests/infra/)
and source directories (src/app/, src/infra/).
"""

import sys
from pathlib import Path

# Get the src directory
src_dir = Path(__file__).parent.parent / "src"

# Remove tests directory from sys.path if it's there
tests_dir = Path(__file__).parent
if str(tests_dir) in sys.path:
    sys.path.remove(str(tests_dir))

# Add src directory at the beginning of sys.path
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))
else:
    # If src is already in sys.path, move it to the front
    sys.path.remove(str(src_dir))
    sys.path.insert(0, str(src_dir))
