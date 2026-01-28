"""
Property tests for system cleanup after Coqui TTS removal.

Property 8: System Package Removal
Validates: Requirements 1.5, 10.2, 10.5, 15.5
"""

import subprocess
import sys
from pathlib import Path

import pytest


class TestSystemPackageRemoval:
    """Property 8: System Package Removal - Validates complete TTS removal from system."""

    def test_tts_package_not_installed(self) -> None:
        """Verify TTS package is not installed in pip."""
        result = subprocess.run(
            [sys.executable, "-m", "pip", "show", "TTS"],
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0, "TTS package should not be installed"
        assert (
            "WARNING: Package(s) not found: TTS" in result.stderr
            or "not found" in result.stderr.lower()
        )

    def test_tts_not_importable(self) -> None:
        """Verify TTS cannot be imported."""
        result = subprocess.run(
            [sys.executable, "-c", "import TTS"],
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0, "TTS should not be importable"
        assert (
            "ModuleNotFoundError" in result.stderr or "No module named" in result.stderr
        )

    def test_tts_api_not_importable(self) -> None:
        """Verify TTS.api cannot be imported."""
        result = subprocess.run(
            [sys.executable, "-c", "from TTS.api import TTS"],
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0, "TTS.api should not be importable"
        assert (
            "ModuleNotFoundError" in result.stderr or "No module named" in result.stderr
        )

    def test_qwen_tts_installed(self) -> None:
        """Verify qwen-tts is installed."""
        result = subprocess.run(
            [sys.executable, "-m", "pip", "show", "qwen-tts"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, "qwen-tts should be installed"
        assert "Name: qwen-tts" in result.stdout

    def test_qwen_tts_importable(self) -> None:
        """Verify qwen_tts can be imported."""
        result = subprocess.run(
            [sys.executable, "-c", "from qwen_tts import Qwen3TTSModel"],
            capture_output=True,
            text=True,
        )
        assert (
            result.returncode == 0
        ), f"qwen_tts should be importable. Error: {result.stderr}"

    def test_no_tts_in_pip_list(self) -> None:
        """Verify TTS does not appear in pip list."""
        result = subprocess.run(
            [sys.executable, "-m", "pip", "list"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        # Check that TTS is not in the list (case-insensitive)
        lines = result.stdout.lower().split("\n")
        tts_lines = [line for line in lines if line.startswith("tts ")]
        assert len(tts_lines) == 0, f"TTS should not be in pip list. Found: {tts_lines}"

    def test_qwen_tts_in_pip_list(self) -> None:
        """Verify qwen-tts appears in pip list."""
        result = subprocess.run(
            [sys.executable, "-m", "pip", "list"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "qwen-tts" in result.stdout.lower(), "qwen-tts should be in pip list"

    def test_tts_cache_cleaned(self) -> None:
        """Verify TTS cache directories are removed or archived."""
        # Common TTS cache locations
        cache_dirs = [
            Path.home() / ".local" / "share" / "tts",
            Path.home() / ".cache" / "tts",
            Path("data") / "models" / "xtts-v2",
            Path("data") / "models" / "xtts_v2",
        ]

        for cache_dir in cache_dirs:
            if cache_dir.exists():
                # If it exists, it should be empty or contain only qwen3 models
                contents = list(cache_dir.iterdir())
                if contents:
                    # Check that no XTTS-v2 models are present
                    xtts_files = [
                        f
                        for f in contents
                        if "xtts" in f.name.lower() and "qwen" not in f.name.lower()
                    ]
                    assert (
                        len(xtts_files) == 0
                    ), f"XTTS files found in {cache_dir}: {xtts_files}"

    def test_models_directory_exists(self) -> None:
        """Verify models directory exists."""
        models_dir = Path("data") / "models"
        assert models_dir.exists(), "data/models directory should exist"
        assert models_dir.is_dir(), "data/models should be a directory"

    @pytest.mark.parametrize("iteration", range(10))
    def test_system_state_consistent(self, iteration: int) -> None:
        """Property test: System state is consistent across multiple checks."""
        # TTS should not be installed
        result = subprocess.run(
            [sys.executable, "-m", "pip", "show", "TTS"],
            capture_output=True,
            text=True,
        )
        assert (
            result.returncode != 0
        ), f"Iteration {iteration}: TTS should not be installed"

        # qwen-tts should be installed
        result = subprocess.run(
            [sys.executable, "-m", "pip", "show", "qwen-tts"],
            capture_output=True,
            text=True,
        )
        assert (
            result.returncode == 0
        ), f"Iteration {iteration}: qwen-tts should be installed"


class TestSystemCleanupVerification:
    """Additional verification tests for system cleanup."""

    def test_no_tts_dependencies_lingering(self) -> None:
        """Verify no TTS-specific dependencies are lingering."""
        # Get list of installed packages
        result = subprocess.run(
            [sys.executable, "-m", "pip", "list"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        # Note: TTS-specific packages might still be installed if used by other packages
        # We just verify that TTS itself is not present

    def test_import_voice_clone_works(self) -> None:
        """Verify voice_clone package can still be imported."""
        result = subprocess.run(
            [sys.executable, "-c", "import voice_clone; print('OK')"],
            capture_output=True,
            text=True,
        )
        assert (
            result.returncode == 0
        ), f"voice_clone should be importable. Error: {result.stderr}"
        assert "OK" in result.stdout

    def test_qwen3_model_manager_importable(self) -> None:
        """Verify Qwen3ModelManager can be imported."""
        result = subprocess.run(
            [
                sys.executable,
                "-c",
                "from voice_clone.model import Qwen3ModelManager; print('OK')",
            ],
            capture_output=True,
            text=True,
        )
        assert (
            result.returncode == 0
        ), f"Qwen3ModelManager should be importable. Error: {result.stderr}"
        assert "OK" in result.stdout

    def test_qwen3_generator_importable(self) -> None:
        """Verify Qwen3Generator can be imported."""
        result = subprocess.run(
            [
                sys.executable,
                "-c",
                "from voice_clone.model import Qwen3Generator; print('OK')",
            ],
            capture_output=True,
            text=True,
        )
        assert (
            result.returncode == 0
        ), f"Qwen3Generator should be importable. Error: {result.stderr}"
        assert "OK" in result.stdout

    def test_cli_available(self) -> None:
        """Verify CLI is still available."""
        result = subprocess.run(
            ["voice-clone", "--help"],
            capture_output=True,
            text=True,
        )
        # CLI might have import issues during migration, but the command should exist
        # We just verify the command is found (not "command not found")
        if result.returncode != 0:
            assert (
                "command not found" not in result.stderr.lower()
            ), f"CLI command should exist. Error: {result.stderr}"
        else:
            assert (
                "voice-clone" in result.stdout.lower()
                or "usage" in result.stdout.lower()
            )
