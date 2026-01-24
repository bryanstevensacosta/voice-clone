"""Configuration management for voice cloning.

This module handles loading, merging, and validating configuration files.
"""
from pathlib import Path
from typing import Any, cast

import yaml  # type: ignore[import-untyped]


class ConfigManager:
    """Manages configuration loading and validation."""

    DEFAULT_CONFIG_PATH = Path("config/default.yaml")
    USER_CONFIG_PATH = Path("config/config.yaml")

    @classmethod
    def load_config(cls, user_config_path: Path | None = None) -> dict[str, Any]:
        """Load and merge configurations.

        Loads default configuration and merges with user configuration if it exists.

        Args:
            user_config_path: Optional path to user configuration file.
                            Defaults to config/config.yaml

        Returns:
            Merged configuration dictionary

        Raises:
            FileNotFoundError: If default config file doesn't exist
            yaml.YAMLError: If config files are invalid YAML
        """
        # Load default config
        if not cls.DEFAULT_CONFIG_PATH.exists():
            raise FileNotFoundError(
                f"Default configuration not found: {cls.DEFAULT_CONFIG_PATH}"
            )

        with open(cls.DEFAULT_CONFIG_PATH) as f:
            config = cast(dict[str, Any], yaml.safe_load(f))

        # Load and merge user config if it exists
        user_path = user_config_path or cls.USER_CONFIG_PATH
        if user_path.exists():
            with open(user_path) as f:
                user_config = cast(dict[str, Any] | None, yaml.safe_load(f))
                if user_config:
                    config = cls._merge_configs(config, user_config)

        # Validate the merged configuration
        validation_result = cls.validate_config(config)
        if not validation_result["valid"]:
            # Log warnings but use defaults for invalid values
            for error in validation_result["errors"]:
                print(f"Warning: {error}")

        return config

    @classmethod
    def _merge_configs(
        cls, default: dict[str, Any], user: dict[str, Any]
    ) -> dict[str, Any]:
        """Recursively merge user config into default config.

        Args:
            default: Default configuration dictionary
            user: User configuration dictionary

        Returns:
            Merged configuration dictionary
        """
        merged = default.copy()

        for key, value in user.items():
            if (
                key in merged
                and isinstance(merged[key], dict)
                and isinstance(value, dict)
            ):
                merged[key] = cls._merge_configs(merged[key], value)
            else:
                merged[key] = value

        return merged

    @classmethod
    def validate_config(cls, config: dict[str, Any]) -> dict[str, Any]:
        """Validate configuration parameters.

        Checks that all required parameters are present and within valid ranges.

        Args:
            config: Configuration dictionary to validate

        Returns:
            Dictionary with 'valid' boolean and 'errors' list
        """
        errors: list[str] = []

        # Validate temperature (0.5-1.0)
        if "generation" in config and "temperature" in config["generation"]:
            temp = config["generation"]["temperature"]
            if not isinstance(temp, int | float) or not (0.5 <= temp <= 1.0):
                errors.append(
                    f"Invalid temperature: {temp}. Must be between 0.5 and 1.0. "
                    "Using default: 0.75"
                )
                config["generation"]["temperature"] = 0.75

        # Validate speed (0.8-1.2)
        if "generation" in config and "speed" in config["generation"]:
            speed = config["generation"]["speed"]
            if not isinstance(speed, int | float) or not (0.8 <= speed <= 1.2):
                errors.append(
                    f"Invalid speed: {speed}. Must be between 0.8 and 1.2. "
                    "Using default: 1.0"
                )
                config["generation"]["speed"] = 1.0

        # Validate sample rate
        if "audio" in config and "sample_rate" in config["audio"]:
            sample_rate = config["audio"]["sample_rate"]
            if not isinstance(sample_rate, int) or sample_rate <= 0:
                errors.append(
                    f"Invalid sample_rate: {sample_rate}. Must be a positive integer. "
                    "Using default: 22050"
                )
                config["audio"]["sample_rate"] = 22050

        # Validate paths exist (create if they don't)
        if "paths" in config:
            for path_key in ["samples", "outputs", "models", "cache"]:
                if path_key in config["paths"]:
                    path = Path(config["paths"][path_key])
                    if not path.exists():
                        try:
                            path.mkdir(parents=True, exist_ok=True)
                        except Exception as e:
                            errors.append(f"Cannot create directory {path}: {e}")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
        }

    @classmethod
    def get_default_config(cls) -> dict[str, Any]:
        """Return default configuration.

        Returns:
            Default configuration dictionary
        """
        return {
            "model": {
                "name": "tts_models/multilingual/multi-dataset/xtts_v2",
                "device": "auto",
            },
            "audio": {
                "sample_rate": 22050,
                "format": "wav",
                "mono": True,
                "channels": 1,
                "bit_depth": 16,
            },
            "paths": {
                "samples": "./data/samples",
                "outputs": "./data/outputs",
                "models": "./data/models",
                "cache": "./data/cache",
            },
            "generation": {
                "language": "es",
                "temperature": 0.75,
                "speed": 1.0,
                "max_length": 400,
                "repetition_penalty": 2.0,
                "top_k": 50,
                "top_p": 0.85,
            },
            "performance": {
                "use_gpu": True,
                "fp16": True,
                "batch_size": 1,
                "max_memory_allocated": "8GB",
                "clear_cache_between_batches": True,
            },
            "logging": {
                "level": "INFO",
                "format": "%(message)s",
                "rich_tracebacks": True,
            },
        }
