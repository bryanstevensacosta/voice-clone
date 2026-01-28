"""Qwen3-TTS Inference Engine.

Handles text-to-speech generation using Qwen3-TTS.
"""

import re
from pathlib import Path
from typing import Any

import numpy as np
import soundfile as sf

from .model_loader import Qwen3ModelLoader


class Qwen3Inference:
    """Generates speech from text using Qwen3-TTS voice cloning."""

    def __init__(self, model_loader: Qwen3ModelLoader, config: dict[str, Any]):
        """Initialize Qwen3Inference.

        Args:
            model_loader: Qwen3ModelLoader instance
            config: Configuration dictionary
        """
        self.model_loader = model_loader
        self.config = config
        self.max_chunk_size = config.get("generation", {}).get("max_length", 400)
        self.language = config.get("generation", {}).get("language", "Spanish")
        self.max_new_tokens = config.get("generation", {}).get("max_new_tokens", 2048)

    def _chunk_text(self, text: str) -> list[str]:
        """Split long text at sentence boundaries.

        Args:
            text: Input text to chunk

        Returns:
            List of text chunks
        """
        if len(text) <= self.max_chunk_size:
            return [text]

        chunks = []
        current_chunk = ""

        # Split by sentences (period, exclamation, question mark)
        sentences = re.split(r"([.!?]+\s+)", text)

        for i in range(0, len(sentences), 2):
            sentence = sentences[i]
            separator = sentences[i + 1] if i + 1 < len(sentences) else ""

            # If adding this sentence exceeds max size, save current chunk
            if (
                current_chunk
                and len(current_chunk + sentence + separator) > self.max_chunk_size
            ):
                chunks.append(current_chunk.strip())
                current_chunk = sentence + separator
            else:
                current_chunk += sentence + separator

        # Add remaining chunk
        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    def generate(
        self,
        text: str,
        ref_audio: str | Path,
        ref_text: str,
        language: str | None = None,
        max_new_tokens: int | None = None,
    ) -> tuple[np.ndarray, int] | None:
        """Generate audio with voice cloning using Qwen3-TTS.

        Args:
            text: Text to convert to speech
            ref_audio: Path to reference audio file
            ref_text: Transcript of reference audio
            language: Language for generation (default: from config)
            max_new_tokens: Maximum tokens to generate (default: from config)

        Returns:
            Tuple of (audio_array, sample_rate) or None on failure
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

            # Generate using Qwen3-TTS
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

    def generate_batch(
        self,
        texts: list[str],
        ref_audio: str | Path,
        ref_text: str,
        **kwargs: Any,
    ) -> list[tuple[np.ndarray, int]]:
        """Generate multiple audio files with same voice.

        Args:
            texts: List of texts to generate
            ref_audio: Path to reference audio file
            ref_text: Transcript of reference audio
            **kwargs: Additional arguments for generate()

        Returns:
            List of (audio_array, sample_rate) tuples
        """
        results = []

        for text in texts:
            result = self.generate(text, ref_audio, ref_text, **kwargs)

            if result is None:
                continue

            results.append(result)

        return results

    def generate_to_file(
        self,
        text: str,
        ref_audio: str | Path,
        ref_text: str,
        output_path: Path | str,
        language: str | None = None,
        max_new_tokens: int | None = None,
    ) -> bool:
        """Generate speech and save to file.

        Args:
            text: Text to convert to speech
            ref_audio: Path to reference audio file
            ref_text: Transcript of reference audio
            output_path: Path to save generated audio
            language: Language for generation (default: from config)
            max_new_tokens: Maximum tokens to generate (default: from config)

        Returns:
            True if successful, False otherwise
        """
        output_path = Path(output_path)

        # Validate inputs
        if not text or len(text.strip()) == 0:
            raise ValueError("Text cannot be empty")

        if not Path(ref_audio).exists():
            raise FileNotFoundError(f"Reference audio not found: {ref_audio}")

        if not ref_text or len(ref_text.strip()) == 0:
            raise ValueError("Reference text cannot be empty")

        if not self.model_loader.is_loaded():
            raise RuntimeError("Model not loaded")

        try:
            # Generate audio
            result = self.generate(text, ref_audio, ref_text, language, max_new_tokens)

            if result is None:
                return False

            audio, sample_rate = result

            # Save to file
            output_path.parent.mkdir(parents=True, exist_ok=True)
            sf.write(output_path, audio, sample_rate)

            return True

        except Exception as e:
            raise RuntimeError(f"Generation failed: {str(e)}") from e
