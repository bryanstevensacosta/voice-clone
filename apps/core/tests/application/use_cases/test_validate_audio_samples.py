"""Tests for ValidateAudioSamplesUseCase."""

from pathlib import Path
from unittest.mock import Mock

import pytest
from app.use_cases.validate_audio_samples import (
    SampleValidationResult,
    ValidateAudioSamplesUseCase,
    ValidationSummary,
)
from domain.ports.audio_processor import AudioProcessor


@pytest.fixture
def mock_audio_processor():
    """Create a mock audio processor."""
    processor = Mock(spec=AudioProcessor)
    processor.validate_sample.return_value = True
    return processor


@pytest.fixture
def use_case(mock_audio_processor):
    """Create the use case with mocked dependencies."""
    return ValidateAudioSamplesUseCase(audio_processor=mock_audio_processor)


def test_validate_audio_samples_all_valid(use_case, mock_audio_processor):
    """Test validation when all samples are valid."""
    # Arrange
    from domain.models.audio_sample import AudioSample

    sample_paths = [Path("sample1.wav"), Path("sample2.wav"), Path("sample3.wav")]
    mock_audio_processor.validate_sample.return_value = True
    mock_audio_processor.process_sample.return_value = AudioSample(
        path=Path("test.wav"),
        duration=10.0,
        sample_rate=12000,
        channels=1,
        bit_depth=16,
    )

    # Act
    summary = use_case.execute(sample_paths)

    # Assert
    assert isinstance(summary, ValidationSummary)
    assert summary.total_samples == 3
    assert summary.valid_samples == 3
    assert summary.invalid_samples == 0
    assert summary.all_valid is True
    assert len(summary.results) == 3
    assert all(r.valid for r in summary.results)

    # Verify interactions
    assert mock_audio_processor.validate_sample.call_count == 3


def test_validate_audio_samples_some_invalid(use_case, mock_audio_processor):
    """Test validation when some samples are invalid."""
    # Arrange
    from domain.exceptions import InvalidSampleException
    from domain.models.audio_sample import AudioSample

    sample_paths = [Path("sample1.wav"), Path("sample2.wav"), Path("sample3.wav")]

    # Mock: first and third valid, second invalid
    def validate_side_effect(path):
        if path == Path("sample2.wav"):
            return False
        return True

    def process_side_effect(path):
        if path == Path("sample2.wav"):
            raise InvalidSampleException("Invalid sample")
        return AudioSample(
            path=path,
            duration=10.0,
            sample_rate=12000,
            channels=1,
            bit_depth=16,
        )

    mock_audio_processor.validate_sample.side_effect = validate_side_effect
    mock_audio_processor.process_sample.side_effect = process_side_effect

    # Act
    summary = use_case.execute(sample_paths)

    # Assert
    assert summary.total_samples == 3
    assert summary.valid_samples == 2
    assert summary.invalid_samples == 1
    assert summary.all_valid is False

    # Check individual results
    assert summary.results[0].valid is True
    assert summary.results[1].valid is False
    assert summary.results[2].valid is True


def test_validate_audio_samples_all_invalid(use_case, mock_audio_processor):
    """Test validation when all samples are invalid."""
    # Arrange
    sample_paths = [Path("sample1.wav"), Path("sample2.wav")]
    mock_audio_processor.validate_sample.return_value = False

    # Act
    summary = use_case.execute(sample_paths)

    # Assert
    assert summary.total_samples == 2
    assert summary.valid_samples == 0
    assert summary.invalid_samples == 2
    assert summary.all_valid is False
    assert all(not r.valid for r in summary.results)


def test_validate_audio_samples_empty_list(use_case):
    """Test validation with empty sample list."""
    # Arrange
    sample_paths = []

    # Act
    summary = use_case.execute(sample_paths)

    # Assert
    assert summary.total_samples == 0
    assert summary.valid_samples == 0
    assert summary.invalid_samples == 0
    assert summary.all_valid is True  # Vacuously true
    assert len(summary.results) == 0


