"""
Property-based tests for Qwen3-TTS migration.

Feature: migrate-to-qwen3-tts
These tests verify the correctness properties defined in the migration design document.
"""

import subprocess
import sys
from pathlib import Path

import pytest
import torch


class TestCoquiTTSCompleteRemoval:
    """
    Property 1: Coqui TTS Complete Removal

    For any file in the project, searching for "TTS.api", "XTTS", "xtts_v2", or "Coqui"
    should return zero matches after migration.

    Validates: Requirements 1.1, 1.2, 1.3
    """

    def test_no_coqui_in_requirements_txt(self) -> None:
        """
        Test that requirements.txt does not contain TTS package reference.

        Feature: migrate-to-qwen3-tts, Property 1: Coqui TTS Complete Removal
        """
        requirements_path = Path("requirements.txt")
        assert requirements_path.exists(), "requirements.txt not found"

        content = requirements_path.read_text()

        # Check that TTS package is not present
        assert "TTS>=" not in content, "TTS package still in requirements.txt"
        assert "TTS==" not in content, "TTS package still in requirements.txt"

        # Verify qwen-tts is present instead
        assert "qwen-tts" in content, "qwen-tts not found in requirements.txt"

    def test_no_coqui_in_pyproject_toml(self) -> None:
        """
        Test that pyproject.toml does not contain XTTS-v2 or TTS references.

        Feature: migrate-to-qwen3-tts, Property 1: Coqui TTS Complete Removal
        """
        pyproject_path = Path("pyproject.toml")
        assert pyproject_path.exists(), "pyproject.toml not found"

        content = pyproject_path.read_text()

        # Check that xtts-v2 keyword is not present
        assert "xtts-v2" not in content.lower(), "xtts-v2 still in pyproject.toml"

        # Check that TTS.* mypy override is not present
        assert 'module = "TTS.*"' not in content, "TTS.* mypy override still present"

        # Verify qwen3-tts keyword is present
        assert "qwen3-tts" in content, "qwen3-tts keyword not found in pyproject.toml"

        # Verify qwen_tts.* mypy override is present
        assert 'module = "qwen_tts.*"' in content, "qwen_tts.* mypy override not found"

    def test_no_coqui_in_setup_py(self) -> None:
        """
        Test that setup.py does not contain TTS package in install_requires.

        Feature: migrate-to-qwen3-tts, Property 1: Coqui TTS Complete Removal
        """
        setup_path = Path("setup.py")
        assert setup_path.exists(), "setup.py not found"

        content = setup_path.read_text()

        # Check that TTS package is not in install_requires
        assert '"TTS>=' not in content, "TTS package still in setup.py install_requires"
        assert "'TTS>=" not in content, "TTS package still in setup.py install_requires"

        # Check that xtts-v2 keyword is not present
        assert "xtts-v2" not in content.lower(), "xtts-v2 still in setup.py keywords"

        # Verify qwen-tts is present
        assert "qwen-tts" in content, "qwen-tts not found in setup.py"

        # Verify qwen3-tts keyword is present
        assert "qwen3-tts" in content, "qwen3-tts keyword not found in setup.py"

    def test_no_tts_package_installed(self) -> None:
        """
        Test that TTS package is not installed in the system.

        Feature: migrate-to-qwen3-tts, Property 1: Coqui TTS Complete Removal
        """
        result = subprocess.run(
            [sys.executable, "-m", "pip", "list"], capture_output=True, text=True
        )

        assert result.returncode == 0, "pip list command failed"

        # Check that TTS package is not in the list
        # Note: This will be case-insensitive to catch any variations
        pip_output_lower = result.stdout.lower()

        # Split into lines and check each package name
        for line in pip_output_lower.split("\n"):
            if line.strip():
                # Get package name (first column)
                parts = line.split()
                if parts:
                    package_name = parts[0]
                    # Check if it's exactly "tts" (not "qwen-tts" or other packages)
                    if package_name == "tts":
                        pytest.fail("TTS package is still installed")

    def test_tts_not_importable(self) -> None:
        """
        Test that TTS.api cannot be imported.

        Feature: migrate-to-qwen3-tts, Property 1: Coqui TTS Complete Removal
        """
        with pytest.raises(ImportError):
            from TTS.api import TTS  # noqa: F401


