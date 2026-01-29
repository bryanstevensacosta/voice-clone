"""API Layer - Entry points for TTS Studio.

This layer wires together all the hexagonal architecture components
and provides a clean, simple API for external consumers (Tauri backend).
"""

from api.studio import TTSStudio

__all__ = ["TTSStudio"]
