"""List Voice Profiles Use Case.

Use case for listing all available voice profiles.
"""

from app.dto.voice_profile_dto import VoiceProfileDTO
from domain.ports.profile_repository import ProfileRepository


class ListVoiceProfilesUseCase:
    """Use case for listing voice profiles.

    Retrieves all voice profiles from the repository and converts
    them to DTOs for the application layer.
    """

    def __init__(self, profile_repository: ProfileRepository):
        """Initialize the use case.

        Args:
            profile_repository: Profile repository port implementation
        """
        self._repository = profile_repository

    def execute(self) -> list[VoiceProfileDTO]:
        """Execute the use case to list all profiles.

        Returns:
            List of VoiceProfileDTO objects
        """
        # Get all profiles from repository
        profiles = self._repository.list_all()

        # Convert to DTOs
        return [VoiceProfileDTO.from_entity(profile) for profile in profiles]
