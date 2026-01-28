"""Audio effects and post-processing utilities.

Provides utilities for applying effects like fade, silence removal, etc.
"""

import subprocess
from pathlib import Path

import librosa


class AudioEffects:
    """Handles audio effects and post-processing using ffmpeg."""

    @staticmethod
    def apply_fade(
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

    @staticmethod
    def remove_silence(
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

    @staticmethod
    def normalize_loudness(
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
