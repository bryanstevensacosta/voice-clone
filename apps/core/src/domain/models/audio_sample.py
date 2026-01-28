"""Audio Sample Value Object.

Immutable value object representing an audio sample for voice cloning.
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AudioSample:
    """Immutable audio sample value object.

    Represents a single audio sample with its metadata.
    This is a value object - it has no identity and is immutable.
    """

    path: Path
    duration: float  # in seconds
    sample_rate: int  # in Hz
    channels: int
    bit_depth: int
    emotion: str | None = None

    def __post_init__(self) -> None:
        """Validate audio sample after initialization."""
        """Validate audio sample on creation."""
        if not self.is_valid_duration():
            raise ValueError(
                f"Invalid duration: {self.duration}s. "
                f"Must be between 3 and 30 seconds."
            )

        if not self.is_valid_sample_rate():
            raise ValueError(
                f"Invalid sample rate: {self.sample_rate} Hz. "
                f"Must be 12000 Hz (Qwen3-TTS native)."
            )

        if self.channels != 1:
            raise ValueError(
                f"Invalid channels: {self.channels}. " f"Must be mono (1 channel)."
            )

        if self.bit_depth != 16:
            raise ValueError(
                f"Invalid bit depth: {self.bit_depth}. " f"Must be 16-bit."
            )

    def is_valid_duration(self) -> bool:
        """Check if duration is within acceptable range.

        Returns:
            True if duration is between 3 and 30 seconds
        """
        return 3.0 <= self.duration <= 30.0

    def is_valid_sample_rate(self) -> bool:
        """Check if sample rate matches Qwen3-TTS native format.

        Returns:
            True if sample rate is 12000 Hz
        """
        return self.sample_rate == 12000

    def __str__(self) -> str:
        """String representation of audio sample."""
        emotion_str = f" ({self.emotion})" if self.emotion else ""
        return (
            f"AudioSample({self.path.name}{emotion_str}, "
            f"{self.duration:.1f}s, {self.sample_rate}Hz)"
        )
