"""Librosa Audio Processor Adapter.

Implements the AudioProcessor port using librosa and ffmpeg.
"""

from pathlib import Path

import librosa
import soundfile as sf
from domain.exceptions import InvalidSampleException
from domain.models.audio_sample import AudioSample
from domain.ports.audio_processor import AudioProcessor

from .validator import AudioValidator


class LibrosaAudioProcessor(AudioProcessor):
    """Audio processor implementation using librosa.

    This adapter wraps librosa and ffmpeg functionality and exposes it through
    the AudioProcessor interface defined in the domain layer.
    """

    def __init__(
        self,
        sample_rate: int = 12000,
        channels: int = 1,
        bit_depth: int = 16,
    ):
        """Initialize LibrosaAudioProcessor.

        Args:
            sample_rate: Target sample rate in Hz (default: 12000 for Qwen3-TTS)
            channels: Target number of channels (default: 1 for mono)
            bit_depth: Target bit depth (default: 16)
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.bit_depth = bit_depth
        self.validator = AudioValidator(sample_rate, channels, bit_depth)

    def validate_sample(self, sample_path: Path) -> bool:
        """Validate an audio sample meets requirements.

        Args:
            sample_path: Path to the audio file to validate

        Returns:
            True if sample is valid

        Raises:
            InvalidSampleException: If sample is invalid
        """
        result = self.validator.validate(sample_path)

        if not result.is_valid():
            error_msg = "\n".join(result.errors)
            raise InvalidSampleException(
                f"Audio sample validation failed for {sample_path.name}:\n{error_msg}"
            )

        return True

    def process_sample(self, sample_path: Path) -> AudioSample:
        """Process an audio file and create an AudioSample.

        This method loads the audio file, extracts metadata,
        and creates an AudioSample value object.

        Args:
            sample_path: Path to the audio file

        Returns:
            AudioSample value object with metadata

        Raises:
            InvalidSampleException: If sample cannot be processed
        """
        # First validate the sample
        self.validate_sample(sample_path)

        try:
            # Load audio to get metadata
            audio, sr = librosa.load(sample_path, sr=None, mono=False)
            duration = librosa.get_duration(y=audio, sr=sr)

            # Get file info
            info = sf.info(sample_path)

            # Extract bit depth from subtype (e.g., "PCM_16" -> 16)
            bit_depth = self.bit_depth  # Default
            if hasattr(info, "subtype") and info.subtype:
                # Try to extract bit depth from subtype string
                import re

                match = re.search(r"(\d+)", info.subtype)
                if match:
                    bit_depth = int(match.group(1))

            # Create AudioSample
            return AudioSample(
                path=sample_path,
                duration=duration,
                sample_rate=sr,
                channels=info.channels,
                bit_depth=bit_depth,
            )

        except Exception as e:
            raise InvalidSampleException(
                f"Failed to process audio sample {sample_path.name}: {str(e)}"
            ) from e

    def normalize_audio(
        self, input_path: Path, output_path: Path, target_lufs: float = -16.0
    ) -> Path:
        """Normalize audio loudness using EBU R128.

        Args:
            input_path: Path to input audio file
            output_path: Path to save normalized audio
            target_lufs: Target loudness in LUFS (default: -16.0)

        Returns:
            Path to normalized audio file

        Raises:
            InvalidSampleException: If normalization fails
        """
        try:
            import subprocess

            output_path.parent.mkdir(parents=True, exist_ok=True)

            cmd = [
                "ffmpeg",
                "-i",
                str(input_path),
                "-af",
                f"loudnorm=I={target_lufs}:TP=-1.5:LRA=11",
                "-y",
                str(output_path),
            ]

            result = subprocess.run(cmd, capture_output=True, check=False)

            if result.returncode != 0 or not output_path.exists():
                raise InvalidSampleException(
                    f"Failed to normalize audio: {result.stderr.decode()}"
                )

            return output_path

        except Exception as e:
            raise InvalidSampleException(f"Audio normalization failed: {str(e)}") from e
