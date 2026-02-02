"""Unit tests for AudioGenerationService."""

from pathlib import Path
from unittest.mock import Mock

import pytest

from domain.models.audio_sample import AudioSample
from domain.models.voice_profile import VoiceProfile
from domain.ports.tts_engine import EngineCapabilities, TTSEngine
from domain.services.audio_generation import AudioGenerationService


@pytest.fixture
def mock_tts_engine():
    """Create a mock TTS engine."""
    engine = Mock(spec=TTSEngine)
    # Default capabilities
    engine.get_capabilities.return_value = EngineCapabilities(
        max_text_length=2048,
        recommended_text_length=400,
        supports_streaming=False,
        min_sample_duration=3.0,
        max_sample_duration=30.0,
    )
    engine.get_supported_modes.return_value = ["clone"]
    engine.validate_profile.return_value = True
    return engine


@pytest.fixture
def valid_profile():
    """Create a valid voice profile."""
    samples = [
        AudioSample(
            path=Path("sample1.wav"),
            duration=10.0,
            sample_rate=12000,
            channels=1,
            bit_depth=16,
        ),
        AudioSample(
            path=Path("sample2.wav"),
            duration=15.0,
            sample_rate=12000,
            channels=1,
            bit_depth=16,
        ),
    ]
    return VoiceProfile.create(name="test_profile", samples=samples)


@pytest.fixture
def audio_generation_service(mock_tts_engine):
    """Create an audio generation service with mocked dependencies."""
    return AudioGenerationService(tts_engine=mock_tts_engine)


class TestTextLengthValidation:
    """Test text length validation (defense in depth)."""

    def test_text_within_recommended_length_succeeds(
        self, audio_generation_service, mock_tts_engine, valid_profile
    ):
        """Test that text within recommended length succeeds."""
        text = "A" * 300  # Within 400 char recommended limit
        output_path = Path("output.wav")
        mock_tts_engine.generate_audio.return_value = output_path

        result = audio_generation_service.generate_with_profile(
            text=text, profile=valid_profile, output_path=output_path
        )

        assert result == output_path
        mock_tts_engine.generate_audio.assert_called_once()

    def test_text_exceeds_recommended_but_within_max_logs_warning(
        self, audio_generation_service, mock_tts_engine, valid_profile, caplog
    ):
        """Test that text exceeding recommended but within max logs warning."""
        text = "A" * 500  # Exceeds 400 recommended, but within 2048 max
        output_path = Path("output.wav")
        mock_tts_engine.generate_audio.return_value = output_path

        result = audio_generation_service.generate_with_profile(
            text=text, profile=valid_profile, output_path=output_path
        )

        # Should succeed but log warning
        assert result == output_path
        assert "exceeds recommended limit" in caplog.text
        assert "400 characters" in caplog.text
        mock_tts_engine.generate_audio.assert_called_once()

    def test_text_exceeds_max_length_raises_error(
        self, audio_generation_service, mock_tts_engine, valid_profile
    ):
        """Test that text exceeding max length raises error."""
        text = "A" * 3000  # Exceeds 2048 max
        output_path = Path("output.wav")

        with pytest.raises(ValueError) as exc_info:
            audio_generation_service.generate_with_profile(
                text=text, profile=valid_profile, output_path=output_path
            )

        error_msg = str(exc_info.value)
        assert "exceeds maximum limit" in error_msg
        assert "2048 characters" in error_msg
        assert "3000 characters" in error_msg
        mock_tts_engine.generate_audio.assert_not_called()

    def test_text_at_exact_max_length_succeeds(
        self, audio_generation_service, mock_tts_engine, valid_profile, caplog
    ):
        """Test that text at exact max length succeeds with warning."""
        text = "A" * 2048  # Exactly at max
        output_path = Path("output.wav")
        mock_tts_engine.generate_audio.return_value = output_path

        result = audio_generation_service.generate_with_profile(
            text=text, profile=valid_profile, output_path=output_path
        )

        # Should succeed with warning (exceeds recommended)
        assert result == output_path
        assert "exceeds recommended limit" in caplog.text
        mock_tts_engine.generate_audio.assert_called_once()

    def test_text_at_exact_recommended_length_succeeds_no_warning(
        self, audio_generation_service, mock_tts_engine, valid_profile, caplog
    ):
        """Test that text at exact recommended length succeeds without warning."""
        text = "A" * 400  # Exactly at recommended
        output_path = Path("output.wav")
        mock_tts_engine.generate_audio.return_value = output_path

        result = audio_generation_service.generate_with_profile(
            text=text, profile=valid_profile, output_path=output_path
        )

        # Should succeed without warning
        assert result == output_path
        assert "exceeds recommended limit" not in caplog.text
        mock_tts_engine.generate_audio.assert_called_once()

    def test_validation_uses_engine_capabilities(self, mock_tts_engine, valid_profile):
        """Test that validation uses engine-specific capabilities."""
        # Create engine with different limits
        mock_tts_engine.get_capabilities.return_value = EngineCapabilities(
            max_text_length=1000,  # Different max
            recommended_text_length=200,  # Different recommended
            supports_streaming=False,
        )
        service = AudioGenerationService(tts_engine=mock_tts_engine)

        text = "A" * 1500  # Exceeds new max of 1000
        output_path = Path("output.wav")

        with pytest.raises(ValueError) as exc_info:
            service.generate_with_profile(
                text=text, profile=valid_profile, output_path=output_path
            )

        error_msg = str(exc_info.value)
        assert "1000 characters" in error_msg  # Uses engine's max


