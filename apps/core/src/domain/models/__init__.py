"""Domain models for TTS Studio.

This module contains pure business entities and value objects.
NO infrastructure dependencies allowed.
"""

from apps.core.src.domain.models.audio_sample import AudioSample
from apps.core.src.domain.models.voice_profile import VoiceProfile

__all__ = ["AudioSample", "VoiceProfile"]
