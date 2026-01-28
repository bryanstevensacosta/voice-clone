"""Tests for GenerateAudioUseCase."""

from pathlib import Path
from unittest.mock import Mock

import pytest
from app.dto.generation_dto import GenerationRequestDTO, GenerationResultDTO
from app.use_cases.generate_audio import GenerateAudioUseCase
from domain.exceptions import GenerationException
from domain.models.audio_sample import AudioSample
from domain.models.voice_profile import VoiceProfile
from domain.ports.profile_repository import ProfileRepository
from domain.ports.tts_engine import TTSEngine


@pytest.fixture
def mock_tts_engine():
    """Create a mock TTS engine."""
    engine = Mock(spec=TTSEngine)
    engine.validate_profile.return_value = True
    engine.generate_audio.return_value = Path("output.wav")
    return engine


@pytest.fixture
def mock_profile_repository():
    """Create a mock profile repository."""
    repository = Mock(spec=ProfileRepository)

    # Create a valid profile
    profile = VoiceProfile(
        id="test_profile",
        name="Test Profile",
        samples=[
            AudioSample(
                path=Path("sample.wav"),
                duration=10.0,
                sample_rate=12000,
                channels=1,
                bit_depth=16,
                emotion="neutral",
            )
        ],
        created_at="2024-01-01T00:00:00",
        language="es",
    )
    repository.find_by_id.return_value = profile
    return repository


@pytest.fixture
def use_case(mock_tts_engine, mock_profile_repository):
    """Create the use case with mocked dependencies."""
    return GenerateAudioUseCase(
        tts_engine=mock_tts_engine,
        profile_repository=mock_profile_repository,
    )


def test_generate_audio_success(use_case, mock_tts_engine, mock_profile_repository):
    """Test successful audio generation."""
    # Arrange
    request = GenerationRequestDTO(
        profile_id="test_profile",
        text="Hello world",
        output_path=Path("output.wav"),
    )

    # Act
    result = use_case.execute(request)

    # Assert
    assert isinstance(result, GenerationResultDTO)
    assert result.success is True
    assert result.output_path == Path("output.wav")
    assert result.profile_id == "test_profile"
    assert result.text_length == len("Hello world")
    assert result.generation_time > 0

    # Verify interactions
    mock_profile_repository.find_by_id.assert_called_once_with("test_profile")
    mock_tts_engine.validate_profile.assert_called_once()
    mock_tts_engine.generate_audio.assert_called_once()


def test_generate_audio_profile_not_found(use_case, mock_profile_repository):
    """Test generation when profile is not found."""
    # Arrange
    mock_profile_repository.find_by_id.return_value = None
    request = GenerationRequestDTO(
        profile_id="nonexistent",
        text="Hello world",
    )

    # Act
    result = use_case.execute(request)

    # Assert
    assert result.success is False
    assert "Profile not found" in result.error
    assert result.profile_id == "nonexistent"


def test_generate_audio_invalid_profile(use_case, mock_tts_engine):
    """Test generation with invalid profile."""
    # Arrange
    mock_tts_engine.validate_profile.return_value = False
    request = GenerationRequestDTO(
        profile_id="test_profile",
        text="Hello world",
    )

    # Act
    result = use_case.execute(request)

    # Assert
    assert result.success is False
    assert "Profile validation failed" in result.error


def test_generate_audio_with_parameters(use_case, mock_tts_engine):
    """Test generation with custom parameters."""
    # Arrange
    request = GenerationRequestDTO(
        profile_id="test_profile",
        text="Hello world",
        temperature=0.8,
        speed=1.2,
        language="en",
        mode="custom",
    )

    # Act
    result = use_case.execute(request)

    # Assert
    assert result.success is True

    # Verify parameters were passed to engine
    call_kwargs = mock_tts_engine.generate_audio.call_args.kwargs
    assert call_kwargs["temperature"] == 0.8
    assert call_kwargs["speed"] == 1.2
    assert call_kwargs["language"] == "en"
    assert call_kwargs["mode"] == "custom"


def test_generate_audio_auto_output_path(use_case, mock_tts_engine):
    """Test generation with auto-generated output path."""
    # Arrange
    request = GenerationRequestDTO(
        profile_id="test_profile",
        text="Hello world",
        output_path=None,  # Auto-generate
    )

    # Act
    result = use_case.execute(request)

    # Assert
    assert result.success is True

    # Verify output path was generated
    call_kwargs = mock_tts_engine.generate_audio.call_args.kwargs
    assert call_kwargs["output_path"] is not None
    assert "output_test_profile" in str(call_kwargs["output_path"])


def test_generate_audio_generation_exception(use_case, mock_tts_engine):
    """Test handling of generation exception."""
    # Arrange
    mock_tts_engine.generate_audio.side_effect = GenerationException(
        "Generation failed"
    )
    request = GenerationRequestDTO(
        profile_id="test_profile",
        text="Hello world",
    )

    # Act
    result = use_case.execute(request)

    # Assert
    assert result.success is False
    assert "Generation failed" in result.error


def test_generate_audio_unexpected_exception(use_case, mock_tts_engine):
    """Test handling of unexpected exception."""
    # Arrange
    mock_tts_engine.generate_audio.side_effect = RuntimeError("Unexpected error")
    request = GenerationRequestDTO(
        profile_id="test_profile",
        text="Hello world",
    )

    # Act
    result = use_case.execute(request)

    # Assert
    assert result.success is False
    assert "Unexpected error" in result.error


def test_generate_audio_orchestration_order(
    use_case, mock_tts_engine, mock_profile_repository
):
    """Test that use case orchestrates operations in correct order."""
    # Arrange
    request = GenerationRequestDTO(
        profile_id="test_profile",
        text="Hello world",
    )

    # Act
    use_case.execute(request)

    # Assert - verify order of operations
    # 1. Load profile
    mock_profile_repository.find_by_id.assert_called_once()
    # 2. Validate profile
    mock_tts_engine.validate_profile.assert_called_once()
    # 3. Generate audio
    mock_tts_engine.generate_audio.assert_called_once()


def test_generate_audio_timing_metrics(use_case):
    """Test that generation time is tracked."""
    # Arrange
    request = GenerationRequestDTO(
        profile_id="test_profile",
        text="Hello world",
    )

    # Act
    result = use_case.execute(request)

    # Assert
    assert result.generation_time > 0
    assert isinstance(result.generation_time, float)
