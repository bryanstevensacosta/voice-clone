"""Unit tests for VoiceCloningService."""

from pathlib import Path
from unittest.mock import Mock

import pytest

from domain.models.audio_sample import AudioSample
from domain.models.voice_profile import VoiceProfile
from domain.ports.audio_processor import AudioProcessor
from domain.services.voice_cloning import VoiceCloningService


@pytest.fixture
def mock_audio_processor():
    """Create a mock audio processor."""
    return Mock(spec=AudioProcessor)


@pytest.fixture
def valid_audio_sample():
    """Create a valid audio sample."""
    return AudioSample(
        path=Path("test_sample.wav"),
        duration=10.0,
        sample_rate=12000,
        channels=1,
        bit_depth=16,
        emotion="neutral",
    )


@pytest.fixture
def voice_cloning_service(mock_audio_processor):
    """Create a voice cloning service with mocked dependencies."""
    return VoiceCloningService(audio_processor=mock_audio_processor)


class TestCreateProfileFromSamples:
    """Test create_profile_from_samples method."""

    def test_create_profile_success(
        self, voice_cloning_service, mock_audio_processor, valid_audio_sample
    ):
        """Test successful profile creation."""
        # Setup mocks
        sample_paths = [Path("sample1.wav"), Path("sample2.wav")]
        mock_audio_processor.validate_sample.return_value = True
        mock_audio_processor.process_sample.return_value = valid_audio_sample

        # Execute
        profile = voice_cloning_service.create_profile_from_samples(
            name="test_profile", sample_paths=sample_paths
        )

        # Verify
        assert isinstance(profile, VoiceProfile)
        assert profile.name == "test_profile"
        assert len(profile.samples) == 2
        assert profile.language == "es"

        # Verify mocks were called correctly
        assert mock_audio_processor.validate_sample.call_count == 2
        assert mock_audio_processor.process_sample.call_count == 2

    def test_create_profile_with_custom_language(
        self, voice_cloning_service, mock_audio_processor, valid_audio_sample
    ):
        """Test profile creation with custom language."""
        sample_paths = [Path("sample1.wav")]
        mock_audio_processor.validate_sample.return_value = True
        mock_audio_processor.process_sample.return_value = valid_audio_sample

        profile = voice_cloning_service.create_profile_from_samples(
            name="test_profile", sample_paths=sample_paths, language="en"
        )

        assert profile.language == "en"

    def test_create_profile_with_reference_text(
        self, voice_cloning_service, mock_audio_processor, valid_audio_sample
    ):
        """Test profile creation with reference text."""
        sample_paths = [Path("sample1.wav")]
        mock_audio_processor.validate_sample.return_value = True
        mock_audio_processor.process_sample.return_value = valid_audio_sample

        profile = voice_cloning_service.create_profile_from_samples(
            name="test_profile",
            sample_paths=sample_paths,
            reference_text="Test reference",
        )

        assert profile.reference_text == "Test reference"

    def test_create_profile_invalid_sample_fails(
        self, voice_cloning_service, mock_audio_processor
    ):
        """Test that invalid sample causes failure."""
        sample_paths = [Path("invalid_sample.wav")]
        mock_audio_processor.validate_sample.return_value = False

        with pytest.raises(ValueError, match="Invalid sample"):
            voice_cloning_service.create_profile_from_samples(
                name="test_profile", sample_paths=sample_paths
            )

        # Verify validation was called but processing was not
        mock_audio_processor.validate_sample.assert_called_once()
        mock_audio_processor.process_sample.assert_not_called()

    def test_create_profile_validates_all_samples_before_processing(
        self, voice_cloning_service, mock_audio_processor, valid_audio_sample
    ):
        """Test that all samples are validated before any processing."""
        sample_paths = [Path("sample1.wav"), Path("sample2.wav"), Path("sample3.wav")]

        # First two samples valid, third invalid
        mock_audio_processor.validate_sample.side_effect = [True, True, False]

        with pytest.raises(ValueError, match="Invalid sample"):
            voice_cloning_service.create_profile_from_samples(
                name="test_profile", sample_paths=sample_paths
            )

        # Verify all validations were attempted
        assert mock_audio_processor.validate_sample.call_count == 3
        # But no processing happened
        mock_audio_processor.process_sample.assert_not_called()

    def test_create_profile_with_empty_name_fails(
        self, voice_cloning_service, mock_audio_processor, valid_audio_sample
    ):
        """Test that empty profile name fails."""
        sample_paths = [Path("sample1.wav")]
        mock_audio_processor.validate_sample.return_value = True
        mock_audio_processor.process_sample.return_value = valid_audio_sample

        with pytest.raises(ValueError, match="Profile name cannot be empty"):
            voice_cloning_service.create_profile_from_samples(
                name="", sample_paths=sample_paths
            )

    def test_create_profile_with_no_samples_fails(
        self, voice_cloning_service, mock_audio_processor
    ):
        """Test that no samples fails."""
        with pytest.raises(ValueError, match="at least 1 audio sample"):
            voice_cloning_service.create_profile_from_samples(
                name="test_profile", sample_paths=[]
            )


