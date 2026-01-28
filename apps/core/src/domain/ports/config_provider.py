"""Config Provider Port.

Interface for configuration management.
Infrastructure adapters (e.g., YAMLConfigProvider) must implement this interface.
"""

from abc import ABC, abstractmethod
from typing import Any


class ConfigProvider(ABC):
    """Abstract interface for configuration providers.

    This port defines the contract that all config provider adapters must implement.
    Examples: YAMLConfigProvider, EnvConfigProvider, etc.
    """

    @abstractmethod
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value.

        Args:
            key: Configuration key (can use dot notation, e.g., "model.device")
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        pass

    @abstractmethod
    def get_all(self) -> dict[str, Any]:
        """Get all configuration values.

        Returns:
            Dictionary with all configuration
        """
        pass

    @abstractmethod
    def reload(self) -> None:
        """Reload configuration from source.

        This allows updating configuration without restarting the application.
        """
        pass
