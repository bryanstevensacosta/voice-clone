"""Tests for Qwen3Adapter.

Tests the Qwen3-TTS engine adapter implementation.
"""

from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from domain.exceptions import GenerationException
from domain.models.audio_sample import AudioSample
from domain.models.voice_profile import VoiceProfile
from domain.ports.tts_engine import EngineCapabilities
from infra.engines.qwen3.adapter import Qwen3Adapter


@pytest.fixture
def qwen3_config():
    """Create a test configuration for Qwen3Adapter."""
    return {
        "model_name": "Qwen/Qwen3-TTS-12Hz-1.7B-Base",
        "device": "cpu",
        "dtype": "float32",
        "cache_dir": "./data/models",
    }


@pytest.fixture
def sample_audio_sample(tmp_path):
    """Create a sample AudioSample for testing."""
    # Create a dummy audio file
    audio_file = tmp_path / "test_sample.wav"
    audio_file.touch()

    return AudioSample(
        path=audio_file,
        duration=10.0,
        sample_rate=12000,
        channels=1,
        bit_depth=16,
        emotion="neutral",
    )


@pytest.fixture
def sample_profile(sample_audio_sample):
    """Create a sample VoiceProfile for testing."""
    return VoiceProfile.create(
        name="test_profile",
        samples=[sample_audio_sample],
        language="es",
        reference_text="Test reference text",
    )


