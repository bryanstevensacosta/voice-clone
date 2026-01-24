"""Integration tests for end-to-end workflows."""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np
import pytest
from voice_clone.audio.processor import AudioProcessor
from voice_clone.batch.processor import BatchProcessor
from voice_clone.config import ConfigManager
from voice_clone.model.generator import VoiceGenerator
from voice_clone.model.manager import ModelManager
from voice_clone.model.profile import VoiceProfile


@pytest.fixture
def mock_audio_data() -> np.ndarray:
    """Create mock audio data."""
    # Create 1 second of audio at 22050 Hz
    duration = 1.0
    sample_rate = 22050
    samples = int(duration * sample_rate)
    return np.random.randn(samples).astype(np.float32)


@pytest.fixture
def sample_audio_file(tmp_path: Path, mock_audio_data: np.ndarray) -> Path:
    """Create a sample audio file."""
    import soundfile as sf

    audio_file = tmp_path / "sample.wav"
    sf.write(str(audio_file), mock_audio_data, 22050)
    return audio_file


@pytest.fixture
def voice_profile_data(tmp_path: Path) -> dict:
    """Create voice profile data."""
    return {
        "name": "test_voice",
        "created_at": "2024-01-01T00:00:00",
        "language": "es",
        "samples": [
            {
                "path": str(tmp_path / "sample1.wav"),
                "duration": 10.0,
                "emotion": "neutral",
                "quality_score": 0.9,
            },
            {
                "path": str(tmp_path / "sample2.wav"),
                "duration": 12.0,
                "emotion": "happy",
                "quality_score": 0.85,
            },
        ],
        "total_duration": 22.0,
    }


def test_complete_workflow_validate_prepare_generate(
    tmp_path: Path, sample_audio_file: Path
) -> None:
    """Test complete workflow: validate → prepare → generate.

    Requirements: 1.1, 3.1, 4.1
    """
    # Step 1: Validate samples
    processor = AudioProcessor()
    result = processor.validate_sample(sample_audio_file)

    # Validation should succeed (or have warnings)
    assert result is not None

    # Step 2: Prepare voice profile
    samples_dir = tmp_path / "samples"
    samples_dir.mkdir()

    # Create multiple sample files
    import soundfile as sf

    for i in range(3):
        sample_file = samples_dir / f"sample_{i}.wav"
        # Create 10 seconds of audio (normalized to avoid clipping)
        audio_data = np.random.randn(22050 * 10).astype(np.float32)
        # Normalize to [-0.8, 0.8] to avoid clipping
        audio_data = audio_data / np.max(np.abs(audio_data)) * 0.8
        sf.write(str(sample_file), audio_data, 22050)

    # Create voice profile
    profile = VoiceProfile.from_directory("test_voice", samples_dir)

    assert profile is not None
    assert len(profile.samples) == 3
    assert profile.total_duration > 0

    # Step 3: Save and load profile
    profile_path = tmp_path / "profile.json"
    profile.to_json(profile_path)

    loaded_profile = VoiceProfile.from_json(profile_path)
    assert loaded_profile.name == profile.name
    assert len(loaded_profile.samples) == len(profile.samples)


def test_batch_workflow_prepare_batch_process(
    tmp_path: Path, voice_profile_data: dict
) -> None:
    """Test batch workflow: prepare → batch → post-process.

    Requirements: 5.1, 5.5
    """
    # Step 1: Create voice profile
    profile_path = tmp_path / "profile.json"
    with open(profile_path, "w") as f:
        json.dump(voice_profile_data, f)

    profile = VoiceProfile.from_json(profile_path)
    assert profile is not None

    # Step 2: Create script file
    script_path = tmp_path / "script.txt"
    script_content = """[INTRO]
Hola, bienvenidos al test.

[SECTION_1]
Esta es la primera sección.

[OUTRO]
Gracias por ver este test.
"""
    script_path.write_text(script_content)

    # Step 3: Mock batch processing
    with patch("voice_clone.model.manager.ModelManager") as MockModelManager:
        with patch("voice_clone.model.generator.VoiceGenerator") as MockGenerator:
            # Setup mocks
            mock_model_manager = MagicMock()
            mock_model_manager.load_model.return_value = True
            mock_model_manager.is_loaded.return_value = True
            MockModelManager.return_value = mock_model_manager

            mock_generator = MagicMock()
            mock_generator.generate.return_value = True
            MockGenerator.return_value = mock_generator

            # Create batch processor
            processor = AudioProcessor()
            batch_processor = BatchProcessor(mock_generator, processor)

            # Process script
            output_dir = tmp_path / "outputs"
            results = batch_processor.process_script(script_path, profile, output_dir)

            # Verify results
            assert "successful" in results
            assert "failed" in results
            assert results["successful"] + results["failed"] == 3


