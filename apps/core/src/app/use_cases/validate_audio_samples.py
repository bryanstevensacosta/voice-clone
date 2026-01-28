"""Validate Audio Samples Use Case.

Use case for validating audio samples before creating a profile.
"""

from dataclasses import dataclass
from pathlib import Path

from domain.exceptions import InvalidSampleException
from domain.ports.audio_processor import AudioProcessor


@dataclass
class SampleValidationResult:
    """Result of validating a single audio sample."""

    path: Path
    valid: bool
    error: str | None = None
    duration: float | None = None
    sample_rate: int | None = None
    channels: int | None = None
    bit_depth: int | None = None


@dataclass
class ValidationSummary:
    """Summary of validation results for multiple samples."""

    total_samples: int
    valid_samples: int
    invalid_samples: int
    results: list[SampleValidationResult]
    total_duration: float

    @property
    def all_valid(self) -> bool:
        """Check if all samples are valid."""
        return self.invalid_samples == 0


class ValidateAudioSamplesUseCase:
    """Use case for validating audio samples.

    Validates audio samples to ensure they meet requirements
    before creating a voice profile.
    """

    def __init__(self, audio_processor: AudioProcessor):
        """Initialize the use case.

        Args:
            audio_processor: Audio processor port implementation
        """
        self._processor = audio_processor

    def execute(self, sample_paths: list[Path]) -> ValidationSummary:
        """Execute the use case to validate audio samples.

        Args:
            sample_paths: List of paths to audio sample files

        Returns:
            ValidationSummary with validation results for all samples
        """
        results: list[SampleValidationResult] = []
        total_duration = 0.0

        for path in sample_paths:
            try:
                # Validate the sample
                is_valid = self._processor.validate_sample(path)

                # If valid, process to get metadata
                if is_valid:
                    sample = self._processor.process_sample(path)
                    results.append(
                        SampleValidationResult(
                            path=path,
                            valid=True,
                            duration=sample.duration,
                            sample_rate=sample.sample_rate,
                            channels=sample.channels,
                            bit_depth=sample.bit_depth,
                        )
                    )
                    total_duration += sample.duration
                else:
                    results.append(
                        SampleValidationResult(
                            path=path,
                            valid=False,
                            error="Validation failed",
                        )
                    )

            except InvalidSampleException as e:
                results.append(
                    SampleValidationResult(
                        path=path,
                        valid=False,
                        error=str(e),
                    )
                )
            except Exception as e:
                results.append(
                    SampleValidationResult(
                        path=path,
                        valid=False,
                        error=f"Unexpected error: {e}",
                    )
                )

        # Create summary
        valid_count = sum(1 for r in results if r.valid)
        invalid_count = len(results) - valid_count

        return ValidationSummary(
            total_samples=len(results),
            valid_samples=valid_count,
            invalid_samples=invalid_count,
            results=results,
            total_duration=total_duration,
        )
