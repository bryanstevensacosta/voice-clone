"""Unit tests for Qwen3-TTS configuration."""
# mypy: disable-error-code="no-untyped-def"

from pathlib import Path

import yaml  # type: ignore[import-untyped]


class TestDefaultConfig:
    """Tests for default.yaml configuration."""

    def test_default_config_exists(self):
        """Test that default.yaml exists."""
        config_path = Path("config/default.yaml")
        assert config_path.exists()

    def test_default_config_valid_yaml(self):
        """Test that default.yaml is valid YAML."""
        config_path = Path("config/default.yaml")
        with open(config_path) as f:
            config = yaml.safe_load(f)
        assert config is not None
        assert isinstance(config, dict)

    def test_model_name_is_qwen3(self):
        """Test that model name is Qwen3-TTS."""
        config_path = Path("config/default.yaml")
        with open(config_path) as f:
            config = yaml.safe_load(f)

        assert "model" in config
        assert "name" in config["model"]
        assert config["model"]["name"] == "Qwen/Qwen3-TTS-12Hz-1.7B-Base"

    def test_sample_rate_is_12000(self):
        """Test that sample rate is 12000 Hz (Qwen3-TTS native)."""
        config_path = Path("config/default.yaml")
        with open(config_path) as f:
            config = yaml.safe_load(f)

        assert "audio" in config
        assert "sample_rate" in config["audio"]
        assert config["audio"]["sample_rate"] == 12000

    def test_dtype_is_float32(self):
        """Test that dtype is float32 (required for MPS)."""
        config_path = Path("config/default.yaml")
        with open(config_path) as f:
            config = yaml.safe_load(f)

        assert "model" in config
        assert "dtype" in config["model"]
        assert config["model"]["dtype"] == "float32"

    def test_models_path_is_qwen3(self):
        """Test that models path is qwen3_models."""
        config_path = Path("config/default.yaml")
        with open(config_path) as f:
            config = yaml.safe_load(f)

        assert "paths" in config
        assert "models" in config["paths"]
        assert "qwen3" in config["paths"]["models"]

    def test_no_xtts_references(self):
        """Test that there are no XTTS-v2 references."""
        config_path = Path("config/default.yaml")
        with open(config_path) as f:
            content = f.read()

        # Should not contain XTTS references
        assert "xtts" not in content.lower()
        assert "coqui" not in content.lower()
        assert "22050" not in content  # Old sample rate

    def test_has_max_new_tokens(self):
        """Test that generation config has max_new_tokens."""
        config_path = Path("config/default.yaml")
        with open(config_path) as f:
            config = yaml.safe_load(f)

        assert "generation" in config
        assert "max_new_tokens" in config["generation"]
        assert config["generation"]["max_new_tokens"] == 2048


class TestPersonalConfig:
    """Tests for config.yaml (personal overrides)."""

    def test_personal_config_exists(self):
        """Test that config.yaml exists."""
        config_path = Path("config/config.yaml")
        assert config_path.exists()

    def test_personal_config_valid_yaml(self):
        """Test that config.yaml is valid YAML."""
        config_path = Path("config/config.yaml")
        with open(config_path) as f:
            config = yaml.safe_load(f)
        assert config is not None
        assert isinstance(config, dict)

    def test_device_is_mps_or_cpu(self):
        """Test that device is set to mps or cpu."""
        config_path = Path("config/config.yaml")
        with open(config_path) as f:
            config = yaml.safe_load(f)

        if "model" in config and "device" in config["model"]:
            device = config["model"]["device"]
            assert device in ["mps", "cpu", "cuda", "auto"]

    def test_dtype_is_float32_if_present(self):
        """Test that dtype is float32 if present."""
        config_path = Path("config/config.yaml")
        with open(config_path) as f:
            config = yaml.safe_load(f)

        if "model" in config and "dtype" in config["model"]:
            assert config["model"]["dtype"] == "float32"


class TestEnvExample:
    """Tests for .env.example file."""

    def test_env_example_exists(self):
        """Test that .env.example exists."""
        env_path = Path(".env.example")
        assert env_path.exists()

    def test_env_has_qwen_model_name(self):
        """Test that .env.example has Qwen3-TTS model name."""
        env_path = Path(".env.example")
        with open(env_path) as f:
            content = f.read()

        assert "Qwen/Qwen3-TTS" in content

    def test_env_has_12000_sample_rate(self):
        """Test that .env.example has 12000 Hz sample rate."""
        env_path = Path(".env.example")
        with open(env_path) as f:
            content = f.read()

        assert "SAMPLE_RATE=12000" in content

    def test_env_has_qwen_cache_dir(self):
        """Test that .env.example has QWEN_TTS_CACHE_DIR."""
        env_path = Path(".env.example")
        with open(env_path) as f:
            content = f.read()

        assert "QWEN_TTS_CACHE_DIR" in content

    def test_env_no_xtts_references(self):
        """Test that .env.example has no XTTS references."""
        env_path = Path(".env.example")
        with open(env_path) as f:
            content = f.read()

        assert "xtts" not in content.lower()
        assert "22050" not in content


class TestConfigurationCorrectness:
    """Property 6: Configuration Correctness tests."""

    def test_property_6_model_name_correctness(self):
        """Property 6: Model name should be Qwen3-TTS in all configs.

        Feature: migrate-to-qwen3-tts, Property 6: Configuration Correctness
        Validates: Requirements 5.1, 5.3, 8.2
        """
        # Check default.yaml
        with open("config/default.yaml") as f:
            default_config = yaml.safe_load(f)

        assert default_config["model"]["name"] == "Qwen/Qwen3-TTS-12Hz-1.7B-Base"

        # Check .env.example
        with open(".env.example") as f:
            env_content = f.read()

        assert "Qwen/Qwen3-TTS" in env_content

    def test_property_6_sample_rate_correctness(self):
        """Property 6: Sample rate should be 12000 Hz in all configs.

        Feature: migrate-to-qwen3-tts, Property 6: Configuration Correctness
        Validates: Requirements 5.1, 5.3, 8.2
        """
        # Check default.yaml
        with open("config/default.yaml") as f:
            default_config = yaml.safe_load(f)

        assert default_config["audio"]["sample_rate"] == 12000

        # Check .env.example
        with open(".env.example") as f:
            env_content = f.read()

        assert "SAMPLE_RATE=12000" in env_content

    def test_property_6_no_xtts_references(self):
        """Property 6: No XTTS-v2 references should exist in configs.

        Feature: migrate-to-qwen3-tts, Property 6: Configuration Correctness
        Validates: Requirements 5.1, 5.3, 8.2
        """
        config_files = [
            "config/default.yaml",
            "config/config.yaml",
            ".env.example",
        ]

        for config_file in config_files:
            with open(config_file) as f:
                content = f.read().lower()

            # Should not contain XTTS references
            assert "xtts" not in content, f"Found 'xtts' in {config_file}"
            assert (
                "22050" not in content
            ), f"Found old sample rate '22050' in {config_file}"
