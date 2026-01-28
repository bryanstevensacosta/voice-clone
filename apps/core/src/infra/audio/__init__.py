"""Audio processing infrastructure adapters.

Implements audio processing ports using librosa and ffmpeg.
"""

from .processor_adapter import LibrosaAudioProcessor

__all__ = ["LibrosaAudioProcessor"]