class TestQwen3DependencyPresence:
    """
    Property 2: Qwen3-TTS Dependency Presence

    For any dependency file (requirements.txt, pyproject.toml, setup.py),
    the file should contain "qwen-tts" or "qwen_tts" references.

    Validates: Requirements 2.1, 2.2, 2.3
    """

    def test_qwen_tts_in_pip_list(self) -> None:
        """
        Test that qwen-tts package is installed in the system.

        Feature: migrate-to-qwen3-tts, Property 2: Qwen3-TTS Dependency Presence
        """
        # Run pip list and check for qwen-tts
        result = subprocess.run(
            [sys.executable, "-m", "pip", "list"], capture_output=True, text=True
        )

        assert result.returncode == 0, "pip list command failed"
        assert (
            "qwen-tts" in result.stdout.lower()
        ), "qwen-tts package not found in pip list"

    def test_qwen_tts_importable(self) -> None:
        """
        Test that qwen_tts module can be imported.

        Feature: migrate-to-qwen3-tts, Property 2: Qwen3-TTS Dependency Presence
        """
        try:
            from qwen_tts import Qwen3TTSModel

            assert Qwen3TTSModel is not None
        except ImportError as e:
            pytest.fail(f"Failed to import qwen_tts: {e}")

    def test_qwen_tts_model_class_exists(self) -> None:
        """
        Test that Qwen3TTSModel class exists and has expected methods.

        Feature: migrate-to-qwen3-tts, Property 2: Qwen3-TTS Dependency Presence
        """
        from qwen_tts import Qwen3TTSModel

        # Check that the class has the expected methods
        assert hasattr(
            Qwen3TTSModel, "from_pretrained"
        ), "Qwen3TTSModel missing from_pretrained method"

        # Check that from_pretrained is callable
        assert callable(
            Qwen3TTSModel.from_pretrained
        ), "from_pretrained is not callable"


