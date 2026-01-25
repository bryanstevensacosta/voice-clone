"""Unit tests for VoiceProfile with Qwen3-TTS updates."""

import json
from pathlib import Path

import pytest
from voice_clone.model.profile import VoiceProfile, VoiceSample


class TestVoiceProfileQwen3Fields:
    """Test VoiceProfile with Qwen3-TTS fields."""

    def test_voice_profile_has_ref_text_field(self) -> None:
        """Test that VoiceProfile has ref_text field."""
        profile = VoiceProfile(name="test", ref_text="Test reference text")

        assert hasattr(profile, "ref_text")
        assert profile.ref_text == "Test reference text"

    def test_voice_profile_has_sample_rate_field(self) -> None:
        """Test that VoiceProfile has sample_rate field."""
        profile = VoiceProfile(name="test")

        assert hasattr(profile, "sample_rate")
        assert profile.sample_rate == 12000  # Default for Qwen3-TTS

    def test_voice_profile_default_sample_rate_is_12000(self) -> None:
        """Test that default sample rate is 12000 Hz."""
        profile = VoiceProfile(name="test")

        assert profile.sample_rate == 12000

    def test_voice_profile_custom_sample_rate(self) -> None:
        """Test that custom sample rate can be set."""
        profile = VoiceProfile(name="test", sample_rate=22050)

        assert profile.sample_rate == 22050

    def test_voice_profile_default_ref_text_is_empty(self) -> None:
        """Test that default ref_text is empty string."""
        profile = VoiceProfile(name="test")

        assert profile.ref_text == ""


class TestVoiceProfileSerialization:
    """Test VoiceProfile serialization with Qwen3-TTS fields."""

    def test_to_json_includes_ref_text(self, tmp_path: Path) -> None:
        """Test that to_json includes ref_text field."""
        profile = VoiceProfile(
            name="test",
            ref_text="This is a test reference text",
            language="es",
        )

        output_path = tmp_path / "profile.json"
        profile.to_json(output_path)

        # Load and verify
        with open(output_path) as f:
            data = json.load(f)

        assert "ref_text" in data
        assert data["ref_text"] == "This is a test reference text"

    def test_to_json_includes_sample_rate(self, tmp_path: Path) -> None:
        """Test that to_json includes sample_rate field."""
        profile = VoiceProfile(name="test", sample_rate=12000)

        output_path = tmp_path / "profile.json"
        profile.to_json(output_path)

        # Load and verify
        with open(output_path) as f:
            data = json.load(f)

        assert "sample_rate" in data
        assert data["sample_rate"] == 12000

    def test_from_json_loads_ref_text(self, tmp_path: Path) -> None:
        """Test that from_json loads ref_text field."""
        # Create profile JSON with ref_text
        data = {
            "name": "test",
            "created_at": "2024-01-01T00:00:00",
            "language": "es",
            "total_duration": 10.0,
            "ref_text": "Reference text for testing",
            "sample_rate": 12000,
            "samples": [],
        }

        profile_path = tmp_path / "profile.json"
        with open(profile_path, "w") as f:
            json.dump(data, f)

        # Load profile
        profile = VoiceProfile.from_json(profile_path)

        assert profile.ref_text == "Reference text for testing"

    def test_from_json_loads_sample_rate(self, tmp_path: Path) -> None:
        """Test that from_json loads sample_rate field."""
        # Create profile JSON with sample_rate
        data = {
            "name": "test",
            "created_at": "2024-01-01T00:00:00",
            "language": "es",
            "total_duration": 10.0,
            "ref_text": "",
            "sample_rate": 12000,
            "samples": [],
        }

        profile_path = tmp_path / "profile.json"
        with open(profile_path, "w") as f:
            json.dump(data, f)

        # Load profile
        profile = VoiceProfile.from_json(profile_path)

        assert profile.sample_rate == 12000

    def test_from_json_defaults_ref_text_if_missing(self, tmp_path: Path) -> None:
        """Test that from_json defaults ref_text to empty string if missing."""
        # Create old profile JSON without ref_text
        data = {
            "name": "test",
            "created_at": "2024-01-01T00:00:00",
            "language": "es",
            "total_duration": 10.0,
            "samples": [],
        }

        profile_path = tmp_path / "profile.json"
        with open(profile_path, "w") as f:
            json.dump(data, f)

        # Load profile
        profile = VoiceProfile.from_json(profile_path)

        assert profile.ref_text == ""

    def test_from_json_defaults_sample_rate_if_missing(self, tmp_path: Path) -> None:
        """Test that from_json defaults sample_rate to 12000 if missing."""
        # Create old profile JSON without sample_rate
        data = {
            "name": "test",
            "created_at": "2024-01-01T00:00:00",
            "language": "es",
            "total_duration": 10.0,
            "samples": [],
        }

        profile_path = tmp_path / "profile.json"
        with open(profile_path, "w") as f:
            json.dump(data, f)

        # Load profile
        profile = VoiceProfile.from_json(profile_path)

        assert profile.sample_rate == 12000

    def test_round_trip_serialization(self, tmp_path: Path) -> None:
        """Test that profile can be saved and loaded without data loss."""
        # Create profile with all fields
        original = VoiceProfile(
            name="test_profile",
            ref_text="This is the reference text for voice cloning",
            sample_rate=12000,
            language="es",
        )

        # Add a sample
        sample = VoiceSample(
            path="/path/to/sample.wav",
            duration=10.5,
            emotion="neutral",
            quality_score=0.95,
        )
        original.samples.append(sample)
        original.total_duration = 10.5

        # Save
        output_path = tmp_path / "profile.json"
        original.to_json(output_path)

        # Load
        loaded = VoiceProfile.from_json(output_path)

        # Verify all fields
        assert loaded.name == original.name
        assert loaded.ref_text == original.ref_text
        assert loaded.sample_rate == original.sample_rate
        assert loaded.language == original.language
        assert loaded.total_duration == original.total_duration
        assert len(loaded.samples) == len(original.samples)


