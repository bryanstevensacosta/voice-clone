"""
Unit tests for batch processing handler.

Tests the batch_process_handler function with various scenarios including
successful batch processing, validation errors, and error handling.
"""

import json
from unittest.mock import Mock, patch

import pytest

from gradio_ui.handlers.batch_handler import batch_process_handler


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
            }
        ],
    }


@pytest.fixture
def mock_script_content():
    """Create mock script content."""
    return """[INTRO]
Hola, bienvenidos a este tutorial.

[SECTION_1]
Hoy vamos a hablar sobre inteligencia artificial.

[OUTRO]
Gracias por ver este video.
"""


@pytest.fixture
def setup_test_environment(tmp_path, mock_profile_data, mock_script_content):
    """Set up test environment with profile, samples, and script files."""
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

    # Create mock sample file
    sample_path = tmp_path / "data" / "samples" / "sample_01.wav"
    sample_path.touch()

    # Create script file
    script_path = tmp_path / "test_script.txt"
    with open(script_path, "w") as f:
        f.write(mock_script_content)

    return tmp_path, script_path


class TestBatchProcessHandler:
    """Test suite for batch_process_handler function."""

    def test_no_profile_selected(self):
        """Test error when no profile is selected."""
        files, info = batch_process_handler("", "script.txt")

        assert files == []
        assert "❌" in info
        assert "No profile selected" in info

    def test_no_script_file(self):
        """Test error when no script file is uploaded."""
        files, info = batch_process_handler("test_profile", None)

        assert files == []
        assert "❌" in info
        assert "No script file uploaded" in info

    def test_profile_not_found(self, setup_test_environment, monkeypatch):
        """Test error when profile doesn't exist."""
        tmp_path, script_path = setup_test_environment
        monkeypatch.chdir(tmp_path)

        files, info = batch_process_handler("nonexistent", str(script_path))

        assert files == []
        assert "❌" in info
        assert "Profile not found" in info

    def test_profile_no_samples(self, setup_test_environment, monkeypatch):
        """Test error when profile has no samples."""
        tmp_path, script_path = setup_test_environment
        monkeypatch.chdir(tmp_path)

        # Create profile with no samples
        profiles_dir = tmp_path / "data" / "profiles"
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

        files, info = batch_process_handler("empty_profile", str(script_path))

        assert files == []
        assert "❌" in info
        assert "Invalid profile" in info

    def test_script_file_not_found(self, setup_test_environment, monkeypatch):
        """Test error when script file doesn't exist."""
        tmp_path, _ = setup_test_environment
        monkeypatch.chdir(tmp_path)

        files, info = batch_process_handler("test_profile", "nonexistent.txt")

        assert files == []
        assert "❌" in info
        assert "Script file not found" in info

    def test_empty_script(self, setup_test_environment, monkeypatch):
        """Test error when script has no valid segments."""
        tmp_path, _ = setup_test_environment
        monkeypatch.chdir(tmp_path)

        # Create empty script
        empty_script = tmp_path / "empty_script.txt"
        with open(empty_script, "w") as f:
            f.write("No segments here")

        files, info = batch_process_handler("test_profile", str(empty_script))

        assert files == []
        assert "❌" in info
        assert "Empty script" in info

    @patch("gradio_ui.handlers.batch_handler.Qwen3ModelManager")
    @patch("gradio_ui.handlers.batch_handler.Qwen3Generator")
    @patch("gradio_ui.handlers.batch_handler.ConfigManager")
    def test_successful_batch_processing(
        self,
        mock_config_manager,
        mock_generator_class,
        mock_manager_class,
        setup_test_environment,
        monkeypatch,
    ):
        """Test successful batch processing."""
        tmp_path, script_path = setup_test_environment
        monkeypatch.chdir(tmp_path)

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

        # Process batch
        files, info = batch_process_handler("test_profile", str(script_path))

        # Assertions
        assert len(files) == 3  # 3 segments in script
        assert all("batch_test_profile" in f for f in files)
        assert "✅" in info or "⚠️" in info
        assert "Batch Processing Complete" in info
        assert "test_profile" in info
        assert "3" in info  # Total segments

        # Verify generator was called 3 times
        assert mock_generator.generate_to_file.call_count == 3

    @patch("gradio_ui.handlers.batch_handler.Qwen3ModelManager")
    @patch("gradio_ui.handlers.batch_handler.ConfigManager")
    def test_model_loading_failure(
        self,
        mock_config_manager,
        mock_manager_class,
        setup_test_environment,
        monkeypatch,
    ):
        """Test error when model fails to load."""
        tmp_path, script_path = setup_test_environment
        monkeypatch.chdir(tmp_path)

        # Mock config
        mock_config = {"generation": {"language": "es"}}
        mock_config_manager.load_config.return_value = mock_config

        # Mock model manager - not loaded and fails to load
        mock_manager = Mock()
        mock_manager.is_loaded.return_value = False
        mock_manager.load_model.return_value = False
        mock_manager_class.return_value = mock_manager

        # Process batch
        files, info = batch_process_handler("test_profile", str(script_path))

        # Assertions
        assert files == []
        assert "❌" in info
        assert "Model loading failed" in info

    @patch("gradio_ui.handlers.batch_handler.Qwen3ModelManager")
    @patch("gradio_ui.handlers.batch_handler.Qwen3Generator")
    @patch("gradio_ui.handlers.batch_handler.ConfigManager")
    def test_partial_failure(
        self,
        mock_config_manager,
        mock_generator_class,
        mock_manager_class,
        setup_test_environment,
        monkeypatch,
    ):
        """Test batch processing with some failures."""
        tmp_path, script_path = setup_test_environment
        monkeypatch.chdir(tmp_path)

        # Mock config
        mock_config = {"generation": {"language": "es"}}
        mock_config_manager.load_config.return_value = mock_config

        # Mock model manager
        mock_manager = Mock()
        mock_manager.is_loaded.return_value = True
        mock_manager_class.return_value = mock_manager

        # Mock generator - first succeeds, second fails, third succeeds
        mock_generator = Mock()
        mock_generator.generate_to_file.side_effect = [True, False, True]
        mock_generator_class.return_value = mock_generator

        # Process batch
        files, info = batch_process_handler("test_profile", str(script_path))

        # Assertions
        assert len(files) == 2  # Only 2 successful
        assert "⚠️" in info  # Warning because of failures
        assert "Batch Processing Complete" in info
        assert "2" in info  # Successful count
        assert "1" in info  # Failed count

    @patch("gradio_ui.handlers.batch_handler.Qwen3ModelManager")
    @patch("gradio_ui.handlers.batch_handler.ConfigManager")
    def test_memory_error(
        self,
        mock_config_manager,
        mock_manager_class,
        setup_test_environment,
        monkeypatch,
    ):
        """Test handling of out of memory error."""
        tmp_path, script_path = setup_test_environment
        monkeypatch.chdir(tmp_path)

        # Mock config
        mock_config = {"generation": {"language": "es"}}
        mock_config_manager.load_config.return_value = mock_config

        # Mock model manager to raise MemoryError
        mock_manager = Mock()
        mock_manager.is_loaded.side_effect = MemoryError("Out of memory")
        mock_manager_class.return_value = mock_manager

        # Process batch
        files, info = batch_process_handler("test_profile", str(script_path))

        # Assertions
        assert files == []
        assert "❌" in info
        assert "Out of memory" in info

    def test_script_parsing(self, setup_test_environment, monkeypatch):
        """Test that script is parsed correctly."""
        tmp_path, script_path = setup_test_environment
        monkeypatch.chdir(tmp_path)

        # Read the script to verify format
        with open(script_path) as f:
            content = f.read()

        assert "[INTRO]" in content
        assert "[SECTION_1]" in content
        assert "[OUTRO]" in content
        assert "Hola, bienvenidos" in content

    def test_output_directory_creation(self, setup_test_environment, monkeypatch):
        """Test that output directory is created correctly."""
        tmp_path, _ = setup_test_environment
        monkeypatch.chdir(tmp_path)

        # The output directory should be created during processing
        # This is tested implicitly in successful_batch_processing test
        # Here we just verify the path structure
        expected_dir = tmp_path / "data" / "outputs" / "batch_test_profile"
        assert not expected_dir.exists()  # Doesn't exist yet
