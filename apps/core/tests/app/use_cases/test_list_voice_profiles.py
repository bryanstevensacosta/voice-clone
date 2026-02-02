"""Tests for ListVoiceProfilesUseCase."""

from pathlib import Path
from unittest.mock import Mock

import pytest

from app.dto.voice_profile_dto import VoiceProfileDTO
from app.use_cases.list_voice_profiles import ListVoiceProfilesUseCase
from domain.models.audio_sample import AudioSample
from domain.models.voice_profile import VoiceProfile
from domain.ports.profile_repository import ProfileRepository


@pytest.fixture
def mock_profile_repository():
    """Create a mock profile repository."""
    repository = Mock(spec=ProfileRepository)
    return repository


@pytest.fixture
def use_case(mock_profile_repository):
    """Create the use case with mocked dependencies."""
    return ListVoiceProfilesUseCase(profile_repository=mock_profile_repository)


@pytest.fixture
def sample_profiles():
    """Create sample profiles for testing."""
    from datetime import datetime

    return [
        VoiceProfile(
            id="profile1",
            name="Profile 1",
            samples=[
                AudioSample(
                    path=Path("sample1.wav"),
                    duration=10.0,
                    sample_rate=12000,
                    channels=1,
                    bit_depth=16,
                    emotion="neutral",
                )
            ],
            created_at=datetime(2024, 1, 1, 0, 0, 0),
            language="es",
        ),
        VoiceProfile(
            id="profile2",
            name="Profile 2",
            samples=[
                AudioSample(
                    path=Path("sample2.wav"),
                    duration=15.0,
                    sample_rate=12000,
                    channels=1,
                    bit_depth=16,
                    emotion="happy",
                )
            ],
            created_at=datetime(2024, 1, 2, 0, 0, 0),
            language="en",
        ),
    ]


def test_list_voice_profiles_success(
    use_case, mock_profile_repository, sample_profiles
):
    """Test successful listing of voice profiles."""
    # Arrange
    mock_profile_repository.list_all.return_value = sample_profiles

    # Act
    result = use_case.execute()

    # Assert
    assert len(result) == 2
    assert all(isinstance(dto, VoiceProfileDTO) for dto in result)
    assert result[0].name == "Profile 1"
    assert result[1].name == "Profile 2"

    # Verify interaction
    mock_profile_repository.list_all.assert_called_once()


def test_list_voice_profiles_empty_repository(use_case, mock_profile_repository):
    """Test listing when repository is empty."""
    # Arrange
    mock_profile_repository.list_all.return_value = []

    # Act
    result = use_case.execute()

    # Assert
    assert result == []
    assert isinstance(result, list)


def test_list_voice_profiles_dto_conversion(
    use_case, mock_profile_repository, sample_profiles
):
    """Test that entities are correctly converted to DTOs."""
    # Arrange
    mock_profile_repository.list_all.return_value = sample_profiles

    # Act
    result = use_case.execute()

    # Assert - verify DTO fields
    dto1 = result[0]
    assert dto1.id == "profile1"
    assert dto1.name == "Profile 1"
    assert dto1.created_at == "2024-01-01T00:00:00"
    assert dto1.language == "es"
    assert len(dto1.samples) == 1
    assert dto1.total_duration == 10.0

    dto2 = result[1]
    assert dto2.id == "profile2"
    assert dto2.name == "Profile 2"
    assert dto2.language == "en"


def test_list_voice_profiles_preserves_order(
    use_case, mock_profile_repository, sample_profiles
):
    """Test that profile order is preserved."""
    # Arrange
    mock_profile_repository.list_all.return_value = sample_profiles

    # Act
    result = use_case.execute()

    # Assert
    assert result[0].id == "profile1"
    assert result[1].id == "profile2"


def test_list_voice_profiles_single_profile(
    use_case, mock_profile_repository, sample_profiles
):
    """Test listing with single profile."""
    # Arrange
    mock_profile_repository.list_all.return_value = [sample_profiles[0]]

    # Act
    result = use_case.execute()

    # Assert
    assert len(result) == 1
    assert result[0].id == "profile1"


def test_list_voice_profiles_multiple_samples(use_case, mock_profile_repository):
    """Test listing profile with multiple samples."""
    # Arrange
    from datetime import datetime

    profile = VoiceProfile(
        id="profile_multi",
        name="Multi Sample Profile",
        samples=[
            AudioSample(
                path=Path(f"sample{i}.wav"),
                duration=10.0,
                sample_rate=12000,
                channels=1,
                bit_depth=16,
                emotion="neutral",
            )
            for i in range(5)
        ],
        created_at=datetime(2024, 1, 1, 0, 0, 0),
        language="es",
    )
    mock_profile_repository.list_all.return_value = [profile]

    # Act
    result = use_case.execute()

    # Assert
    assert len(result) == 1
    assert len(result[0].samples) == 5
    assert result[0].total_duration == 50.0


def test_list_voice_profiles_exception_handling(use_case, mock_profile_repository):
    """Test handling of repository exceptions."""
    # Arrange
    mock_profile_repository.list_all.side_effect = RuntimeError("Repository error")

    # Act & Assert
    with pytest.raises(RuntimeError, match="Repository error"):
        use_case.execute()
