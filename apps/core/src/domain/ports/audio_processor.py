"""Audio Processor Port.

Interface for audio processing operations.
Infrastructure adapters (e.g., LibrosaAudioProcessor) must implement this interface.
"""

from abc import ABC, abstractmethod
from pathlib import Path

from apps.core.src.domain.models.audio_sample import AudioSample


class AudioProcessor(ABC):
    """Abstract interface for audio processing.

    This port defines the contract that all audio processor adapters must implement.
    Examples: LibrosaAudioProcessor, PyDubAudioProcessor, etc.
    """

    @abstractmethod
    def validate_sample(self, sample_path: Path) -> bool:
        """Validate an audio sample meets requirements.

        Args:
            sample_path: Path to the audio file to validate

        Returns:
            True if sample is valid

        Raises:
            InvalidSampleException: If sample is invalid
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def normalize_audio(
        self, input_path: Path, output_path: Path, target_lufs: float = -16.0
    ) -> Path:
        """Normalize audio loudness.

        Args:
            input_path: Path to input audio file
            output_path: Path to save normalized audio
            target_lufs: Target loudness in LUFS (default: -16.0)

        Returns:
            Path to normalized audio file
        """
        pass
