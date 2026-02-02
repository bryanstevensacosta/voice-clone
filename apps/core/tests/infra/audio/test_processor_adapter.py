"""Tests for LibrosaAudioProcessor.

Tests the librosa-based audio processor adapter implementation.
"""

from unittest.mock import Mock, patch

import pytest

from domain.exceptions import InvalidSampleException
from domain.models.audio_sample import AudioSample
from infra.audio.processor_adapter import LibrosaAudioProcessor


@pytest.fixture
def processor():
    """Create a LibrosaAudioProcessor instance."""
    return LibrosaAudioProcessor(
        sample_rate=12000,
        channels=1,
        bit_depth=16,
    )


@pytest.fixture
def valid_audio_file(tmp_path):
    """Create a valid audio file for testing."""
    audio_file = tmp_path / "valid_sample.wav"
    audio_file.touch()
    return audio_file


class TestLibrosaAudioProcessor:
    """Test suite for LibrosaAudioProcessor."""

    def test_implements_audio_processor_port(self, processor):
        """Test that LibrosaAudioProcessor implements AudioProcessor port."""
        from domain.ports.audio_processor import AudioProcessor

        assert isinstance(processor, AudioProcessor)

    def test_init_with_defaults(self):
        """Test initialization with default parameters."""
        processor = LibrosaAudioProcessor()

        assert processor.sample_rate == 12000
        assert processor.channels == 1
        assert processor.bit_depth == 16

    def test_init_with_custom_params(self):
        """Test initialization with custom parameters."""
        processor = LibrosaAudioProcessor(
            sample_rate=22050,
            channels=2,
            bit_depth=24,
        )

        assert processor.sample_rate == 22050
        assert processor.channels == 2
        assert processor.bit_depth == 24

    @patch("infra.audio.processor_adapter.AudioValidator")
    def test_validate_sample_valid(
        self, mock_validator_class, processor, valid_audio_file
    ):
        """Test validating a valid audio sample."""
        # Setup mock validator
        mock_validator = Mock()
        mock_result = Mock()
        mock_result.is_valid.return_value = True
        mock_result.errors = []
        mock_validator.validate.return_value = mock_result
        mock_validator_class.return_value = mock_validator

        # Create new processor to use mocked validator
        processor = LibrosaAudioProcessor()

        result = processor.validate_sample(valid_audio_file)

        assert result is True
        mock_validator.validate.assert_called_once_with(valid_audio_file)

    @patch("infra.audio.processor_adapter.AudioValidator")
    def test_validate_sample_invalid(
        self, mock_validator_class, processor, valid_audio_file
    ):
        """Test validating an invalid audio sample raises exception."""
        # Setup mock validator to return invalid result
        mock_validator = Mock()
        mock_result = Mock()
        mock_result.is_valid.return_value = False
        mock_result.errors = ["Sample rate is incorrect", "Duration too short"]
        mock_validator.validate.return_value = mock_result
        mock_validator_class.return_value = mock_validator

        # Create new processor to use mocked validator
        processor = LibrosaAudioProcessor()

        with pytest.raises(InvalidSampleException, match="validation failed"):
            processor.validate_sample(valid_audio_file)

    @patch("infra.audio.processor_adapter.AudioValidator")
    @patch("infra.audio.processor_adapter.librosa")
    @patch("infra.audio.processor_adapter.sf")
    def test_process_sample_success(
        self,
        mock_sf,
        mock_librosa,
        mock_validator_class,
        processor,
        valid_audio_file,
    ):
        """Test successfully processing an audio sample."""
        # Setup mock validator
        mock_validator = Mock()
        mock_result = Mock()
        mock_result.is_valid.return_value = True
        mock_validator.validate.return_value = mock_result
        mock_validator_class.return_value = mock_validator

        # Setup mock librosa
        mock_audio = Mock()
        mock_librosa.load.return_value = (mock_audio, 12000)
        mock_librosa.get_duration.return_value = 10.5

        # Setup mock soundfile
        mock_info = Mock()
        mock_info.channels = 1
        mock_info.subtype = "PCM_16"
        mock_sf.info.return_value = mock_info

        # Create new processor to use mocked dependencies
        processor = LibrosaAudioProcessor()

        result = processor.process_sample(valid_audio_file)

        assert isinstance(result, AudioSample)
        assert result.path == valid_audio_file
        assert result.duration == 10.5
        assert result.sample_rate == 12000
        assert result.channels == 1
        assert result.bit_depth == 16

    @patch("infra.audio.processor_adapter.AudioValidator")
    def test_process_sample_validation_fails(
        self, mock_validator_class, processor, valid_audio_file
    ):
        """Test processing sample when validation fails."""
        # Setup mock validator to fail
        mock_validator = Mock()
        mock_result = Mock()
        mock_result.is_valid.return_value = False
        mock_result.errors = ["Invalid sample"]
        mock_validator.validate.return_value = mock_result
        mock_validator_class.return_value = mock_validator

        # Create new processor to use mocked validator
        processor = LibrosaAudioProcessor()

        with pytest.raises(InvalidSampleException):
            processor.process_sample(valid_audio_file)

    @patch("infra.audio.processor_adapter.AudioValidator")
    @patch("infra.audio.processor_adapter.librosa")
    def test_process_sample_load_error(
        self, mock_librosa, mock_validator_class, processor, valid_audio_file
    ):
        """Test processing sample when librosa fails to load."""
        # Setup mock validator
        mock_validator = Mock()
        mock_result = Mock()
        mock_result.is_valid.return_value = True
        mock_validator.validate.return_value = mock_result
        mock_validator_class.return_value = mock_validator

        # Setup mock librosa to raise error
        mock_librosa.load.side_effect = Exception("Failed to load audio")

        # Create new processor to use mocked dependencies
        processor = LibrosaAudioProcessor()

        with pytest.raises(InvalidSampleException, match="Failed to process"):
            processor.process_sample(valid_audio_file)

    @patch("infra.audio.processor_adapter.AudioValidator")
    @patch("infra.audio.processor_adapter.librosa")
    @patch("infra.audio.processor_adapter.sf")
    def test_process_sample_extracts_bit_depth(
        self,
        mock_sf,
        mock_librosa,
        mock_validator_class,
        processor,
        valid_audio_file,
    ):
        """Test that process_sample correctly extracts bit depth from subtype."""
        # Setup mock validator
        mock_validator = Mock()
        mock_result = Mock()
        mock_result.is_valid.return_value = True
        mock_validator.validate.return_value = mock_result
        mock_validator_class.return_value = mock_validator

        # Setup mock librosa
        mock_audio = Mock()
        mock_librosa.load.return_value = (mock_audio, 12000)
        mock_librosa.get_duration.return_value = 10.0

        # Setup mock soundfile with 16-bit (valid)
        mock_info = Mock()
        mock_info.channels = 1
        mock_info.subtype = "PCM_16"  # 16-bit audio (valid)
        mock_sf.info.return_value = mock_info

        # Create new processor to use mocked dependencies
        processor = LibrosaAudioProcessor()

        result = processor.process_sample(valid_audio_file)

        assert result.bit_depth == 16

    @patch("infra.audio.processor_adapter.subprocess.run")
    def test_normalize_audio_success(self, mock_run, processor, tmp_path):
        """Test successful audio normalization."""
        input_path = tmp_path / "input.wav"
        output_path = tmp_path / "output.wav"
        input_path.touch()

        # Setup mock subprocess with side effect to create output file
        def create_output(*args, **kwargs):
            output_path.touch()
            mock_result = Mock()
            mock_result.returncode = 0
            return mock_result

        mock_run.side_effect = create_output

        result = processor.normalize_audio(input_path, output_path)

        assert result == output_path
        assert output_path.exists()
        mock_run.assert_called_once()

        # Verify ffmpeg command
        call_args = mock_run.call_args[0][0]
        assert "ffmpeg" in call_args
        assert "-i" in call_args
        assert str(input_path) in call_args
        assert str(output_path) in call_args
        assert any("loudnorm" in str(arg) for arg in call_args)

    @patch("infra.audio.processor_adapter.subprocess.run")
    def test_normalize_audio_custom_lufs(self, mock_run, processor, tmp_path):
        """Test audio normalization with custom LUFS target."""
        input_path = tmp_path / "input.wav"
        output_path = tmp_path / "output.wav"
        input_path.touch()

        # Setup mock subprocess with side effect to create output file
        def create_output(*args, **kwargs):
            output_path.touch()
            mock_result = Mock()
            mock_result.returncode = 0
            return mock_result

        mock_run.side_effect = create_output

        result = processor.normalize_audio(input_path, output_path, target_lufs=-14.0)

        assert result == output_path
        assert output_path.exists()

        # Verify LUFS value in command
        call_args = mock_run.call_args[0][0]
        assert any("loudnorm=I=-14.0" in str(arg) for arg in call_args)

    @patch("infra.audio.processor_adapter.subprocess.run")
    def test_normalize_audio_ffmpeg_failure(self, mock_run, processor, tmp_path):
        """Test audio normalization when ffmpeg fails."""
        input_path = tmp_path / "input.wav"
        output_path = tmp_path / "output.wav"
        input_path.touch()

        # Setup mock subprocess to fail
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stderr.decode.return_value = "FFmpeg error"
        mock_run.return_value = mock_result

        with pytest.raises(InvalidSampleException, match="Failed to normalize"):
            processor.normalize_audio(input_path, output_path)

    @patch("infra.audio.processor_adapter.subprocess.run")
    def test_normalize_audio_creates_output_directory(
        self, mock_run, processor, tmp_path
    ):
        """Test that normalize_audio creates output directory if needed."""
        input_path = tmp_path / "input.wav"
        output_dir = tmp_path / "nested" / "output"
        output_path = output_dir / "output.wav"
        input_path.touch()

        # Setup mock subprocess with side effect to create output file
        def create_output(*args, **kwargs):
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.touch()
            mock_result = Mock()
            mock_result.returncode = 0
            return mock_result

        mock_run.side_effect = create_output

        result = processor.normalize_audio(input_path, output_path)

        assert result == output_path
        assert output_path.exists()
        assert output_path.parent.exists()

    @patch("infra.audio.processor_adapter.subprocess.run")
    def test_normalize_audio_exception_handling(self, mock_run, processor, tmp_path):
        """Test that normalize_audio handles unexpected exceptions."""
        input_path = tmp_path / "input.wav"
        output_path = tmp_path / "output.wav"
        input_path.touch()

        # Setup mock subprocess to raise exception
        mock_run.side_effect = Exception("Unexpected error")

        with pytest.raises(InvalidSampleException, match="normalization failed"):
            processor.normalize_audio(input_path, output_path)