class TestVoiceProfileValidation:
    """Test VoiceProfile validation with Qwen3-TTS requirements."""

    def test_validate_warns_missing_ref_text(self) -> None:
        """Test that validation warns when ref_text is missing."""
        profile = VoiceProfile(name="test", ref_text="")

        # Add a sample to make it otherwise valid
        sample = VoiceSample(path="test.wav", duration=10.0)
        profile.samples.append(sample)
        profile.total_duration = 10.0

        is_valid, warnings = profile.validate()

        assert any("ref_text" in warning for warning in warnings)
        assert any("required for Qwen3-TTS" in warning for warning in warnings)

    def test_validate_warns_non_12khz_sample_rate(self) -> None:
        """Test that validation warns when sample rate is not 12kHz."""
        profile = VoiceProfile(
            name="test",
            ref_text="Test text",
            sample_rate=22050,  # Not Qwen3-TTS native
        )

        # Add a sample
        sample = VoiceSample(path="test.wav", duration=10.0)
        profile.samples.append(sample)
        profile.total_duration = 10.0

        is_valid, warnings = profile.validate()

        assert any("12000 Hz" in warning for warning in warnings)

    def test_validate_passes_with_ref_text_and_12khz(self) -> None:
        """Test that validation passes with ref_text and 12kHz."""
        profile = VoiceProfile(
            name="test",
            ref_text="This is a valid reference text",
            sample_rate=12000,
        )

        # Add sufficient samples
        for i in range(6):
            sample = VoiceSample(path=f"sample_{i}.wav", duration=10.0)
            profile.samples.append(sample)
        profile.total_duration = 60.0

        is_valid, warnings = profile.validate()

        assert is_valid
        # Should not have ref_text or sample_rate warnings
        assert not any("ref_text" in warning for warning in warnings)
        assert not any("12000 Hz" in warning for warning in warnings)

    def test_validate_minimum_duration_3_seconds(self) -> None:
        """Test that validation requires minimum 3 seconds total duration."""
        profile = VoiceProfile(
            name="test",
            ref_text="Test",
            sample_rate=12000,
        )

        # Add a 3-second sample
        sample = VoiceSample(path="test.wav", duration=3.0)
        profile.samples.append(sample)
        profile.total_duration = 3.0

        is_valid, warnings = profile.validate()

        assert is_valid  # 3 seconds should be valid

    def test_validate_fails_below_3_seconds(self) -> None:
        """Test that validation fails for < 3 seconds total duration."""
        profile = VoiceProfile(
            name="test",
            ref_text="Test",
            sample_rate=12000,
        )

        # Add a 2-second sample (too short)
        sample = VoiceSample(path="test.wav", duration=2.0)
        profile.samples.append(sample)
        profile.total_duration = 2.0

        is_valid, warnings = profile.validate()

        assert not is_valid  # Should fail


class TestVoiceProfileFromDirectory:
    """Test VoiceProfile.from_directory with ref_text parameter."""

    def test_from_directory_accepts_ref_text(self, tmp_path: Path) -> None:
        """Test that from_directory accepts ref_text parameter."""
        samples_dir = tmp_path / "samples"
        samples_dir.mkdir()

        # Create a dummy WAV file (won't be validated in this test)
        (samples_dir / "test.wav").touch()

        # This should not raise an error
        try:
            profile = VoiceProfile.from_directory(
                name="test",
                samples_dir=samples_dir,
                ref_text="Test reference text",
            )
            assert profile.ref_text == "Test reference text"
        except TypeError:
            pytest.fail("from_directory should accept ref_text parameter")

    def test_from_directory_sets_ref_text(self, tmp_path: Path) -> None:
        """Test that from_directory sets ref_text field."""
        samples_dir = tmp_path / "samples"
        samples_dir.mkdir()

        profile = VoiceProfile.from_directory(
            name="test",
            samples_dir=samples_dir,
            ref_text="Reference text for testing",
        )

        assert profile.ref_text == "Reference text for testing"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