class TestQwen3Adapter:
    """Test suite for Qwen3Adapter."""

    def test_implements_tts_engine_port(self, qwen3_config):
        """Test that Qwen3Adapter implements TTSEngine port."""
        from domain.ports.tts_engine import TTSEngine

        adapter = Qwen3Adapter(qwen3_config)

        assert isinstance(adapter, TTSEngine)

    def test_get_capabilities(self, qwen3_config):
        """Test getting engine capabilities."""
        adapter = Qwen3Adapter(qwen3_config)

        capabilities = adapter.get_capabilities()

        assert isinstance(capabilities, EngineCapabilities)
        assert capabilities.max_text_length == 2048
        assert capabilities.recommended_text_length == 400
        assert capabilities.supports_streaming is False
        assert capabilities.min_sample_duration == 3.0
        assert capabilities.max_sample_duration == 30.0

    def test_get_supported_modes(self, qwen3_config):
        """Test getting supported generation modes."""
        adapter = Qwen3Adapter(qwen3_config)

        modes = adapter.get_supported_modes()

        assert isinstance(modes, list)
        assert "clone" in modes
        assert len(modes) >= 1

    def test_validate_profile_valid(self, qwen3_config, sample_profile):
        """Test validating a valid profile."""
        adapter = Qwen3Adapter(qwen3_config)

        result = adapter.validate_profile(sample_profile)

        assert result is True

    def test_validate_profile_no_samples(self, qwen3_config):
        """Test validating a profile with no samples."""
        adapter = Qwen3Adapter(qwen3_config)

        # Create profile with no samples
        profile = VoiceProfile(
            id="test_id",
            name="test",
            samples=[],
            created_at=None,
        )

        result = adapter.validate_profile(profile)

        assert result is False

    def test_validate_profile_sample_too_short(self, qwen3_config, tmp_path):
        """Test validating a profile with sample that's too short."""
        adapter = Qwen3Adapter(qwen3_config)

        # Create sample with duration < 3 seconds
        audio_file = tmp_path / "short_sample.wav"
        audio_file.touch()

        # Create sample with valid duration first, then manually set invalid duration
        # to bypass AudioSample validation (for testing adapter validation)
        short_sample = AudioSample(
            path=audio_file,
            duration=10.0,  # Valid for creation
            sample_rate=12000,
            channels=1,
            bit_depth=16,
        )
        # Manually set invalid duration to test adapter validation
        object.__setattr__(short_sample, "duration", 2.0)

        profile = VoiceProfile(
            id="test_id",
            name="test",
            samples=[short_sample],
            created_at=None,
        )

        result = adapter.validate_profile(profile)

        assert result is False

    def test_validate_profile_sample_too_long(self, qwen3_config, tmp_path):
        """Test validating a profile with sample that's too long."""
        adapter = Qwen3Adapter(qwen3_config)

        # Create sample with duration > 30 seconds
        audio_file = tmp_path / "long_sample.wav"
        audio_file.touch()

        # Create sample with valid duration first, then manually set invalid duration
        long_sample = AudioSample(
            path=audio_file,
            duration=10.0,  # Valid for creation
            sample_rate=12000,
            channels=1,
            bit_depth=16,
        )
        # Manually set invalid duration to test adapter validation
        object.__setattr__(long_sample, "duration", 35.0)

        profile = VoiceProfile(
            id="test_id",
            name="test",
            samples=[long_sample],
            created_at=None,
        )

        result = adapter.validate_profile(profile)

        assert result is False

    def test_validate_profile_total_duration_too_short(self, qwen3_config, tmp_path):
        """Test validating a profile with total duration < 10 seconds."""
        adapter = Qwen3Adapter(qwen3_config)

        # Create sample with valid individual duration but total < 10s
        audio_file = tmp_path / "sample.wav"
        audio_file.touch()

        sample = AudioSample(
            path=audio_file,
            duration=5.0,  # Valid individually, but total < 10s
            sample_rate=12000,
            channels=1,
            bit_depth=16,
        )

        # Create profile directly without validation to test adapter validation
        profile = VoiceProfile(
            id="test_id",
            name="test",
            samples=[sample],
            created_at=None,
        )

        result = adapter.validate_profile(profile)

        assert result is False

    def test_validate_profile_sample_file_not_exists(self, qwen3_config):
        """Test validating a profile with non-existent sample file."""
        adapter = Qwen3Adapter(qwen3_config)

        # Create sample with non-existent file
        sample = AudioSample(
            path=Path("/nonexistent/file.wav"),
            duration=10.0,
            sample_rate=12000,
            channels=1,
            bit_depth=16,
        )

        profile = VoiceProfile.create(
            name="test",
            samples=[sample],
        )

        result = adapter.validate_profile(profile)

        assert result is False

    def test_generate_audio_unsupported_mode(
        self, qwen3_config, sample_profile, tmp_path
    ):
        """Test generating audio with unsupported mode raises error."""
        adapter = Qwen3Adapter(qwen3_config)
        output_path = tmp_path / "output.wav"

        with pytest.raises(GenerationException, match="Unsupported mode"):
            adapter.generate_audio(
                text="Test text",
                profile=sample_profile,
                output_path=output_path,
                mode="unsupported_mode",
            )

    def test_generate_audio_invalid_profile(self, qwen3_config, tmp_path):
        """Test generating audio with invalid profile raises error."""
        adapter = Qwen3Adapter(qwen3_config)
        output_path = tmp_path / "output.wav"

        # Create invalid profile (no samples)
        invalid_profile = VoiceProfile(
            id="test_id",
            name="test",
            samples=[],
            created_at=None,
        )

        with pytest.raises(GenerationException, match="Invalid profile"):
            adapter.generate_audio(
                text="Test text",
                profile=invalid_profile,
                output_path=output_path,
            )

    @patch("infra.engines.qwen3.adapter.Qwen3ModelLoader")
    @patch("infra.engines.qwen3.adapter.Qwen3Inference")
    def test_generate_audio_success(
        self,
        mock_inference_class,
        mock_loader_class,
        qwen3_config,
        sample_profile,
        tmp_path,
    ):
        """Test successful audio generation."""
        # Setup mocks
        mock_loader = Mock()
        mock_loader.load_model.return_value = True
        mock_loader_class.return_value = mock_loader

        mock_inference = Mock()
        mock_inference.generate_to_file.return_value = True
        mock_inference_class.return_value = mock_inference

        adapter = Qwen3Adapter(qwen3_config)
        output_path = tmp_path / "output.wav"

        # Generate audio
        result = adapter.generate_audio(
            text="Test text",
            profile=sample_profile,
            output_path=output_path,
        )

        # Verify
        assert result == output_path
        mock_loader.load_model.assert_called_once()
        mock_inference.generate_to_file.assert_called_once()

    @patch("infra.engines.qwen3.adapter.Qwen3ModelLoader")
    def test_generate_audio_model_load_failure(
        self, mock_loader_class, qwen3_config, sample_profile, tmp_path
    ):
        """Test audio generation when model fails to load."""
        # Setup mock to fail loading
        mock_loader = Mock()
        mock_loader.load_model.return_value = False
        mock_loader_class.return_value = mock_loader

        adapter = Qwen3Adapter(qwen3_config)
        output_path = tmp_path / "output.wav"

        with pytest.raises(GenerationException, match="Failed to load"):
            adapter.generate_audio(
                text="Test text",
                profile=sample_profile,
                output_path=output_path,
            )

    @patch("infra.engines.qwen3.adapter.Qwen3ModelLoader")
    @patch("infra.engines.qwen3.adapter.Qwen3Inference")
    def test_generate_audio_generation_failure(
        self,
        mock_inference_class,
        mock_loader_class,
        qwen3_config,
        sample_profile,
        tmp_path,
    ):
        """Test audio generation when generation fails."""
        # Setup mocks
        mock_loader = Mock()
        mock_loader.load_model.return_value = True
        mock_loader_class.return_value = mock_loader

        mock_inference = Mock()
        mock_inference.generate_to_file.return_value = False  # Generation fails
        mock_inference_class.return_value = mock_inference

        adapter = Qwen3Adapter(qwen3_config)
        output_path = tmp_path / "output.wav"

        with pytest.raises(GenerationException, match="Audio generation failed"):
            adapter.generate_audio(
                text="Test text",
                profile=sample_profile,
                output_path=output_path,
            )

    @patch("infra.engines.qwen3.adapter.Qwen3ModelLoader")
    def test_unload_model(self, mock_loader_class, qwen3_config):
        """Test unloading the model."""
        mock_loader = Mock()
        mock_loader.load_model.return_value = True
        mock_loader_class.return_value = mock_loader

        adapter = Qwen3Adapter(qwen3_config)

        # Load model first
        adapter._loaded = True
        adapter.inference = Mock()

        # Unload
        adapter.unload_model()

        assert adapter._loaded is False
        assert adapter.inference is None
        mock_loader.unload_model.assert_called_once()

    def test_is_loaded_initially_false(self, qwen3_config):
        """Test that model is not loaded initially."""
        adapter = Qwen3Adapter(qwen3_config)

        assert adapter.is_loaded() is False

    @patch("infra.engines.qwen3.adapter.Qwen3ModelLoader")
    @patch("infra.engines.qwen3.adapter.Qwen3Inference")
    def test_is_loaded_after_generation(
        self,
        mock_inference_class,
        mock_loader_class,
        qwen3_config,
        sample_profile,
        tmp_path,
    ):
        """Test that model is loaded after successful generation."""
        # Setup mocks
        mock_loader = Mock()
        mock_loader.load_model.return_value = True
        mock_loader_class.return_value = mock_loader

        mock_inference = Mock()
        mock_inference.generate_to_file.return_value = True
        mock_inference_class.return_value = mock_inference

        adapter = Qwen3Adapter(qwen3_config)
        output_path = tmp_path / "output.wav"

        # Generate audio
        adapter.generate_audio(
            text="Test text",
            profile=sample_profile,
            output_path=output_path,
        )

        assert adapter.is_loaded() is True
