"""Property-based tests for configuration management.

Tests universal properties of configuration loading, merging, and validation.
"""

from typing import Any

from hypothesis import given
from hypothesis import strategies as st

from voice_clone.config import ConfigManager


# Hypothesis strategies for generating test data
@st.composite
def config_dict(draw: Any) -> dict[str, Any]:
    """Generate a valid configuration dictionary."""
    return {
        "model": {
            "name": draw(st.text(min_size=1, max_size=50)),
            "device": draw(st.sampled_from(["auto", "cpu", "cuda", "mps"])),
        },
        "audio": {
            "sample_rate": draw(st.integers(min_value=8000, max_value=48000)),
            "format": draw(st.sampled_from(["wav", "mp3", "flac"])),
        },
        "generation": {
            "temperature": draw(st.floats(min_value=0.1, max_value=2.0)),
            "speed": draw(st.floats(min_value=0.5, max_value=2.0)),
        },
    }


@given(user_config=config_dict())
def test_property_32_configuration_merging(user_config: dict[str, Any]) -> None:
    """Property 32: Configuration merging.

    Feature: voice-clone-cli, Property 32: Configuration merging

    For any custom configuration file provided, the resulting configuration
    should contain all default values with custom values overriding defaults
    where specified.

    Validates: Requirements 8.2
    """
    # Get default config
    default_config = ConfigManager.get_default_config()

    # Merge user config into default
    merged = ConfigManager._merge_configs(default_config, user_config)

    # Property: All default keys should still exist
    for key in default_config:
        assert key in merged, f"Default key {key} missing after merge"

    # Property: User values should override defaults
    for key, value in user_config.items():
        if key in merged:
            if isinstance(value, dict):
                # For nested dicts, check that user values are present
                for subkey, subvalue in value.items():
                    assert (
                        merged[key][subkey] == subvalue
                    ), f"User value not applied: {key}.{subkey}"
            else:
                assert merged[key] == value, f"User value not applied: {key}"


def test_property_32_empty_user_config() -> None:
    """Test that empty user config returns default config."""
    default_config = ConfigManager.get_default_config()
    merged = ConfigManager._merge_configs(default_config, {})

    assert merged == default_config, "Empty user config should return default config"


def test_property_32_partial_override() -> None:
    """Test that partial user config only overrides specified values."""
    default_config = ConfigManager.get_default_config()
    user_config = {
        "generation": {
            "temperature": 0.9,
        }
    }

    merged = ConfigManager._merge_configs(default_config, user_config)

    # Temperature should be overridden
    assert merged["generation"]["temperature"] == 0.9

    # Other generation values should remain default
    assert merged["generation"]["speed"] == default_config["generation"]["speed"]
    assert merged["generation"]["language"] == default_config["generation"]["language"]

    # Other sections should remain unchanged
    assert merged["model"] == default_config["model"]
    assert merged["audio"] == default_config["audio"]


@given(temperature=st.floats(min_value=0.5, max_value=1.0))
def test_property_33_temperature_validation_valid(temperature: float) -> None:
    """Property 33: Temperature validation (valid range).

    Feature: voice-clone-cli, Property 33: Temperature validation

    For any configuration with a temperature parameter, values between 0.5 and 1.0
    (inclusive) should be accepted.

    Validates: Requirements 8.3
    """
    config = {
        "generation": {
            "temperature": temperature,
        }
    }

    result = ConfigManager.validate_config(config)

    # Valid temperature should not produce errors
    assert result["valid"], f"Valid temperature {temperature} was rejected"
    assert len(result["errors"]) == 0
    assert config["generation"]["temperature"] == temperature


@given(
    temperature=st.one_of(
        st.floats(max_value=0.49),
        st.floats(min_value=1.01),
    )
)
def test_property_33_temperature_validation_invalid(temperature: float) -> None:
    """Property 33: Temperature validation (invalid range).

    Feature: voice-clone-cli, Property 33: Temperature validation

    For any configuration with a temperature parameter, values outside the range
    0.5-1.0 should be rejected with a validation error.

    Validates: Requirements 8.3
    """
    config = {
        "generation": {
            "temperature": temperature,
        }
    }

    result = ConfigManager.validate_config(config)

    # Invalid temperature should produce error and use default
    assert not result["valid"], f"Invalid temperature {temperature} was accepted"
    assert len(result["errors"]) > 0
    assert config["generation"]["temperature"] == 0.75  # Default value


