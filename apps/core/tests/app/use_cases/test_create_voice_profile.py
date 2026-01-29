"""Tests for CreateVoiceProfileUseCase."""

from pathlib import Path
from unittest.mock import Mock

import pytest
from app.dto.voice_profile_dto import VoiceProfileDTO
from app.use_cases.create_voice_profile import CreateVoiceProfileUseCase
from domain.models.audio_sample import AudioSample
from domain.ports.audio_processor import AudioProcessor
from domain.ports.profile_repository import ProfileRepository


@pytest.fixture
def mock_audio_processor():
    """Create a mock audio processor."""
    processor = Mock(spec=AudioProcessor)
    processor.validate_sample.return_value = True
    processor.process_sample.return_value = AudioSample(
        path=Path("test.wav"),
        duration=10.0,
        sample_rate=12000,
        channels=1,
        bit_depth=16,
        emotion="neutral",
    )
    return processor


@pytest.fixture
def mock_profile_repository():
    """Create a mock profile repository."""
    repository = Mock(spec=ProfileRepository)
    repository.save.return_value = None
    return repository


@pytest.fixture
def use_case(mock_audio_processor, mock_profile_repository):
    """Create the use case with mocked dependencies."""
    return CreateVoiceProfileUseCase(
        audio_processor=mock_audio_processor,
        profile_repository=mock_profile_repository,
    )


def test_create_voice_profile_success(
    use_case, mock_audio_processor, mock_profile_repository
):
    """Test successful voice profile creation."""
    # Arrange
    name = "test_profile"
    sample_paths = [Path("sample1.wav"), Path("sample2.wav")]

    # Act
    result = use_case.execute(name, sample_paths)

    # Assert
    assert isinstance(result, VoiceProfileDTO)
    assert result.name == name
    assert len(result.samples) == 2
    assert result.total_duration == 20.0  # 2 samples * 10s each

    # Verify interactions
    assert mock_audio_processor.validate_sample.call_count == 2
    assert mock_audio_processor.process_sample.call_count == 2
    mock_profile_repository.save.assert_called_once()


def test_create_voice_profile_with_reference_text(
    use_case, mock_audio_processor, mock_profile_repository
):
    """Test profile creation with reference text."""
    # Arrange
    name = "test_profile"
    sample_paths = [Path("sample1.wav")]
    reference_text = "This is a test reference"

    # Act
    result = use_case.execute(name, sample_paths, reference_text=reference_text)

    # Assert
    assert result.reference_text == reference_text


def test_create_voice_profile_invalid_sample(use_case, mock_audio_processor):
    """Test profile creation with invalid sample."""
    # Arrange
    name = "test_profile"
    sample_paths = [Path("invalid.wav")]
    mock_audio_processor.validate_sample.return_value = False

    # Act & Assert
    with pytest.raises(ValueError, match="Invalid sample"):
        use_case.execute(name, sample_paths)


def test_create_voice_profile_empty_samples(use_case):
    """Test profile creation with no samples."""
    # Arrange
    name = "test_profile"
    sample_paths = []

    # Act & Assert
    with pytest.raises(ValueError, match="Profile must have at least 1 audio sample"):
        use_case.execute(name, sample_paths)


def test_create_voice_profile_empty_name(use_case):
    """Test profile creation with empty name."""
    # Arrange
    name = ""
    sample_paths = [Path("sample1.wav")]

    # Act & Assert
    with pytest.raises(ValueError, match="Profile name cannot be empty"):
        use_case.execute(name, sample_paths)


def test_create_voice_profile_orchestration(
    use_case, mock_audio_processor, mock_profile_repository
):
    """Test that use case orchestrates domain service and repository correctly."""
    # Arrange
    name = "test_profile"
    sample_paths = [Path("sample1.wav")]

    # Act
    result = use_case.execute(name, sample_paths)

    # Assert - verify orchestration order
    # 1. Validate samples
    mock_audio_processor.validate_sample.assert_called()
    # 2. Process samples
    mock_audio_processor.process_sample.assert_called()
    # 3. Save profile
    mock_profile_repository.save.assert_called_once()
    # 4. Return DTO
    assert isinstance(result, VoiceProfileDTO)


def test_create_voice_profile_dto_conversion(
    use_case, mock_audio_processor, mock_profile_repository
):
    """Test that entity is correctly converted to DTO."""
    # Arrange
    name = "test_profile"
    sample_paths = [Path("sample1.wav")]

    # Act
    result = use_case.execute(name, sample_paths)

    # Assert - verify DTO fields
    assert result.name == name
    assert result.id is not None
    assert result.created_at is not None
    assert isinstance(result.samples, list)
    assert result.total_duration > 0
    assert result.language == "es"


def test_create_voice_profile_multiple_samples(
    use_case, mock_audio_processor, mock_profile_repository
):
    """Test profile creation with multiple samples."""
    # Arrange
    name = "test_profile"
    sample_paths = [Path(f"sample{i}.wav") for i in range(5)]

    # Act
    result = use_case.execute(name, sample_paths)

    # Assert
    assert len(result.samples) == 5
    assert result.total_duration == 50.0  # 5 samples * 10s each
    assert mock_audio_processor.validate_sample.call_count == 5
    assert mock_audio_processor.process_sample.call_count == 5
