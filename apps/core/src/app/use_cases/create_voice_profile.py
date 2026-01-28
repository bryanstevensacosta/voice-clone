"""Create Voice Profile Use Case.

Use case for creating a new voice profile from audio samples.
"""

from pathlib import Path

from app.dto.voice_profile_dto import VoiceProfileDTO
from domain.ports.audio_processor import AudioProcessor
from domain.ports.profile_repository import ProfileRepository
from domain.services.voice_cloning import VoiceCloningService


class CreateVoiceProfileUseCase:
    """Use case for creating a voice profile.

    Orchestrates the voice cloning service and profile repository
    to create and persist a new voice profile.
    """

    def __init__(
        self,
        audio_processor: AudioProcessor,
        profile_repository: ProfileRepository,
    ):
        """Initialize the use case.

        Args:
            audio_processor: Audio processor port implementation
            profile_repository: Profile repository port implementation
        """
        self._voice_cloning = VoiceCloningService(audio_processor)
        self._repository = profile_repository

    def execute(
        self,
        name: str,
        sample_paths: list[Path],
        language: str = "es",
        reference_text: str | None = None,
    ) -> VoiceProfileDTO:
        """Execute the use case to create a voice profile.

        Args:
            name: Name for the voice profile
            sample_paths: List of paths to audio sample files
            language: Language code (default: "es")
            reference_text: Optional reference text describing the samples

        Returns:
            VoiceProfileDTO with the created profile data

        Raises:
            InvalidSampleException: If samples are invalid
            InvalidProfileException: If profile doesn't meet requirements
        """
        # Use domain service to create profile from samples
        profile = self._voice_cloning.create_profile_from_samples(
            name=name,
            sample_paths=sample_paths,
            language=language,
            reference_text=reference_text,
        )

        # Persist the profile
        self._repository.save(profile)

        # Convert to DTO and return
        return VoiceProfileDTO.from_entity(profile)
