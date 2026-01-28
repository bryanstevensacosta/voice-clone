"""Audio validation for infrastructure layer.

Validates audio files against Qwen3-TTS requirements.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import librosa
import numpy as np
import soundfile as sf


@dataclass
class ValidationResult:
    """Result of audio validation operation."""

    success: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def is_valid(self) -> bool:
        """Check if validation passed (no errors).

        Warnings are acceptable, only errors make validation fail.

        Returns:
            True if no errors, False otherwise
        """
        return len(self.errors) == 0

    def format_message(self) -> str:
        """Format validation result as user-friendly message.

        Returns:
            Formatted message string
        """
        lines = []

        if self.success and self.is_valid():
            lines.append("✓ Validation passed")
        else:
            lines.append("✗ Validation failed")

        # Add errors
        for error in self.errors:
            lines.append(f"  ✗ ERROR: {error}")

        # Add warnings
        for warning in self.warnings:
            lines.append(f"  ⚠ WARNING: {warning}")

        # Add metadata if present
        if self.metadata:
            lines.append("\nMetadata:")
            for key, value in self.metadata.items():
                lines.append(f"  {key}: {value}")

        return "\n".join(lines)


class AudioValidator:
    """Validates audio files against requirements."""

    def __init__(
        self,
        sample_rate: int = 12000,
        channels: int = 1,
        bit_depth: int = 16,
    ):
        """Initialize AudioValidator.

        Args:
            sample_rate: Target sample rate in Hz (default: 12000 for Qwen3-TTS)
            channels: Target number of channels (default: 1 for mono)
            bit_depth: Target bit depth (default: 16)
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.bit_depth = bit_depth

    def validate(self, file_path: Path | str) -> ValidationResult:
        """Validate audio file against Qwen3-TTS requirements.

        Checks:
        - Sample rate (warn if not 12000 Hz)
        - Channels (error if not mono)
        - Bit depth (warn if not 16-bit)
        - Duration (error if < 3s, warn if > 30s)
        - Clipping (error if detected)

        Args:
            file_path: Path to audio file

        Returns:
            ValidationResult with status, warnings, and errors
        """
        file_path = Path(file_path)
        errors = []
        warnings = []
        metadata = {}

        try:
            # Load audio file
            audio, sr = librosa.load(file_path, sr=None, mono=False)

            # Get audio info
            info = sf.info(file_path)

            # Check sample rate
            if sr != self.sample_rate:
                warnings.append(
                    f"Sample rate is {sr} Hz (recommended: {self.sample_rate} Hz)"
                )
            metadata["sample_rate"] = sr

            # Check channels
            if len(audio.shape) > 1:
                num_channels = audio.shape[0]
            else:
                num_channels = 1

            if num_channels != self.channels:
                errors.append(
                    f"Audio has {num_channels} channels (required: {self.channels} for mono)"
                )
            metadata["channels"] = num_channels

            # Check bit depth
            if hasattr(info, "subtype"):
                if "16" not in info.subtype and self.bit_depth == 16:
                    warnings.append(
                        f"Bit depth is {info.subtype} (recommended: 16-bit PCM)"
                    )
                metadata["bit_depth"] = info.subtype

            # Check duration (Qwen3-TTS requires minimum 3 seconds)
            duration = librosa.get_duration(y=audio, sr=sr)
            metadata["duration"] = duration

            if duration < 3.0:
                errors.append(
                    f"Duration is {duration:.2f}s (minimum: 3s for Qwen3-TTS)"
                )
            elif duration > 30.0:
                warnings.append(
                    f"Duration is {duration:.2f}s (recommended: 3-30s for diminishing returns)"
                )

            # Check for clipping
            if len(audio.shape) > 1:
                # Stereo: check both channels
                max_amplitude = np.max(np.abs(audio))
            else:
                # Mono
                max_amplitude = np.max(np.abs(audio))

            if max_amplitude >= 0.99:  # Close to maximum
                errors.append(
                    "Audio clipping detected (distortion). Re-record with lower volume."
                )
            metadata["max_amplitude"] = max_amplitude

            # Determine success
            success = len(errors) == 0

            return ValidationResult(
                success=success,
                errors=errors,
                warnings=warnings,
                metadata=metadata,
            )

        except Exception as e:
            return ValidationResult(
                success=False,
                errors=[f"Failed to validate audio: {str(e)}"],
                warnings=[],
                metadata={},
            )
