"""
Property-based tests for Qwen3-TTS migration.

Feature: migrate-to-qwen3-tts
These tests verify the correctness properties defined in the migration design document.
"""

import subprocess
import sys
from pathlib import Path

import pytest


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


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
