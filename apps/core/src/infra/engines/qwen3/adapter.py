"""Qwen3-TTS Engine Adapter.

Implements the TTSEngine port using Qwen3-TTS.
"""

from pathlib import Path
from typing import Any

from domain.exceptions import GenerationException
from domain.models.voice_profile import VoiceProfile
from domain.ports.tts_engine import TTSEngine

from .inference import Qwen3Inference
from .model_loader import Qwen3ModelLoader


class Qwen3Adapter(TTSEngine):
    """Qwen3-TTS implementation of TTSEngine port.

    This adapter wraps Qwen3-TTS functionality and exposes it through
    the TTSEngine interface defined in the domain layer.
    """

    def __init__(self, config: dict[str, Any]):
        """Initialize Qwen3Adapter.

        Args:
            config: Configuration dictionary with model settings
        """
        self.config = config
        self.model_loader = Qwen3ModelLoader(config)
        self.inference: Qwen3Inference | None = None
        self._loaded = False

    def get_supported_modes(self) -> list[str]:
        """Get list of supported generation modes.

        Qwen3-TTS supports:
        - clone: Voice cloning with reference audio
        - custom: Custom voice with multiple samples (future)
        - design: Voice design from scratch (future)

        Returns:
            List of mode names
        """
        return ["clone"]  # Only clone mode implemented for now

    def generate_audio(
        self,
        text: str,
        profile: VoiceProfile,
        output_path: Path,
        mode: str = "clone",
        **kwargs: Any,
    ) -> Path:
        """Generate audio from text using a voice profile.

        Args:
            text: Text to convert to speech
            profile: Voice profile to use for generation
            output_path: Where to save the generated audio
            mode: Generation mode (default: "clone")
            **kwargs: Additional parameters:
                - language: Language for generation (default: from config)
                - max_new_tokens: Maximum tokens to generate (default: from config)
                - temperature: Sampling temperature (default: 0.75)

        Returns:
            Path to the generated audio file

        Raises:
            GenerationException: If generation fails
        """
        # Validate mode
        if mode not in self.get_supported_modes():
            raise GenerationException(
                f"Unsupported mode: {mode}. Supported modes: {self.get_supported_modes()}",
                profile_id=profile.id,
                text_length=len(text),
            )

        # Validate profile
        if not self.validate_profile(profile):
            raise GenerationException(
                f"Invalid profile: {profile.id}",
                profile_id=profile.id,
                text_length=len(text),
            )

        # Ensure model is loaded
        if not self._loaded:
            if not self.model_loader.load_model():
                raise GenerationException(
                    "Failed to load Qwen3-TTS model",
                    profile_id=profile.id,
                    text_length=len(text),
                )
            self.inference = Qwen3Inference(self.model_loader, self.config)
            self._loaded = True

        # Generate audio
        try:
            assert self.inference is not None, "Inference engine not initialized"

            # Use first sample as reference (clone mode)
            if not profile.samples:
                raise GenerationException(
                    "Profile has no samples",
                    profile_id=profile.id,
                    text_length=len(text),
                )

            ref_sample = profile.samples[0]

            # Generate
            success = self.inference.generate_to_file(
                text=text,
                ref_audio=ref_sample.path,
                ref_text=profile.reference_text or "Reference audio sample",
                output_path=output_path,
                **kwargs,
            )

            if not success:
                raise GenerationException(
                    "Audio generation failed",
                    profile_id=profile.id,
                    text_length=len(text),
                )

            return output_path

        except GenerationException:
            raise
        except Exception as e:
            raise GenerationException(
                f"Unexpected error during generation: {str(e)}",
                profile_id=profile.id,
                text_length=len(text),
            ) from e

    def validate_profile(self, profile: VoiceProfile) -> bool:
        """Validate that a profile is compatible with Qwen3-TTS.

        Args:
            profile: Voice profile to validate

        Returns:
            True if profile is valid for Qwen3-TTS
        """
        # Check profile has at least one sample
        if not profile.samples:
            return False

        # Check samples are valid
        for sample in profile.samples:
            # Check sample file exists
            if not sample.path.exists():
                return False

            # Check sample duration (3-30 seconds recommended)
            if sample.duration < 3.0 or sample.duration > 30.0:
                return False

        # Check total duration (at least 10 seconds recommended)
        if profile.total_duration < 10.0:
            return False

        return True

    def unload_model(self) -> None:
        """Unload model and free memory."""
        if self._loaded:
            self.model_loader.unload_model()
            self.inference = None
            self._loaded = False

    def is_loaded(self) -> bool:
        """Check if model is loaded.

        Returns:
            True if model is loaded
        """
        return self._loaded