class TestValidateProfileForCloning:
    """Test validate_profile_for_cloning method."""

    def test_valid_profile_passes_validation(self, voice_cloning_service):
        """Test that a valid profile passes validation."""
        # Create a valid profile with 2 samples, 25s total
        samples = [
            AudioSample(
                path=Path("sample1.wav"),
                duration=10.0,
                sample_rate=12000,
                channels=1,
                bit_depth=16,
            ),
            AudioSample(
                path=Path("sample2.wav"),
                duration=15.0,
                sample_rate=12000,
                channels=1,
                bit_depth=16,
            ),
        ]
        profile = VoiceProfile.create(name="test_profile", samples=samples)

        result = voice_cloning_service.validate_profile_for_cloning(profile)

        assert result is True

    def test_profile_with_one_sample_fails(self, voice_cloning_service):
        """Test that profile with only 1 sample fails validation."""
        sample = AudioSample(
            path=Path("sample1.wav"),
            duration=20.0,
            sample_rate=12000,
            channels=1,
            bit_depth=16,
        )
        profile = VoiceProfile.create(name="test_profile", samples=[sample])

        result = voice_cloning_service.validate_profile_for_cloning(profile)

        assert result is False

    def test_profile_with_short_duration_fails(self, voice_cloning_service):
        """Test that profile with <20s total duration fails."""
        # Create 2 samples with 15s total (7.5s each)
        samples = [
            AudioSample(
                path=Path("sample1.wav"),
                duration=7.5,
                sample_rate=12000,
                channels=1,
                bit_depth=16,
            ),
            AudioSample(
                path=Path("sample2.wav"),
                duration=7.5,
                sample_rate=12000,
                channels=1,
                bit_depth=16,
            ),
        ]
        profile = VoiceProfile.create(name="test_profile", samples=samples)

        result = voice_cloning_service.validate_profile_for_cloning(profile)

        assert result is False

    def test_invalid_profile_fails(self, voice_cloning_service):
        """Test that an invalid profile fails validation."""
        # Create an invalid profile (empty samples)
        from datetime import datetime

        profile = VoiceProfile(
            id="test-id",
            name="test_profile",
            samples=[],
            created_at=datetime.now(),
        )

        result = voice_cloning_service.validate_profile_for_cloning(profile)

        assert result is False


class TestVoiceCloningServiceDependencies:
    """Test service dependencies and initialization."""

    def test_service_requires_audio_processor(self):
        """Test that service requires audio processor."""
        mock_processor = Mock(spec=AudioProcessor)
        service = VoiceCloningService(audio_processor=mock_processor)

        assert service._audio_processor is mock_processor

    def test_service_uses_injected_audio_processor(
        self, voice_cloning_service, mock_audio_processor, valid_audio_sample
    ):
        """Test that service uses the injected audio processor."""
        sample_paths = [Path("sample1.wav")]
        mock_audio_processor.validate_sample.return_value = True
        mock_audio_processor.process_sample.return_value = valid_audio_sample

        voice_cloning_service.create_profile_from_samples(
            name="test_profile", sample_paths=sample_paths
        )

        # Verify the injected processor was used
        mock_audio_processor.validate_sample.assert_called_once_with(sample_paths[0])
        mock_audio_processor.process_sample.assert_called_once_with(sample_paths[0])
