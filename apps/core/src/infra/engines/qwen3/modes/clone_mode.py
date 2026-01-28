"""Clone Mode Implementation for Qwen3-TTS.

Voice cloning mode uses reference audio samples to clone a voice.
"""

from pathlib import Path
from typing import Any

import numpy as np

from ..model_loader import Qwen3ModelLoader


class CloneMode:
    """Voice cloning mode implementation.

    This mode uses reference audio samples to clone a voice and generate
    speech with that voice.
    """

    def __init__(self, model_loader: Qwen3ModelLoader, config: dict[str, Any]):
        """Initialize CloneMode.

        Args:
            model_loader: Qwen3ModelLoader instance
            config: Configuration dictionary
        """
        self.model_loader = model_loader
        self.config = config
        self.language = config.get("generation", {}).get("language", "Spanish")
        self.max_new_tokens = config.get("generation", {}).get("max_new_tokens", 2048)

    def generate(
        self,
        text: str,
        ref_audio: str | Path,
        ref_text: str,
        language: str | None = None,
        max_new_tokens: int | None = None,
    ) -> tuple[np.ndarray, int]:
        """Generate audio with voice cloning.

        Args:
            text: Text to convert to speech
            ref_audio: Path to reference audio file
            ref_text: Transcript of reference audio
            language: Language for generation (default: from config)
            max_new_tokens: Maximum tokens to generate (default: from config)

        Returns:
            Tuple of (audio_array, sample_rate)

        Raises:
            RuntimeError: If model is not loaded or generation fails
        """
        if not self.model_loader.is_loaded():
            raise RuntimeError(
                "Model not loaded. Call model_loader.load_model() first."
            )

        try:
            model = self.model_loader.get_model()
            assert model is not None, "Model is None"

            # Use config defaults if not specified
            if language is None:
                language = self.language
            if max_new_tokens is None:
                max_new_tokens = self.max_new_tokens

            # Convert ref_audio to string
            ref_audio_str = str(ref_audio)

            # Generate using Qwen3-TTS voice cloning
            audio, sample_rate = model.generate_voice_clone(
                text=text,
                language=language,
                ref_audio=ref_audio_str,
                ref_text=ref_text,
                max_new_tokens=max_new_tokens,
            )

            return audio, sample_rate

        except Exception as e:
            raise RuntimeError(f"Failed to generate audio: {str(e)}") from e

    def validate_inputs(self, text: str, ref_audio: str | Path, ref_text: str) -> None:
        """Validate inputs for clone mode generation.

        Args:
            text: Text to convert to speech
            ref_audio: Path to reference audio file
            ref_text: Transcript of reference audio

        Raises:
            ValueError: If inputs are invalid
            FileNotFoundError: If reference audio doesn't exist
        """
        if not text or len(text.strip()) == 0:
            raise ValueError("Text cannot be empty")

        if not Path(ref_audio).exists():
            raise FileNotFoundError(f"Reference audio not found: {ref_audio}")

        if not ref_text or len(ref_text.strip()) == 0:
            raise ValueError("Reference text cannot be empty")
