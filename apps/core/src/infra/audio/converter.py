"""Audio format conversion utilities.

Provides utilities for converting audio between different formats using ffmpeg.
"""

import subprocess
from pathlib import Path


class AudioConverter:
    """Handles audio format conversions using ffmpeg."""

    def __init__(
        self,
        sample_rate: int = 12000,
        channels: int = 1,
        bit_depth: int = 16,
    ):
        """Initialize AudioConverter.

        Args:
            sample_rate: Target sample rate in Hz (default: 12000 for Qwen3-TTS)
            channels: Target number of channels (default: 1 for mono)
            bit_depth: Target bit depth (default: 16)
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.bit_depth = bit_depth

    def convert_to_target_format(
        self,
        input_path: Path | str,
        output_path: Path | str,
    ) -> bool:
        """Convert audio to Qwen3-TTS native format using ffmpeg.

        Converts to:
        - Sample rate: 12000 Hz (Qwen3-TTS native)
        - Channels: Mono
        - Format: WAV PCM 16-bit

        Args:
            input_path: Input audio file path
            output_path: Output audio file path

        Returns:
            True if successful, False otherwise
        """
        input_path = Path(input_path)
        output_path = Path(output_path)

        try:
            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Build ffmpeg command
            cmd = [
                "ffmpeg",
                "-i",
                str(input_path),
                "-ar",
                str(self.sample_rate),
                "-ac",
                str(self.channels),
                "-sample_fmt",
                "s16",  # 16-bit
                "-y",  # Overwrite output file
                str(output_path),
            ]

            # Run ffmpeg
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False,
            )

            if result.returncode != 0:
                print(f"FFmpeg error: {result.stderr}")
                return False

            return output_path.exists()

        except Exception as e:
            print(f"Conversion failed: {str(e)}")
            return False

    def convert_sample_rate(
        self,
        input_path: Path | str,
        output_path: Path | str,
        target_sr: int,
    ) -> bool:
        """Convert audio file to specific sample rate using ffmpeg.

        Args:
            input_path: Input audio file path
            output_path: Output audio file path
            target_sr: Target sample rate in Hz

        Returns:
            True if successful, False otherwise
        """
        input_path = Path(input_path)
        output_path = Path(output_path)

        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)

            cmd = [
                "ffmpeg",
                "-i",
                str(input_path),
                "-ar",
                str(target_sr),
                "-y",
                str(output_path),
            ]

            result = subprocess.run(cmd, capture_output=True, check=False)
            return result.returncode == 0 and output_path.exists()

        except Exception:
            return False

    def export_format(
        self,
        input_path: Path | str,
        output_path: Path | str,
        format_type: str,
        bitrate: str = "192k",
    ) -> bool:
        """Export audio to specified format.

        Args:
            input_path: Input audio file path
            output_path: Output audio file path
            format_type: Format type ('mp3', 'aac', 'flac')
            bitrate: Bitrate for lossy formats

        Returns:
            True if successful, False otherwise
        """
        input_path = Path(input_path)
        output_path = Path(output_path)

        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)

            if format_type == "mp3":
                cmd = [
                    "ffmpeg",
                    "-i",
                    str(input_path),
                    "-codec:a",
                    "libmp3lame",
                    "-b:a",
                    bitrate,
                    "-y",
                    str(output_path),
                ]
            elif format_type == "aac":
                cmd = [
                    "ffmpeg",
                    "-i",
                    str(input_path),
                    "-codec:a",
                    "aac",
                    "-b:a",
                    bitrate,
                    "-y",
                    str(output_path),
                ]
            elif format_type == "flac":
                cmd = [
                    "ffmpeg",
                    "-i",
                    str(input_path),
                    "-codec:a",
                    "flac",
                    "-compression_level",
                    "8",
                    "-y",
                    str(output_path),
                ]
            else:
                return False

            result = subprocess.run(cmd, capture_output=True, check=False)
            return result.returncode == 0 and output_path.exists()

        except Exception:
            return False
