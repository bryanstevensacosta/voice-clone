"""Unit tests for Qwen3ModelManager."""

import sys
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
import torch
from voice_clone.model.qwen3_manager import Qwen3ModelManager


class TestQwen3ModelManagerInitialization:
    """Test Qwen3ModelManager initialization."""

    def test_initialization_with_default_config(self) -> None:
        """Test Qwen3ModelManager initializes with default config."""
        config: dict[str, Any] = {
            "model": {},
            "paths": {},
        }

        manager = Qwen3ModelManager(config)

        assert manager.config == config
        assert manager.model is None
        assert manager.device in ["mps", "cpu"]
        assert manager.dtype in [torch.float32, torch.float16, torch.bfloat16]
        assert manager.model_name == "Qwen/Qwen3-TTS-12Hz-1.7B-Base"
        assert isinstance(manager.models_cache, Path)

    def test_initialization_with_custom_model_name(self) -> None:
        """Test initialization with custom model name."""
        config: dict[str, Any] = {
            "model": {"name": "custom/model-name"},
            "paths": {},
        }

        manager = Qwen3ModelManager(config)

        assert manager.model_name == "custom/model-name"

    def test_initialization_with_custom_cache_path(self) -> None:
        """Test initialization with custom cache path."""
        config: dict[str, Any] = {
            "model": {},
            "paths": {"models": "./custom/cache/path"},
        }

        manager = Qwen3ModelManager(config)

        assert manager.models_cache == Path("./custom/cache/path")


class TestDeviceDetection:
    """Test device detection logic."""

    def test_device_detection_auto_mps_on_darwin(self) -> None:
        """Test device detection selects MPS on macOS with MPS available."""
        config: dict[str, Any] = {
            "model": {"device": "auto"},
            "paths": {},
        }

        with patch("sys.platform", "darwin"):
            with patch("torch.backends.mps.is_available", return_value=True):
                manager = Qwen3ModelManager(config)

                device, dtype = manager.get_device_info()

                assert device == "mps"
                assert dtype == torch.float32  # MPS requires float32

    def test_device_detection_auto_cpu_on_darwin_no_mps(self) -> None:
        """Test device detection falls back to CPU on macOS without MPS."""
        config: dict[str, Any] = {
            "model": {"device": "auto"},
            "paths": {},
        }

        with patch("sys.platform", "darwin"):
            with patch("torch.backends.mps.is_available", return_value=False):
                manager = Qwen3ModelManager(config)

                device, dtype = manager.get_device_info()

                assert device == "cpu"
                assert dtype == torch.float32

    def test_device_detection_auto_cpu_on_linux(self) -> None:
        """Test device detection selects CPU on Linux."""
        config: dict[str, Any] = {
            "model": {"device": "auto"},
            "paths": {},
        }

        with patch("sys.platform", "linux"):
            manager = Qwen3ModelManager(config)

            device, dtype = manager.get_device_info()

            assert device == "cpu"
            assert dtype == torch.float32

    def test_device_detection_explicit_mps(self) -> None:
        """Test device detection with explicit MPS configuration."""
        config: dict[str, Any] = {
            "model": {"device": "mps"},
            "paths": {},
        }

        manager = Qwen3ModelManager(config)

        device, dtype = manager.get_device_info()

        assert device == "mps"
        assert dtype == torch.float32  # MPS forces float32

    def test_device_detection_explicit_cpu(self) -> None:
        """Test device detection with explicit CPU configuration."""
        config: dict[str, Any] = {
            "model": {"device": "cpu"},
            "paths": {},
        }

        manager = Qwen3ModelManager(config)

        device, dtype = manager.get_device_info()

        assert device == "cpu"
        assert dtype == torch.float32


class TestDtypeConfiguration:
    """Test dtype configuration logic."""

    def test_dtype_float32_default(self) -> None:
        """Test default dtype is float32."""
        config: dict[str, Any] = {
            "model": {},
            "paths": {},
        }

        manager = Qwen3ModelManager(config)

        _, dtype = manager.get_device_info()

        assert dtype == torch.float32

    def test_dtype_float32_explicit(self) -> None:
        """Test explicit float32 dtype configuration."""
        config: dict[str, Any] = {
            "model": {"dtype": "float32"},
            "paths": {},
        }

        manager = Qwen3ModelManager(config)

        _, dtype = manager.get_device_info()

        assert dtype == torch.float32

    def test_dtype_float16_on_cpu(self) -> None:
        """Test float16 dtype configuration on CPU."""
        config: dict[str, Any] = {
            "model": {"device": "cpu", "dtype": "float16"},
            "paths": {},
        }

        manager = Qwen3ModelManager(config)

        _, dtype = manager.get_device_info()

        assert dtype == torch.float16

    def test_dtype_bfloat16_on_cpu(self) -> None:
        """Test bfloat16 dtype configuration on CPU."""
        config: dict[str, Any] = {
            "model": {"device": "cpu", "dtype": "bfloat16"},
            "paths": {},
        }

        manager = Qwen3ModelManager(config)

        _, dtype = manager.get_device_info()

        assert dtype == torch.bfloat16

    def test_dtype_forced_float32_on_mps(self) -> None:
        """Test dtype is forced to float32 on MPS regardless of config."""
        config: dict[str, Any] = {
            "model": {"device": "mps", "dtype": "float16"},
            "paths": {},
        }

        manager = Qwen3ModelManager(config)

        _, dtype = manager.get_device_info()

        # MPS should force float32
        assert dtype == torch.float32

    def test_dtype_invalid_defaults_to_float32(self) -> None:
        """Test invalid dtype defaults to float32."""
        config: dict[str, Any] = {
            "model": {"dtype": "invalid_dtype"},
            "paths": {},
        }

        manager = Qwen3ModelManager(config)

        _, dtype = manager.get_device_info()

        assert dtype == torch.float32


