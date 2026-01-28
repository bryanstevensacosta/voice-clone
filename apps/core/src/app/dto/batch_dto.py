"""Batch Processing Data Transfer Objects.

DTOs for batch audio generation requests and results.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .generation_dto import GenerationRequestDTO, GenerationResultDTO


@dataclass
class BatchSegment:
    """Represents a single segment in a batch processing request.

    Each segment has an ID, text, and optional metadata.
    """

    id: str
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert segment to dictionary.

        Returns:
            Dictionary representation of the segment
        """
        return {
            "id": self.id,
            "text": self.text,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BatchSegment":
        """Create segment from dictionary.

        Args:
            data: Dictionary with segment data

        Returns:
            BatchSegment instance
        """
        return cls(
            id=data["id"],
            text=data["text"],
            metadata=data.get("metadata", {}),
        )


@dataclass
class BatchRequestDTO:
    """Data Transfer Object for batch processing request.

    Contains all parameters needed to process multiple text segments.
    """

    profile_id: str
    segments: list[BatchSegment]
    output_dir: Path
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
            "segments": [seg.to_dict() for seg in self.segments],
            "output_dir": str(self.output_dir),
            "temperature": self.temperature,
            "speed": self.speed,
            "language": self.language,
            "mode": self.mode,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BatchRequestDTO":
        """Create DTO from dictionary.

        Args:
            data: Dictionary with request data

        Returns:
            BatchRequestDTO instance
        """
        segments = [BatchSegment.from_dict(seg) for seg in data["segments"]]

        return cls(
            profile_id=data["profile_id"],
            segments=segments,
            output_dir=Path(data["output_dir"]),
            temperature=data.get("temperature", 0.75),
            speed=data.get("speed", 1.0),
            language=data.get("language", "es"),
            mode=data.get("mode", "clone"),
            metadata=data.get("metadata", {}),
        )

    def to_generation_requests(self) -> list[GenerationRequestDTO]:
        """Convert batch request to individual generation requests.

        Returns:
            List of GenerationRequestDTO, one per segment
        """
        requests = []
        for segment in self.segments:
            output_path = self.output_dir / f"{segment.id}.wav"
            request = GenerationRequestDTO(
                profile_id=self.profile_id,
                text=segment.text,
                output_path=output_path,
                temperature=self.temperature,
                speed=self.speed,
                language=self.language,
                mode=self.mode,
                metadata={
                    **self.metadata,
                    **segment.metadata,
                    "segment_id": segment.id,
                },
            )
            requests.append(request)
        return requests


@dataclass
class BatchResultDTO:
    """Data Transfer Object for batch processing result.

    Contains the results of processing multiple segments.
    """

    success: bool
    total_segments: int
    successful_segments: int
    failed_segments: int
    results: list[GenerationResultDTO]
    total_duration: float | None = None
    total_generation_time: float | None = None
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert DTO to dictionary.

        Returns:
            Dictionary representation of the result
        """
        return {
            "success": self.success,
            "total_segments": self.total_segments,
            "successful_segments": self.successful_segments,
            "failed_segments": self.failed_segments,
            "results": [result.to_dict() for result in self.results],
            "total_duration": self.total_duration,
            "total_generation_time": self.total_generation_time,
            "error": self.error,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BatchResultDTO":
        """Create DTO from dictionary.

        Args:
            data: Dictionary with result data

        Returns:
            BatchResultDTO instance
        """
        results = [GenerationResultDTO.from_dict(res) for res in data["results"]]

        return cls(
            success=data["success"],
            total_segments=data["total_segments"],
            successful_segments=data["successful_segments"],
            failed_segments=data["failed_segments"],
            results=results,
            total_duration=data.get("total_duration"),
            total_generation_time=data.get("total_generation_time"),
            error=data.get("error"),
            metadata=data.get("metadata", {}),
        )

    @classmethod
    def from_results(cls, results: list[GenerationResultDTO]) -> "BatchResultDTO":
        """Create batch result from individual generation results.

        Args:
            results: List of generation results

        Returns:
            BatchResultDTO summarizing all results
        """
        total_segments = len(results)
        successful_segments = sum(1 for r in results if r.success)
        failed_segments = total_segments - successful_segments

        # Calculate totals
        total_duration = sum(r.duration for r in results if r.duration is not None)
        total_generation_time = sum(
            r.generation_time for r in results if r.generation_time is not None
        )

        # Overall success if all segments succeeded
        success = failed_segments == 0

        # Collect error messages if any
        error = None
        if failed_segments > 0:
            errors = [r.error for r in results if r.error]
            error = f"{failed_segments} segment(s) failed: {'; '.join(errors[:3])}"
            if len(errors) > 3:
                error += f" (and {len(errors) - 3} more)"

        return cls(
            success=success,
            total_segments=total_segments,
            successful_segments=successful_segments,
            failed_segments=failed_segments,
            results=results,
            total_duration=total_duration if total_duration > 0 else None,
            total_generation_time=(
                total_generation_time if total_generation_time > 0 else None
            ),
            error=error,
        )
