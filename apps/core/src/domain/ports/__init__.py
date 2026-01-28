"""Domain ports (interfaces) for TTS Studio.

Ports define the contracts that infrastructure adapters must implement.
This follows the Dependency Inversion Principle - domain defines interfaces,
infrastructure provides implementations.
"""

from .audio_processor import AudioProcessor
from .config_provider import ConfigProvider
from .profile_repository import ProfileRepository
from .tts_engine import TTSEngine

__all__ = [
    "AudioProcessor",
    "ConfigProvider",
    "ProfileRepository",
    "TTSEngine",
]
