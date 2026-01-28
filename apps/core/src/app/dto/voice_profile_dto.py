"""Voice Profile Data Transfer Object.

DTOs for transferring voice profile data between layers.
"""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from domain.models.voice_profile import VoiceProfile


@dataclass
class VoiceProfileDTO:
    """Data Transfer Object for VoiceProfile.

    Used to transfer voice profile data between application layers
    and serialize/deserialize for external interfaces.
    """

    id: str
    name: str
    samples: list[dict[str, Any]]
    created_at: str
    total_duration: float
    language: str
    reference_text: str | None = None

    @classmethod
    def from_entity(cls, profile: VoiceProfile) -> "VoiceProfileDTO":
        """Create DTO from domain entity.

        Args:
            profile: VoiceProfile domain entity

        Returns:
            VoiceProfileDTO instance
        """
        # Convert AudioSample objects to dictionaries
        samples = [
            {
                "path": str(sample.path),
                "duration": sample.duration,
                "sample_rate": sample.sample_rate,
                "channels": sample.channels,
                "bit_depth": sample.bit_depth,
            }
            for sample in profile.samples
        ]

        return cls(
            id=profile.id,
            name=profile.name,
            samples=samples,
            created_at=profile.created_at.isoformat(),
            total_duration=profile.total_duration,
            language=profile.language,
            reference_text=profile.reference_text,
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert DTO to dictionary.

        Returns:
            Dictionary representation of the DTO
        """
        return {
            "id": self.id,
            "name": self.name,
            "samples": self.samples,
            "created_at": self.created_at,
            "total_duration": self.total_duration,
            "language": self.language,
            "reference_text": self.reference_text,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "VoiceProfileDTO":
        """Create DTO from dictionary.

        Args:
            data: Dictionary with profile data

        Returns:
            VoiceProfileDTO instance
        """
        return cls(
            id=data["id"],
            name=data["name"],
            samples=data["samples"],
            created_at=data["created_at"],
            total_duration=data["total_duration"],
            language=data["language"],
            reference_text=data.get("reference_text"),
        )

    def to_entity(self) -> VoiceProfile:
        """Convert DTO back to domain entity.

        Returns:
            VoiceProfile domain entity

        Note:
            This requires reconstructing AudioSample objects from the sample data.
            The samples should be validated before creating the entity.
        """
        from domain.models.audio_sample import AudioSample

        # Reconstruct AudioSample objects
        audio_samples = [
            AudioSample(
                path=Path(sample["path"]),
                duration=sample["duration"],
                sample_rate=sample["sample_rate"],
                channels=sample["channels"],
                bit_depth=sample["bit_depth"],
            )
            for sample in self.samples
        ]

        # Create VoiceProfile
        profile = VoiceProfile(
            id=self.id,
            name=self.name,
            samples=audio_samples,
            created_at=datetime.fromisoformat(self.created_at),
            language=self.language,
            reference_text=self.reference_text,
        )

        return profile
