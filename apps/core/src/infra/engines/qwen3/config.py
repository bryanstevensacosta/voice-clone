"""Qwen3-TTS Configuration.

Default configuration for Qwen3-TTS engine.
"""

from typing import Any


def get_default_config() -> dict[str, Any]:
    """Get default Qwen3-TTS configuration.

    Returns:
        Configuration dictionary
    """
    return {
        "model": {
            "name": "Qwen/Qwen3-TTS-12Hz-1.7B-Base",
            "device": "auto",  # auto, mps, cpu, cuda
            "dtype": "float32",  # float32, float16, bfloat16
        },
        "paths": {
            "models": "./data/models",
            "samples": "./data/samples",
            "outputs": "./data/outputs",
            "profiles": "./data/profiles",
        },
        "generation": {
            "language": "Spanish",
            "max_length": 400,  # Max characters per chunk
            "max_new_tokens": 2048,  # Max tokens to generate
            "temperature": 0.75,  # Sampling temperature
        },
        "audio": {
            "sample_rate": 12000,  # Native Qwen3-TTS sample rate
            "format": "wav",
            "mono": True,
        },
    }


def merge_config(user_config: dict[str, Any]) -> dict[str, Any]:
    """Merge user config with defaults.

    Args:
        user_config: User-provided configuration

    Returns:
        Merged configuration
    """
    default = get_default_config()

    # Deep merge
    def deep_merge(base: dict, override: dict) -> dict:
        result = base.copy()
        for key, value in override.items():
            if (
                key in result
                and isinstance(result[key], dict)
                and isinstance(value, dict)
            ):
                result[key] = deep_merge(result[key], value)
            else:
                result[key] = value
        return result

    return deep_merge(default, user_config)
