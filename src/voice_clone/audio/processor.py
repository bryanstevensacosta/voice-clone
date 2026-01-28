"""Audio processing for voice cloning."""

import subprocess
from pathlib import Path

import librosa
import numpy as np
import soundfile as sf

from voice_clone.audio.validator import ValidationResult


class AudioProcessor:
    """Handles audio processing operations."""

    def __init__(
        self,
        sample_rate: int = 12000,
        channels: int = 1,
        bit_depth: int = 16,
    ):
        """Initialize AudioProcessor.

        Args:
            sample_rate: Target sample rate in Hz (default: 12000 for Qwen3-TTS)
            channels: Target number of channels (default: 1 for mono)
            bit_depth: Target bit depth (default: 16)
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.bit_depth = bit_depth

    def validate_sample(self, file_path: Path | str) -> ValidationResult:
        """Validate audio file against Qwen3-TTS requirements.

        Checks:
        - Sample rate (warn if not 12000 Hz)
        - Channels (error if not mono)
        - Bit depth (warn if not 16-bit)
        - Duration (error if < 3s, warn if > 30s)
        - Clipping (error if detected)

        Args:
            file_path: Path to audio file

        Returns:
            ValidationResult with status, warnings, and errors
        """
        file_path = Path(file_path)
        errors = []
        warnings = []
        metadata = {}

        try:
            # Load audio file
            audio, sr = librosa.load(file_path, sr=None, mono=False)

            # Get audio info
            info = sf.info(file_path)

            # Check sample rate
            if sr != self.sample_rate:
                warnings.append(
                    f"Sample rate is {sr} Hz (recommended: {self.sample_rate} Hz)"
                )
            metadata["sample_rate"] = sr

            # Check channels
            if len(audio.shape) > 1:
                num_channels = audio.shape[0]
            else:
                num_channels = 1

            if num_channels != self.channels:
                errors.append(
                    f"Audio has {num_channels} channels (required: {self.channels} for mono)"
                )
            metadata["channels"] = num_channels

            # Check bit depth
            if hasattr(info, "subtype"):
                if "16" not in info.subtype and self.bit_depth == 16:
                    warnings.append(
                        f"Bit depth is {info.subtype} (recommended: 16-bit PCM)"
                    )
                metadata["bit_depth"] = info.subtype

            # Check duration (Qwen3-TTS requires minimum 3 seconds)
            duration = librosa.get_duration(y=audio, sr=sr)
            metadata["duration"] = duration

            if duration < 3.0:
                errors.append(
                    f"Duration is {duration:.2f}s (minimum: 3s for Qwen3-TTS)"
                )
            elif duration > 30.0:
                warnings.append(
                    f"Duration is {duration:.2f}s (recommended: 3-30s for diminishing returns)"
                )

            # Check for clipping
            if len(audio.shape) > 1:
                # Stereo: check both channels
                max_amplitude = np.max(np.abs(audio))
            else:
                # Mono
                max_amplitude = np.max(np.abs(audio))

            if max_amplitude >= 0.99:  # Close to maximum
                errors.append(
                    "Audio clipping detected (distortion). Re-record with lower volume."
                )
            metadata["max_amplitude"] = max_amplitude

            # Determine success
            success = len(errors) == 0

            return ValidationResult(
                success=success,
                errors=errors,
                warnings=warnings,
                metadata=metadata,
            )

        except Exception as e:
            return ValidationResult(
                success=False,
                errors=[f"Failed to validate audio: {str(e)}"],
                warnings=[],
                metadata={},
            )

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
        - 22050 Hz sample rate
        - Mono (1 channel)
        - 16-bit PCM WAV

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

    def normalize_loudness(
        self,
        input_path: Path | str,
        output_path: Path | str,
        target_lufs: float = -16.0,
    ) -> bool:
        """Apply EBU R128 loudness normalization using ffmpeg.

        Args:
            input_path: Input audio file path
            output_path: Output audio file path
            target_lufs: Target loudness in LUFS (default: -16)

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
                "-af",
                f"loudnorm=I={target_lufs}:TP=-1.5:LRA=11",
                "-y",
                str(output_path),
            ]

            result = subprocess.run(cmd, capture_output=True, check=False)
            return result.returncode == 0 and output_path.exists()

        except Exception:
            return False

    def apply_fade(
        self,
        input_path: Path | str,
        output_path: Path | str,
        fade_in_duration: float = 0.5,
        fade_out_duration: float = 1.0,
    ) -> bool:
        """Apply fade in/out effects to audio.

        Args:
            input_path: Input audio file path
            output_path: Output audio file path
            fade_in_duration: Fade in duration in seconds
            fade_out_duration: Fade out duration in seconds

        Returns:
            True if successful, False otherwise
        """
        input_path = Path(input_path)
        output_path = Path(output_path)

        try:
            # Get audio duration
            audio, sr = librosa.load(input_path, sr=None)
            duration = librosa.get_duration(y=audio, sr=sr)
            fade_out_start = max(0, duration - fade_out_duration)

            output_path.parent.mkdir(parents=True, exist_ok=True)

            cmd = [
                "ffmpeg",
                "-i",
                str(input_path),
                "-af",
                f"afade=t=in:st=0:d={fade_in_duration},afade=t=out:st={fade_out_start}:d={fade_out_duration}",
                "-y",
                str(output_path),
            ]

            result = subprocess.run(cmd, capture_output=True, check=False)
            return result.returncode == 0 and output_path.exists()

        except Exception:
            return False

    def remove_silence(
        self,
        input_path: Path | str,
        output_path: Path | str,
    ) -> bool:
        """Remove leading and trailing silence from audio.

        Args:
            input_path: Input audio file path
            output_path: Output audio file path

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
                "-af",
                "silenceremove=start_periods=1:stop_periods=-1:detection=peak",
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

    def resample_to_qwen3(
        self,
        input_path: Path | str,
        output_path: Path | str,
    ) -> bool:
        """Resample audio to Qwen3-TTS native format (12kHz, mono, 16-bit).

        Args:
            input_path: Input audio file path
            output_path: Output audio file path

        Returns:
            True if successful, False otherwise
        """
        return self.convert_to_target_format(input_path, output_path)

    def upsample_output(
        self,
        audio: np.ndarray,
        source_sr: int,
        target_sr: int = 22050,
    ) -> np.ndarray:
        """Upsample Qwen3-TTS output to higher sample rate.

        Useful for mixing with music or video production that requires higher sample rates.

        Args:
            audio: Audio array from Qwen3-TTS (typically 12kHz)
            source_sr: Source sample rate (typically 12000)
            target_sr: Target sample rate (default: 22050)

        Returns:
            Upsampled audio array
        """
        if source_sr == target_sr:
            return audio

        try:
            upsampled = librosa.resample(
                audio,
                orig_sr=source_sr,
                target_sr=target_sr,
                res_type="kaiser_best",
            )
            return upsampled
        except Exception as e:
            # Log error and return original
            print(f"Warning: Upsampling failed: {e}")
            return audio

    def upsample_file(
        self,
        input_path: Path | str,
        output_path: Path | str,
        target_sr: int = 22050,
    ) -> bool:
        """Upsample audio file to higher sample rate.

        Args:
            input_path: Input audio file path (typically 12kHz Qwen3-TTS output)
            output_path: Output audio file path
            target_sr: Target sample rate (default: 22050)

        Returns:
            True if successful, False otherwise
        """
        input_path = Path(input_path)
        output_path = Path(output_path)

        try:
            # Load audio
            audio, sr = librosa.load(input_path, sr=None, mono=True)

            # Upsample
            upsampled = self.upsample_output(audio, int(sr), target_sr)

            # Save
            output_path.parent.mkdir(parents=True, exist_ok=True)
            sf.write(output_path, upsampled, target_sr)

            return True

        except Exception as e:
            print(f"Error upsampling file: {e}")
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
