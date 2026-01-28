"""Domain ports (interfaces) for TTS Studio.

Ports define the contracts that infrastructure adapters must implement.
This follows the Dependency Inversion Principle - domain defines interfaces,
infrastructure provides implementations.
"""

from apps.core.src.domain.ports.audio_processor import AudioProcessor
from apps.core.src.domain.ports.config_provider import ConfigProvider
from apps.core.src.domain.ports.profile_repository import ProfileRepository
from apps.core.src.domain.ports.tts_engine import TTSEngine

__all__ = [
    "AudioProcessor",
    "ConfigProvider",
    "ProfileRepository",
    "TTSEngine",
]
