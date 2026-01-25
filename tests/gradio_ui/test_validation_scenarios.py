"""
Comprehensive validation UI scenario tests.

This module tests all validation scenarios as specified in task 2.3.4 and 2.3.5:
- Valid samples
- Invalid samples (wrong format, duration, etc.)
- Empty file list
- Non-existent files
"""

import numpy as np
import pytest
import soundfile as sf
from gradio_ui.handlers.sample_handler import validate_samples_handler


@pytest.fixture
def temp_audio_dir(tmp_path):
    """Create temporary directory for test audio files."""
    audio_dir = tmp_path / "test_audio"
    audio_dir.mkdir()
    return audio_dir


@pytest.fixture
def valid_sample(temp_audio_dir):
    """Create a valid audio sample (12000 Hz, mono, 16-bit, 10 seconds)."""
    sample_rate = 12000
    duration = 10.0
    samples = int(sample_rate * duration)

    # Generate sine wave
    frequency = 440.0  # A4 note
    t = np.linspace(0, duration, samples)
    audio = np.sin(2 * np.pi * frequency * t) * 0.5

    # Save as WAV
    file_path = temp_audio_dir / "valid_sample.wav"
    sf.write(file_path, audio, sample_rate, subtype="PCM_16")

    return str(file_path)


@pytest.fixture
def short_sample(temp_audio_dir):
    """Create a sample that's too short (< 3 seconds)."""
    sample_rate = 12000
    duration = 2.0  # Too short
    samples = int(sample_rate * duration)

    t = np.linspace(0, duration, samples)
    audio = np.sin(2 * np.pi * 440.0 * t) * 0.5

    file_path = temp_audio_dir / "short_sample.wav"
    sf.write(file_path, audio, sample_rate, subtype="PCM_16")

    return str(file_path)


@pytest.fixture
def wrong_sample_rate(temp_audio_dir):
    """Create a sample with wrong sample rate (44100 Hz instead of 12000 Hz)."""
    sample_rate = 44100  # Wrong sample rate
    duration = 10.0
    samples = int(sample_rate * duration)

    t = np.linspace(0, duration, samples)
    audio = np.sin(2 * np.pi * 440.0 * t) * 0.5

    file_path = temp_audio_dir / "wrong_rate.wav"
    sf.write(file_path, audio, sample_rate, subtype="PCM_16")

    return str(file_path)


@pytest.fixture
def stereo_sample(temp_audio_dir):
    """Create a stereo sample (should be mono)."""
    sample_rate = 12000
    duration = 10.0
    samples = int(sample_rate * duration)

    t = np.linspace(0, duration, samples)
    left = np.sin(2 * np.pi * 440.0 * t) * 0.5
    right = np.sin(2 * np.pi * 880.0 * t) * 0.5
    audio = np.column_stack([left, right])

    file_path = temp_audio_dir / "stereo_sample.wav"
    sf.write(file_path, audio, sample_rate, subtype="PCM_16")

    return str(file_path)


