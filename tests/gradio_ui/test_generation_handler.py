"""
Unit tests for audio generation handler.

Tests the generate_audio_handler function with various scenarios including
successful generation, validation errors, and error handling.
"""

import json
from unittest.mock import Mock, patch

import numpy as np
import pytest

from gradio_ui.handlers.generation_handler import generate_audio_handler


@pytest.fixture
def mock_profile_data():
    """Create mock profile data."""
    return {
        "name": "test_profile",
        "created_at": "2024-01-01T00:00:00",
        "language": "es",
        "total_duration": 30.0,
        "ref_text": "Esta es una muestra de voz para clonación.",
        "sample_rate": 12000,
        "samples": [
            {
                "path": "data/samples/sample_01.wav",
                "duration": 10.0,
                "emotion": "neutral",
                "quality_score": 1.0,
            },
            {
                "path": "data/samples/sample_02.wav",
                "duration": 10.0,
                "emotion": "happy",
                "quality_score": 1.0,
            },
            {
                "path": "data/samples/sample_03.wav",
                "duration": 10.0,
                "emotion": "serious",
                "quality_score": 1.0,
            },
        ],
    }


@pytest.fixture
def setup_test_environment(tmp_path, mock_profile_data):
    """Set up test environment with profile and sample files."""
    # Create profiles directory
    profiles_dir = tmp_path / "data" / "profiles"
    profiles_dir.mkdir(parents=True, exist_ok=True)

    # Create samples directory
    samples_dir = tmp_path / "data" / "samples"
    samples_dir.mkdir(parents=True, exist_ok=True)

    # Create outputs directory
    outputs_dir = tmp_path / "data" / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)

    # Create profile JSON file
    profile_path = profiles_dir / "test_profile.json"
    with open(profile_path, "w") as f:
        json.dump(mock_profile_data, f)

    # Create mock sample files (empty WAV files for testing)
    for sample in mock_profile_data["samples"]:
        sample_path = tmp_path / sample["path"]
        sample_path.parent.mkdir(parents=True, exist_ok=True)
        sample_path.touch()

    return tmp_path


