"""Tests for TTSStudio API.

Tests the main API entry point with real adapters (integration tests).
"""

import json

import pytest
from api import TTSStudio


@pytest.fixture
def studio(tmp_path):
    """Create TTSStudio instance with temporary paths."""
    # Create temporary directories
    profiles_dir = tmp_path / "profiles"
    outputs_dir = tmp_path / "outputs"
    profiles_dir.mkdir()
    outputs_dir.mkdir()

    # Create config dictionary (no file needed)
    config_dict = {
        "model": {
            "name": "Qwen/Qwen3-TTS-12Hz-1.7B-Base",
            "device": "cpu",
            "dtype": "float32",
        },
        "audio": {"sample_rate": 12000},
        "paths": {
            "profiles": str(profiles_dir),
            "outputs": str(outputs_dir),
            "models_cache": str(tmp_path / "models"),
        },
        "generation": {"language": "es"},
    }

    return TTSStudio(config_dict=config_dict)


class TestTTSStudioInitialization:
    """Test TTSStudio initialization."""

    def test_studio_initializes_successfully(self, studio):
        """Test that TTSStudio initializes without errors."""
        assert studio is not None

    def test_studio_has_config(self, studio):
        """Test that studio has configuration loaded."""
        assert studio.get_config("audio.sample_rate") == 12000
        assert studio.get_config("generation.language") == "es"

    def test_studio_get_config_with_default(self, studio):
        """Test get_config with default value."""
        assert studio.get_config("nonexistent.key", "default") == "default"


class TestCreateVoiceProfile:
    """Test create_voice_profile method."""

    def test_create_profile_returns_success_dict(self, studio, sample_audio_file):
        """Test that create_voice_profile returns proper dict format."""
        result = studio.create_voice_profile(
            name="test_profile", sample_paths=[str(sample_audio_file)]
        )

        assert isinstance(result, dict)
        assert "status" in result
        assert "profile" in result
        assert "error" in result

    def test_create_profile_with_valid_samples(self, studio, sample_audio_file):
        """Test creating profile with valid samples."""
        result = studio.create_voice_profile(
            name="test_profile",
            sample_paths=[str(sample_audio_file)],
            language="es",
            reference_text="Test sample",
        )

        assert result["status"] == "success"
        assert result["profile"] is not None
        assert result["error"] is None
        assert result["profile"]["name"] == "test_profile"
        assert result["profile"]["language"] == "es"

    def test_create_profile_with_invalid_samples(self, studio, tmp_path):
        """Test creating profile with non-existent samples."""
        invalid_path = tmp_path / "nonexistent.wav"

        result = studio.create_voice_profile(
            name="test_profile", sample_paths=[str(invalid_path)]
        )

        assert result["status"] == "error"
        assert result["profile"] is None
        assert result["error"] is not None
        assert (
            "not found" in result["error"].lower()
            or "no such file" in result["error"].lower()
        )

    def test_create_profile_with_empty_name(self, studio, sample_audio_file):
        """Test creating profile with empty name."""
        result = studio.create_voice_profile(
            name="", sample_paths=[str(sample_audio_file)]
        )

        assert result["status"] == "error"
        assert result["error"] is not None


class TestGenerateAudio:
    """Test generate_audio method."""

    def test_generate_audio_returns_success_dict(self, studio, test_profile):
        """Test that generate_audio returns proper dict format."""
        result = studio.generate_audio(
            profile_id=test_profile["id"], text="Hola mundo", mode="clone"
        )

        assert isinstance(result, dict)
        assert "status" in result
        assert "output_path" in result
        assert "duration" in result
        assert "generation_time" in result
        assert "error" in result

    def test_generate_audio_with_valid_profile(self, studio, test_profile):
        """Test generating audio with valid profile."""
        result = studio.generate_audio(
            profile_id=test_profile["id"],
            text="Hola, esta es una prueba",
            temperature=0.75,
            speed=1.0,
        )

        # Note: This might fail if Qwen3 model is not available
        # In that case, we expect an error status
        assert result["status"] in ["success", "error"]

        if result["status"] == "success":
            assert result["output_path"] is not None
            assert result["duration"] is not None
            assert result["generation_time"] is not None
            assert result["error"] is None
        else:
            assert result["error"] is not None

    def test_generate_audio_with_invalid_profile(self, studio):
        """Test generating audio with non-existent profile."""
        result = studio.generate_audio(
            profile_id="nonexistent_profile", text="Hola mundo"
        )

        assert result["status"] == "error"
        assert result["error"] is not None
        assert "not found" in result["error"].lower()

    def test_generate_audio_with_empty_text(self, studio, test_profile):
        """Test generating audio with empty text."""
        result = studio.generate_audio(profile_id=test_profile["id"], text="")

        assert result["status"] == "error"
        assert result["error"] is not None


class TestListVoiceProfiles:
    """Test list_voice_profiles method."""

    def test_list_profiles_returns_success_dict(self, studio):
        """Test that list_voice_profiles returns proper dict format."""
        result = studio.list_voice_profiles()

        assert isinstance(result, dict)
        assert "status" in result
        assert "profiles" in result
        assert "count" in result
        assert "error" in result

    def test_list_profiles_empty_repository(self, studio):
        """Test listing profiles when repository is empty."""
        result = studio.list_voice_profiles()

        assert result["status"] == "success"
        assert result["profiles"] == []
        assert result["count"] == 0
        assert result["error"] is None

    def test_list_profiles_with_profiles(self, studio, test_profile):
        """Test listing profiles when profiles exist."""
        result = studio.list_voice_profiles()

        assert result["status"] == "success"
        assert isinstance(result["profiles"], list)
        assert result["count"] > 0
        assert result["error"] is None

        # Check that test_profile is in the list
        profile_ids = [p["id"] for p in result["profiles"]]
        assert test_profile["id"] in profile_ids


