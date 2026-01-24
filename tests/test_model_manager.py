"""Unit tests for ModelManager."""

from pathlib import Path
from typing import Any

from voice_clone.model.manager import ModelManager


def test_model_manager_initialization() -> None:
    """Test ModelManager initializes with config."""
    config: dict[str, Any] = {
        "model": {"name": "tts_models/multilingual/multi-dataset/xtts_v2"},
        "paths": {"models": "./data/models"},
    }

    manager = ModelManager(config)

    assert manager.config == config
    assert manager.model is None
    assert manager.device in ["mps", "cuda", "cpu"]
    assert manager.model_name == "tts_models/multilingual/multi-dataset/xtts_v2"
    assert isinstance(manager.models_cache, Path)


def test_model_manager_device_detection() -> None:
    """Test device detection returns valid device."""
    config: dict[str, Any] = {"model": {}, "paths": {}}
    manager = ModelManager(config)

    device = manager._detect_device()

    assert device in ["mps", "cuda", "cpu"]


def test_model_manager_is_loaded_initially_false() -> None:
    """Test model is not loaded initially."""
    config: dict[str, Any] = {"model": {}, "paths": {}}
    manager = ModelManager(config)

    assert not manager.is_loaded()
    assert manager.get_model() is None


def test_model_manager_unload_when_not_loaded() -> None:
    """Test unload works even when model not loaded."""
    config: dict[str, Any] = {"model": {}, "paths": {}}
    manager = ModelManager(config)

    # Should not raise error
    manager.unload_model()

    assert not manager.is_loaded()
