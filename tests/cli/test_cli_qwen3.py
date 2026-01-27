"""Unit tests for CLI commands with Qwen3-TTS."""

# mypy: disable-error-code="no-untyped-def"

import json
from unittest.mock import Mock, patch

import pytest
from cli.cli import cli
from click.testing import CliRunner


@pytest.fixture
def runner():
    """Create CLI test runner."""
    return CliRunner()


@pytest.fixture
def mock_config():
    """Mock configuration."""
    return {
        "model": {
            "name": "Qwen/Qwen3-TTS-12Hz-1.7B-Base",
            "device": "mps",
            "dtype": "float32",
        },
        "audio": {
            "sample_rate": 12000,
            "output_format": "wav",
        },
        "paths": {
            "models": "./data/models",
        },
    }


@pytest.fixture
def mock_profile(tmp_path):
    """Create mock voice profile."""
    profile_data = {
        "name": "test_voice",
        "samples": [str(tmp_path / "sample1.wav")],
        "ref_text": "This is a test transcript",
        "language": "Spanish",
        "sample_rate": 12000,
        "total_duration": 10.0,
        "created_at": "2024-01-01T00:00:00",
    }

    profile_path = tmp_path / "profile.json"
    with open(profile_path, "w") as f:
        json.dump(profile_data, f)

    return profile_path


class TestValidateSamplesCommand:
    """Tests for validate-samples command."""

    def test_validate_samples_no_wav_files(self, runner, tmp_path):
        """Test validation with no WAV files."""
        result = runner.invoke(cli, ["validate-samples", "--dir", str(tmp_path)])

        assert result.exit_code == 1
        assert "No WAV files found" in result.output

    @patch("cli.cli.AudioProcessor")
    def test_validate_samples_all_valid(self, mock_processor_class, runner, tmp_path):
        """Test validation with all valid samples."""
        # Create mock WAV files
        (tmp_path / "sample1.wav").touch()
        (tmp_path / "sample2.wav").touch()

        # Mock processor
        mock_processor = Mock()
        mock_result = Mock()
        mock_result.is_valid.return_value = True
        mock_result.errors = []
        mock_result.warnings = []
        mock_processor.validate_sample.return_value = mock_result
        mock_processor_class.return_value = mock_processor

        result = runner.invoke(cli, ["validate-samples", "--dir", str(tmp_path)])

        assert result.exit_code == 0
        assert "2/2 samples valid" in result.output

    @patch("cli.cli.AudioProcessor")
    def test_validate_samples_some_invalid(
        self, mock_processor_class, runner, tmp_path
    ):
        """Test validation with some invalid samples."""
        # Create mock WAV files
        (tmp_path / "sample1.wav").touch()
        (tmp_path / "sample2.wav").touch()

        # Mock processor - first valid, second invalid
        mock_processor = Mock()

        valid_result = Mock()
        valid_result.is_valid.return_value = True
        valid_result.errors = []
        valid_result.warnings = []

        invalid_result = Mock()
        invalid_result.is_valid.return_value = False
        invalid_result.errors = ["Sample too short"]
        invalid_result.warnings = []

        mock_processor.validate_sample.side_effect = [valid_result, invalid_result]
        mock_processor_class.return_value = mock_processor

        result = runner.invoke(cli, ["validate-samples", "--dir", str(tmp_path)])

        assert result.exit_code == 1
        assert "1/2 samples valid" in result.output


