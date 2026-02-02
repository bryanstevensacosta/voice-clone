"""Tests for ProcessBatchUseCase."""

from pathlib import Path
from unittest.mock import Mock

import pytest

from app.dto.batch_dto import BatchRequestDTO, BatchResultDTO, BatchSegment
from app.use_cases.process_batch import ProcessBatchUseCase
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
    return ProcessBatchUseCase(
        tts_engine=mock_tts_engine,
        profile_repository=mock_profile_repository,
    )


def test_process_batch_success(use_case, mock_tts_engine):
    """Test successful batch processing."""
    # Arrange
    segments = [
        BatchSegment(id="seg1", text="Hello world"),
        BatchSegment(id="seg2", text="Goodbye world"),
    ]
    request = BatchRequestDTO(
        profile_id="test_profile",
        segments=segments,
        output_dir=Path("output"),
    )

    # Act
    result = use_case.execute(request)

    # Assert
    assert isinstance(result, BatchResultDTO)
    assert result.total_segments == 2
    assert result.successful_segments == 2
    assert result.failed_segments == 0
    assert len(result.results) == 2
    assert all(r.success for r in result.results)

    # Verify interactions
    assert mock_tts_engine.generate_audio.call_count == 2


def test_process_batch_partial_failure(use_case, mock_tts_engine):
    """Test batch processing with some failures."""
    # Arrange
    from domain.exceptions import GenerationException

    segments = [
        BatchSegment(id="seg1", text="Hello world"),
        BatchSegment(id="seg2", text="Goodbye world"),
        BatchSegment(id="seg3", text="Test"),
    ]
    request = BatchRequestDTO(
        profile_id="test_profile",
        segments=segments,
        output_dir=Path("output"),
    )

    # Mock: first and third succeed, second fails
    def generate_side_effect(*args, **kwargs):
        output_path = kwargs.get("output_path")
        if "seg2" in str(output_path):
            raise GenerationException("Generation failed")
        return output_path

    mock_tts_engine.generate_audio.side_effect = generate_side_effect

    # Act
    result = use_case.execute(request)

    # Assert
    assert result.total_segments == 3
    assert result.successful_segments == 2
    assert result.failed_segments == 1

    # Check individual results
    assert result.results[0].success is True
    assert result.results[1].success is False
    assert result.results[2].success is True


def test_process_batch_all_failures(use_case, mock_tts_engine):
    """Test batch processing when all segments fail."""
    # Arrange
    from domain.exceptions import GenerationException

    segments = [
        BatchSegment(id="seg1", text="Hello"),
        BatchSegment(id="seg2", text="World"),
    ]
    request = BatchRequestDTO(
        profile_id="test_profile",
        segments=segments,
        output_dir=Path("output"),
    )

    # Mock: all fail
    mock_tts_engine.generate_audio.side_effect = GenerationException(
        "Generation failed"
    )

    # Act
    result = use_case.execute(request)

    # Assert
    assert result.total_segments == 2
    assert result.successful_segments == 0
    assert result.failed_segments == 2
    assert all(not r.success for r in result.results)


def test_process_batch_empty_segments(use_case):
    """Test batch processing with no segments."""
    # Arrange
    request = BatchRequestDTO(
        profile_id="test_profile",
        segments=[],
        output_dir=Path("output"),
    )

    # Act
    result = use_case.execute(request)

    # Assert
    assert result.total_segments == 0
    assert result.successful_segments == 0
    assert result.failed_segments == 0
    assert len(result.results) == 0


def test_process_batch_single_segment(use_case, mock_tts_engine):
    """Test batch processing with single segment."""
    # Arrange
    segments = [
        BatchSegment(id="seg1", text="Hello world"),
    ]
    request = BatchRequestDTO(
        profile_id="test_profile",
        segments=segments,
        output_dir=Path("output"),
    )

    # Act
    result = use_case.execute(request)

    # Assert
    assert result.total_segments == 1
    assert result.successful_segments == 1
    assert mock_tts_engine.generate_audio.call_count == 1


def test_process_batch_with_parameters(use_case, mock_tts_engine):
    """Test batch processing with custom parameters."""
    # Arrange
    segments = [
        BatchSegment(id="seg1", text="Hello"),
    ]
    request = BatchRequestDTO(
        profile_id="test_profile",
        segments=segments,
        output_dir=Path("output"),
        temperature=0.8,
        speed=1.2,
        language="en",
        mode="custom",
    )

    # Act
    result = use_case.execute(request)

    # Assert
    assert result.successful_segments == 1

    # Verify parameters were passed
    call_kwargs = mock_tts_engine.generate_audio.call_args.kwargs
    assert call_kwargs["temperature"] == 0.8
    assert call_kwargs["speed"] == 1.2
    assert call_kwargs["language"] == "en"
    assert call_kwargs["mode"] == "custom"


def test_process_batch_output_paths(use_case, mock_tts_engine):
    """Test that output paths are correctly constructed."""
    # Arrange
    segments = [
        BatchSegment(id="seg1", text="Hello"),
        BatchSegment(id="seg2", text="World"),
    ]
    request = BatchRequestDTO(
        profile_id="test_profile",
        segments=segments,
        output_dir=Path("output"),
    )

    # Act
    use_case.execute(request)

    # Assert - verify output paths
    calls = mock_tts_engine.generate_audio.call_args_list

    call1_kwargs = calls[0].kwargs
    assert call1_kwargs["output_path"] == Path("output/seg1.wav")

    call2_kwargs = calls[1].kwargs
    assert call2_kwargs["output_path"] == Path("output/seg2.wav")


def test_process_batch_preserves_segment_order(use_case, mock_tts_engine):
    """Test that segment order is preserved in results."""
    # Arrange
    segments = [
        BatchSegment(id="seg1", text="First"),
        BatchSegment(id="seg2", text="Second"),
        BatchSegment(id="seg3", text="Third"),
    ]
    request = BatchRequestDTO(
        profile_id="test_profile",
        segments=segments,
        output_dir=Path("output"),
    )

    # Act
    result = use_case.execute(request)

    # Assert
    assert len(result.results) == 3
    # Results should be in same order as segments


def test_process_batch_exception_handling(use_case, mock_tts_engine):
    """Test handling of unexpected exceptions during batch processing."""
    # Arrange
    segments = [
        BatchSegment(id="seg1", text="Hello"),
        BatchSegment(id="seg2", text="World"),
    ]
    request = BatchRequestDTO(
        profile_id="test_profile",
        segments=segments,
        output_dir=Path("output"),
    )

    # Mock: first succeeds, second raises exception
    def generate_side_effect(*args, **kwargs):
        output_path = kwargs.get("output_path")
        if "seg2" in str(output_path):
            raise RuntimeError("Unexpected error")
        return output_path

    mock_tts_engine.generate_audio.side_effect = generate_side_effect

    # Act
    result = use_case.execute(request)

    # Assert - batch continues despite exception
    assert result.total_segments == 2
    assert result.successful_segments == 1
    assert result.failed_segments == 1
    assert result.results[0].success is True
    assert result.results[1].success is False
    assert "Unexpected error" in result.results[1].error


def test_batch_segment_dataclass():
    """Test BatchSegment dataclass."""
    # Arrange & Act
    segment = BatchSegment(
        id="seg1",
        text="Hello world",
    )

    # Assert
    assert segment.id == "seg1"
    assert segment.text == "Hello world"
