"""Unit tests for VoiceProfile entity."""

from datetime import datetime
from pathlib import Path

import pytest

from domain.models.audio_sample import AudioSample
from domain.models.voice_profile import VoiceProfile


@pytest.fixture
def valid_sample():
    """Create a valid audio sample for testing."""
    return AudioSample(
        path=Path("test_sample.wav"),
        duration=10.0,
        sample_rate=12000,
        channels=1,
        bit_depth=16,
        emotion="neutral",
    )


@pytest.fixture
def valid_samples():
    """Create a list of valid audio samples for testing."""
    return [
        AudioSample(
            path=Path("sample1.wav"),
            duration=10.0,
            sample_rate=12000,
            channels=1,
            bit_depth=16,
            emotion="neutral",
        ),
        AudioSample(
            path=Path("sample2.wav"),
            duration=15.0,
            sample_rate=12000,
            channels=1,
            bit_depth=16,
            emotion="happy",
        ),
    ]


class TestVoiceProfileCreation:
    """Test voice profile creation."""

    def test_create_valid_profile(self, valid_samples):
        """Test creating a valid voice profile."""
        profile = VoiceProfile.create(
            name="test_profile", samples=valid_samples, language="es"
        )

        assert profile.id is not None
        assert profile.name == "test_profile"
        assert len(profile.samples) == 2
        assert profile.language == "es"
        assert isinstance(profile.created_at, datetime)

    def test_create_profile_generates_unique_ids(self, valid_samples):
        """Test that each profile gets a unique ID."""
        profile1 = VoiceProfile.create(name="profile1", samples=valid_samples)
        profile2 = VoiceProfile.create(name="profile2", samples=valid_samples)

        assert profile1.id != profile2.id

    def test_create_profile_with_reference_text(self, valid_samples):
        """Test creating profile with reference text."""
        profile = VoiceProfile.create(
            name="test_profile",
            samples=valid_samples,
            reference_text="This is a test",
        )

        assert profile.reference_text == "This is a test"

    def test_create_profile_with_empty_name_fails(self, valid_samples):
        """Test that creating profile with empty name fails."""
        with pytest.raises(ValueError, match="Profile name cannot be empty"):
            VoiceProfile.create(name="", samples=valid_samples)

    def test_create_profile_with_no_samples_fails(self):
        """Test that creating profile with no samples fails."""
        with pytest.raises(ValueError, match="at least 1 audio sample"):
            VoiceProfile.create(name="test_profile", samples=[])


class TestVoiceProfileValidation:
    """Test voice profile validation."""

    def test_valid_profile_is_valid(self, valid_samples):
        """Test that a valid profile passes validation."""
        profile = VoiceProfile.create(name="test_profile", samples=valid_samples)

        assert profile.is_valid()
        assert len(profile.validation_errors()) == 0

    def test_profile_with_too_few_samples_invalid(self):
        """Test that profile with 0 samples is invalid."""
        # Create profile directly (bypass factory validation)
        profile = VoiceProfile(
            id="test-id",
            name="test_profile",
            samples=[],
            created_at=datetime.now(),
        )

        assert not profile.is_valid()
        assert any("at least 1" in err for err in profile.validation_errors())

    def test_profile_with_too_many_samples_invalid(self, valid_sample):
        """Test that profile with >10 samples is invalid."""
        # Create 11 samples
        samples = [valid_sample] * 11

        profile = VoiceProfile(
            id="test-id",
            name="test_profile",
            samples=samples,
            created_at=datetime.now(),
        )

        assert not profile.is_valid()
        assert any("Maximum is 10" in err for err in profile.validation_errors())

    def test_profile_with_short_duration_invalid(self):
        """Test that profile with <10s total duration is invalid."""
        short_sample = AudioSample(
            path=Path("short.wav"),
            duration=5.0,
            sample_rate=12000,
            channels=1,
            bit_depth=16,
        )

        profile = VoiceProfile(
            id="test-id",
            name="test_profile",
            samples=[short_sample],
            created_at=datetime.now(),
        )

        assert not profile.is_valid()
        assert any(
            "Minimum is 10 seconds" in err for err in profile.validation_errors()
        )

    def test_profile_with_long_duration_invalid(self):
        """Test that profile with >300s total duration is invalid."""
        # Create samples totaling >300s
        long_samples = [
            AudioSample(
                path=Path(f"sample{i}.wav"),
                duration=30.0,
                sample_rate=12000,
                channels=1,
                bit_depth=16,
            )
            for i in range(11)  # 11 * 30 = 330s
        ]

        profile = VoiceProfile(
            id="test-id",
            name="test_profile",
            samples=long_samples,
            created_at=datetime.now(),
        )

        assert not profile.is_valid()
        # Should fail both max samples and max duration
        errors = profile.validation_errors()
        assert any("Maximum is 300 seconds" in err for err in errors)


class TestVoiceProfileMethods:
    """Test voice profile methods."""

    def test_total_duration_calculation(self, valid_samples):
        """Test that total_duration is calculated correctly."""
        profile = VoiceProfile.create(name="test_profile", samples=valid_samples)

        # 10.0 + 15.0 = 25.0
        assert profile.total_duration == 25.0

    def test_add_sample_success(self, valid_samples, valid_sample):
        """Test adding a sample to profile."""
        profile = VoiceProfile.create(name="test_profile", samples=valid_samples)
        initial_count = len(profile.samples)

        profile.add_sample(valid_sample)

        assert len(profile.samples) == initial_count + 1
        assert valid_sample in profile.samples

    def test_add_sample_exceeding_max_fails(self, valid_sample):
        """Test that adding sample when at max fails."""
        # Create profile with 10 samples (max)
        samples = [valid_sample] * 10
        profile = VoiceProfile(
            id="test-id",
            name="test_profile",
            samples=samples,
            created_at=datetime.now(),
        )

        with pytest.raises(ValueError, match="Maximum 10 samples"):
            profile.add_sample(valid_sample)

    def test_remove_sample_success(self, valid_samples):
        """Test removing a sample from profile."""
        profile = VoiceProfile.create(name="test_profile", samples=valid_samples)
        sample_to_remove = valid_samples[0]

        result = profile.remove_sample(sample_to_remove.path)

        assert result is True
        assert sample_to_remove not in profile.samples
        assert len(profile.samples) == 1

    def test_remove_sample_not_found(self, valid_samples):
        """Test removing a sample that doesn't exist."""
        profile = VoiceProfile.create(name="test_profile", samples=valid_samples)

        result = profile.remove_sample(Path("nonexistent.wav"))

        assert result is False
        assert len(profile.samples) == 2

    def test_remove_last_sample_fails(self, valid_sample):
        """Test that removing the last sample fails."""
        profile = VoiceProfile.create(name="test_profile", samples=[valid_sample])

        with pytest.raises(ValueError, match="at least 1 sample"):
            profile.remove_sample(valid_sample.path)

    def test_str_representation(self, valid_samples):
        """Test string representation of profile."""
        profile = VoiceProfile.create(name="test_profile", samples=valid_samples)

        str_repr = str(profile)

        assert "VoiceProfile" in str_repr
        assert "test_profile" in str_repr
        assert "samples=2" in str_repr
        assert "25.0s" in str_repr
