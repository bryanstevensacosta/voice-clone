"""Voice Profile Entity.

Entity representing a voice profile with identity and behavior.
"""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from .audio_sample import AudioSample


@dataclass
class VoiceProfile:
    """Voice profile entity with identity.

    This is an entity - it has identity (id) and can change over time.
    Contains business logic for managing voice profiles.
    """

    id: str
    name: str
    samples: list[AudioSample]
    created_at: datetime
    language: str = "es"
    reference_text: str | None = None

    @classmethod
    def create(
        cls,
        name: str,
        samples: list[AudioSample],
        language: str = "es",
        reference_text: str | None = None,
    ) -> "VoiceProfile":
        """Create a new voice profile with generated ID.

        Args:
            name: Profile name
            samples: List of audio samples
            language: Language code (default: "es")
            reference_text: Optional reference text

        Returns:
            New VoiceProfile instance

        Raises:
            ValueError: If profile is invalid
        """
        profile = cls(
            id=str(uuid4()),
            name=name,
            samples=samples,
            created_at=datetime.now(),
            language=language,
            reference_text=reference_text,
        )

        if not profile.is_valid():
            raise ValueError(f"Invalid voice profile: {profile.validation_errors()}")

        return profile

    def add_sample(self, sample: AudioSample) -> None:
        """Add an audio sample to the profile.

        Args:
            sample: Audio sample to add

        Raises:
            ValueError: If adding sample would make profile invalid
        """
        # Check if adding this sample would exceed limits
        if len(self.samples) >= 10:
            raise ValueError("Cannot add more samples. Maximum 10 samples per profile.")

        self.samples.append(sample)

        # Validate after adding
        if not self.is_valid():
            # Rollback
            self.samples.remove(sample)
            raise ValueError(
                f"Adding sample would make profile invalid: "
                f"{self.validation_errors()}"
            )

    def remove_sample(self, sample_path: Path) -> bool:
        """Remove a sample from the profile.

        Args:
            sample_path: Path of the sample to remove

        Returns:
            True if sample was removed, False if not found

        Raises:
            ValueError: If removing sample would make profile invalid
        """
        # Find sample
        sample_to_remove = None
        for sample in self.samples:
            if sample.path == sample_path:
                sample_to_remove = sample
                break

        if sample_to_remove is None:
            return False

        # Check if removing would make profile invalid
        if len(self.samples) <= 1:
            raise ValueError(
                "Cannot remove sample. Profile must have at least 1 sample."
            )

        self.samples.remove(sample_to_remove)
        return True

    @property
    def total_duration(self) -> float:
        """Calculate total duration of all samples.

        Returns:
            Total duration in seconds
        """
        return sum(sample.duration for sample in self.samples)

    def is_valid(self) -> bool:
        """Check if profile meets all business rules.

        Returns:
            True if profile is valid
        """
        return len(self.validation_errors()) == 0

    def validation_errors(self) -> list[str]:
        """Get list of validation errors.

        Returns:
            List of error messages (empty if valid)
        """
        errors = []

        # Must have at least 1 sample
        if len(self.samples) == 0:
            errors.append("Profile must have at least 1 audio sample")

        # Must have at most 10 samples
        if len(self.samples) > 10:
            errors.append(
                f"Profile has {len(self.samples)} samples. " f"Maximum is 10 samples."
            )

        # Total duration must be between 10 and 300 seconds
        total_dur = self.total_duration
        if total_dur < 10.0:
            errors.append(
                f"Total duration is {total_dur:.1f}s. " f"Minimum is 10 seconds."
            )
        if total_dur > 300.0:
            errors.append(
                f"Total duration is {total_dur:.1f}s. " f"Maximum is 300 seconds."
            )

        # Name must not be empty
        if not self.name or not self.name.strip():
            errors.append("Profile name cannot be empty")

        # All samples must be valid
        for i, sample in enumerate(self.samples):
            if not sample.is_valid_duration():
                errors.append(f"Sample {i+1} ({sample.path.name}) has invalid duration")
            if not sample.is_valid_sample_rate():
                errors.append(
                    f"Sample {i+1} ({sample.path.name}) has invalid sample rate"
                )

        return errors

    def __str__(self) -> str:
        """String representation of voice profile."""
        return (
            f"VoiceProfile(id={self.id[:8]}..., name='{self.name}', "
            f"samples={len(self.samples)}, duration={self.total_duration:.1f}s)"
        )
