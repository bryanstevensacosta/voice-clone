"""Model management for Qwen3-TTS."""

import sys
from pathlib import Path
from typing import Any

import torch

from voice_clone.utils.logger import logger


class Qwen3ModelManager:
    """Manages Qwen3-TTS model loading and caching."""

    def __init__(self, config: dict[str, Any]):
        """Initialize Qwen3ModelManager.

        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.model: Any | None = None

        # Detect device and dtype
        self.device, self.dtype = self._get_device_info()

        # Model configuration
        self.model_name = config.get("model", {}).get(
            "name", "Qwen/Qwen3-TTS-12Hz-1.7B-Base"
        )
        self.models_cache = Path(
            config.get("paths", {}).get("models", "./data/qwen3_models")
        )

    def _get_device_info(self) -> tuple[str, torch.dtype]:
        """Detect optimal device (MPS/CPU) and dtype.

        For Apple Silicon M1 Pro, uses MPS with float32.
        For other platforms, uses CPU with float32.

        Returns:
            Tuple of (device_string, dtype)
        """
        # Check config first
        config_device = self.config.get("model", {}).get("device", "auto")
        config_dtype = self.config.get("model", {}).get("dtype", "float32")

        # Parse dtype
        if config_dtype == "float32":
            dtype = torch.float32
        elif config_dtype == "float16":
            dtype = torch.float16
        elif config_dtype == "bfloat16":
            dtype = torch.bfloat16
        else:
            dtype = torch.float32

        # Auto-detect device if needed
        if config_device == "auto":
            # Check for MPS (Apple Silicon)
            if sys.platform == "darwin":
                if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
                    logger.info("Using Metal Performance Shaders (MPS)")
                    # MPS requires float32 for Qwen3-TTS
                    return "mps", torch.float32

            # Fallback to CPU
            logger.info("Using CPU")
            return "cpu", dtype
        else:
            logger.info(f"Using device from config: {config_device}")
            # Force float32 for MPS
            if config_device == "mps":
                return config_device, torch.float32
            return config_device, dtype

    def load_model(self) -> bool:
        """Load Qwen3-TTS model with MPS optimization.

        Downloads model if not cached, then loads into memory.

        Returns:
            True if successful, False otherwise
        """
        if self.model is not None:
            logger.info("Model already loaded")
            return True

        try:
            # Import Qwen3-TTS
            try:
                from qwen_tts import Qwen3TTSModel
            except ImportError:
                logger.error(
                    "qwen-tts library not installed. Install with: pip install qwen-tts>=1.0.0"
                )
                return False

            # Create cache directory
            self.models_cache.mkdir(parents=True, exist_ok=True)

            logger.info(f"Loading model: {self.model_name}")
            logger.info(f"Device: {self.device}")
            logger.info(f"Dtype: {self.dtype}")
            logger.info(f"Cache directory: {self.models_cache}")

            # Load model with from_pretrained
            self.model = Qwen3TTSModel.from_pretrained(
                self.model_name,
                cache_dir=str(self.models_cache),
                torch_dtype=self.dtype,
            )

            # Move model to device
            self.model = self.model.to(self.device)

            logger.info("✓ Model loaded successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            logger.exception("Full traceback:")
            self.model = None
            return False

    def unload_model(self) -> None:
        """Unload model and free memory."""
        if self.model is not None:
            del self.model
            self.model = None

            # Clear MPS cache if available
            if self.device == "mps" and hasattr(torch.backends, "mps"):
                try:
                    # MPS doesn't have empty_cache, but we can trigger garbage collection
                    import gc

                    gc.collect()
                except Exception:
                    pass

            # Clear CUDA cache if available
            if self.device == "cuda" and torch.cuda.is_available():
                torch.cuda.empty_cache()

            logger.info("Model unloaded from memory")

    def is_loaded(self) -> bool:
        """Check if model is loaded.

        Returns:
            True if model is loaded, False otherwise
        """
        return self.model is not None

    def get_model(self) -> Any | None:
        """Get loaded model instance.

        Returns:
            Model instance or None if not loaded
        """
        return self.model

    def get_device_info(self) -> tuple[str, torch.dtype]:
        """Get device and dtype information.

        Returns:
            Tuple of (device_string, dtype)
        """
        return self.device, self.dtype
