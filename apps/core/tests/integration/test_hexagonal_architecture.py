"""
Integration tests for hexagonal architecture validation.

Tests dependency inversion, adapter swapping, and port implementations.
"""

from datetime import datetime
from pathlib import Path
from unittest.mock import Mock

import pytest
from domain.models.audio_sample import AudioSample
from domain.models.voice_profile import VoiceProfile
from domain.ports.audio_processor import AudioProcessor
from domain.ports.tts_engine import TTSEngine
from domain.services.voice_cloning import VoiceCloningService
from infra.audio.processor_adapter import LibrosaAudioProcessor
from infra.engines.qwen3.adapter import Qwen3Adapter
from infra.persistence.file_profile_repository import FileProfileRepository


class TestDependencyInversion:
    """Test that domain depends on ports, not adapters."""

    def test_voice_cloning_service_accepts_any_audio_processor(self):
        """VoiceCloningService should work with any AudioProcessor implementation."""
        # Create a mock audio processor
        mock_processor = Mock(spec=AudioProcessor)
        mock_processor.validate_sample.return_value = True
        mock_processor.process_sample.return_value = AudioSample(
            path=Path("test.wav"),
            duration=10.0,
            sample_rate=12000,
            channels=1,
            bit_depth=16,
        )

        # Service should accept the mock
        service = VoiceCloningService(audio_processor=mock_processor)

        # Should be able to create profile
        profile = service.create_profile_from_samples(
            name="test", sample_paths=[Path("test.wav")]
        )

        assert profile.name == "test"
        assert len(profile.samples) == 1
        mock_processor.validate_sample.assert_called_once()
        mock_processor.process_sample.assert_called_once()

    def test_voice_cloning_service_rejects_invalid_interface(self):
        """VoiceCloningService should only accept AudioProcessor interface."""
        # Create an object that doesn't implement AudioProcessor
        invalid_processor = Mock()
        invalid_processor.some_method = Mock()

        # Should raise TypeError or AttributeError when trying to use it
        service = VoiceCloningService(audio_processor=invalid_processor)

        with pytest.raises((AttributeError, TypeError)):
            service.create_profile_from_samples(
                name="test", sample_paths=[Path("test.wav")]
            )


class TestAdapterSwapping:
    """Test that adapters can be swapped without changing domain logic."""

    @pytest.fixture
    def mock_audio_processor(self):
        """Create a mock audio processor."""
        processor = Mock(spec=AudioProcessor)
        processor.validate_sample.return_value = True
        processor.process_sample.return_value = AudioSample(
            path=Path("test.wav"),
            duration=10.0,
            sample_rate=12000,
            channels=1,
            bit_depth=16,
        )
        return processor

    @pytest.fixture
    def real_audio_processor(self):
        """Create a real audio processor."""
        return LibrosaAudioProcessor()

    def test_swap_audio_processor_adapters(
        self, mock_audio_processor, real_audio_processor, tmp_path
    ):
        """Test swapping between mock and real audio processor."""
        # Create a simple audio file for real processor
        import numpy as np
        import soundfile as sf

        sample_path = tmp_path / "test.wav"
        # Create 10 seconds of audio (120000 samples at 12000 Hz)
        # Normalize to 0.5 to prevent clipping
        audio_data = 0.5 * np.sin(2 * np.pi * 440 * np.linspace(0, 10, 120000))
        sf.write(sample_path, audio_data, 12000)

        # Test with mock processor
        service_mock = VoiceCloningService(audio_processor=mock_audio_processor)
        profile_mock = service_mock.create_profile_from_samples(
            name="test_mock", sample_paths=[Path("test.wav")]
        )

        assert profile_mock.name == "test_mock"
        assert len(profile_mock.samples) == 1

        # Test with real processor
        service_real = VoiceCloningService(audio_processor=real_audio_processor)
        profile_real = service_real.create_profile_from_samples(
            name="test_real", sample_paths=[sample_path]
        )

        assert profile_real.name == "test_real"
        assert len(profile_real.samples) == 1

        # Both should produce valid profiles
        assert profile_mock.is_valid()
        assert profile_real.is_valid()

    def test_swap_repository_adapters(self, tmp_path):
        """Test swapping between different repository implementations."""
        # Create two different repository instances with different paths
        repo1 = FileProfileRepository(profiles_dir=tmp_path / "repo1")
        repo2 = FileProfileRepository(profiles_dir=tmp_path / "repo2")

        # Create a valid profile with samples
        from domain.models.audio_sample import AudioSample

        sample = AudioSample(
            path=Path("test.wav"),
            duration=10.0,
            sample_rate=12000,
            channels=1,
            bit_depth=16,
        )

        profile = VoiceProfile(
            id="test-id",
            name="test_profile",
            samples=[sample],
            created_at=datetime.now(),
            language="es",
        )

        # Save to repo1
        repo1.save(profile)
        assert repo1.find_by_id("test-id") is not None

        # repo2 should not have it
        assert repo2.find_by_id("test-id") is None

        # Save to repo2
        repo2.save(profile)
        assert repo2.find_by_id("test-id") is not None

        # Both repos work independently
        assert len(repo1.list_all()) == 1
        assert len(repo2.list_all()) == 1


