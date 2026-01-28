"""Qwen3-TTS Generation Modes.

Different modes for voice generation:
- clone: Voice cloning with reference audio
- custom: Custom voice with multiple samples (future)
- design: Voice design from scratch (future)
"""

from .clone_mode import CloneMode

__all__ = ["CloneMode"]
