"""Domain services for TTS Studio.

Domain services contain business logic that doesn't naturally fit
within a single entity or value object.
"""

from .audio_generation import AudioGenerationService
from .voice_cloning import VoiceCloningService

__all__ = [
    "AudioGenerationService",
    "VoiceCloningService",
]