class TestGenerateAudioHandler:
    """Test suite for generate_audio_handler function."""

    def test_no_profile_selected(self):
        """Test error when no profile is selected."""
        audio_path, info = generate_audio_handler("", "Some text", 0.75, 1.0)

        assert audio_path is None
        assert "❌" in info
        assert "No profile selected" in info
        assert "select a voice profile" in info.lower()

    def test_empty_text(self):
        """Test error when text is empty."""
        audio_path, info = generate_audio_handler("test_profile", "", 0.75, 1.0)

        assert audio_path is None
        assert "❌" in info
        assert "No text provided" in info
        assert "enter the text" in info.lower()

    def test_whitespace_only_text(self):
        """Test error when text is only whitespace."""
        audio_path, info = generate_audio_handler("test_profile", "   \n  ", 0.75, 1.0)

        assert audio_path is None
        assert "❌" in info
        assert "No text provided" in info

    def test_profile_not_found(self, setup_test_environment, monkeypatch):
        """Test error when profile file doesn't exist."""
        # Change to test directory
        monkeypatch.chdir(setup_test_environment)

        audio_path, info = generate_audio_handler(
            "nonexistent_profile", "Some text", 0.75, 1.0
        )

        assert audio_path is None
        assert "❌" in info
        assert "Profile not found" in info
        assert "nonexistent_profile" in info

    def test_profile_no_samples(self, setup_test_environment, monkeypatch):
        """Test error when profile has no samples."""
        # Change to test directory
        monkeypatch.chdir(setup_test_environment)

        # Create profile with no samples
        profiles_dir = setup_test_environment / "data" / "profiles"
        profile_path = profiles_dir / "empty_profile.json"
        with open(profile_path, "w") as f:
            json.dump(
                {
                    "name": "empty_profile",
                    "created_at": "2024-01-01T00:00:00",
                    "language": "es",
                    "total_duration": 0.0,
                    "ref_text": "Test",
                    "sample_rate": 12000,
                    "samples": [],
                },
                f,
            )

        audio_path, info = generate_audio_handler(
            "empty_profile", "Some text", 0.75, 1.0
        )

        assert audio_path is None
        assert "❌" in info
        assert "Invalid profile" in info
        assert "no audio samples" in info.lower()

    def test_profile_missing_ref_text(self, setup_test_environment, monkeypatch):
        """Test error when profile is missing reference text."""
        # Change to test directory
        monkeypatch.chdir(setup_test_environment)

        # Create profile without ref_text
        profiles_dir = setup_test_environment / "data" / "profiles"
        profile_path = profiles_dir / "no_ref_text.json"
        with open(profile_path, "w") as f:
            json.dump(
                {
                    "name": "no_ref_text",
                    "created_at": "2024-01-01T00:00:00",
                    "language": "es",
                    "total_duration": 10.0,
                    "ref_text": "",
                    "sample_rate": 12000,
                    "samples": [
                        {
                            "path": "data/samples/sample_01.wav",
                            "duration": 10.0,
                            "emotion": "neutral",
                            "quality_score": 1.0,
                        }
                    ],
                },
                f,
            )

        audio_path, info = generate_audio_handler("no_ref_text", "Some text", 0.75, 1.0)

        assert audio_path is None
        assert "❌" in info
        assert "Missing reference text" in info

    def test_reference_audio_not_found(self, setup_test_environment, monkeypatch):
        """Test error when reference audio file doesn't exist."""
        # Change to test directory
        monkeypatch.chdir(setup_test_environment)

        # Delete the sample file
        sample_path = setup_test_environment / "data" / "samples" / "sample_01.wav"
        sample_path.unlink()

        audio_path, info = generate_audio_handler(
            "test_profile", "Some text", 0.75, 1.0
        )

        assert audio_path is None
        assert "❌" in info
        assert "Reference audio not found" in info

    @patch("gradio_ui.handlers.generation_handler.Qwen3ModelManager")
    @patch("gradio_ui.handlers.generation_handler.Qwen3Generator")
    @patch("gradio_ui.handlers.generation_handler.ConfigManager")
    @patch("soundfile.read")
    def test_successful_generation(
        self,
        mock_sf_read,
        mock_config_manager,
        mock_generator_class,
        mock_manager_class,
        setup_test_environment,
        monkeypatch,
    ):
        """Test successful audio generation."""
        # Change to test directory
        monkeypatch.chdir(setup_test_environment)

        # Mock config
        mock_config = {"generation": {"language": "es"}}
        mock_config_manager.load_config.return_value = mock_config

        # Mock model manager
        mock_manager = Mock()
        mock_manager.is_loaded.return_value = True
        mock_manager_class.return_value = mock_manager

        # Mock generator
        mock_generator = Mock()
        mock_generator.generate_to_file.return_value = True
        mock_generator_class.return_value = mock_generator

        # Mock soundfile read (for duration calculation)
        mock_audio = np.zeros(12000 * 5)  # 5 seconds of audio at 12000 Hz
        mock_sf_read.return_value = (mock_audio, 12000)

        # Generate audio
        audio_path, info = generate_audio_handler(
            "test_profile", "Hola, este es un texto de prueba.", 0.75, 1.0
        )

        # Assertions
        assert audio_path is not None
        assert "generated_test_profile.wav" in audio_path
        assert "✅" in info
        assert "Audio Generated Successfully" in info
        assert "test_profile" in info
        assert "0.75" in info
        assert "1.0" in info

        # Verify generator was called correctly
        mock_generator.generate_to_file.assert_called_once()
        call_kwargs = mock_generator.generate_to_file.call_args[1]
        assert call_kwargs["text"] == "Hola, este es un texto de prueba."
        assert "ref_audio" in call_kwargs
        assert call_kwargs["ref_text"] == "Esta es una muestra de voz para clonación."

    @patch("gradio_ui.handlers.generation_handler.Qwen3ModelManager")
    @patch("gradio_ui.handlers.generation_handler.ConfigManager")
    def test_model_loading_failure(
        self,
        mock_config_manager,
        mock_manager_class,
        setup_test_environment,
        monkeypatch,
    ):
        """Test error when model fails to load."""
        # Change to test directory
        monkeypatch.chdir(setup_test_environment)

        # Mock config
        mock_config = {"generation": {"language": "es"}}
        mock_config_manager.load_config.return_value = mock_config

        # Mock model manager - not loaded and fails to load
        mock_manager = Mock()
        mock_manager.is_loaded.return_value = False
        mock_manager.load_model.return_value = False
        mock_manager_class.return_value = mock_manager

        # Generate audio
        audio_path, info = generate_audio_handler(
            "test_profile", "Some text", 0.75, 1.0
        )

        # Assertions
        assert audio_path is None
        assert "❌" in info
        assert "Model loading failed" in info

    @patch("gradio_ui.handlers.generation_handler.Qwen3ModelManager")
    @patch("gradio_ui.handlers.generation_handler.Qwen3Generator")
    @patch("gradio_ui.handlers.generation_handler.ConfigManager")
    def test_generation_failure(
        self,
        mock_config_manager,
        mock_generator_class,
        mock_manager_class,
        setup_test_environment,
        monkeypatch,
    ):
        """Test error when generation fails."""
        # Change to test directory
        monkeypatch.chdir(setup_test_environment)

        # Mock config
        mock_config = {"generation": {"language": "es"}}
        mock_config_manager.load_config.return_value = mock_config

        # Mock model manager
        mock_manager = Mock()
        mock_manager.is_loaded.return_value = True
        mock_manager_class.return_value = mock_manager

        # Mock generator - generation fails
        mock_generator = Mock()
        mock_generator.generate_to_file.return_value = False
        mock_generator_class.return_value = mock_generator

        # Generate audio
        audio_path, info = generate_audio_handler(
            "test_profile", "Some text", 0.75, 1.0
        )

        # Assertions
        assert audio_path is None
        assert "❌" in info
        assert "Generation failed" in info

    @patch("gradio_ui.handlers.generation_handler.Qwen3ModelManager")
    @patch("gradio_ui.handlers.generation_handler.ConfigManager")
    def test_memory_error(
        self,
        mock_config_manager,
        mock_manager_class,
        setup_test_environment,
        monkeypatch,
    ):
        """Test handling of out of memory error."""
        # Change to test directory
        monkeypatch.chdir(setup_test_environment)

        # Mock config
        mock_config = {"generation": {"language": "es"}}
        mock_config_manager.load_config.return_value = mock_config

        # Mock model manager to raise MemoryError
        mock_manager = Mock()
        mock_manager.is_loaded.side_effect = MemoryError("Out of memory")
        mock_manager_class.return_value = mock_manager

        # Generate audio
        audio_path, info = generate_audio_handler(
            "test_profile", "Some text", 0.75, 1.0
        )

        # Assertions
        assert audio_path is None
        assert "❌" in info
        assert "Out of memory" in info

    @patch("gradio_ui.handlers.generation_handler.Qwen3ModelManager")
    @patch("gradio_ui.handlers.generation_handler.ConfigManager")
    def test_permission_error(
        self,
        mock_config_manager,
        mock_manager_class,
        setup_test_environment,
        monkeypatch,
    ):
        """Test handling of permission error."""
        # Change to test directory
        monkeypatch.chdir(setup_test_environment)

        # Mock config
        mock_config = {"generation": {"language": "es"}}
        mock_config_manager.load_config.return_value = mock_config

        # Mock model manager to raise PermissionError
        mock_manager = Mock()
        mock_manager.is_loaded.side_effect = PermissionError("Permission denied")
        mock_manager_class.return_value = mock_manager

        # Generate audio
        audio_path, info = generate_audio_handler(
            "test_profile", "Some text", 0.75, 1.0
        )

        # Assertions
        assert audio_path is None
        assert "❌" in info
        assert "Permission denied" in info

    def test_long_text_warning(self, setup_test_environment, monkeypatch):
        """Test that long text doesn't crash the handler."""
        # Change to test directory
        monkeypatch.chdir(setup_test_environment)

        # Create very long text
        long_text = "A" * 600

        # This will fail at profile loading, but shouldn't crash
        audio_path, info = generate_audio_handler("test_profile", long_text, 0.75, 1.0)

        # Should return error (profile not found or other issue), not crash
        assert audio_path is None
        assert "❌" in info

    def test_parameter_ranges(self, setup_test_environment, monkeypatch):
        """Test that parameters are passed correctly."""
        # This is more of an integration test to ensure parameters flow through
        # We'll just verify the function accepts the parameter ranges

        # Change to test directory
        monkeypatch.chdir(setup_test_environment)

        # Test with minimum temperature
        audio_path, info = generate_audio_handler("test_profile", "Text", 0.5, 1.0)
        assert audio_path is None  # Will fail but shouldn't crash

        # Test with maximum temperature
        audio_path, info = generate_audio_handler("test_profile", "Text", 1.0, 1.0)
        assert audio_path is None  # Will fail but shouldn't crash

        # Test with minimum speed
        audio_path, info = generate_audio_handler("test_profile", "Text", 0.75, 0.8)
        assert audio_path is None  # Will fail but shouldn't crash

        # Test with maximum speed
        audio_path, info = generate_audio_handler("test_profile", "Text", 0.75, 1.2)
        assert audio_path is None  # Will fail but shouldn't crash
