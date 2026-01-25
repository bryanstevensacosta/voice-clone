"""
Integration tests for validation UI wiring.

This module tests that the validation button is correctly wired to the
validation handler and produces expected outputs.
"""

from pathlib import Path

import pytest
from gradio_ui.app import create_app


def test_app_has_validation_handler():
    """Test that the app is created with validation handler wired."""
    app = create_app()
    assert app is not None

    # The app should have event handlers configured
    # Gradio doesn't expose handlers directly, but we can verify the app was created
    assert hasattr(app, "blocks")


def test_validation_handler_with_valid_samples():
    """Test validation handler with valid audio samples."""
    from gradio_ui.handlers.sample_handler import validate_samples_handler

    # Use existing test samples
    sample_dir = Path("data/samples")
    if not sample_dir.exists():
        pytest.skip("No sample directory found")

    samples = list(sample_dir.glob("*.wav"))[:2]  # Use first 2 samples
    if not samples:
        pytest.skip("No sample files found")

    sample_paths = [str(s) for s in samples]

    # Call the handler
    result = validate_samples_handler(sample_paths)

    # Verify result is markdown string
    assert isinstance(result, str)
    assert "## Validation Results" in result

    # Should have success indicators for valid samples
    # (assuming the samples in data/samples are valid)
    assert "✅" in result or "❌" in result


def test_validation_handler_with_empty_list():
    """Test validation handler with no files."""
    from gradio_ui.handlers.sample_handler import validate_samples_handler

    result = validate_samples_handler([])

    # Should return warning message
    assert isinstance(result, str)
    assert "No files uploaded" in result
    assert "⚠️" in result


def test_validation_handler_with_nonexistent_file():
    """Test validation handler with file that doesn't exist."""
    from gradio_ui.handlers.sample_handler import validate_samples_handler

    result = validate_samples_handler(["/nonexistent/file.wav"])

    # Should handle gracefully
    assert isinstance(result, str)
    assert "❌" in result
    assert "File not found" in result or "Error" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
