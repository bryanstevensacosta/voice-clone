"""YAML Configuration Provider.

Implementation of ConfigProvider port using YAML files.
Supports default config + user overrides pattern.
"""

import logging
from pathlib import Path
from typing import Any

import yaml

from domain.ports.config_provider import ConfigProvider

logger = logging.getLogger(__name__)


class YAMLConfigProvider(ConfigProvider):
    """YAML-based configuration provider.

    Loads configuration from YAML files with support for:
    - Default configuration (version controlled)
    - User overrides (git-ignored)
    - Dot notation for nested keys (e.g., "model.device")
    - Configuration reloading without restart
    """

    def __init__(self, default_config_path: Path, user_config_path: Path | None = None):
        """Initialize YAML config provider.

        Args:
            default_config_path: Path to default config file (required)
            user_config_path: Path to user config file (optional overrides)
        """
        self.default_config_path = Path(default_config_path)
        self.user_config_path = Path(user_config_path) if user_config_path else None
        self._config: dict[str, Any] = {}
        self.reload()

    def reload(self) -> None:
        """Reload configuration from YAML files.

        Loads default config first, then merges user config if it exists.
        """
        # Load default config
        if not self.default_config_path.exists():
            raise FileNotFoundError(
                f"Default config not found: {self.default_config_path}"
            )

        with open(self.default_config_path, encoding="utf-8") as f:
            self._config = yaml.safe_load(f) or {}

        logger.debug(f"Loaded default config from {self.default_config_path}")

        # Merge user config if it exists
        if self.user_config_path and self.user_config_path.exists():
            with open(self.user_config_path, encoding="utf-8") as f:
                user_config = yaml.safe_load(f) or {}

            self._merge_config(self._config, user_config)
            logger.debug(f"Merged user config from {self.user_config_path}")
        else:
            logger.debug("No user config found, using defaults only")

    def _merge_config(self, base: dict[str, Any], override: dict[str, Any]) -> None:
        """Recursively merge override config into base config.

        Args:
            base: Base configuration dictionary (modified in place)
            override: Override configuration dictionary
        """
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                # Recursively merge nested dictionaries
                self._merge_config(base[key], value)
            else:
                # Override value
                base[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value using dot notation.

        Args:
            key: Configuration key (supports dot notation, e.g., "model.device")
            default: Default value if key not found

        Returns:
            Configuration value or default

        Examples:
            >>> config.get("model.device")
            "mps"
            >>> config.get("model.name")
            "Qwen/Qwen3-TTS-12Hz-1.7B-Base"
            >>> config.get("nonexistent.key", "fallback")
            "fallback"
        """
        # Split key by dots for nested access
        keys = key.split(".")
        value = self._config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def get_all(self) -> dict[str, Any]:
        """Get all configuration values.

        Returns:
            Complete configuration dictionary
        """
        return self._config.copy()

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value (runtime only, not persisted).

        Args:
            key: Configuration key (supports dot notation)
            value: Value to set

        Note:
            This only modifies the in-memory configuration.
            Changes are not persisted to disk.
        """
        keys = key.split(".")
        config = self._config

        # Navigate to the parent dictionary
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        # Set the value
        config[keys[-1]] = value
        logger.debug(f"Set config: {key} = {value}")

    def has(self, key: str) -> bool:
        """Check if a configuration key exists.

        Args:
            key: Configuration key (supports dot notation)

        Returns:
            True if key exists, False otherwise
        """
        keys = key.split(".")
        value = self._config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return False

        return True