class TestPrepareCommand:
    """Tests for prepare command."""

    @patch("cli.cli.VoiceProfile")
    def test_prepare_success(self, mock_profile_class, runner, tmp_path):
        """Test successful profile preparation."""
        # Create mock samples directory
        samples_dir = tmp_path / "samples"
        samples_dir.mkdir()
        (samples_dir / "sample1.wav").touch()

        output_path = tmp_path / "profile.json"

        # Mock profile
        mock_profile = Mock()
        mock_profile.samples = ["sample1.wav"]
        mock_profile.total_duration = 10.0
        mock_profile.language = "Spanish"
        mock_profile.sample_rate = 12000
        mock_profile.validate.return_value = (True, [])
        mock_profile_class.from_directory.return_value = mock_profile

        result = runner.invoke(
            cli,
            [
                "prepare",
                "--samples",
                str(samples_dir),
                "--output",
                str(output_path),
                "--name",
                "test_voice",
                "--ref-text",
                "This is a test transcript",
            ],
        )

        assert result.exit_code == 0
        assert "Voice profile created successfully" in result.output
        assert "Reference Text" in result.output
        mock_profile_class.from_directory.assert_called_once_with(
            "test_voice", samples_dir, ref_text="This is a test transcript"
        )

    @patch("cli.cli.VoiceProfile")
    def test_prepare_no_samples(self, mock_profile_class, runner, tmp_path):
        """Test preparation with no valid samples."""
        samples_dir = tmp_path / "samples"
        samples_dir.mkdir()
        output_path = tmp_path / "profile.json"

        # Mock profile with no samples
        mock_profile = Mock()
        mock_profile.samples = []
        mock_profile_class.from_directory.return_value = mock_profile

        result = runner.invoke(
            cli,
            [
                "prepare",
                "--samples",
                str(samples_dir),
                "--output",
                str(output_path),
                "--name",
                "test_voice",
                "--ref-text",
                "Test",
            ],
        )

        assert result.exit_code == 1
        assert "No valid samples found" in result.output

    @patch("cli.cli.VoiceProfile")
    def test_prepare_validation_failed(self, mock_profile_class, runner, tmp_path):
        """Test preparation with validation failure."""
        samples_dir = tmp_path / "samples"
        samples_dir.mkdir()
        output_path = tmp_path / "profile.json"

        # Mock profile that fails validation
        mock_profile = Mock()
        mock_profile.samples = ["sample1.wav"]
        mock_profile.validate.return_value = (False, ["Error"])
        mock_profile_class.from_directory.return_value = mock_profile

        result = runner.invoke(
            cli,
            [
                "prepare",
                "--samples",
                str(samples_dir),
                "--output",
                str(output_path),
                "--name",
                "test_voice",
                "--ref-text",
                "Test",
            ],
        )

        assert result.exit_code == 1
        assert "Profile validation failed" in result.output


class TestGenerateCommand:
    """Tests for generate command."""

    @patch("cli.cli.Qwen3Generator")
    @patch("cli.cli.Qwen3ModelManager")
    @patch("cli.cli.ConfigManager")
    @patch("cli.cli.VoiceProfile")
    def test_generate_success(
        self,
        mock_profile_class,
        mock_config_class,
        mock_manager_class,
        mock_generator_class,
        runner,
        tmp_path,
        mock_profile,
    ):
        """Test successful audio generation."""
        output_path = tmp_path / "output.wav"

        # Mock config
        mock_config = Mock()
        mock_config.load_config.return_value = {"model": {}, "audio": {}}
        mock_config_class.return_value = mock_config

        # Mock profile
        mock_profile_obj = Mock()
        mock_profile_obj.samples = [str(tmp_path / "sample1.wav")]
        mock_profile_obj.ref_text = "Test transcript"
        mock_profile_obj.language = "Spanish"
        mock_profile_class.from_json.return_value = mock_profile_obj

        # Mock model manager
        mock_manager = Mock()
        mock_manager.load_model.return_value = True
        mock_manager_class.return_value = mock_manager

        # Mock generator
        mock_generator = Mock()
        mock_generator.generate_to_file.return_value = True
        mock_generator_class.return_value = mock_generator

        result = runner.invoke(
            cli,
            [
                "generate",
                "--profile",
                str(mock_profile),
                "--text",
                "Test text",
                "--output",
                str(output_path),
            ],
        )

        assert result.exit_code == 0
        assert "Audio generated successfully" in result.output
        assert "12000 Hz" in result.output
        mock_generator.generate_to_file.assert_called_once()

    @patch("cli.cli.Qwen3ModelManager")
    @patch("cli.cli.ConfigManager")
    @patch("cli.cli.VoiceProfile")
    def test_generate_model_load_failed(
        self,
        mock_profile_class,
        mock_config_class,
        mock_manager_class,
        runner,
        tmp_path,
        mock_profile,
    ):
        """Test generation with model load failure."""
        output_path = tmp_path / "output.wav"

        # Mock config
        mock_config = Mock()
        mock_config.load_config.return_value = {"model": {}}
        mock_config_class.return_value = mock_config

        # Mock profile
        mock_profile_obj = Mock()
        mock_profile_class.from_json.return_value = mock_profile_obj

        # Mock model manager that fails to load
        mock_manager = Mock()
        mock_manager.load_model.return_value = False
        mock_manager_class.return_value = mock_manager

        result = runner.invoke(
            cli,
            [
                "generate",
                "--profile",
                str(mock_profile),
                "--text",
                "Test text",
                "--output",
                str(output_path),
            ],
        )

        assert result.exit_code == 1
        assert "Failed to load Qwen3-TTS model" in result.output


