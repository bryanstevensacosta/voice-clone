"""Generation Data Transfer Objects.

DTOs for audio generation requests and results.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class GenerationRequestDTO:
    """Data Transfer Object for audio generation request.

    Contains all parameters needed to generate audio from text.
    """

    profile_id: str
    text: str
    output_path: Path | None = None
    temperature: float = 0.75
    speed: float = 1.0
    language: str = "es"
    mode: str = "clone"
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert DTO to dictionary.

        Returns:
            Dictionary representation of the request
        """
        return {
            "profile_id": self.profile_id,
            "text": self.text,
            "output_path": str(self.output_path) if self.output_path else None,
            "temperature": self.temperature,
            "speed": self.speed,
            "language": self.language,
            "mode": self.mode,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "GenerationRequestDTO":
        """Create DTO from dictionary.

        Args:
            data: Dictionary with request data

        Returns:
            GenerationRequestDTO instance
        """
        output_path = data.get("output_path")
        if output_path:
            output_path = Path(output_path)

        return cls(
            profile_id=data["profile_id"],
            text=data["text"],
            output_path=output_path,
            temperature=data.get("temperature", 0.75),
            speed=data.get("speed", 1.0),
            language=data.get("language", "es"),
            mode=data.get("mode", "clone"),
            metadata=data.get("metadata", {}),
        )


@dataclass
class GenerationResultDTO:
    """Data Transfer Object for audio generation result.

    Contains the result of an audio generation operation.
    """

    success: bool
    output_path: Path | None = None
    duration: float | None = None
    error: str | None = None
    profile_id: str | None = None
    text_length: int | None = None
    generation_time: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert DTO to dictionary.

        Returns:
            Dictionary representation of the result
        """
        return {
            "success": self.success,
            "output_path": str(self.output_path) if self.output_path else None,
            "duration": self.duration,
            "error": self.error,
            "profile_id": self.profile_id,
            "text_length": self.text_length,
            "generation_time": self.generation_time,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "GenerationResultDTO":
        """Create DTO from dictionary.

        Args:
            data: Dictionary with result data

        Returns:
            GenerationResultDTO instance
        """
        output_path = data.get("output_path")
        if output_path:
            output_path = Path(output_path)

        return cls(
            success=data["success"],
            output_path=output_path,
            duration=data.get("duration"),
            error=data.get("error"),
            profile_id=data.get("profile_id"),
            text_length=data.get("text_length"),
            generation_time=data.get("generation_time"),
            metadata=data.get("metadata", {}),
        )

    @classmethod
    def success_result(
        cls,
        output_path: Path,
        duration: float,
        profile_id: str,
        text_length: int,
        generation_time: float,
        **kwargs: Any,
    ) -> "GenerationResultDTO":
        """Create a successful generation result.

        Args:
            output_path: Path to generated audio file
            duration: Duration of generated audio in seconds
            profile_id: ID of the voice profile used
            text_length: Length of input text in characters
            generation_time: Time taken to generate in seconds
            **kwargs: Additional metadata

        Returns:
            GenerationResultDTO with success=True
        """
        return cls(
            success=True,
            output_path=output_path,
            duration=duration,
            profile_id=profile_id,
            text_length=text_length,
            generation_time=generation_time,
            metadata=kwargs,
        )

    @classmethod
    def error_result(
        cls, error: str, profile_id: str | None = None
    ) -> "GenerationResultDTO":
        """Create an error generation result.

        Args:
            error: Error message
            profile_id: Optional profile ID if known

        Returns:
            GenerationResultDTO with success=False
        """
        return cls(
            success=False,
            error=error,
            profile_id=profile_id,
        )
