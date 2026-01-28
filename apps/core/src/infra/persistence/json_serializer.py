"""JSON Serializer for Voice Profiles.

Handles serialization and deserialization of VoiceProfile entities to/from JSON.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from domain.models.audio_sample import AudioSample  # type: ignore[import-untyped]
from domain.models.voice_profile import VoiceProfile  # type: ignore[import-untyped]


class JSONSerializer:
    """Serializer for converting VoiceProfile to/from JSON.

    This class handles the conversion between domain entities and JSON format
    for file-based storage.
    """

    @staticmethod
    def serialize(profile: VoiceProfile) -> dict[str, Any]:
        """Convert VoiceProfile to JSON-serializable dictionary.

        Args:
            profile: Voice profile to serialize

        Returns:
            Dictionary that can be serialized to JSON
        """
        return {
            "id": profile.id,
            "name": profile.name,
            "language": profile.language,
            "reference_text": profile.reference_text,
            "created_at": profile.created_at.isoformat(),
            "samples": [
                {
                    "path": str(sample.path),
                    "duration": sample.duration,
                    "sample_rate": sample.sample_rate,
                    "channels": sample.channels,
                    "bit_depth": sample.bit_depth,
                    "emotion": sample.emotion,
                }
                for sample in profile.samples
            ],
        }

    @staticmethod
    def deserialize(data: dict[str, Any]) -> VoiceProfile:
        """Convert JSON dictionary to VoiceProfile.

        Args:
            data: Dictionary loaded from JSON

        Returns:
            Reconstructed VoiceProfile instance

        Raises:
            ValueError: If data is invalid or missing required fields
            KeyError: If required fields are missing
        """
        # Reconstruct audio samples
        samples = [
            AudioSample(
                path=Path(sample_data["path"]),
                duration=sample_data["duration"],
                sample_rate=sample_data["sample_rate"],
                channels=sample_data["channels"],
                bit_depth=sample_data["bit_depth"],
                emotion=sample_data.get("emotion"),
            )
            for sample_data in data["samples"]
        ]

        # Reconstruct voice profile
        profile = VoiceProfile(
            id=data["id"],
            name=data["name"],
            samples=samples,
            created_at=datetime.fromisoformat(data["created_at"]),
            language=data.get("language", "es"),
            reference_text=data.get("reference_text"),
        )

        return profile

    @staticmethod
    def to_json_string(profile: VoiceProfile, indent: int = 2) -> str:
        """Convert VoiceProfile to JSON string.

        Args:
            profile: Voice profile to serialize
            indent: Number of spaces for indentation (default: 2)

        Returns:
            JSON string representation
        """
        data = JSONSerializer.serialize(profile)
        return json.dumps(data, indent=indent, ensure_ascii=False)

    @staticmethod
    def from_json_string(json_string: str) -> VoiceProfile:
        """Convert JSON string to VoiceProfile.

        Args:
            json_string: JSON string to deserialize

        Returns:
            Reconstructed VoiceProfile instance

        Raises:
            ValueError: If JSON is invalid or data is malformed
            json.JSONDecodeError: If JSON parsing fails
        """
        data = json.loads(json_string)
        return JSONSerializer.deserialize(data)
