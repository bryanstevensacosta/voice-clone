"""Profile Repository Port.

Interface for voice profile persistence.
Infrastructure adapters (e.g., FileProfileRepository) must implement this interface.
"""

from abc import ABC, abstractmethod

from apps.core.src.domain.models.voice_profile import VoiceProfile


class ProfileRepository(ABC):
    """Abstract interface for profile storage.

    This port defines the contract that all profile repository adapters must implement.
    Examples: FileProfileRepository, DatabaseProfileRepository, etc.
    """

    @abstractmethod
    def save(self, profile: VoiceProfile) -> None:
        """Save a voice profile.

        Args:
            profile: Voice profile to save

        Raises:
            Exception: If save operation fails
        """
        pass

    @abstractmethod
    def find_by_id(self, profile_id: str) -> VoiceProfile | None:
        """Find a profile by its ID.

        Args:
            profile_id: Unique identifier of the profile

        Returns:
            VoiceProfile if found, None otherwise
        """
        pass

    @abstractmethod
    def list_all(self) -> list[VoiceProfile]:
        """List all available voice profiles.

        Returns:
            List of all voice profiles
        """
        pass

    @abstractmethod
    def delete(self, profile_id: str) -> bool:
        """Delete a voice profile.

        Args:
            profile_id: Unique identifier of the profile to delete

        Returns:
            True if profile was deleted, False if not found
        """
        pass
