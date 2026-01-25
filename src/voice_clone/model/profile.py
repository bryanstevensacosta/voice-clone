"""Voice profile data models."""

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from voice_clone.audio.processor import AudioProcessor


@dataclass
class VoiceSample:
    """Represents a single voice sample."""

    path: str
    duration: float
    emotion: str = "neutral"
    quality_score: float = 1.0

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "path": self.path,
            "duration": self.duration,
            "emotion": self.emotion,
            "quality_score": self.quality_score,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "VoiceSample":
        """Create from dictionary."""
        return cls(
            path=data["path"],
            duration=data["duration"],
            emotion=data.get("emotion", "neutral"),
            quality_score=data.get("quality_score", 1.0),
        )


@dataclass
class VoiceProfile:
    """Voice profile containing reference samples and metadata for Qwen3-TTS."""

    name: str
    samples: list[VoiceSample] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    language: str = "es"
    total_duration: float = 0.0
    ref_text: str = ""  # NEW: Required for Qwen3-TTS voice cloning
    sample_rate: int = 12000  # NEW: Qwen3-TTS native sample rate

    def __post_init__(self) -> None:
        """Calculate total duration after initialization."""
        if self.samples:
            self.total_duration = sum(s.duration for s in self.samples)

    @classmethod
    def from_directory(
        cls,
        name: str,
        samples_dir: Path | str,
        language: str = "es",
        ref_text: str = "",
    ) -> "VoiceProfile":
        """Create voice profile from directory of audio samples.

        Args:
            name: Profile name
            samples_dir: Directory containing audio samples
            language: Language code (default: "es")
            ref_text: Reference text (transcript of reference audio) for Qwen3-TTS

        Returns:
            VoiceProfile instance
        """
        samples_dir = Path(samples_dir)
        processor = AudioProcessor()
        samples = []

        # Find all WAV files in directory
        for audio_file in sorted(samples_dir.glob("*.wav")):
            # Validate sample
            result = processor.validate_sample(audio_file)

            if not result.is_valid():
                print(f"Skipping {audio_file.name}: {result.errors}")
                continue

            # Get duration
            duration_str = result.metadata.get("duration", "0s")
            duration = float(duration_str.rstrip("s"))

            # Infer emotion from filename
            emotion = "neutral"
            filename_lower = audio_file.stem.lower()
            if "happy" in filename_lower or "excited" in filename_lower:
                emotion = "happy"
            elif "sad" in filename_lower:
                emotion = "sad"
            elif "angry" in filename_lower:
                emotion = "angry"
            elif "calm" in filename_lower:
                emotion = "calm"
            elif "serious" in filename_lower:
                emotion = "serious"

            # Calculate quality score based on validation
            quality_score = 1.0
            if result.warnings:
                quality_score = 0.8  # Reduce score if there are warnings

            sample = VoiceSample(
                path=str(audio_file),
                duration=duration,
                emotion=emotion,
                quality_score=quality_score,
            )
            samples.append(sample)

        profile = cls(
            name=name,
            samples=samples,
            language=language,
            ref_text=ref_text,
        )

        return profile

    def to_json(self, output_path: Path | str) -> None:
        """Save profile to JSON file.

        Args:
            output_path: Path to output JSON file
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "name": self.name,
            "created_at": self.created_at,
            "language": self.language,
            "total_duration": self.total_duration,
            "ref_text": self.ref_text,  # NEW: Include ref_text for Qwen3-TTS
            "sample_rate": self.sample_rate,  # NEW: Include sample_rate
            "samples": [s.to_dict() for s in self.samples],
        }

        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)

    @classmethod
    def from_json(cls, input_path: Path | str) -> "VoiceProfile":
        """Load profile from JSON file.

        Args:
            input_path: Path to input JSON file

        Returns:
            VoiceProfile instance
        """
        input_path = Path(input_path)

        with open(input_path) as f:
            data = json.load(f)

        samples = [VoiceSample.from_dict(s) for s in data["samples"]]

        return cls(
            name=data["name"],
            samples=samples,
            created_at=data["created_at"],
            language=data["language"],
            total_duration=data["total_duration"],
            ref_text=data.get("ref_text", ""),  # NEW: Load ref_text (default to empty)
            sample_rate=data.get(
                "sample_rate", 12000
            ),  # NEW: Load sample_rate (default to 12000)
        )

    def validate(self) -> tuple[bool, list[str]]:
        """Validate that profile has sufficient samples and duration for Qwen3-TTS.

        Returns:
            Tuple of (is_valid, warnings)
        """
        warnings = []

        # Check minimum number of samples
        if len(self.samples) < 6:
            warnings.append(
                f"Profile has only {len(self.samples)} samples (recommended: 6-10)"
            )

        # Check total duration (Qwen3-TTS minimum is 3s per sample)
        if self.total_duration < 18.0:  # 6 samples * 3s minimum
            warnings.append(
                f"Total duration is {self.total_duration:.1f}s (recommended: 60-180s)"
            )
        elif self.total_duration > 300.0:
            warnings.append(
                f"Total duration is {self.total_duration:.1f}s (diminishing returns beyond 300s)"
            )

        # Check for emotion variety
        emotions = {s.emotion for s in self.samples}
        if len(emotions) < 2:
            warnings.append(
                "Profile has limited emotion variety (recommended: multiple emotions)"
            )

        # NEW: Check for ref_text (required for Qwen3-TTS)
        if not self.ref_text or len(self.ref_text.strip()) == 0:
            warnings.append(
                "Profile missing ref_text (required for Qwen3-TTS voice cloning)"
            )

        # NEW: Check sample rate
        if self.sample_rate != 12000:
            warnings.append(
                f"Sample rate is {self.sample_rate} Hz (Qwen3-TTS native: 12000 Hz)"
            )

        is_valid = len(self.samples) >= 1 and self.total_duration >= 3.0

        return is_valid, warnings