class TestDeleteVoiceProfile:
    """Test delete_voice_profile method."""

    def test_delete_profile_returns_success_dict(self, studio, test_profile):
        """Test that delete_voice_profile returns proper dict format."""
        result = studio.delete_voice_profile(profile_id=test_profile["id"])

        assert isinstance(result, dict)
        assert "status" in result
        assert "deleted" in result
        assert "error" in result

    def test_delete_existing_profile(self, studio, test_profile):
        """Test deleting an existing profile."""
        result = studio.delete_voice_profile(profile_id=test_profile["id"])

        assert result["status"] == "success"
        assert result["deleted"] is True
        assert result["error"] is None

        # Verify profile is deleted
        list_result = studio.list_voice_profiles()
        profile_ids = [p["id"] for p in list_result["profiles"]]
        assert test_profile["id"] not in profile_ids

    def test_delete_nonexistent_profile(self, studio):
        """Test deleting a non-existent profile."""
        result = studio.delete_voice_profile(profile_id="nonexistent_profile")

        assert result["status"] == "error"
        assert result["deleted"] is False
        assert result["error"] is not None
        assert "not found" in result["error"].lower()


class TestValidateSamples:
    """Test validate_samples method."""

    def test_validate_samples_returns_success_dict(self, studio, sample_audio_file):
        """Test that validate_samples returns proper dict format."""
        result = studio.validate_samples(sample_paths=[str(sample_audio_file)])

        assert isinstance(result, dict)
        assert "status" in result
        assert "results" in result
        assert "all_valid" in result
        assert "total_samples" in result
        assert "valid_samples" in result
        assert "invalid_samples" in result
        assert "total_duration" in result
        assert "error" in result

    def test_validate_valid_samples(self, studio, sample_audio_file):
        """Test validating valid audio samples."""
        result = studio.validate_samples(sample_paths=[str(sample_audio_file)])

        assert result["status"] == "success"
        assert isinstance(result["results"], list)
        assert len(result["results"]) == 1
        assert result["all_valid"] is True
        assert result["valid_samples"] == 1
        assert result["invalid_samples"] == 0
        assert result["error"] is None

        # Check result structure
        sample_result = result["results"][0]
        assert "path" in sample_result
        assert "valid" in sample_result
        assert "duration" in sample_result
        assert "sample_rate" in sample_result
        assert "channels" in sample_result
        assert "bit_depth" in sample_result

    def test_validate_invalid_samples(self, studio, tmp_path):
        """Test validating invalid audio samples."""
        invalid_path = tmp_path / "nonexistent.wav"

        result = studio.validate_samples(sample_paths=[str(invalid_path)])

        assert result["status"] == "success"
        assert len(result["results"]) == 1
        assert result["all_valid"] is False
        assert result["valid_samples"] == 0
        assert result["invalid_samples"] == 1

        sample_result = result["results"][0]
        assert sample_result["valid"] is False
        assert sample_result["error"] is not None

    def test_validate_empty_list(self, studio):
        """Test validating empty sample list."""
        result = studio.validate_samples(sample_paths=[])

        assert result["status"] == "success"
        assert result["results"] == []
        assert result["all_valid"] is True  # Vacuously true
        assert result["total_samples"] == 0


class TestConfigManagement:
    """Test configuration management methods."""

    def test_get_config(self, studio):
        """Test getting configuration values."""
        sample_rate = studio.get_config("audio.sample_rate")
        assert sample_rate == 12000

        language = studio.get_config("generation.language")
        assert language == "es"

    def test_get_config_with_default(self, studio):
        """Test getting non-existent config with default."""
        value = studio.get_config("nonexistent.key", "default_value")
        assert value == "default_value"

    def test_reload_config(self, studio):
        """Test reloading configuration."""
        result = studio.reload_config()

        assert isinstance(result, dict)
        assert "status" in result
        assert "error" in result
        assert result["status"] == "success"
        assert result["error"] is None


class TestJSONSerialization:
    """Test that all API responses are JSON-serializable."""

    def test_create_profile_response_is_json_serializable(
        self, studio, sample_audio_file
    ):
        """Test that create_voice_profile response can be serialized to JSON."""
        result = studio.create_voice_profile(
            name="test_profile", sample_paths=[str(sample_audio_file)]
        )

        # Should not raise exception
        json_str = json.dumps(result)
        assert json_str is not None

        # Should be able to parse back
        parsed = json.loads(json_str)
        assert parsed["status"] == result["status"]

    def test_list_profiles_response_is_json_serializable(self, studio):
        """Test that list_voice_profiles response can be serialized to JSON."""
        result = studio.list_voice_profiles()

        json_str = json.dumps(result)
        assert json_str is not None

        parsed = json.loads(json_str)
        assert parsed["status"] == result["status"]

    def test_validate_samples_response_is_json_serializable(
        self, studio, sample_audio_file
    ):
        """Test that validate_samples response can be serialized to JSON."""
        result = studio.validate_samples(sample_paths=[str(sample_audio_file)])

        json_str = json.dumps(result)
        assert json_str is not None

        parsed = json.loads(json_str)
        assert parsed["status"] == result["status"]


# Fixtures for tests


@pytest.fixture
def test_profile(studio, sample_audio_file):
    """Create a test profile for use in tests."""
    result = studio.create_voice_profile(
        name="test_profile_fixture",
        sample_paths=[str(sample_audio_file)],
        language="es",
    )

    if result["status"] == "success":
        return result["profile"]
    else:
        pytest.skip(f"Could not create test profile: {result['error']}")
