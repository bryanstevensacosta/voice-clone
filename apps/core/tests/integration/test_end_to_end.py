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
        return TTSStudio(config)

    @pytest.fixture
    def sample_audio_files(self, tmp_path):
        """Create temporary sample audio files for testing."""
        import numpy as np
        import soundfile as sf

        samples = []
        for i in range(2):
            # Create a simple sine wave audio file
            sample_rate = 12000
            duration = 2.0  # 2 seconds
            frequency = 440.0  # A4 note

            t = np.linspace(0, duration, int(sample_rate * duration))
            audio_data = np.sin(2 * np.pi * frequency * t)

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
        assert profile_result["profile"]["samples"] == 2

        # Step 2: Generate audio using the profile
        generation_result = studio.generate_audio(
            profile_name="test_profile",
            text="Hello, this is a test of voice cloning.",
            temperature=0.75,
            speed=1.0,
        )

        assert generation_result["status"] == "success"
        assert "audio_path" in generation_result
        assert Path(generation_result["audio_path"]).exists()

        # Verify generated audio file
        audio_path = Path(generation_result["audio_path"])
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
            assert result["is_valid"] is True

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
        for i in range(3):
            result = studio.create_voice_profile(
                name=f"profile_{i}",
                sample_paths=sample_audio_files,
                reference_text=f"Profile {i}",
            )
            assert result["status"] == "success"

        # Step 2: List all profiles
        list_result = studio.list_voice_profiles()

        assert list_result["status"] == "success"
        assert "profiles" in list_result
        assert len(list_result["profiles"]) == 3

        # Step 3: Delete one profile
        delete_result = studio.delete_voice_profile(profile_name="profile_1")

        assert delete_result["status"] == "success"

        # Step 4: Verify profile was deleted
        list_result = studio.list_voice_profiles()
        assert len(list_result["profiles"]) == 2
        profile_names = [p["name"] for p in list_result["profiles"]]
        assert "profile_1" not in profile_names

    def test_workflow_error_handling(self, studio):
        """Test error handling in complete workflow."""
        # Try to generate audio without creating profile first
        result = studio.generate_audio(
            profile_name="nonexistent_profile",
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

        # Try to generate with empty text
        result = studio.generate_audio(
            profile_name="test_profile_empty", text="", temperature=0.75, speed=1.0
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

        # Generate with long text (should be chunked automatically)
        long_text = " ".join(["This is a test sentence."] * 50)  # ~500 chars

        result = studio.generate_audio(
            profile_name="test_profile_long",
            text=long_text,
            temperature=0.75,
            speed=1.0,
        )

        assert result["status"] == "success"
        assert Path(result["audio_path"]).exists()
