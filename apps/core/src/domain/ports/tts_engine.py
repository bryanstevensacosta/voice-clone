"""TTS Engine Port.

Interface for text-to-speech engines.
Infrastructure adapters (e.g., Qwen3Adapter) must implement this interface.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..models.voice_profile import VoiceProfile


@dataclass
class EngineCapabilities:
    """Capabilities and limitations of a TTS engine.

    Used by the UI to enforce appropriate limits.
    """

    max_text_length: int  # Maximum characters per generation
    recommended_text_length: int  # Recommended for best quality
    supports_streaming: bool = False  # Future: streaming generation
    min_sample_duration: float = 3.0  # Minimum seconds per sample
    max_sample_duration: float = 30.0  # Maximum seconds per sample


class TTSEngine(ABC):
    """Abstract interface for TTS engines.

    This port defines the contract that all TTS engine adapters must implement.
    Examples: Qwen3Adapter, XTTSAdapter, etc.
    """

    @abstractmethod
    def get_capabilities(self) -> EngineCapabilities:
        """Get engine capabilities and limitations.

        Returns:
            EngineCapabilities describing what this engine can do
        """
        ...

    @abstractmethod
    def get_supported_modes(self) -> list[str]:
        """Get list of supported generation modes.

        Returns:
            List of mode names (e.g., ["clone", "custom", "design"])
        """
        ...

    @abstractmethod
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
            mode: Generation mode (e.g., "clone", "custom", "design")
            **kwargs: Additional engine-specific parameters

        Returns:
            Path to the generated audio file

        Raises:
            GenerationException: If generation fails
        """
        ...

    @abstractmethod
    def validate_profile(self, profile: VoiceProfile) -> bool:
        """Validate that a profile is compatible with this engine.

        Args:
            profile: Voice profile to validate

        Returns:
            True if profile is valid for this engine
        """
        ...
