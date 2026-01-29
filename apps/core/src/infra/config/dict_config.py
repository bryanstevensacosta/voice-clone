"""Dictionary Configuration Provider.

Simple in-memory configuration provider for testing.
"""

import logging
from typing import Any

from domain.ports.config_provider import ConfigProvider

logger = logging.getLogger(__name__)


class DictConfigProvider(ConfigProvider):
    """Dictionary-based configuration provider.

    Simple in-memory configuration for testing purposes.
    Does not require any files.
    """

    def __init__(self, config: dict[str, Any]):
        """Initialize dict config provider.

        Args:
            config: Configuration dictionary
        """
        self._config = config.copy()

    def reload(self) -> None:
        """Reload configuration (no-op for dict provider)."""
        pass

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value using dot notation.

        Args:
            key: Configuration key (supports dot notation, e.g., "model.device")
            default: Default value if key not found

        Returns:
            Configuration value or default
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
        """Set a configuration value.

        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
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
