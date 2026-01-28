"""Voice Cloning Domain Service.

Contains business logic for creating voice profiles from audio samples.
"""

from pathlib import Path

from apps.core.src.domain.models.voice_profile import VoiceProfile
from apps.core.src.domain.ports.audio_processor import AudioProcessor


class VoiceCloningService:
    """Domain service for voice cloning operations.

    This service orchestrates the creation of voice profiles from audio samples,
    applying business rules and validation logic.
    """

    def __init__(self, audio_processor: AudioProcessor):
        """Initialize the voice cloning service.

        Args:
            audio_processor: Audio processor port for sample validation/processing
        """
        self._audio_processor = audio_processor

    def create_profile_from_samples(
        self,
        name: str,
        sample_paths: list[Path],
        language: str = "es",
        reference_text: str | None = None,
    ) -> VoiceProfile:
        """Create a voice profile from audio samples.

        This method applies business rules:
        - Validates all samples before processing
        - Ensures samples meet quality requirements
        - Creates a valid voice profile

        Args:
            name: Profile name
            sample_paths: List of paths to audio samples
            language: Language code (default: "es")
            reference_text: Optional reference text

        Returns:
            Valid VoiceProfile entity

        Raises:
            InvalidSampleException: If any sample is invalid
            ValueError: If profile cannot be created
        """
        # Validate all samples first
        for sample_path in sample_paths:
            if not self._audio_processor.validate_sample(sample_path):
                raise ValueError(f"Invalid sample: {sample_path}")

        # Process samples to create AudioSample value objects
        samples = []
        for sample_path in sample_paths:
            audio_sample = self._audio_processor.process_sample(sample_path)
            samples.append(audio_sample)

        # Create voice profile using factory method
        # This will validate business rules (1-10 samples, 10-300s duration, etc.)
        profile = VoiceProfile.create(
            name=name,
            samples=samples,
            language=language,
            reference_text=reference_text,
        )

        return profile

    def validate_profile_for_cloning(self, profile: VoiceProfile) -> bool:
        """Validate that a profile is suitable for voice cloning.

        Args:
            profile: Voice profile to validate

        Returns:
            True if profile is valid for cloning
        """
        # Check basic validity
        if not profile.is_valid():
            return False

        # Additional business rules for cloning
        # At least 2 samples recommended for better quality
        if len(profile.samples) < 2:
            return False

        # Total duration should be at least 20 seconds for good quality
        if profile.total_duration < 20.0:
            return False

        return True
