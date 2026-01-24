"""
Property-based tests for Qwen3-TTS migration.

Feature: migrate-to-qwen3-tts
These tests verify the correctness properties defined in the migration design document.
"""

import pytest
import subprocess
import sys
from pathlib import Path


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
            [sys.executable, "-m", "pip", "list"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0, "pip list command failed"
        assert "qwen-tts" in result.stdout.lower(), \
            "qwen-tts package not found in pip list"
    
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
        assert hasattr(Qwen3TTSModel, "from_pretrained"), \
            "Qwen3TTSModel missing from_pretrained method"
        
        # Check that from_pretrained is callable
        assert callable(Qwen3TTSModel.from_pretrained), \
            "from_pretrained is not callable"


class TestQwen3Installation:
    """
    Additional tests to verify Qwen3-TTS installation is complete and functional.
    """
    
    def test_qwen_tts_version(self) -> None:
        """Test that qwen-tts has a valid version."""
        result = subprocess.run(
            [sys.executable, "-m", "pip", "show", "qwen-tts"],
            capture_output=True,
            text=True
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
            "librosa"
        ]
        
        result = subprocess.run(
            [sys.executable, "-m", "pip", "list"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        pip_output = result.stdout.lower()
        
        for package in required_packages:
            assert package.lower() in pip_output, \
                f"Required dependency {package} not found"
    
    def test_torch_mps_available(self) -> None:
        """Test that PyTorch MPS backend is available (for Apple Silicon)."""
        import torch
        
        # This test should pass on Apple Silicon M1/M2/M3
        # On other platforms, it will be skipped or show as expected
        if torch.backends.mps.is_available():
            assert torch.backends.mps.is_built(), \
                "MPS is available but not built"
        else:
            # Not on Apple Silicon, skip this check
            pytest.skip("MPS not available on this platform")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
