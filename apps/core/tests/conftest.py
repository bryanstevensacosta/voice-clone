"""Pytest configuration for core library tests."""

import sys
from pathlib import Path

# Add src directory to Python path so tests can import from domain, infra, etc.
src_dir = Path(__file__).parent.parent / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

print(f"[conftest.py] Added {src_dir} to sys.path")
print(f"[conftest.py] sys.path: {sys.path[:3]}")
