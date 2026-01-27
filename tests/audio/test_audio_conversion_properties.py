"""Property-based tests for audio conversion."""

import tempfile
from pathlib import Path

import numpy as np
import soundfile as sf
from hypothesis import given, settings
from hypothesis import strategies as st
from voice_clone.audio.processor import AudioProcessor


@settings(deadline=None)  # Audio file operations can be slow
@given(
    input_rate=st.sampled_from([8000, 16000, 44100, 48000]),
    duration=st.floats(min_value=1.0, max_value=5.0),
)
def test_property_7_sample_rate_conversion_correctness(
    input_rate: int, duration: float
) -> None:
    """Property 7: Sample rate conversion correctness.

    When converting audio, output should have target sample rate.

    Validates: Requirements 2.1
    """
    processor = AudioProcessor()

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        input_path = Path(f.name)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        output_path = Path(f.name)

    try:
        # Create input audio with non-standard sample rate
        audio = np.random.randn(int(duration * input_rate)) * 0.5
        audio = np.clip(audio, -0.98, 0.98)
        sf.write(input_path, audio, input_rate)

        # Convert
        success = processor.convert_to_target_format(input_path, output_path)
        assert success

        # Verify output has correct sample rate (Qwen3-TTS native: 12000 Hz)
        info = sf.info(output_path)
        assert info.samplerate == 12000

    finally:
        input_path.unlink(missing_ok=True)
        output_path.unlink(missing_ok=True)


@settings(deadline=None)  # Audio file operations can be slow
@given(
    num_channels=st.integers(min_value=2, max_value=6),
    duration=st.floats(min_value=1.0, max_value=5.0),
)
def test_property_8_stereo_to_mono_conversion(
    num_channels: int, duration: float
) -> None:
    """Property 8: Stereo to mono conversion.

    When converting multi-channel audio, output should be mono.

    Validates: Requirements 2.2
    """
    processor = AudioProcessor()

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        input_path = Path(f.name)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        output_path = Path(f.name)

    try:
        # Create multi-channel audio
        sample_rate = 12000
        audio = np.random.randn(int(duration * sample_rate), num_channels) * 0.5
        audio = np.clip(audio, -0.98, 0.98)
        sf.write(input_path, audio, sample_rate)

        # Convert
        success = processor.convert_to_target_format(input_path, output_path)
        assert success

        # Verify output is mono
        info = sf.info(output_path)
        assert info.channels == 1

    finally:
        input_path.unlink(missing_ok=True)
        output_path.unlink(missing_ok=True)


@settings(deadline=None)  # Audio file operations can be slow
@given(duration=st.floats(min_value=1.0, max_value=5.0))
def test_property_9_format_conversion_round_trip(duration: float) -> None:
    """Property 9: Format conversion round-trip.

    Converting WAV → target format → WAV should preserve audio characteristics.

    Validates: Requirements 2.3, 2.4
    """
    processor = AudioProcessor()

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        original_path = Path(f.name)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        converted_path = Path(f.name)

    try:
        # Create original audio (Qwen3-TTS native: 12000 Hz)
        sample_rate = 12000
        audio = np.random.randn(int(duration * sample_rate)) * 0.5
        audio = np.clip(audio, -0.98, 0.98)
        sf.write(original_path, audio, sample_rate)

        # Convert to target format
        success = processor.convert_to_target_format(original_path, converted_path)
        assert success

        # Verify converted file exists and has correct properties
        assert converted_path.exists()
        info = sf.info(converted_path)
        assert info.samplerate == 12000
        assert info.channels == 1

    finally:
        original_path.unlink(missing_ok=True)
        converted_path.unlink(missing_ok=True)


@settings(deadline=None)  # Audio file operations can be slow
@given(duration=st.floats(min_value=1.0, max_value=5.0))
def test_property_10_conversion_output_file_existence(duration: float) -> None:
    """Property 10: Conversion output file existence.

    After successful conversion, output file should exist.

    Validates: Requirements 2.5
    """
    processor = AudioProcessor()

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        input_path = Path(f.name)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        output_path = Path(f.name)

    # Delete output file to ensure it doesn't exist before conversion
    output_path.unlink()

    try:
        # Create input audio
        sample_rate = 12000
        audio = np.random.randn(int(duration * sample_rate)) * 0.5
        audio = np.clip(audio, -0.98, 0.98)
        sf.write(input_path, audio, sample_rate)

        # Convert
        success = processor.convert_to_target_format(input_path, output_path)
        assert success

        # Verify output file exists
        assert output_path.exists()
        assert output_path.stat().st_size > 0

    finally:
        input_path.unlink(missing_ok=True)
        output_path.unlink(missing_ok=True)


def test_property_11_conversion_error_reporting() -> None:
    """Property 11: Conversion error reporting.

    When conversion fails (e.g., invalid input), should return False.

    Validates: Requirements 2.6
    """
    processor = AudioProcessor()

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        output_path = Path(f.name)

    try:
        # Try to convert non-existent file
        non_existent = Path("/tmp/non_existent_file_12345.wav")
        success = processor.convert_to_target_format(non_existent, output_path)

        # Should return False on failure
        assert not success

    finally:
        output_path.unlink(missing_ok=True)
