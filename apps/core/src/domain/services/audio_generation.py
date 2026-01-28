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

    Note: Text length limits are enforced at the UI level based on
    engine capabilities. This service assumes text is within limits.
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
        **kwargs,
    ) -> Path:
        """Generate audio using a voice profile.

        This method applies business rules:
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
            ValueError: If inputs are invalid
            GenerationException: If generation fails
        """
        # Validate inputs
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

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
