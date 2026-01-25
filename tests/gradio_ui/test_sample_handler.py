"""
Tests for sample validation handler.
"""

from pathlib import Path

import pytest
from gradio_ui.handlers.sample_handler import validate_samples_handler


def test_validate_samples_empty():
    """Test validation with no files."""
    result = validate_samples_handler([])

    assert "No files uploaded" in result
    assert "⚠️" in result
    assert "Please upload 1-3 audio samples" in result


def test_validate_samples_file_not_found():
    """Test validation with non-existent file."""
    result = validate_samples_handler(["/nonexistent/file.wav"])

    assert "❌" in result
    assert "File not found" in result or "file.wav" in result


def test_validate_samples_invalid_format():
    """Test validation with invalid file format."""
    # Create a temporary text file (not audio)
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write("This is not an audio file")
        temp_path = f.name

    try:
        result = validate_samples_handler([temp_path])

        # Should show error
        assert "❌" in result
        assert "Error processing file" in result or "Failed to validate" in result
    finally:
        # Cleanup
        Path(temp_path).unlink(missing_ok=True)


def test_validate_samples_markdown_format():
    """Test that output is properly formatted Markdown."""
    result = validate_samples_handler([])

    # Should contain Markdown elements
    assert "**" in result  # Bold text
    assert "\n" in result  # Line breaks

    # Should be user-friendly
    assert "⚠️" in result or "✅" in result or "❌" in result


def test_validate_samples_summary():
    """Test that summary is included in results."""
    result = validate_samples_handler([])

    # Empty list should still have helpful message
    assert "upload" in result.lower() or "samples" in result.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
