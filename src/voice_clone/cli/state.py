"""CLI state management."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from voice_clone.config import ConfigManager
from voice_clone.model.manager import ModelManager
from voice_clone.model.profile import VoiceProfile


@dataclass
class CLIState:
    """Manages the state of the CLI application."""

    # Configuration
    config_manager: Optional[ConfigManager] = None
    config: Optional[dict] = None

    # Voice profile
    current_profile: Optional[VoiceProfile] = None
    current_profile_path: Optional[Path] = None

    # Model
    model_manager: Optional[ModelManager] = None
    model_loaded: bool = False

    # Recent paths
    recent_samples_dir: Optional[Path] = None
    recent_output_dir: Optional[Path] = None

    def load_config(self) -> dict:
        """Load configuration if not already loaded."""
        if self.config is None:
            self.config_manager = ConfigManager()
            self.config = self.config_manager.load_config()
        return self.config

    def load_profile(self, profile_path: Path) -> VoiceProfile:
        """Load voice profile."""
        self.current_profile = VoiceProfile.from_json(profile_path)
        self.current_profile_path = profile_path
        return self.current_profile

    def load_model(self) -> bool:
        """Load TTS model if not already loaded."""
        if not self.model_loaded:
            config = self.load_config()
            self.model_manager = ModelManager(config)
            self.model_loaded = self.model_manager.load_model()
        return self.model_loaded

    def unload_model(self) -> None:
        """Unload TTS model to free memory."""
        if self.model_manager:
            self.model_manager.unload_model()
        self.model_loaded = False

    def reset(self) -> None:
        """Reset state (useful for testing)."""
        self.current_profile = None
        self.current_profile_path = None
        self.unload_model()