def test_validate_audio_samples_single_sample(use_case, mock_audio_processor):
    """Test validation with single sample."""
    # Arrange
    from domain.models.audio_sample import AudioSample

    sample_paths = [Path("sample.wav")]
    mock_audio_processor.validate_sample.return_value = True
    mock_audio_processor.process_sample.return_value = AudioSample(
        path=Path("sample.wav"),
        duration=10.0,
        sample_rate=12000,
        channels=1,
        bit_depth=16,
    )

    # Act
    summary = use_case.execute(sample_paths)

    # Assert
    assert summary.total_samples == 1
    assert summary.valid_samples == 1
    assert summary.all_valid is True


def test_validate_audio_samples_result_details(use_case, mock_audio_processor):
    """Test that validation results contain correct details."""
    # Arrange
    from domain.models.audio_sample import AudioSample

    sample_paths = [Path("sample1.wav"), Path("sample2.wav")]

    def validate_side_effect(path):
        return path == Path("sample1.wav")

    def process_side_effect(path):
        if path == Path("sample1.wav"):
            return AudioSample(
                path=path,
                duration=10.0,
                sample_rate=12000,
                channels=1,
                bit_depth=16,
            )
        raise ValueError("Invalid sample")

    mock_audio_processor.validate_sample.side_effect = validate_side_effect
    mock_audio_processor.process_sample.side_effect = process_side_effect

    # Act
    summary = use_case.execute(sample_paths)

    # Assert - check result details
    result1 = summary.results[0]
    assert result1.path == Path("sample1.wav")
    assert result1.valid is True
    assert result1.error is None

    result2 = summary.results[1]
    assert result2.path == Path("sample2.wav")
    assert result2.valid is False
    assert result2.error is not None


def test_validate_audio_samples_exception_handling(use_case, mock_audio_processor):
    """Test handling of validation exceptions."""
    # Arrange
    from domain.models.audio_sample import AudioSample

    sample_paths = [Path("sample1.wav"), Path("sample2.wav")]

    def validate_side_effect(path):
        return True

    def process_side_effect(path):
        if path == Path("sample1.wav"):
            return AudioSample(
                path=path,
                duration=10.0,
                sample_rate=12000,
                channels=1,
                bit_depth=16,
            )
        raise RuntimeError("Validation error")

    mock_audio_processor.validate_sample.side_effect = validate_side_effect
    mock_audio_processor.process_sample.side_effect = process_side_effect

    # Act
    summary = use_case.execute(sample_paths)

    # Assert - first sample valid, second has error
    assert summary.total_samples == 2
    assert summary.valid_samples == 1
    assert summary.invalid_samples == 1

    result2 = summary.results[1]
    assert result2.valid is False
    assert "Validation error" in result2.error


def test_validate_audio_samples_preserves_order(use_case, mock_audio_processor):
    """Test that sample order is preserved in results."""
    # Arrange
    from domain.models.audio_sample import AudioSample

    sample_paths = [
        Path("sample1.wav"),
        Path("sample2.wav"),
        Path("sample3.wav"),
    ]
    mock_audio_processor.validate_sample.return_value = True

    def process_side_effect(path):
        return AudioSample(
            path=path,
            duration=10.0,
            sample_rate=12000,
            channels=1,
            bit_depth=16,
        )

    mock_audio_processor.process_sample.side_effect = process_side_effect

    # Act
    summary = use_case.execute(sample_paths)

    # Assert
    assert summary.results[0].path == Path("sample1.wav")
    assert summary.results[1].path == Path("sample2.wav")
    assert summary.results[2].path == Path("sample3.wav")


def test_sample_validation_result_dataclass():
    """Test SampleValidationResult dataclass."""
    # Arrange & Act
    result = SampleValidationResult(
        path=Path("test.wav"),
        valid=True,
        error=None,
    )

    # Assert
    assert result.path == Path("test.wav")
    assert result.valid is True
    assert result.error is None


def test_validation_summary_dataclass():
    """Test ValidationSummary dataclass."""
    # Arrange
    results = [
        SampleValidationResult(Path("sample1.wav"), True, None),
        SampleValidationResult(Path("sample2.wav"), False, "Error"),
    ]

    # Act
    summary = ValidationSummary(
        total_samples=2,
        valid_samples=1,
        invalid_samples=1,
        results=results,
        total_duration=10.0,
    )

    # Assert
    assert summary.total_samples == 2
    assert summary.valid_samples == 1
    assert summary.invalid_samples == 1
    assert summary.all_valid is False
    assert len(summary.results) == 2
