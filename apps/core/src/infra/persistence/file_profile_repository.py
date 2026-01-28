"""File-based Profile Repository.

Implementation of ProfileRepository port using JSON files for local storage.
Perfect for desktop-first offline applications.
"""

import json
import logging
from pathlib import Path

from ...domain.models.voice_profile import VoiceProfile
from ...domain.ports.profile_repository import (
    ProfileRepository,  # type: ignore[import-untyped]
)
from .json_serializer import JSONSerializer

logger = logging.getLogger(__name__)


class FileProfileRepository(ProfileRepository):
    """File-based repository for voice profiles.

    Stores voice profiles as JSON files in a local directory.
    Each profile is saved as {profile_id}.json.

    This implementation is perfect for desktop-first offline applications:
    - No database server required
    - Works completely offline
    - Easy to backup (just copy files)
    - Human-readable JSON format
    """

    def __init__(self, profiles_dir: Path):
        """Initialize file-based repository.

        Args:
            profiles_dir: Directory where profile JSON files will be stored
        """
        self.profiles_dir = Path(profiles_dir)
        self._ensure_directory_exists()

    def _ensure_directory_exists(self) -> None:
        """Create profiles directory if it doesn't exist."""
        self.profiles_dir.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Profiles directory: {self.profiles_dir}")

    def _get_profile_path(self, profile_id: str) -> Path:
        """Get file path for a profile.

        Args:
            profile_id: Profile identifier

        Returns:
            Path to profile JSON file
        """
        return self.profiles_dir / f"{profile_id}.json"

    def save(self, profile: VoiceProfile) -> None:
        """Save a voice profile to JSON file.

        Args:
            profile: Voice profile to save

        Raises:
            OSError: If file write fails
            ValueError: If profile is invalid
        """
        if not profile.is_valid():
            raise ValueError(
                f"Cannot save invalid profile: {profile.validation_errors()}"
            )

        file_path = self._get_profile_path(profile.id)

        try:
            # Serialize to JSON
            data = JSONSerializer.serialize(profile)

            # Write to file with pretty formatting
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            logger.info(f"Saved profile '{profile.name}' to {file_path}")

        except OSError as e:
            logger.error(f"Failed to save profile {profile.id}: {e}")
            raise

    def find_by_id(self, profile_id: str) -> VoiceProfile | None:
        """Find a profile by its ID.

        Args:
            profile_id: Unique identifier of the profile

        Returns:
            VoiceProfile if found, None otherwise
        """
        file_path = self._get_profile_path(profile_id)

        if not file_path.exists():
            logger.debug(f"Profile {profile_id} not found at {file_path}")
            return None

        try:
            # Read JSON file
            with open(file_path, encoding="utf-8") as f:
                data = json.load(f)

            # Deserialize to VoiceProfile
            profile = JSONSerializer.deserialize(data)
            logger.debug(f"Loaded profile '{profile.name}' from {file_path}")
            return profile

        except (OSError, json.JSONDecodeError, ValueError, KeyError) as e:
            logger.error(f"Failed to load profile {profile_id}: {e}")
            return None

    def list_all(self) -> list[VoiceProfile]:
        """List all available voice profiles.

        Returns:
            List of all voice profiles (empty list if none found)
        """
        profiles = []

        try:
            # Find all JSON files in profiles directory
            json_files = list(self.profiles_dir.glob("*.json"))
            logger.debug(f"Found {len(json_files)} profile files")

            for file_path in json_files:
                try:
                    # Read and deserialize each profile
                    with open(file_path, encoding="utf-8") as f:
                        data = json.load(f)

                    profile = JSONSerializer.deserialize(data)
                    profiles.append(profile)

                except (json.JSONDecodeError, ValueError, KeyError) as e:
                    # Skip invalid files but log the error
                    logger.warning(f"Skipping invalid profile file {file_path}: {e}")
                    continue

        except OSError as e:
            logger.error(f"Failed to list profiles: {e}")

        logger.info(f"Loaded {len(profiles)} profiles")
        return profiles

    def delete(self, profile_id: str) -> bool:
        """Delete a voice profile.

        Args:
            profile_id: Unique identifier of the profile to delete

        Returns:
            True if profile was deleted, False if not found
        """
        file_path = self._get_profile_path(profile_id)

        if not file_path.exists():
            logger.debug(f"Profile {profile_id} not found, cannot delete")
            return False

        try:
            file_path.unlink()
            logger.info(f"Deleted profile {profile_id} from {file_path}")
            return True

        except OSError as e:
            logger.error(f"Failed to delete profile {profile_id}: {e}")
            raise

    def exists(self, profile_id: str) -> bool:
        """Check if a profile exists.

        Args:
            profile_id: Profile identifier to check

        Returns:
            True if profile exists, False otherwise
        """
        return self._get_profile_path(profile_id).exists()

    def count(self) -> int:
        """Count total number of profiles.

        Returns:
            Number of profile files in directory
        """
        try:
            return len(list(self.profiles_dir.glob("*.json")))
        except OSError:
            return 0