@given(speed=st.floats(min_value=0.8, max_value=1.2))
def test_property_34_speed_validation_valid(speed: float) -> None:
    """Property 34: Speed validation (valid range).

    Feature: voice-clone-cli, Property 34: Speed validation

    For any configuration with a speed parameter, values between 0.8 and 1.2
    (inclusive) should be accepted.

    Validates: Requirements 8.4
    """
    config = {
        "generation": {
            "speed": speed,
        }
    }

    result = ConfigManager.validate_config(config)

    # Valid speed should not produce errors
    assert result["valid"], f"Valid speed {speed} was rejected"
    assert len(result["errors"]) == 0
    assert config["generation"]["speed"] == speed


@given(
    speed=st.one_of(
        st.floats(max_value=0.79),
        st.floats(min_value=1.21),
    )
)
def test_property_34_speed_validation_invalid(speed: float) -> None:
    """Property 34: Speed validation (invalid range).

    Feature: voice-clone-cli, Property 34: Speed validation

    For any configuration with a speed parameter, values outside the range
    0.8-1.2 should be rejected with a validation error.

    Validates: Requirements 8.4
    """
    config = {
        "generation": {
            "speed": speed,
        }
    }

    result = ConfigManager.validate_config(config)

    # Invalid speed should produce error and use default
    assert not result["valid"], f"Invalid speed {speed} was accepted"
    assert len(result["errors"]) > 0
    assert config["generation"]["speed"] == 1.0  # Default value


def test_property_35_invalid_configuration_fallback() -> None:
    """Property 35: Invalid configuration fallback.

    Feature: voice-clone-cli, Property 35: Invalid configuration fallback

    For any invalid configuration, validation errors should be reported and
    default values should be used for invalid parameters.

    Validates: Requirements 8.5
    """
    # Create config with multiple invalid values
    config: dict[str, Any] = {
        "generation": {
            "temperature": 2.5,  # Invalid: > 1.0
            "speed": 0.5,  # Invalid: < 0.8
        },
        "audio": {
            "sample_rate": -100,  # Invalid: negative
        },
    }

    result = ConfigManager.validate_config(config)

    # Should report errors
    assert not result["valid"], "Invalid config was marked as valid"
    errors_list = result["errors"]
    assert isinstance(errors_list, list)
    assert len(errors_list) >= 3, "Not all errors were reported"

    # Should use default values for invalid parameters
    assert (
        config["generation"]["temperature"] == 0.75
    ), "Temperature not reset to default"
    assert config["generation"]["speed"] == 1.0, "Speed not reset to default"
    assert config["audio"]["sample_rate"] == 22050, "Sample rate not reset to default"


@given(
    temperature=st.floats(allow_nan=False, allow_infinity=False),
    speed=st.floats(allow_nan=False, allow_infinity=False),
)
def test_property_35_any_invalid_value_uses_default(
    temperature: float, speed: float
) -> None:
    """Property 35: Any invalid value uses default.

    For any temperature or speed value outside valid ranges, the system should
    fall back to default values.

    Validates: Requirements 8.5
    """
    config: dict[str, Any] = {
        "generation": {
            "temperature": temperature,
            "speed": speed,
        }
    }

    ConfigManager.validate_config(config)

    # After validation, values should either be unchanged (if valid) or default
    temp_valid = 0.5 <= temperature <= 1.0
    speed_valid = 0.8 <= speed <= 1.2

    if not temp_valid:
        assert (
            config["generation"]["temperature"] == 0.75
        ), f"Invalid temperature {temperature} not reset to default"

    if not speed_valid:
        assert (
            config["generation"]["speed"] == 1.0
        ), f"Invalid speed {speed} not reset to default"
