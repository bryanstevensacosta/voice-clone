"""Tests for FileProfileRepository.

Tests the file-based profile repository adapter with real file operations.
"""

import json
from datetime import datetime
from pathlib import Path

import pytest
from domain.models.audio_sample import AudioSample
from domain.models.voice_profile import VoiceProfile
from infra.persistence.file_profile_repository import FileProfileRepository


@pytest.fixture
def temp_profiles_dir(tmp_path):
    """Create a temporary directory for profile storage."""
    profiles_dir = tmp_path / "profiles"
    profiles_dir.mkdir()
    return profiles_dir


@pytest.fixture
def sample_audio_sample():
    """Create a sample AudioSample for testing."""
    return AudioSample(
        path=Path("test_sample.wav"),
        duration=10.0,
        sample_rate=12000,
        channels=1,
        bit_depth=16,
        emotion="neutral",
    )


@pytest.fixture
def sample_profile(sample_audio_sample):
    """Create a sample VoiceProfile for testing."""
    return VoiceProfile.create(
        name="test_profile",
        samples=[sample_audio_sample],
        language="es",
        reference_text="Test reference text",
    )


class TestFileProfileRepository:
    """Test suite for FileProfileRepository."""

    def test_init_creates_directory(self, tmp_path):
        """Test that repository creates profiles directory if it doesn't exist."""
        profiles_dir = tmp_path / "new_profiles"
        assert not profiles_dir.exists()

        FileProfileRepository(profiles_dir)

        assert profiles_dir.exists()
        assert profiles_dir.is_dir()

    def test_save_profile(self, temp_profiles_dir, sample_profile):
        """Test saving a profile to JSON file."""
        repo = FileProfileRepository(temp_profiles_dir)

        repo.save(sample_profile)

        # Check file was created
        profile_file = temp_profiles_dir / f"{sample_profile.id}.json"
        assert profile_file.exists()

        # Check file content
        with open(profile_file) as f:
            data = json.load(f)

        assert data["id"] == sample_profile.id
        assert data["name"] == sample_profile.name
        assert data["language"] == sample_profile.language
        assert len(data["samples"]) == 1

    def test_find_by_id_existing(self, temp_profiles_dir, sample_profile):
        """Test finding an existing profile by ID."""
        repo = FileProfileRepository(temp_profiles_dir)
        repo.save(sample_profile)

        found_profile = repo.find_by_id(sample_profile.id)

        assert found_profile is not None
        assert found_profile.id == sample_profile.id
        assert found_profile.name == sample_profile.name
        assert len(found_profile.samples) == 1

    def test_find_by_id_nonexistent(self, temp_profiles_dir):
        """Test finding a non-existent profile returns None."""
        repo = FileProfileRepository(temp_profiles_dir)

        found_profile = repo.find_by_id("nonexistent_id")

        assert found_profile is None

    def test_list_all_empty(self, temp_profiles_dir):
        """Test listing profiles when directory is empty."""
        repo = FileProfileRepository(temp_profiles_dir)

        profiles = repo.list_all()

        assert profiles == []

    def test_list_all_multiple_profiles(self, temp_profiles_dir, sample_audio_sample):
        """Test listing multiple profiles."""
        repo = FileProfileRepository(temp_profiles_dir)

        # Create and save multiple profiles
        profile1 = VoiceProfile.create(name="profile1", samples=[sample_audio_sample])
        profile2 = VoiceProfile.create(name="profile2", samples=[sample_audio_sample])

        repo.save(profile1)
        repo.save(profile2)

        profiles = repo.list_all()

        assert len(profiles) == 2
        profile_names = {p.name for p in profiles}
        assert profile_names == {"profile1", "profile2"}

    def test_delete_existing_profile(self, temp_profiles_dir, sample_profile):
        """Test deleting an existing profile."""
        repo = FileProfileRepository(temp_profiles_dir)
        repo.save(sample_profile)

        result = repo.delete(sample_profile.id)

        assert result is True
        assert repo.find_by_id(sample_profile.id) is None

    def test_delete_nonexistent_profile(self, temp_profiles_dir):
        """Test deleting a non-existent profile returns False."""
        repo = FileProfileRepository(temp_profiles_dir)

        result = repo.delete("nonexistent_id")

        assert result is False

    def test_exists(self, temp_profiles_dir, sample_profile):
        """Test checking if a profile exists."""
        repo = FileProfileRepository(temp_profiles_dir)

        assert not repo.exists(sample_profile.id)

        repo.save(sample_profile)

        assert repo.exists(sample_profile.id)

    def test_count(self, temp_profiles_dir, sample_audio_sample):
        """Test counting profiles."""
        repo = FileProfileRepository(temp_profiles_dir)

        assert repo.count() == 0

        profile1 = VoiceProfile.create(name="profile1", samples=[sample_audio_sample])
        profile2 = VoiceProfile.create(name="profile2", samples=[sample_audio_sample])

        repo.save(profile1)
        assert repo.count() == 1

        repo.save(profile2)
        assert repo.count() == 2

    def test_save_invalid_profile_raises_error(
        self, temp_profiles_dir, sample_audio_sample
    ):
        """Test that saving an invalid profile raises ValueError."""
        repo = FileProfileRepository(temp_profiles_dir)

        # Create invalid profile (no samples)
        invalid_profile = VoiceProfile(
            id="test_id",
            name="invalid",
            samples=[],  # Empty samples list is invalid
            created_at=datetime.now(),
        )

        with pytest.raises(ValueError, match="Cannot save invalid profile"):
            repo.save(invalid_profile)

    def test_roundtrip_preserves_data(self, temp_profiles_dir, sample_profile):
        """Test that save/load roundtrip preserves all profile data."""
        repo = FileProfileRepository(temp_profiles_dir)

        # Save profile
        repo.save(sample_profile)

        # Load profile
        loaded_profile = repo.find_by_id(sample_profile.id)

        # Verify all data is preserved
        assert loaded_profile.id == sample_profile.id
        assert loaded_profile.name == sample_profile.name
        assert loaded_profile.language == sample_profile.language
        assert loaded_profile.reference_text == sample_profile.reference_text
        assert len(loaded_profile.samples) == len(sample_profile.samples)

        # Verify sample data
        original_sample = sample_profile.samples[0]
        loaded_sample = loaded_profile.samples[0]
        assert loaded_sample.path == original_sample.path
        assert loaded_sample.duration == original_sample.duration
        assert loaded_sample.sample_rate == original_sample.sample_rate
        assert loaded_sample.channels == original_sample.channels
        assert loaded_sample.bit_depth == original_sample.bit_depth
        assert loaded_sample.emotion == original_sample.emotion
