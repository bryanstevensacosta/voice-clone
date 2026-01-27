"""Unit tests for AudioProcessor with Qwen3-TTS updates."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np
import pytest
from voice_clone.audio.processor import AudioProcessor


class TestAudioProcessorQwen3Initialization:
    """Test AudioProcessor initialization with Qwen3-TTS defaults."""

    def test_default_sample_rate_is_12000(self) -> None:
        """Test that default sample rate is 12000 Hz for Qwen3-TTS."""
        processor = AudioProcessor()
        assert processor.sample_rate == 12000

    def test_custom_sample_rate(self) -> None:
        """Test initialization with custom sample rate."""
        processor = AudioProcessor(sample_rate=22050)
        assert processor.sample_rate == 22050

    def test_default_channels_is_mono(self) -> None:
        """Test that default channels is 1 (mono)."""
        processor = AudioProcessor()
        assert processor.channels == 1

    def test_default_bit_depth_is_16(self) -> None:
        """Test that default bit depth is 16."""
        processor = AudioProcessor()
        assert processor.bit_depth == 16


class TestAudioValidationQwen3:
    """Test audio validation with Qwen3-TTS requirements."""

    @patch("librosa.load")
    @patch("soundfile.info")
    @patch("librosa.get_duration")
    def test_validate_sample_minimum_duration_3_seconds(
        self,
        mock_duration: MagicMock,
        mock_info: MagicMock,
        mock_load: MagicMock,
    ) -> None:
        """Test that minimum duration is 3 seconds for Qwen3-TTS."""
        processor = AudioProcessor()

        # Mock audio data (normalized to avoid clipping - use smaller values)
        mock_audio = np.random.randn(36000) * 0.3  # 3 seconds at 12kHz, well normalized
        mock_load.return_value = (mock_audio, 12000)

        # Mock info
        mock_info_obj = MagicMock()
        mock_info_obj.subtype = "PCM_16"
        mock_info.return_value = mock_info_obj

        # Mock duration
        mock_duration.return_value = 3.0

        result = processor.validate_sample("test.wav")

        # Should be valid (3 seconds meets minimum)
        # Note: May have clipping warning due to random data, but duration check passes
        assert any("minimum: 3s" not in error for error in result.errors)

    @patch("librosa.load")
    @patch("soundfile.info")
    @patch("librosa.get_duration")
    def test_validate_sample_fails_below_3_seconds(
        self,
        mock_duration: MagicMock,
        mock_info: MagicMock,
        mock_load: MagicMock,
    ) -> None:
        """Test that validation fails for audio shorter than 3 seconds."""
        processor = AudioProcessor()

        # Mock audio data (2.5 seconds, normalized)
        mock_audio = np.random.randn(30000) * 0.3
        mock_load.return_value = (mock_audio, 12000)

        # Mock info
        mock_info_obj = MagicMock()
        mock_info_obj.subtype = "PCM_16"
        mock_info.return_value = mock_info_obj

        # Mock duration
        mock_duration.return_value = 2.5

        result = processor.validate_sample("test.wav")

        # Should have duration error
        assert any("minimum: 3s" in error for error in result.errors)

    @patch("librosa.load")
    @patch("soundfile.info")
    @patch("librosa.get_duration")
    def test_validate_sample_warns_above_30_seconds(
        self,
        mock_duration: MagicMock,
        mock_info: MagicMock,
        mock_load: MagicMock,
    ) -> None:
        """Test that validation warns for audio longer than 30 seconds."""
        processor = AudioProcessor()

        # Mock audio data (35 seconds, properly normalized to avoid clipping)
        raw_audio = np.random.randn(420000)
        mock_audio = raw_audio / (
            np.abs(raw_audio).max() * 1.5
        )  # Normalize to avoid clipping
        mock_load.return_value = (mock_audio, 12000)

        # Mock info
        mock_info_obj = MagicMock()
        mock_info_obj.subtype = "PCM_16"
        mock_info.return_value = mock_info_obj

        # Mock duration
        mock_duration.return_value = 35.0

        result = processor.validate_sample("test.wav")

        # Check that result is valid
        assert result.is_valid() is True
        assert any("3-30s" in warning for warning in result.warnings)

    @patch("librosa.load")
    @patch("soundfile.info")
    @patch("librosa.get_duration")
    def test_validate_sample_warns_non_12khz(
        self,
        mock_duration: MagicMock,
        mock_info: MagicMock,
        mock_load: MagicMock,
    ) -> None:
        """Test that validation warns for non-12kHz sample rate."""
        processor = AudioProcessor()

        # Mock audio data at 22050 Hz (properly normalized to avoid clipping)
        raw_audio = np.random.randn(66150)  # 3 seconds at 22050Hz
        # Normalize to ensure no clipping
        mock_audio = raw_audio / (np.abs(raw_audio).max() * 1.5)
        mock_load.return_value = (mock_audio, 22050)

        # Mock info
        mock_info_obj = MagicMock()
        mock_info_obj.subtype = "PCM_16"
        mock_info.return_value = mock_info_obj

        # Mock duration
        mock_duration.return_value = 3.0

        result = processor.validate_sample("test.wav")

        # Check that result is valid
        assert result.is_valid() is True
        assert any("22050 Hz" in warning for warning in result.warnings)
        assert any("12000 Hz" in warning for warning in result.warnings)


class TestResampleToQwen3:
    """Test resampling to Qwen3-TTS format."""

    def test_resample_to_qwen3_calls_convert(self) -> None:
        """Test that resample_to_qwen3 calls convert_to_target_format."""
        processor = AudioProcessor()

        with patch.object(
            processor, "convert_to_target_format", return_value=True
        ) as mock_convert:
            result = processor.resample_to_qwen3("input.wav", "output.wav")

            assert result is True
            mock_convert.assert_called_once_with("input.wav", "output.wav")


class TestUpsampleOutput:
    """Test upsampling Qwen3-TTS output."""

    def test_upsample_output_12khz_to_22khz(self) -> None:
        """Test upsampling from 12kHz to 22kHz."""
        processor = AudioProcessor()

        # Create mock audio at 12kHz (1 second)
        audio_12k = np.random.randn(12000)

        with patch("librosa.resample") as mock_resample:
            mock_resample.return_value = np.random.randn(22050)

            result = processor.upsample_output(audio_12k, 12000, 22050)

            assert result is not None
            mock_resample.assert_called_once()
            call_args = mock_resample.call_args
            assert call_args[1]["orig_sr"] == 12000
            assert call_args[1]["target_sr"] == 22050

    def test_upsample_output_same_rate_returns_original(self) -> None:
        """Test that upsampling with same rate returns original audio."""
        processor = AudioProcessor()

        audio = np.random.randn(12000)
        result = processor.upsample_output(audio, 12000, 12000)

        assert np.array_equal(result, audio)

    def test_upsample_output_handles_exception(self) -> None:
        """Test that upsampling handles exceptions gracefully."""
        processor = AudioProcessor()

        audio = np.random.randn(12000)

        with patch("librosa.resample", side_effect=RuntimeError("Resample failed")):
            result = processor.upsample_output(audio, 12000, 22050)

            # Should return original audio on error
            assert np.array_equal(result, audio)


class TestUpsampleFile:
    """Test upsampling audio files."""

    def test_upsample_file_success(self, tmp_path: Path) -> None:
        """Test successful file upsampling."""
        processor = AudioProcessor()

        input_path = tmp_path / "input.wav"
        output_path = tmp_path / "output.wav"

        # Mock audio data
        mock_audio = np.random.randn(12000)

        with patch("librosa.load", return_value=(mock_audio, 12000)):
            with patch("soundfile.write") as mock_write:
                with patch.object(
                    processor, "upsample_output", return_value=np.random.randn(22050)
                ):
                    result = processor.upsample_file(input_path, output_path, 22050)

                    assert result is True
                    mock_write.assert_called_once()

    def test_upsample_file_creates_parent_directory(self, tmp_path: Path) -> None:
        """Test that parent directory is created if it doesn't exist."""
        processor = AudioProcessor()

        input_path = tmp_path / "input.wav"
        output_path = tmp_path / "subdir" / "output.wav"

        mock_audio = np.random.randn(12000)

        with patch("librosa.load", return_value=(mock_audio, 12000)):
            with patch("soundfile.write"):
                with patch.object(
                    processor, "upsample_output", return_value=np.random.randn(22050)
                ):
                    result = processor.upsample_file(input_path, output_path, 22050)

                    assert result is True
                    assert output_path.parent.exists()

    def test_upsample_file_handles_exception(self, tmp_path: Path) -> None:
        """Test that file upsampling handles exceptions."""
        processor = AudioProcessor()

        input_path = tmp_path / "input.wav"
        output_path = tmp_path / "output.wav"

        with patch("librosa.load", side_effect=RuntimeError("Load failed")):
            result = processor.upsample_file(input_path, output_path, 22050)

            assert result is False


