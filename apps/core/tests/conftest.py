"""Pytest configuration for core library tests.

Ensures src/ directory is prioritized in sys.path before tests/ directory
to avoid naming conflicts between test directories (tests/app/, tests/infra/)
and source directories (src/app/, src/infra/).
"""

import sys
from pathlib import Path

import numpy as np
import pytest
import soundfile as sf

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


@pytest.fixture
def sample_audio_file(tmp_path):
    """Create a sample audio file for testing.

    Creates a valid WAV file with the correct format for TTS Studio:
    - Sample rate: 12000 Hz
    - Channels: Mono (1)
    - Duration: 10 seconds
    - Format: 16-bit PCM
    """
    # Generate 10 seconds of audio at 12000 Hz
    sample_rate = 12000
    duration = 10.0
    num_samples = int(sample_rate * duration)

    # Generate a simple sine wave (440 Hz - A4 note)
    frequency = 440.0
    t = np.linspace(0, duration, num_samples, False)
    audio_data = np.sin(2 * np.pi * frequency * t) * 0.3  # 30% amplitude

    # Save as WAV file
    audio_file = tmp_path / "sample.wav"
    sf.write(audio_file, audio_data, sample_rate, subtype="PCM_16")

    return audio_file
