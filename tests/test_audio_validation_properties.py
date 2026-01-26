"""Property-based tests for audio validation."""

import tempfile
from pathlib import Path

import numpy as np
import soundfile as sf
from hypothesis import given, settings
from hypothesis import strategies as st

from voice_clone.audio.processor import AudioProcessor


@settings(deadline=None)  # Audio file generation can be slow
@given(
    sample_rate=st.integers(min_value=8000, max_value=48000).filter(
        lambda x: x != 22050
    )
)
def test_property_1_sample_rate_validation_detection(sample_rate: int) -> None:
    """Property 1: Sample rate validation detection.

    When audio has non-22050 Hz sample rate, validation should warn.

    Validates: Requirements 1.2
    """
    processor = AudioProcessor()

    # Create temporary audio file with non-standard sample rate
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        temp_path = Path(f.name)

    try:
        # Generate 10 seconds of audio
        duration = 10.0
        audio = np.random.randn(int(duration * sample_rate))
        sf.write(temp_path, audio, sample_rate)

        # Validate
        result = processor.validate_sample(temp_path)

        # Should have warning about sample rate
        assert any("Sample rate" in w for w in result.warnings)
        assert result.metadata["sample_rate"] == sample_rate

    finally:
        temp_path.unlink(missing_ok=True)


@settings(deadline=None)  # Audio file generation can be slow
@given(num_channels=st.integers(min_value=2, max_value=8))
def test_property_2_channel_validation_detection(num_channels: int) -> None:
    """Property 2: Channel validation detection.

    When audio has multiple channels, validation should error.

    Validates: Requirements 1.3
    """
    processor = AudioProcessor()

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        temp_path = Path(f.name)

    try:
        # Generate 10 seconds of multi-channel audio
        duration = 10.0
        sample_rate = 22050
        audio = np.random.randn(int(duration * sample_rate), num_channels)
        sf.write(temp_path, audio, sample_rate)

        # Validate
        result = processor.validate_sample(temp_path)

        # Should have error about channels
        assert any("channels" in e.lower() for e in result.errors)
        assert not result.is_valid()

    finally:
        temp_path.unlink(missing_ok=True)


@settings(deadline=None)  # Audio file generation can be slow
@given(duration=st.floats(min_value=0.5, max_value=5.9))
def test_property_3_duration_validation_short_files(duration: float) -> None:
    """Property 3: Duration validation for short files.

    When audio is shorter than 6 seconds, validation should error.

    Validates: Requirements 1.5
    """
    processor = AudioProcessor()

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        temp_path = Path(f.name)

    try:
        sample_rate = 22050
        audio = np.random.randn(int(duration * sample_rate))
        sf.write(temp_path, audio, sample_rate)

        # Validate
        result = processor.validate_sample(temp_path)

        # Should have error about duration
        assert any("Duration" in e for e in result.errors)
        assert not result.is_valid()

    finally:
        temp_path.unlink(missing_ok=True)


@settings(deadline=None)  # Audio file generation can be slow
@given(duration=st.floats(min_value=30.1, max_value=60.0))
def test_property_4_duration_validation_long_files(duration: float) -> None:
    """Property 4: Duration validation for long files.

    When audio is longer than 30 seconds, validation should warn.

    Validates: Requirements 1.6
    """
    processor = AudioProcessor()

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        temp_path = Path(f.name)

    try:
        sample_rate = 22050
        # Use smaller amplitude and clip to avoid clipping
        audio = np.random.randn(int(duration * sample_rate)) * 0.5
        audio = np.clip(audio, -0.98, 0.98)
        sf.write(temp_path, audio, sample_rate)

        # Validate
        result = processor.validate_sample(temp_path)

        # Should have warning about duration
        assert any("Duration" in w for w in result.warnings)
        # But should still be valid (warnings don't fail validation)
        assert result.is_valid()

    finally:
        temp_path.unlink(missing_ok=True)


def test_property_5_clipping_detection() -> None:
    """Property 5: Clipping detection.

    When audio has clipping (amplitude >= 0.99), validation should error.

    Validates: Requirements 1.7
    """
    processor = AudioProcessor()

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        temp_path = Path(f.name)

    try:
        # Generate audio with clipping
        sample_rate = 22050
        duration = 10.0
        audio = np.random.randn(int(duration * sample_rate))
        # Add clipping
        audio[1000] = 1.0  # Maximum amplitude
        sf.write(temp_path, audio, sample_rate)

        # Validate
        result = processor.validate_sample(temp_path)

        # Should have error about clipping
        assert any("clipping" in e.lower() for e in result.errors)
        assert not result.is_valid()

    finally:
        temp_path.unlink(missing_ok=True)


@settings(deadline=None)  # Audio file generation can be slow
@given(
    duration=st.floats(min_value=6.0, max_value=30.0),
    amplitude=st.floats(min_value=0.1, max_value=0.9),
)
def test_property_6_successful_validation_reporting(
    duration: float, amplitude: float
) -> None:
    """Property 6: Successful validation reporting.

    When audio meets all requirements, validation should succeed.

    Validates: Requirements 1.8
    """
    processor = AudioProcessor()

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        temp_path = Path(f.name)

    try:
        sample_rate = 22050
        # Clip amplitude to ensure no clipping
        audio = np.random.randn(int(duration * sample_rate)) * amplitude
        # Ensure max amplitude is below 0.99
        audio = np.clip(audio, -0.98, 0.98)
        sf.write(temp_path, audio, sample_rate)

        # Validate
        result = processor.validate_sample(temp_path)

        # Should be valid
        assert result.is_valid()
        assert len(result.errors) == 0
        # May have warnings (e.g., bit depth), but no errors
        assert result.metadata["sample_rate"] == sample_rate
        assert result.metadata["channels"] == 1

    finally:
        temp_path.unlink(missing_ok=True)