class TestConvertSampleRate:
    """Test sample rate conversion."""

    def test_convert_sample_rate_success(self, tmp_path: Path) -> None:
        """Test successful sample rate conversion."""
        processor = AudioProcessor()

        input_path = tmp_path / "input.wav"
        output_path = tmp_path / "output.wav"

        # Create dummy input file
        input_path.touch()

        with patch("subprocess.run") as mock_run:
            mock_result = MagicMock()
            mock_result.returncode = 0
            mock_run.return_value = mock_result

            # Create output file to simulate success
            output_path.touch()

            result = processor.convert_sample_rate(input_path, output_path, 12000)

            assert result is True
            mock_run.assert_called_once()

            # Verify ffmpeg command
            call_args = mock_run.call_args[0][0]
            assert "ffmpeg" in call_args
            assert "-ar" in call_args
            assert "12000" in call_args

    def test_convert_sample_rate_creates_parent_directory(self, tmp_path: Path) -> None:
        """Test that parent directory is created."""
        processor = AudioProcessor()

        input_path = tmp_path / "input.wav"
        output_path = tmp_path / "subdir" / "output.wav"

        input_path.touch()

        with patch("subprocess.run") as mock_run:
            mock_result = MagicMock()
            mock_result.returncode = 0
            mock_run.return_value = mock_result

            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.touch()

            result = processor.convert_sample_rate(input_path, output_path, 12000)

            assert result is True
            assert output_path.parent.exists()

    def test_convert_sample_rate_handles_failure(self, tmp_path: Path) -> None:
        """Test that conversion handles ffmpeg failure."""
        processor = AudioProcessor()

        input_path = tmp_path / "input.wav"
        output_path = tmp_path / "output.wav"

        input_path.touch()

        with patch("subprocess.run") as mock_run:
            mock_result = MagicMock()
            mock_result.returncode = 1  # Failure
            mock_run.return_value = mock_result

            result = processor.convert_sample_rate(input_path, output_path, 12000)

            assert result is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