class TestModelLoading:
    """Test model loading functionality."""

    def test_load_model_success(self) -> None:
        """Test successful model loading."""
        config: dict[str, Any] = {
            "model": {},
            "paths": {},
        }

        manager = Qwen3ModelManager(config)

        # Mock the Qwen3TTSModel
        mock_model = MagicMock()
        mock_model.to.return_value = mock_model

        with patch("qwen_tts.Qwen3TTSModel") as MockModel:
            MockModel.from_pretrained.return_value = mock_model

            result = manager.load_model()

            assert result is True
            assert manager.is_loaded()
            assert manager.get_model() is not None
            MockModel.from_pretrained.assert_called_once()

    def test_load_model_already_loaded(self) -> None:
        """Test loading model when already loaded."""
        config: dict[str, Any] = {
            "model": {},
            "paths": {},
        }

        manager = Qwen3ModelManager(config)
        manager.model = MagicMock()  # Simulate already loaded

        result = manager.load_model()

        assert result is True
        assert manager.is_loaded()

    def test_load_model_import_error(self) -> None:
        """Test model loading fails gracefully when qwen-tts not installed."""
        config: dict[str, Any] = {
            "model": {},
            "paths": {},
        }

        manager = Qwen3ModelManager(config)

        # Mock the import to raise ImportError
        with patch.dict(sys.modules, {"qwen_tts": None}):
            result = manager.load_model()

            assert result is False
            assert not manager.is_loaded()
            assert manager.get_model() is None

    def test_load_model_exception_handling(self) -> None:
        """Test model loading handles exceptions gracefully."""
        config: dict[str, Any] = {
            "model": {},
            "paths": {},
        }

        manager = Qwen3ModelManager(config)

        with patch("qwen_tts.Qwen3TTSModel") as MockModel:
            MockModel.from_pretrained.side_effect = RuntimeError("Model load failed")

            result = manager.load_model()

            assert result is False
            assert not manager.is_loaded()
            assert manager.get_model() is None

    def test_load_model_creates_cache_directory(self) -> None:
        """Test model loading creates cache directory if it doesn't exist."""
        config: dict[str, Any] = {
            "model": {},
            "paths": {"models": "./test_cache_dir"},
        }

        manager = Qwen3ModelManager(config)

        mock_model = MagicMock()
        mock_model.to.return_value = mock_model

        with patch("qwen_tts.Qwen3TTSModel") as MockModel:
            MockModel.from_pretrained.return_value = mock_model

            result = manager.load_model()

            assert result is True
            # Cache directory should be created
            assert manager.models_cache.exists()

            # Cleanup
            import shutil

            if manager.models_cache.exists():
                shutil.rmtree(manager.models_cache)


class TestModelUnloading:
    """Test model unloading functionality."""

    def test_unload_model_when_loaded(self) -> None:
        """Test unloading model when it's loaded."""
        config: dict[str, Any] = {
            "model": {},
            "paths": {},
        }

        manager = Qwen3ModelManager(config)
        manager.model = MagicMock()  # Simulate loaded model

        manager.unload_model()

        assert not manager.is_loaded()
        assert manager.get_model() is None

    def test_unload_model_when_not_loaded(self) -> None:
        """Test unloading model when it's not loaded (should not raise error)."""
        config: dict[str, Any] = {
            "model": {},
            "paths": {},
        }

        manager = Qwen3ModelManager(config)

        # Should not raise error
        manager.unload_model()

        assert not manager.is_loaded()

    def test_unload_model_clears_mps_cache(self) -> None:
        """Test unloading model triggers garbage collection for MPS."""
        config: dict[str, Any] = {
            "model": {"device": "mps"},
            "paths": {},
        }

        manager = Qwen3ModelManager(config)
        manager.model = MagicMock()

        with patch("gc.collect") as mock_gc:
            manager.unload_model()

            # Garbage collection should be called for MPS
            mock_gc.assert_called_once()

    def test_unload_model_clears_cuda_cache(self) -> None:
        """Test unloading model clears CUDA cache if available."""
        config: dict[str, Any] = {
            "model": {"device": "cuda"},
            "paths": {},
        }

        manager = Qwen3ModelManager(config)
        manager.model = MagicMock()

        with patch("torch.cuda.is_available", return_value=True):
            with patch("torch.cuda.empty_cache") as mock_empty_cache:
                manager.unload_model()

                # CUDA cache should be cleared
                mock_empty_cache.assert_called_once()


class TestModelState:
    """Test model state checking."""

    def test_is_loaded_false_initially(self) -> None:
        """Test model is not loaded initially."""
        config: dict[str, Any] = {
            "model": {},
            "paths": {},
        }

        manager = Qwen3ModelManager(config)

        assert not manager.is_loaded()

    def test_is_loaded_true_when_model_set(self) -> None:
        """Test is_loaded returns True when model is set."""
        config: dict[str, Any] = {
            "model": {},
            "paths": {},
        }

        manager = Qwen3ModelManager(config)
        manager.model = MagicMock()

        assert manager.is_loaded()

    def test_get_model_returns_none_initially(self) -> None:
        """Test get_model returns None initially."""
        config: dict[str, Any] = {
            "model": {},
            "paths": {},
        }

        manager = Qwen3ModelManager(config)

        assert manager.get_model() is None

    def test_get_model_returns_model_when_loaded(self) -> None:
        """Test get_model returns model instance when loaded."""
        config: dict[str, Any] = {
            "model": {},
            "paths": {},
        }

        manager = Qwen3ModelManager(config)
        mock_model = MagicMock()
        manager.model = mock_model

        assert manager.get_model() == mock_model


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