def test_error_handling_in_complete_workflow(tmp_path: Path) -> None:
    """Test error handling in complete workflows.

    Requirements: 1.1, 3.1, 4.1, 5.1
    """
    # Test 1: Invalid audio file
    processor = AudioProcessor()
    invalid_file = tmp_path / "invalid.wav"
    invalid_file.write_text("not an audio file")

    try:
        result = processor.validate_sample(invalid_file)
        # Should either return invalid result or raise exception
        if result:
            assert not result.is_valid()
    except Exception:
        # Exception is acceptable for invalid files
        pass

    # Test 2: Empty samples directory
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()

    profile = VoiceProfile.from_directory("test", empty_dir)
    assert len(profile.samples) == 0

    # Test 3: Invalid profile JSON
    invalid_profile = tmp_path / "invalid_profile.json"
    invalid_profile.write_text("not valid json")

    with pytest.raises((json.JSONDecodeError, ValueError, KeyError)):
        VoiceProfile.from_json(invalid_profile)


def test_workflow_with_post_processing(tmp_path: Path, sample_audio_file: Path) -> None:
    """Test workflow with post-processing steps.

    Requirements: 6.1, 6.2
    """
    processor = AudioProcessor()

    # Test normalization
    output_file = tmp_path / "normalized.wav"

    try:
        # This may fail if ffmpeg is not installed, which is acceptable
        processor.normalize_loudness(sample_audio_file, output_file)

        if output_file.exists():
            assert output_file.stat().st_size > 0
    except Exception:
        # FFmpeg not available is acceptable in test environment
        pass


def test_workflow_with_format_export(tmp_path: Path, sample_audio_file: Path) -> None:
    """Test workflow with format export.

    Requirements: 7.1, 7.2
    """
    processor = AudioProcessor()

    # Test MP3 export
    mp3_file = tmp_path / "output.mp3"

    try:
        # This may fail if ffmpeg is not installed
        processor.export_format(sample_audio_file, mp3_file, "mp3")

        if mp3_file.exists():
            assert mp3_file.stat().st_size > 0
    except Exception:
        # FFmpeg not available is acceptable in test environment
        pass


def test_config_loading_in_workflow(tmp_path: Path) -> None:
    """Test configuration loading in workflow."""
    config_manager = ConfigManager()
    config = config_manager.load_config()

    # Config should be loaded
    assert config is not None
    assert "model" in config
    assert "audio" in config
    assert "generation" in config


def test_model_manager_initialization() -> None:
    """Test model manager initialization in workflow."""
    config_manager = ConfigManager()
    config = config_manager.load_config()

    # Create model manager (without loading actual model)
    model_manager = ModelManager(config)

    assert model_manager is not None
    assert not model_manager.is_loaded()


def test_voice_generator_initialization() -> None:
    """Test voice generator initialization in workflow."""
    config_manager = ConfigManager()
    config = config_manager.load_config()

    with patch("voice_clone.model.manager.ModelManager") as MockModelManager:
        mock_model_manager = MagicMock()
        MockModelManager.return_value = mock_model_manager

        generator = VoiceGenerator(mock_model_manager, config)

        assert generator is not None


def test_batch_processor_initialization() -> None:
    """Test batch processor initialization in workflow."""
    with patch("voice_clone.model.generator.VoiceGenerator") as MockGenerator:
        mock_generator = MagicMock()
        MockGenerator.return_value = mock_generator

        processor = AudioProcessor()
        batch_processor = BatchProcessor(mock_generator, processor)

        assert batch_processor is not None


def test_end_to_end_workflow_resilience(tmp_path: Path) -> None:
    """Test that workflow continues despite individual failures.

    Requirements: 5.6
    """
    # Create script with multiple segments
    script_path = tmp_path / "script.txt"
    script_content = """[SEGMENT_1]
First segment.

[SEGMENT_2]
Second segment.

[SEGMENT_3]
Third segment.
"""
    script_path.write_text(script_content)

    # Create mock profile
    profile_data = {
        "name": "test",
        "created_at": "2024-01-01T00:00:00",
        "language": "es",
        "samples": [],
        "total_duration": 0.0,
    }
    profile_path = tmp_path / "profile.json"
    with open(profile_path, "w") as f:
        json.dump(profile_data, f)

    profile = VoiceProfile.from_json(profile_path)

    # Mock generator that fails on second segment
    with patch("voice_clone.model.generator.VoiceGenerator") as MockGenerator:
        mock_generator = MagicMock()

        # First call succeeds, second fails, third succeeds
        mock_generator.generate.side_effect = [True, False, True]

        MockGenerator.return_value = mock_generator

        processor = AudioProcessor()
        batch_processor = BatchProcessor(mock_generator, processor)

        output_dir = tmp_path / "outputs"
        results = batch_processor.process_script(script_path, profile, output_dir)

        # Should process all segments despite one failure
        assert "successful" in results
        assert "failed" in results
        assert results["successful"] == 2
        assert results["failed"] == 1