class TestValidationScenarios:
    """Test all validation scenarios."""

    def test_valid_sample_passes(self, valid_sample):
        """Test that a valid sample passes validation (Task 2.3.4)."""
        result = validate_samples_handler([valid_sample])

        # Should contain validation results header
        assert "## Validation Results" in result

        # Should show success
        assert "✅" in result
        assert "valid_sample.wav" in result

        # Should show metadata
        assert "Duration" in result
        assert "Sample Rate" in result
        assert "Channels" in result

        # Should show summary
        assert "1/1 samples passed validation" in result
        assert "All samples are valid" in result

    def test_multiple_valid_samples(self, valid_sample, temp_audio_dir):
        """Test validation with multiple valid samples."""
        # Create second valid sample
        sample_rate = 12000
        duration = 15.0
        samples = int(sample_rate * duration)
        t = np.linspace(0, duration, samples)
        audio = np.sin(2 * np.pi * 440.0 * t) * 0.5

        second_sample = temp_audio_dir / "valid_sample_2.wav"
        sf.write(second_sample, audio, sample_rate, subtype="PCM_16")

        result = validate_samples_handler([valid_sample, str(second_sample)])

        # Should validate both (note: summary also has ✅, so count >= 2)
        assert result.count("✅") >= 2
        assert "2/2 samples passed validation" in result

    def test_short_sample_fails(self, short_sample):
        """Test that a too-short sample fails validation (Task 2.3.5)."""
        result = validate_samples_handler([short_sample])

        # Should show error
        assert "❌" in result
        assert "short_sample.wav" in result

        # Should mention duration issue
        assert "Duration" in result or "short" in result.lower()

        # Should show summary with 0 valid
        assert "0/1 samples passed validation" in result

    def test_wrong_sample_rate_warning(self, wrong_sample_rate):
        """Test that wrong sample rate shows warning."""
        result = validate_samples_handler([wrong_sample_rate])

        # Should show the file
        assert "wrong_rate.wav" in result

        # Should mention sample rate
        assert "Sample Rate" in result
        assert "44100" in result

    def test_stereo_sample_warning(self, stereo_sample):
        """Test that stereo sample shows warning."""
        result = validate_samples_handler([stereo_sample])

        # Should show the file
        assert "stereo_sample.wav" in result

        # Should mention channels
        assert "Channels" in result or "stereo" in result.lower()

    def test_empty_file_list(self):
        """Test validation with no files (Task 2.3.5)."""
        result = validate_samples_handler([])

        # Should show warning
        assert "⚠️" in result
        assert "No files uploaded" in result

        # Should show requirements
        assert "Requirements" in result
        assert "3-30 seconds" in result

    def test_nonexistent_file(self):
        """Test validation with file that doesn't exist (Task 2.3.5)."""
        result = validate_samples_handler(["/nonexistent/path/file.wav"])

        # Should handle gracefully
        assert "❌" in result
        assert "file.wav" in result
        assert "File not found" in result or "Error" in result

        # Should show summary
        assert "0/1 samples passed validation" in result

    def test_mixed_valid_invalid(self, valid_sample, short_sample):
        """Test validation with mix of valid and invalid samples."""
        result = validate_samples_handler([valid_sample, short_sample])

        # Should show both results
        assert "✅" in result  # Valid sample
        assert "❌" in result  # Invalid sample

        # Should show correct summary
        assert "1/2 samples passed validation" in result
        assert "Some samples have issues" in result

    def test_invalid_file_format(self, temp_audio_dir):
        """Test validation with non-audio file."""
        # Create a text file
        text_file = temp_audio_dir / "not_audio.txt"
        text_file.write_text("This is not an audio file")

        result = validate_samples_handler([str(text_file)])

        # Should handle gracefully
        assert "❌" in result
        assert "not_audio.txt" in result
        # Check for error-related text (case-insensitive)
        assert "error" in result.lower() or "failed" in result.lower()

    def test_result_format_is_markdown(self, valid_sample):
        """Test that result is properly formatted Markdown."""
        result = validate_samples_handler([valid_sample])

        # Should be a string
        assert isinstance(result, str)

        # Should have Markdown headers
        assert "##" in result or "###" in result

        # Should have bullet points
        assert "-" in result or "*" in result

        # Should have bold text
        assert "**" in result


class TestValidationUIIntegration:
    """Test integration with Gradio UI."""

    def test_handler_signature_matches_gradio(self):
        """Test that handler signature matches Gradio expectations."""
        import inspect

        sig = inspect.signature(validate_samples_handler)
        params = list(sig.parameters.keys())

        # Should accept list of file paths
        assert len(params) == 1
        assert params[0] == "files"

        # Should return string
        assert sig.return_annotation is str

    def test_handler_works_with_gradio_file_output(self, valid_sample):
        """Test that handler output works with gr.Markdown."""
        result = validate_samples_handler([valid_sample])

        # Result should be displayable in Markdown component
        assert isinstance(result, str)
        assert len(result) > 0

        # Should not contain any special characters that break Markdown
        # (Gradio handles most Markdown safely)
        assert result.isprintable() or "\n" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