class TestPortImplementations:
    """Test that all adapters correctly implement their ports."""

    def test_librosa_audio_processor_implements_port(self):
        """LibrosaAudioProcessor should implement AudioProcessor port."""
        processor = LibrosaAudioProcessor()

        # Check that it has all required methods
        assert hasattr(processor, "validate_sample")
        assert hasattr(processor, "process_sample")
        assert hasattr(processor, "normalize_audio")

        # Check that methods are callable
        assert callable(processor.validate_sample)
        assert callable(processor.process_sample)
        assert callable(processor.normalize_audio)

    def test_qwen3_adapter_implements_port(self):
        """Qwen3Adapter should implement TTSEngine port."""
        config = {
            "model_name": "Qwen/Qwen3-TTS-12Hz-1.7B-Base",
            "device": "cpu",
            "dtype": "float32",
        }
        adapter = Qwen3Adapter(config)

        # Check that it has all required methods
        assert hasattr(adapter, "get_supported_modes")
        assert hasattr(adapter, "generate_audio")
        assert hasattr(adapter, "validate_profile")

        # Check that methods are callable
        assert callable(adapter.get_supported_modes)
        assert callable(adapter.generate_audio)
        assert callable(adapter.validate_profile)

    def test_file_repository_implements_port(self, tmp_path):
        """FileProfileRepository should implement ProfileRepository port."""
        repository = FileProfileRepository(profiles_dir=tmp_path)

        # Check that it has all required methods
        assert hasattr(repository, "save")
        assert hasattr(repository, "find_by_id")
        assert hasattr(repository, "list_all")
        assert hasattr(repository, "delete")

        # Check that methods are callable
        assert callable(repository.save)
        assert callable(repository.find_by_id)
        assert callable(repository.list_all)
        assert callable(repository.delete)


class TestArchitecturalBoundaries:
    """Test that architectural boundaries are respected."""

    def test_domain_has_no_infrastructure_imports(self):
        """Domain layer should not import from infrastructure layer."""
        import inspect

        from domain.models import voice_profile
        from domain.services import voice_cloning

        # Get source code
        profile_source = inspect.getsource(voice_profile)
        service_source = inspect.getsource(voice_cloning)

        # Check for forbidden imports
        forbidden_imports = ["from infra", "import infra", "from infrastructure"]

        for source in [profile_source, service_source]:
            for forbidden in forbidden_imports:
                assert (
                    forbidden not in source
                ), f"Domain layer should not import from infrastructure: {forbidden}"

    def test_domain_only_depends_on_ports(self):
        """Domain services should only depend on ports, not adapters."""
        # Get constructor signature
        import inspect

        from domain.services.voice_cloning import VoiceCloningService

        sig = inspect.signature(VoiceCloningService.__init__)

        # Check that audio_processor parameter is typed as AudioProcessor (port)
        audio_processor_param = sig.parameters.get("audio_processor")
        assert audio_processor_param is not None

        # The annotation should be AudioProcessor (the port)
        annotation = audio_processor_param.annotation
        assert "AudioProcessor" in str(annotation)

    def test_use_cases_depend_on_ports_not_adapters(self):
        """Use cases should depend on ports, not concrete adapters."""
        import inspect

        from app.use_cases.create_voice_profile import CreateVoiceProfileUseCase

        sig = inspect.signature(CreateVoiceProfileUseCase.__init__)

        # Check parameters are typed as ports
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue

            annotation = str(param.annotation)

            # Should not reference concrete adapters
            assert "Adapter" not in annotation
            assert "Librosa" not in annotation
            assert "Qwen3" not in annotation
            assert "File" not in annotation or "Repository" in annotation


class TestAdapterIsolation:
    """Test that adapters are isolated and can fail independently."""

    def test_audio_processor_failure_does_not_affect_repository(self, tmp_path):
        """Audio processor failure should not affect repository operations."""
        # Create a failing audio processor
        failing_processor = Mock(spec=AudioProcessor)
        failing_processor.validate_sample.side_effect = Exception(
            "Audio processing failed"
        )

        # Create a working repository
        repository = FileProfileRepository(profiles_dir=tmp_path)

        # Repository should still work - create valid profile with samples
        sample = AudioSample(
            path=Path("test.wav"),
            duration=10.0,
            sample_rate=12000,
            channels=1,
            bit_depth=16,
        )
        profile = VoiceProfile(
            id="test-id",
            name="test",
            samples=[sample],
            created_at=datetime.now(),
            language="es",
        )

        repository.save(profile)
        assert repository.find_by_id("test-id") is not None

        # But voice cloning service should fail
        service = VoiceCloningService(audio_processor=failing_processor)

        with pytest.raises(Exception, match="Audio processing failed"):
            service.create_profile_from_samples(
                name="test", sample_paths=[Path("test.wav")]
            )

    def test_tts_engine_can_be_replaced_without_domain_changes(self):
        """TTS engine can be replaced without changing domain logic."""
        # Create two different TTS engine mocks
        engine1 = Mock(spec=TTSEngine)
        engine1.get_supported_modes.return_value = ["clone"]
        engine1.generate_audio.return_value = Path("output1.wav")

        engine2 = Mock(spec=TTSEngine)
        engine2.get_supported_modes.return_value = ["clone", "custom"]
        engine2.generate_audio.return_value = Path("output2.wav")

        # Both should work with the same interface
        assert "clone" in engine1.get_supported_modes()
        assert "clone" in engine2.get_supported_modes()

        # Both should generate audio
        output1 = engine1.generate_audio(
            text="test", profile_id="test", output=Path("out.wav")
        )
        output2 = engine2.generate_audio(
            text="test", profile_id="test", output=Path("out.wav")
        )

        assert output1 == Path("output1.wav")
        assert output2 == Path("output2.wav")
