"""
End-to-end integration tests for the complete workflow.

Tests the entire flow: create profile → generate audio with real infrastructure.
"""

from pathlib import Path

import pytest

from api.studio import TTSStudio


class TestEndToEndWorkflow:
    """Test complete workflows with real infrastructure."""

    @pytest.fixture
    def studio(self, tmp_path):
        """Create TTSStudio instance with temporary directories."""
        config = {
            "paths": {
                "profiles": str(tmp_path / "profiles"),
                "outputs": str(tmp_path / "outputs"),
                "models": str(tmp_path / "models"),
            },
            "engines": {
                "qwen3": {
                    "model_name": "Qwen/Qwen3-TTS-12Hz-1.7B-Base",
                    "device": "cpu",  # Use CPU for tests
                    "dtype": "float32",
                }
            },
            "audio": {"sample_rate": 12000, "format": "wav", "mono": True},
            "generation": {"language": "es", "temperature": 0.75, "max_length": 400},
        }
        return TTSStudio(config_dict=config)

    @pytest.fixture
    def sample_audio_files(self, tmp_path):
        """Create temporary sample audio files for testing."""
        import numpy as np
        import soundfile as sf

        samples = []
        for i in range(2):
            # Create a simple sine wave audio file
            sample_rate = 12000
            duration = 10.0  # 10 seconds - meets 3s minimum requirement
            frequency = 440.0  # A4 note

            t = np.linspace(0, duration, int(sample_rate * duration))
            audio_data = np.sin(2 * np.pi * frequency * t)
            # Normalize to prevent clipping
            audio_data = audio_data * 0.5

            sample_path = tmp_path / f"sample_{i}.wav"
            sf.write(sample_path, audio_data, sample_rate)
            samples.append(str(sample_path))

        return samples

    def test_complete_workflow_create_and_generate(self, studio, sample_audio_files):
        """Test complete workflow: create profile → generate audio."""
        # Step 1: Create voice profile
        profile_result = studio.create_voice_profile(
            name="test_profile",
            sample_paths=sample_audio_files,
            reference_text="This is a test voice sample",
        )

        assert profile_result["status"] == "success"
        assert "profile" in profile_result
        assert profile_result["profile"]["name"] == "test_profile"
        # samples is now a list of dicts, not a count
        assert len(profile_result["profile"]["samples"]) == 2

        # Get profile_id for generation
        profile_id = profile_result["profile"]["id"]

        # Step 2: Generate audio using the profile
        generation_result = studio.generate_audio(
            profile_id=profile_id,
            text="Hello, this is a test of voice cloning.",
            temperature=0.75,
            speed=1.0,
        )

        # Skip if model loading failed (model not available in test environment)
        if generation_result[
            "status"
        ] == "error" and "Failed to load model" in generation_result.get("error", ""):
            pytest.skip("Qwen3 model not available in test environment")

        assert generation_result["status"] == "success"
        # API returns "output_path" key
        assert "output_path" in generation_result
        assert Path(generation_result["output_path"]).exists()

        # Verify generated audio file
        audio_path = Path(generation_result["output_path"])
        assert audio_path.suffix == ".wav"
        assert audio_path.stat().st_size > 0

    def test_workflow_with_validation(self, studio, sample_audio_files):
        """Test workflow with sample validation before profile creation."""
        # Step 1: Validate samples
        validation_result = studio.validate_samples(sample_paths=sample_audio_files)

        assert validation_result["status"] == "success"
        assert "results" in validation_result
        assert len(validation_result["results"]) == 2

        # All samples should be valid
        for result in validation_result["results"]:
            assert result["valid"] is True  # Changed from is_valid to valid

        # Step 2: Create profile (should succeed with valid samples)
        profile_result = studio.create_voice_profile(
            name="validated_profile",
            sample_paths=sample_audio_files,
            reference_text="Validated voice sample",
        )

        assert profile_result["status"] == "success"

    def test_workflow_list_and_delete_profiles(self, studio, sample_audio_files):
        """Test workflow: create → list → delete profiles."""
        # Step 1: Create multiple profiles
        profile_ids = []
        for i in range(3):
            result = studio.create_voice_profile(
                name=f"profile_{i}",
                sample_paths=sample_audio_files,
                reference_text=f"Profile {i}",
            )
            assert result["status"] == "success"
            profile_ids.append(result["profile"]["id"])

        # Step 2: List all profiles
        list_result = studio.list_voice_profiles()

        assert list_result["status"] == "success"
        assert "profiles" in list_result
        assert len(list_result["profiles"]) == 3

        # Step 3: Delete one profile (using profile_id, not profile_name)
        delete_result = studio.delete_voice_profile(profile_id=profile_ids[1])

        assert delete_result["status"] == "success"

        # Step 4: Verify profile was deleted
        list_result = studio.list_voice_profiles()
        assert len(list_result["profiles"]) == 2
        remaining_ids = [p["id"] for p in list_result["profiles"]]
        assert profile_ids[1] not in remaining_ids

    def test_workflow_error_handling(self, studio, sample_audio_files):
        """Test error handling in complete workflow."""
        # First create a profile so we have a valid profile_id
        profile_result = studio.create_voice_profile(
            name="test_profile",
            sample_paths=sample_audio_files,
            language="es",
        )

        assert profile_result["status"] == "success"
        # We create a profile but intentionally test with a nonexistent ID
        # to verify error handling
        _profile_id = profile_result["profile"]["id"]  # noqa: F841

        # Try to generate audio with nonexistent profile
        result = studio.generate_audio(
            profile_id="nonexistent_profile_id",
            text="This should fail",
            temperature=0.75,
            speed=1.0,
        )

        assert result["status"] == "error"
        assert "error" in result

    def test_workflow_with_invalid_samples(self, studio, tmp_path):
        """Test workflow with invalid audio samples."""
        # Create an invalid audio file (empty file)
        invalid_sample = tmp_path / "invalid.wav"
        invalid_sample.write_text("not an audio file")

        # Try to create profile with invalid sample
        result = studio.create_voice_profile(
            name="invalid_profile",
            sample_paths=[str(invalid_sample)],
            reference_text="This should fail",
        )

        assert result["status"] == "error"
        assert "error" in result

    def test_workflow_with_empty_text(self, studio, sample_audio_files):
        """Test workflow with empty text for generation."""
        # Create profile first
        profile_result = studio.create_voice_profile(
            name="test_profile_empty",
            sample_paths=sample_audio_files,
            reference_text="Test sample",
        )
        assert profile_result["status"] == "success"
        profile_id = profile_result["profile"]["id"]

        # Try to generate with empty text
        result = studio.generate_audio(
            profile_id=profile_id, text="", temperature=0.75, speed=1.0
        )

        assert result["status"] == "error"
        assert "error" in result

    def test_workflow_with_long_text(self, studio, sample_audio_files):
        """Test workflow with long text (chunking)."""
        # Create profile
        profile_result = studio.create_voice_profile(
            name="test_profile_long",
            sample_paths=sample_audio_files,
            reference_text="Test sample",
        )
        assert profile_result["status"] == "success"
        profile_id = profile_result["profile"]["id"]

        # Generate with long text (should be chunked automatically)
        long_text = " ".join(["This is a test sentence."] * 50)  # ~500 chars

        result = studio.generate_audio(
            profile_id=profile_id,
            text=long_text,
            temperature=0.75,
            speed=1.0,
        )

        # Skip if model loading failed (model not available in test environment)
        if result["status"] == "error" and "Failed to load model" in result.get(
            "error", ""
        ):
            pytest.skip("Qwen3 model not available in test environment")

        assert result["status"] == "success"
        # API returns "output_path" key
        assert Path(result["output_path"]).exists()
