"""Audio Generation Domain Service.

Contains business logic for audio generation orchestration.
"""

from pathlib import Path

from ..models.voice_profile import VoiceProfile
from ..ports.tts_engine import TTSEngine


class AudioGenerationService:
    """Domain service for audio generation operations.

    This service orchestrates audio generation, applying business rules
    and coordinating between different components.

    Text Length Validation Strategy (Defense in Depth):
    - Backend validates against engine capabilities for safety
    - Soft limit (recommended_text_length): Warning logged, generation allowed
    - Hard limit (max_text_length): Error raised, generation blocked
    - UI should enforce limits proactively based on get_capabilities()
    """

    def __init__(self, tts_engine: TTSEngine):
        """Initialize the audio generation service.

        Args:
            tts_engine: TTS engine port for audio generation
        """
        self._tts_engine = tts_engine

    def generate_with_profile(
        self,
        text: str,
        profile: VoiceProfile,
        output_path: Path,
        mode: str = "clone",
        **kwargs: object,
    ) -> Path:
        """Generate audio using a voice profile.

        This method applies business rules:
        - Validates text length against engine capabilities
        - Validates profile before generation
        - Ensures text is not empty
        - Validates mode is supported

        Args:
            text: Text to convert to speech
            profile: Voice profile to use
            output_path: Where to save generated audio
            mode: Generation mode (default: "clone")
            **kwargs: Additional engine-specific parameters

        Returns:
            Path to generated audio file

        Raises:
            ValueError: If inputs are invalid (including text length violations)
            GenerationException: If generation fails
        """
        # Validate inputs
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        # Validate text length against engine capabilities
        capabilities = self._tts_engine.get_capabilities()
        text_length = len(text)

        if text_length > capabilities.max_text_length:
            raise ValueError(
                f"Text length ({text_length} characters) exceeds maximum limit "
                f"of {capabilities.max_text_length} characters for this engine. "
                f"Please split your text into smaller segments."
            )

        if text_length > capabilities.recommended_text_length:
            # This is a soft limit - log warning but allow generation
            # UI should prevent this, but backend allows it
            import logging

            logging.warning(
                f"Text length ({text_length} characters) exceeds recommended limit "
                f"of {capabilities.recommended_text_length} characters. "
                f"Quality may be degraded. Consider using shorter text for best results."
            )

        if not profile.is_valid():
            raise ValueError(f"Invalid profile: {profile.validation_errors()}")

        # Validate mode is supported
        supported_modes = self._tts_engine.get_supported_modes()
        if mode not in supported_modes:
            raise ValueError(
                f"Unsupported mode '{mode}'. "
                f"Supported modes: {', '.join(supported_modes)}"
            )

        # Validate profile is compatible with engine
        if not self._tts_engine.validate_profile(profile):
            raise ValueError("Profile is not compatible with this TTS engine")

        # Generate audio
        result_path = self._tts_engine.generate_audio(
            text=text,
            profile=profile,
            output_path=output_path,
            mode=mode,
            **kwargs,
        )

        return result_path
