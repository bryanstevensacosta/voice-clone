"""Domain models for TTS Studio.

This module contains pure business entities and value objects.
NO infrastructure dependencies allowed.
"""

from .audio_sample import AudioSample
from .voice_profile import VoiceProfile

__all__ = ["AudioSample", "VoiceProfile"]
