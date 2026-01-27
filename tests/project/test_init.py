"""Tests for package initialization."""

import voice_clone


def test_version() -> None:
    """Test that version is defined."""
    assert hasattr(voice_clone, "__version__")
    assert voice_clone.__version__ == "0.2.0"


def test_author() -> None:
    """Test that author is defined."""
    assert hasattr(voice_clone, "__author__")
    assert isinstance(voice_clone.__author__, str)


def test_license() -> None:
    """Test that license is defined."""
    assert hasattr(voice_clone, "__license__")
    assert voice_clone.__license__ == "MIT"