class TestGenerateWithProfile:
    """Test generate_with_profile method."""

    def test_generate_with_valid_inputs_succeeds(
        self, audio_generation_service, mock_tts_engine, valid_profile
    ):
        """Test successful audio generation."""
        text = "Hello, this is a test."
        output_path = Path("output.wav")
        mock_tts_engine.generate_audio.return_value = output_path

        result = audio_generation_service.generate_with_profile(
            text=text, profile=valid_profile, output_path=output_path
        )

        assert result == output_path
        mock_tts_engine.generate_audio.assert_called_once_with(
            text=text,
            profile=valid_profile,
            output_path=output_path,
            mode="clone",
        )

    def test_generate_with_custom_mode(
        self, audio_generation_service, mock_tts_engine, valid_profile
    ):
        """Test generation with custom mode."""
        mock_tts_engine.get_supported_modes.return_value = ["clone", "custom"]
        text = "Test text"
        output_path = Path("output.wav")
        mock_tts_engine.generate_audio.return_value = output_path

        result = audio_generation_service.generate_with_profile(
            text=text, profile=valid_profile, output_path=output_path, mode="custom"
        )

        assert result == output_path
        mock_tts_engine.generate_audio.assert_called_once_with(
            text=text,
            profile=valid_profile,
            output_path=output_path,
            mode="custom",
        )

    def test_generate_with_empty_text_fails(
        self, audio_generation_service, mock_tts_engine, valid_profile
    ):
        """Test that empty text raises error."""
        output_path = Path("output.wav")

        with pytest.raises(ValueError, match="Text cannot be empty"):
            audio_generation_service.generate_with_profile(
                text="", profile=valid_profile, output_path=output_path
            )

        mock_tts_engine.generate_audio.assert_not_called()

    def test_generate_with_whitespace_only_text_fails(
        self, audio_generation_service, mock_tts_engine, valid_profile
    ):
        """Test that whitespace-only text raises error."""
        output_path = Path("output.wav")

        with pytest.raises(ValueError, match="Text cannot be empty"):
            audio_generation_service.generate_with_profile(
                text="   \n\t  ", profile=valid_profile, output_path=output_path
            )

        mock_tts_engine.generate_audio.assert_not_called()

    def test_generate_with_invalid_profile_fails(
        self, audio_generation_service, mock_tts_engine
    ):
        """Test that invalid profile raises error."""
        # Create invalid profile (no samples)
        from datetime import datetime

        invalid_profile = VoiceProfile(
            id="test-id", name="test", samples=[], created_at=datetime.now()
        )

        text = "Test text"
        output_path = Path("output.wav")

        with pytest.raises(ValueError, match="Invalid profile"):
            audio_generation_service.generate_with_profile(
                text=text, profile=invalid_profile, output_path=output_path
            )

        mock_tts_engine.generate_audio.assert_not_called()

    def test_generate_with_unsupported_mode_fails(
        self, audio_generation_service, mock_tts_engine, valid_profile
    ):
        """Test that unsupported mode raises error."""
        mock_tts_engine.get_supported_modes.return_value = ["clone"]
        text = "Test text"
        output_path = Path("output.wav")

        with pytest.raises(ValueError, match="Unsupported mode 'invalid'"):
            audio_generation_service.generate_with_profile(
                text=text,
                profile=valid_profile,
                output_path=output_path,
                mode="invalid",
            )

        mock_tts_engine.generate_audio.assert_not_called()

    def test_generate_with_incompatible_profile_fails(
        self, audio_generation_service, mock_tts_engine, valid_profile
    ):
        """Test that incompatible profile raises error."""
        mock_tts_engine.validate_profile.return_value = False
        text = "Test text"
        output_path = Path("output.wav")

        with pytest.raises(ValueError, match="not compatible with this TTS engine"):
            audio_generation_service.generate_with_profile(
                text=text, profile=valid_profile, output_path=output_path
            )

        mock_tts_engine.generate_audio.assert_not_called()

    def test_generate_passes_kwargs_to_engine(
        self, audio_generation_service, mock_tts_engine, valid_profile
    ):
        """Test that additional kwargs are passed to engine."""
        text = "Test text"
        output_path = Path("output.wav")
        mock_tts_engine.generate_audio.return_value = output_path

        audio_generation_service.generate_with_profile(
            text=text,
            profile=valid_profile,
            output_path=output_path,
            temperature=0.8,
            speed=1.2,
        )

        mock_tts_engine.generate_audio.assert_called_once_with(
            text=text,
            profile=valid_profile,
            output_path=output_path,
            mode="clone",
            temperature=0.8,
            speed=1.2,
        )


class TestServiceDependencies:
    """Test service dependencies and initialization."""

    def test_service_requires_tts_engine(self):
        """Test that service requires TTS engine."""
        mock_engine = Mock(spec=TTSEngine)
        service = AudioGenerationService(tts_engine=mock_engine)

        assert service._tts_engine is mock_engine

    def test_service_uses_injected_tts_engine(
        self, audio_generation_service, mock_tts_engine, valid_profile
    ):
        """Test that service uses the injected TTS engine."""
        text = "Test text"
        output_path = Path("output.wav")
        mock_tts_engine.generate_audio.return_value = output_path

        audio_generation_service.generate_with_profile(
            text=text, profile=valid_profile, output_path=output_path
        )

        # Verify the injected engine was used
        mock_tts_engine.get_capabilities.assert_called()
        mock_tts_engine.get_supported_modes.assert_called()
        mock_tts_engine.validate_profile.assert_called_once_with(valid_profile)
        mock_tts_engine.generate_audio.assert_called_once()