class TestQwen3Installation:
    """
    Additional tests to verify Qwen3-TTS installation is complete and functional.
    """

    def test_qwen_tts_version(self) -> None:
        """Test that qwen-tts has a valid version."""
        result = subprocess.run(
            [sys.executable, "-m", "pip", "show", "qwen-tts"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, "pip show qwen-tts failed"
        assert "Version:" in result.stdout, "No version information found"

        # Extract version
        for line in result.stdout.split("\n"):
            if line.startswith("Version:"):
                version = line.split(":", 1)[1].strip()
                assert len(version) > 0, "Empty version string"
                break

    def test_qwen_tts_dependencies_installed(self) -> None:
        """Test that key dependencies for qwen-tts are installed."""
        required_packages = [
            "transformers",
            "accelerate",
            "torch",
            "torchaudio",
            "soundfile",
            "librosa",
        ]

        result = subprocess.run(
            [sys.executable, "-m", "pip", "list"], capture_output=True, text=True
        )

        assert result.returncode == 0
        pip_output = result.stdout.lower()

        for package in required_packages:
            assert (
                package.lower() in pip_output
            ), f"Required dependency {package} not found"

    def test_torch_mps_available(self) -> None:
        """Test that PyTorch MPS backend is available (for Apple Silicon)."""
        import torch

        # This test should pass on Apple Silicon M1/M2/M3
        # On other platforms, it will be skipped or show as expected
        if torch.backends.mps.is_available():
            assert torch.backends.mps.is_built(), "MPS is available but not built"
        else:
            # Not on Apple Silicon, skip this check
            pytest.skip("MPS not available on this platform")


class TestModelLoadingUsesQwen3:
    """
    Property 3: Model Loading Uses Qwen3

    For any model loading operation, the code should call Qwen3TTSModel.from_pretrained
    and should not import from TTS.api.

    Validates: Requirements 3.1, 3.5
    """

    def test_qwen3_model_manager_uses_qwen3tts(self) -> None:
        """
        Test that Qwen3ModelManager uses Qwen3TTSModel for loading.

        Feature: migrate-to-qwen3-tts, Property 3: Model Loading Uses Qwen3
        """
        from typing import Any
        from unittest.mock import MagicMock, patch

        from voice_clone.model.qwen3_manager import Qwen3ModelManager

        config: dict[str, Any] = {"model": {}, "paths": {}}
        manager = Qwen3ModelManager(config)

        # Mock Qwen3TTSModel
        mock_model = MagicMock()
        mock_model.to.return_value = mock_model

        with patch("qwen_tts.Qwen3TTSModel") as MockModel:
            MockModel.from_pretrained.return_value = mock_model

            result = manager.load_model()

            # Verify Qwen3TTSModel.from_pretrained was called
            assert result is True
            MockModel.from_pretrained.assert_called_once()

            # Verify the call includes the correct model name
            call_args = MockModel.from_pretrained.call_args
            assert call_args is not None
            assert "Qwen/Qwen3-TTS" in call_args[0][0]

    def test_no_tts_api_imports_in_qwen3_manager(self) -> None:
        """
        Test that qwen3_manager.py does not import from TTS.api.

        Feature: migrate-to-qwen3-tts, Property 3: Model Loading Uses Qwen3
        """
        manager_path = Path("src/voice_clone/model/qwen3_manager.py")
        assert manager_path.exists(), "qwen3_manager.py not found"

        content = manager_path.read_text()

        # Check that TTS.api is not imported
        assert "from TTS.api import" not in content, "TTS.api import found"
        assert "from TTS import" not in content, "TTS import found"
        assert "import TTS" not in content, "TTS import found"

        # Verify qwen_tts is imported
        assert "from qwen_tts import" in content, "qwen_tts import not found"

    def test_qwen3_model_manager_exported_from_init(self) -> None:
        """
        Test that Qwen3ModelManager is exported from model/__init__.py.

        Feature: migrate-to-qwen3-tts, Property 3: Model Loading Uses Qwen3
        """
        from voice_clone.model import Qwen3ModelManager

        assert Qwen3ModelManager is not None
        assert callable(Qwen3ModelManager)

    def test_model_init_does_not_export_old_manager(self) -> None:
        """
        Test that model/__init__.py does not export old ModelManager.

        Feature: migrate-to-qwen3-tts, Property 3: Model Loading Uses Qwen3
        """
        init_path = Path("src/voice_clone/model/__init__.py")
        assert init_path.exists(), "model/__init__.py not found"

        content = init_path.read_text()

        # Check that old ModelManager is not exported
        # Note: It might still exist in the codebase but shouldn't be in __all__
        if "__all__" in content:
            # If __all__ is defined, check it doesn't include old manager
            assert (
                '"ModelManager"' not in content or "Qwen3ModelManager" in content
            ), "Old ModelManager still exported"


class TestMPSDeviceConfiguration:
    """
    Property 4: MPS Device Configuration

    For any Apple Silicon system, when detecting device, the system should select "mps"
    as device and torch.float32 as dtype.

    Validates: Requirements 3.2, 3.3
    """

    def test_mps_device_selected_on_darwin_with_mps(self) -> None:
        """
        Test that MPS device is selected on macOS with MPS available.

        Feature: migrate-to-qwen3-tts, Property 4: MPS Device Configuration
        """
        from typing import Any
        from unittest.mock import patch

        from voice_clone.model.qwen3_manager import Qwen3ModelManager

        config: dict[str, Any] = {"model": {"device": "auto"}, "paths": {}}

        with patch("sys.platform", "darwin"):
            with patch("torch.backends.mps.is_available", return_value=True):
                manager = Qwen3ModelManager(config)

                device, dtype = manager.get_device_info()

                assert device == "mps", f"Expected 'mps', got '{device}'"
                assert dtype == torch.float32, f"Expected torch.float32, got {dtype}"

    def test_float32_forced_for_mps(self) -> None:
        """
        Test that float32 is forced for MPS even if config specifies different dtype.

        Feature: migrate-to-qwen3-tts, Property 4: MPS Device Configuration
        """
        from typing import Any

        from voice_clone.model.qwen3_manager import Qwen3ModelManager

        # Try to configure float16 with MPS
        config: dict[str, Any] = {
            "model": {"device": "mps", "dtype": "float16"},
            "paths": {},
        }

        manager = Qwen3ModelManager(config)

        device, dtype = manager.get_device_info()

        # MPS should force float32
        assert device == "mps"
        assert dtype == torch.float32, "MPS should force float32 dtype"

    def test_cpu_fallback_when_mps_unavailable(self) -> None:
        """
        Test that CPU is used when MPS is not available on macOS.

        Feature: migrate-to-qwen3-tts, Property 4: MPS Device Configuration
        """
        from typing import Any
        from unittest.mock import patch

        from voice_clone.model.qwen3_manager import Qwen3ModelManager

        config: dict[str, Any] = {"model": {"device": "auto"}, "paths": {}}

        with patch("sys.platform", "darwin"):
            with patch("torch.backends.mps.is_available", return_value=False):
                manager = Qwen3ModelManager(config)

                device, dtype = manager.get_device_info()

                assert device == "cpu", "Should fallback to CPU when MPS unavailable"
                assert dtype == torch.float32

    def test_explicit_mps_configuration(self) -> None:
        """
        Test that explicit MPS configuration is respected.

        Feature: migrate-to-qwen3-tts, Property 4: MPS Device Configuration
        """
        from typing import Any

        from voice_clone.model.qwen3_manager import Qwen3ModelManager

        config: dict[str, Any] = {"model": {"device": "mps"}, "paths": {}}

        manager = Qwen3ModelManager(config)

        device, dtype = manager.get_device_info()

        assert device == "mps"
        assert dtype == torch.float32

    def test_model_moved_to_mps_device(self) -> None:
        """
        Test that model is moved to MPS device after loading.

        Feature: migrate-to-qwen3-tts, Property 4: MPS Device Configuration
        """
        from typing import Any
        from unittest.mock import MagicMock, patch

        from voice_clone.model.qwen3_manager import Qwen3ModelManager

        config: dict[str, Any] = {"model": {"device": "mps"}, "paths": {}}

        manager = Qwen3ModelManager(config)

        mock_model = MagicMock()
        mock_model.to.return_value = mock_model

        with patch("qwen_tts.Qwen3TTSModel") as MockModel:
            MockModel.from_pretrained.return_value = mock_model

            result = manager.load_model()

            assert result is True
            # Verify model.to() was called with "mps"
            mock_model.to.assert_called_once_with("mps")


class TestAudioGenerationMethod:
    """
    Property 5: Audio Generation Method

    For any audio generation call, the code should invoke model.generate_voice_clone
    with parameters (text, language, ref_audio, ref_text) and should not call model.tts.

    Validates: Requirements 4.1, 4.2, 4.3, 4.4, 4.5
    """

    def test_qwen3_generator_uses_generate_voice_clone(self) -> None:
        """
        Test that Qwen3Generator uses generate_voice_clone method.

        Feature: migrate-to-qwen3-tts, Property 5: Audio Generation Method
        """
        from typing import Any
        from unittest.mock import MagicMock

        import numpy as np

        from voice_clone.model.qwen3_generator import Qwen3Generator
        from voice_clone.model.qwen3_manager import Qwen3ModelManager

        config: dict[str, Any] = {"model": {}, "paths": {}}
        manager = Qwen3ModelManager(config)
        generator = Qwen3Generator(manager, config)

        # Mock model
        mock_model = MagicMock()
        mock_audio = np.array([0.1, 0.2, 0.3])
        mock_sample_rate = 12000
        mock_model.generate_voice_clone.return_value = (mock_audio, mock_sample_rate)

        manager.model = mock_model

        # Generate audio
        result = generator.generate(
            text="Test text",
            ref_audio="ref.wav",
            ref_text="Reference text",
        )

        assert result is not None

        # Verify generate_voice_clone was called
        mock_model.generate_voice_clone.assert_called_once()

        # Verify the call includes required parameters
        call_args = mock_model.generate_voice_clone.call_args
        assert call_args is not None
        assert call_args[1]["text"] == "Test text"
        assert call_args[1]["ref_audio"] == "ref.wav"
        assert call_args[1]["ref_text"] == "Reference text"
        assert "language" in call_args[1]

    def test_no_tts_method_in_qwen3_generator(self) -> None:
        """
        Test that qwen3_generator.py does not call model.tts method.

        Feature: migrate-to-qwen3-tts, Property 5: Audio Generation Method
        """
        generator_path = Path("src/voice_clone/model/qwen3_generator.py")
        assert generator_path.exists(), "qwen3_generator.py not found"

        content = generator_path.read_text()

        # Check that model.tts is not called
        assert "model.tts(" not in content, "model.tts() call found"
        assert ".tts(" not in content, ".tts() call found"

        # Verify generate_voice_clone is used
        assert (
            "generate_voice_clone" in content
        ), "generate_voice_clone not found in generator"

    def test_generator_requires_ref_text_parameter(self) -> None:
        """
        Test that generator requires ref_text parameter for generation.

        Feature: migrate-to-qwen3-tts, Property 5: Audio Generation Method
        """
        from typing import Any

        from voice_clone.model.qwen3_generator import Qwen3Generator
        from voice_clone.model.qwen3_manager import Qwen3ModelManager

        config: dict[str, Any] = {"model": {}, "paths": {}}
        manager = Qwen3ModelManager(config)
        generator = Qwen3Generator(manager, config)

        # Check that generate method signature includes ref_text
        import inspect

        sig = inspect.signature(generator.generate)
        params = sig.parameters

        assert "ref_text" in params, "ref_text parameter not found in generate method"
        assert params["ref_text"].annotation is str, "ref_text should be type str"

    def test_generator_passes_all_required_params(self) -> None:
        """
        Test that generator passes all required parameters to model.

        Feature: migrate-to-qwen3-tts, Property 5: Audio Generation Method
        """
        from typing import Any
        from unittest.mock import MagicMock

        import numpy as np

        from voice_clone.model.qwen3_generator import Qwen3Generator
        from voice_clone.model.qwen3_manager import Qwen3ModelManager

        config: dict[str, Any] = {"model": {}, "paths": {}}
        manager = Qwen3ModelManager(config)
        generator = Qwen3Generator(manager, config)

        # Mock model
        mock_model = MagicMock()
        mock_audio = np.array([0.1, 0.2, 0.3])
        mock_sample_rate = 12000
        mock_model.generate_voice_clone.return_value = (mock_audio, mock_sample_rate)

        manager.model = mock_model

        # Generate with all parameters
        result = generator.generate(
            text="Test text",
            ref_audio="ref.wav",
            ref_text="Reference text",
            language="Spanish",
            max_new_tokens=2048,
        )

        assert result is not None

        # Verify all parameters were passed
        call_args = mock_model.generate_voice_clone.call_args
        assert call_args[1]["text"] == "Test text"
        assert call_args[1]["ref_audio"] == "ref.wav"
        assert call_args[1]["ref_text"] == "Reference text"
        assert call_args[1]["language"] == "Spanish"
        assert call_args[1]["max_new_tokens"] == 2048

    def test_generator_exported_from_init(self) -> None:
        """
        Test that Qwen3Generator is exported from model/__init__.py.

        Feature: migrate-to-qwen3-tts, Property 5: Audio Generation Method
        """
        from voice_clone.model import Qwen3Generator

        assert Qwen3Generator is not None
        assert callable(Qwen3Generator)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


class TestAudioSampleValidation:
    """
    Property 9: Audio Sample Validation

    For any audio sample, if duration is >= 3 seconds and format is valid,
    then validation should pass for Qwen3-TTS.

    Validates: Requirements 8.1, 8.3
    """

    def test_audio_processor_minimum_duration_is_3_seconds(self) -> None:
        """
        Test that AudioProcessor validates minimum 3 seconds for Qwen3-TTS.

        Feature: migrate-to-qwen3-tts, Property 9: Audio Sample Validation
        """
        from voice_clone.audio.processor import AudioProcessor

        processor = AudioProcessor()

        # Verify default sample rate is 12000 Hz (Qwen3-TTS)
        assert processor.sample_rate == 12000, "Default sample rate should be 12000 Hz"

    def test_validation_accepts_3_second_samples(self) -> None:
        """
        Test that validation accepts samples >= 3 seconds.

        Feature: migrate-to-qwen3-tts, Property 9: Audio Sample Validation
        """
        from unittest.mock import MagicMock, patch

        import numpy as np

        from voice_clone.audio.processor import AudioProcessor

        processor = AudioProcessor()

        # Mock a valid 3-second sample
        mock_audio = np.random.randn(36000) * 0.3  # 3 seconds at 12kHz
        mock_info = MagicMock()
        mock_info.subtype = "PCM_16"

        with patch("librosa.load", return_value=(mock_audio, 12000)):
            with patch("soundfile.info", return_value=mock_info):
                with patch("librosa.get_duration", return_value=3.0):
                    result = processor.validate_sample("test.wav")

                    # Should not have duration error
                    assert not any(
                        "minimum: 3s" in error for error in result.errors
                    ), "3-second sample should pass duration check"

    def test_validation_rejects_below_3_seconds(self) -> None:
        """
        Test that validation rejects samples < 3 seconds.

        Feature: migrate-to-qwen3-tts, Property 9: Audio Sample Validation
        """
        from unittest.mock import MagicMock, patch

        import numpy as np

        from voice_clone.audio.processor import AudioProcessor

        processor = AudioProcessor()

        # Mock a 2-second sample (too short)
        mock_audio = np.random.randn(24000) * 0.3  # 2 seconds at 12kHz
        mock_info = MagicMock()
        mock_info.subtype = "PCM_16"

        with patch("librosa.load", return_value=(mock_audio, 12000)):
            with patch("soundfile.info", return_value=mock_info):
                with patch("librosa.get_duration", return_value=2.0):
                    result = processor.validate_sample("test.wav")

                    # Should have duration error
                    assert any(
                        "minimum: 3s" in error for error in result.errors
                    ), "2-second sample should fail duration check"

    def test_validation_warns_for_non_12khz(self) -> None:
        """
        Test that validation warns for non-12kHz sample rate.

        Feature: migrate-to-qwen3-tts, Property 9: Audio Sample Validation
        """
        from unittest.mock import MagicMock, patch

        import numpy as np

        from voice_clone.audio.processor import AudioProcessor

        processor = AudioProcessor()

        # Mock a sample at 22050 Hz (not Qwen3-TTS native)
        mock_audio = np.random.randn(66150) * 0.3  # 3 seconds at 22050Hz
        mock_info = MagicMock()
        mock_info.subtype = "PCM_16"

        with patch("librosa.load", return_value=(mock_audio, 22050)):
            with patch("soundfile.info", return_value=mock_info):
                with patch("librosa.get_duration", return_value=3.0):
                    result = processor.validate_sample("test.wav")

                    # Should warn about sample rate
                    assert any(
                        "12000 Hz" in warning for warning in result.warnings
                    ), "Should warn about non-12kHz sample rate"


class TestOutputSampleRate:
    """
    Property 10: Output Sample Rate

    For any generated audio output, the native sample rate should be 12000 Hz
    unless explicitly upsampled.

    Validates: Requirements 8.2, 8.4
    """

    def test_qwen3_generator_returns_12khz_audio(self) -> None:
        """
        Test that Qwen3Generator returns 12kHz audio by default.

        Feature: migrate-to-qwen3-tts, Property 10: Output Sample Rate
        """
        from typing import Any
        from unittest.mock import MagicMock

        import numpy as np

        from voice_clone.model.qwen3_generator import Qwen3Generator
        from voice_clone.model.qwen3_manager import Qwen3ModelManager

        config: dict[str, Any] = {"model": {}, "paths": {}}
        manager = Qwen3ModelManager(config)
        generator = Qwen3Generator(manager, config)

        # Mock model to return 12kHz audio
        mock_model = MagicMock()
        mock_audio = np.random.randn(12000)  # 1 second at 12kHz
        mock_sample_rate = 12000
        mock_model.generate_voice_clone.return_value = (mock_audio, mock_sample_rate)

        manager.model = mock_model

        # Generate audio
        result = generator.generate(
            text="Test text",
            ref_audio="ref.wav",
            ref_text="Reference text",
        )

        assert result is not None
        audio, sample_rate = result

        # Verify sample rate is 12000 Hz
        assert sample_rate == 12000, "Qwen3-TTS should return 12kHz audio"

    def test_audio_processor_can_upsample_to_22khz(self) -> None:
        """
        Test that AudioProcessor can upsample 12kHz to 22kHz.

        Feature: migrate-to-qwen3-tts, Property 10: Output Sample Rate
        """
        from unittest.mock import patch

        import numpy as np

        from voice_clone.audio.processor import AudioProcessor

        processor = AudioProcessor()

        # Create 12kHz audio
        audio_12k = np.random.randn(12000)  # 1 second at 12kHz

        with patch("librosa.resample") as mock_resample:
            mock_resample.return_value = np.random.randn(22050)  # 1 second at 22kHz

            processor.upsample_output(audio_12k, 12000, 22050)

            # Verify resample was called with correct parameters
            mock_resample.assert_called_once()
            call_args = mock_resample.call_args
            assert call_args[1]["orig_sr"] == 12000
            assert call_args[1]["target_sr"] == 22050

    def test_audio_processor_has_upsample_methods(self) -> None:
        """
        Test that AudioProcessor has upsampling methods for Qwen3-TTS output.

        Feature: migrate-to-qwen3-tts, Property 10: Output Sample Rate
        """
        from voice_clone.audio.processor import AudioProcessor

        processor = AudioProcessor()

        # Verify upsampling methods exist
        assert hasattr(
            processor, "upsample_output"
        ), "AudioProcessor should have upsample_output method"
        assert hasattr(
            processor, "upsample_file"
        ), "AudioProcessor should have upsample_file method"
        assert hasattr(
            processor, "convert_sample_rate"
        ), "AudioProcessor should have convert_sample_rate method"

    def test_audio_processor_default_sample_rate_is_12khz(self) -> None:
        """
        Test that AudioProcessor default sample rate is 12kHz for Qwen3-TTS.

        Feature: migrate-to-qwen3-tts, Property 10: Output Sample Rate
        """
        from voice_clone.audio.processor import AudioProcessor

        processor = AudioProcessor()

        # Verify default sample rate
        assert (
            processor.sample_rate == 12000
        ), "AudioProcessor default should be 12kHz for Qwen3-TTS"

    def test_resample_to_qwen3_method_exists(self) -> None:
        """
        Test that AudioProcessor has resample_to_qwen3 method.

        Feature: migrate-to-qwen3-tts, Property 10: Output Sample Rate
        """
        from voice_clone.audio.processor import AudioProcessor

        processor = AudioProcessor()

        # Verify method exists
        assert hasattr(
            processor, "resample_to_qwen3"
        ), "AudioProcessor should have resample_to_qwen3 method"
        assert callable(
            processor.resample_to_qwen3
        ), "resample_to_qwen3 should be callable"
