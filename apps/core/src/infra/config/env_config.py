"""Environment Variable Configuration Provider.

Implementation of ConfigProvider port using environment variables.
Useful for deployment and CI/CD environments.
"""

import logging
import os
from typing import Any

from ...domain.ports.config_provider import ConfigProvider

logger = logging.getLogger(__name__)


class EnvConfigProvider(ConfigProvider):
    """Environment variable-based configuration provider.

    Reads configuration from environment variables with support for:
    - Prefix filtering (e.g., only read TTS_* variables)
    - Type conversion (string, int, float, bool)
    - Default values
    - Dot notation mapping (TTS_MODEL_DEVICE -> model.device)
    """

    def __init__(self, prefix: str = "TTS_", separator: str = "_"):
        """Initialize environment config provider.

        Args:
            prefix: Prefix for environment variables (default: "TTS_")
            separator: Separator for nested keys (default: "_")

        Examples:
            TTS_MODEL_DEVICE=mps -> model.device = "mps"
            TTS_AUDIO_SAMPLE_RATE=12000 -> audio.sample_rate = 12000
        """
        self.prefix = prefix
        self.separator = separator
        self._config: dict[str, Any] = {}
        self.reload()

    def reload(self) -> None:
        """Reload configuration from environment variables."""
        self._config = {}

        # Find all environment variables with our prefix
        for key, value in os.environ.items():
            if key.startswith(self.prefix):
                # Remove prefix and convert to nested dict
                config_key = key[len(self.prefix) :].lower()
                self._set_nested(config_key, self._convert_type(value))

        logger.debug(f"Loaded {len(self._config)} config values from environment")

    def _set_nested(self, key: str, value: Any) -> None:
        """Set a nested configuration value.

        Args:
            key: Key with separators (e.g., "model_device")
            value: Value to set
        """
        keys = key.split(self.separator)
        config = self._config

        # Navigate to parent dictionary
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        # Set value
        config[keys[-1]] = value

    def _convert_type(self, value: str) -> Any:
        """Convert string value to appropriate type.

        Args:
            value: String value from environment

        Returns:
            Converted value (int, float, bool, or str)
        """
        # Try boolean
        if value.lower() in ("true", "yes", "1", "on"):
            return True
        if value.lower() in ("false", "no", "0", "off"):
            return False

        # Try integer
        try:
            return int(value)
        except ValueError:
            pass

        # Try float
        try:
            return float(value)
        except ValueError:
            pass

        # Return as string
        return value

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value using dot notation.

        Args:
            key: Configuration key (supports dot notation)
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
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

    def set_env(self, key: str, value: str) -> None:
        """Set an environment variable (for testing).

        Args:
            key: Environment variable name (without prefix)
            value: Value to set

        Note:
            This modifies os.environ. Call reload() to update config.
        """
        env_key = f"{self.prefix}{key.upper()}"
        os.environ[env_key] = str(value)
        logger.debug(f"Set environment variable: {env_key} = {value}")