class TestBatchCommand:
    """Tests for batch command."""

    @patch("cli.cli.BatchProcessor")
    @patch("cli.cli.AudioProcessor")
    @patch("cli.cli.Qwen3Generator")
    @patch("cli.cli.Qwen3ModelManager")
    @patch("cli.cli.ConfigManager")
    @patch("cli.cli.VoiceProfile")
    def test_batch_success(
        self,
        mock_profile_class,
        mock_config_class,
        mock_manager_class,
        mock_generator_class,
        mock_processor_class,
        mock_batch_class,
        runner,
        tmp_path,
        mock_profile,
    ):
        """Test successful batch processing."""
        script_path = tmp_path / "script.txt"
        script_path.write_text("[INTRO]\nTest text")
        output_dir = tmp_path / "outputs"

        # Mock config
        mock_config = Mock()
        mock_config.load_config.return_value = {"model": {}}
        mock_config_class.return_value = mock_config

        # Mock profile
        mock_profile_obj = Mock()
        mock_profile_class.from_json.return_value = mock_profile_obj

        # Mock model manager
        mock_manager = Mock()
        mock_manager.load_model.return_value = True
        mock_manager_class.return_value = mock_manager

        # Mock batch processor
        mock_batch = Mock()
        mock_batch.process_script.return_value = {
            "total": 1,
            "successful": 1,
            "failed": 0,
        }
        mock_batch_class.return_value = mock_batch

        result = runner.invoke(
            cli,
            [
                "batch",
                "--profile",
                str(mock_profile),
                "--input",
                str(script_path),
                "--output-dir",
                str(output_dir),
            ],
        )

        assert result.exit_code == 0
        assert "Batch processing complete" in result.output
        assert "12000 Hz" in result.output


class TestTestCommand:
    """Tests for test command."""

    @patch("cli.cli.Qwen3Generator")
    @patch("cli.cli.Qwen3ModelManager")
    @patch("cli.cli.ConfigManager")
    @patch("cli.cli.VoiceProfile")
    def test_test_command_success(
        self,
        mock_profile_class,
        mock_config_class,
        mock_manager_class,
        mock_generator_class,
        runner,
        tmp_path,
        mock_profile,
    ):
        """Test successful test command."""
        # Mock config
        mock_config = Mock()
        mock_config.load_config.return_value = {"model": {}}
        mock_config_class.return_value = mock_config

        # Mock profile
        mock_profile_obj = Mock()
        mock_profile_obj.samples = [str(tmp_path / "sample1.wav")]
        mock_profile_obj.ref_text = "Test transcript"
        mock_profile_obj.language = "Spanish"
        mock_profile_class.from_json.return_value = mock_profile_obj

        # Mock model manager
        mock_manager = Mock()
        mock_manager.load_model.return_value = True
        mock_manager_class.return_value = mock_manager

        # Mock generator
        mock_generator = Mock()
        mock_generator.generate_to_file.return_value = True
        mock_generator_class.return_value = mock_generator

        result = runner.invoke(
            cli,
            ["test", "--profile", str(mock_profile)],
        )

        assert result.exit_code == 0
        assert "Test audio generated successfully" in result.output
        assert "Qwen3-TTS" in result.output
        assert "12000 Hz" in result.output

    @patch("cli.cli.Qwen3Generator")
    @patch("cli.cli.Qwen3ModelManager")
    @patch("cli.cli.ConfigManager")
    @patch("cli.cli.VoiceProfile")
    def test_test_command_custom_text(
        self,
        mock_profile_class,
        mock_config_class,
        mock_manager_class,
        mock_generator_class,
        runner,
        tmp_path,
        mock_profile,
    ):
        """Test test command with custom text."""
        # Mock config
        mock_config = Mock()
        mock_config.load_config.return_value = {"model": {}}
        mock_config_class.return_value = mock_config

        # Mock profile
        mock_profile_obj = Mock()
        mock_profile_obj.samples = [str(tmp_path / "sample1.wav")]
        mock_profile_obj.ref_text = "Test transcript"
        mock_profile_obj.language = "Spanish"
        mock_profile_class.from_json.return_value = mock_profile_obj

        # Mock model manager
        mock_manager = Mock()
        mock_manager.load_model.return_value = True
        mock_manager_class.return_value = mock_manager

        # Mock generator
        mock_generator = Mock()
        mock_generator.generate_to_file.return_value = True
        mock_generator_class.return_value = mock_generator

        custom_text = "Custom test text"
        result = runner.invoke(
            cli,
            ["test", "--profile", str(mock_profile), "--text", custom_text],
        )

        assert result.exit_code == 0
        assert custom_text in result.output


class TestInfoCommand:
    """Tests for info command."""

    def test_info_command_runs(self, runner):
        """Test that info command runs without errors."""
        result = runner.invoke(cli, ["info"])

        # Should run successfully
        assert result.exit_code == 0
        assert "Qwen3-TTS" in result.output
        assert "12000 Hz" in result.output
        assert "3 seconds" in result.output
        # Should show device info (either MPS, CUDA, or CPU)
        assert any(device in result.output for device in ["MPS", "CUDA", "CPU"])
