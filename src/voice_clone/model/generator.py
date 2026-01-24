"""Text-to-speech generation using XTTS-v2."""

import re
from pathlib import Path
from typing import Any

import numpy as np
import soundfile as sf

from voice_clone.model.manager import ModelManager
from voice_clone.model.profile import VoiceProfile
from voice_clone.utils.logger import logger


class VoiceGenerator:
    """Generates speech from text using cloned voice."""

    def __init__(self, model_manager: ModelManager, config: dict[str, Any]):
        """Initialize VoiceGenerator.

        Args:
            model_manager: ModelManager instance
            config: Configuration dictionary
        """
        self.model_manager = model_manager
        self.config = config
        self.max_chunk_size = config.get("generation", {}).get("max_length", 400)
        self.language = config.get("generation", {}).get("language", "es")

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

    def _generate_chunk(
        self,
        text: str,
        voice_profile: VoiceProfile,
    ) -> np.ndarray | None:
        """Generate audio for a single text chunk.

        Args:
            text: Text chunk to generate
            voice_profile: Voice profile with reference samples

        Returns:
            Audio array or None on failure
        """
        if not self.model_manager.is_loaded():
            logger.error("Model not loaded. Call model_manager.load_model() first.")
            return None

        try:
            model = self.model_manager.get_model()
            assert model is not None, "Model is None"

            # Get reference audio paths
            speaker_wav = [
                s.path for s in voice_profile.samples[:3]
            ]  # Use first 3 samples

            # Generate audio
            audio = model.tts(
                text=text,
                speaker_wav=speaker_wav,
                language=self.language,
            )

            return np.array(audio)

        except Exception as e:
            logger.error(f"Failed to generate chunk: {str(e)}")
            return None

    def _concatenate_chunks(self, chunks: list[np.ndarray]) -> np.ndarray:
        """Concatenate audio chunks seamlessly.

        Args:
            chunks: List of audio arrays

        Returns:
            Concatenated audio array
        """
        if not chunks:
            return np.array([])

        if len(chunks) == 1:
            return chunks[0]

        # Simple concatenation (could add crossfade in future)
        return np.concatenate(chunks)

    def generate(
        self,
        text: str,
        voice_profile: VoiceProfile,
        output_path: Path | str,
    ) -> bool:
        """Generate speech from text using voice profile.

        Args:
            text: Text to convert to speech
            voice_profile: Voice profile with reference samples
            output_path: Path to save generated audio

        Returns:
            True if successful, False otherwise
        """
        output_path = Path(output_path)

        # Validate inputs
        if not text or len(text.strip()) == 0:
            logger.error("Text cannot be empty")
            return False

        if not voice_profile.samples:
            logger.error("Voice profile has no samples")
            return False

        if not self.model_manager.is_loaded():
            logger.error("Model not loaded")
            return False

        try:
            # Chunk text
            chunks = self._chunk_text(text)
            logger.info(f"Split text into {len(chunks)} chunks")

            # Generate each chunk
            audio_chunks = []
            for i, chunk in enumerate(chunks):
                logger.info(f"Generating chunk {i+1}/{len(chunks)}")
                audio = self._generate_chunk(chunk, voice_profile)

                if audio is None:
                    logger.error(f"Failed to generate chunk {i+1}")
                    return False

                audio_chunks.append(audio)

            # Concatenate chunks
            final_audio = self._concatenate_chunks(audio_chunks)

            # Save to file
            output_path.parent.mkdir(parents=True, exist_ok=True)
            sample_rate = 22050
            sf.write(output_path, final_audio, sample_rate)

            logger.info(f"✓ Generated audio saved to: {output_path}")
            return True

        except Exception as e:
            logger.error(f"Generation failed: {str(e)}")
            return False
