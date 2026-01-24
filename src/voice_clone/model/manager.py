"""Model management for XTTS-v2."""

import sys
from pathlib import Path
from typing import Any

from voice_clone.utils.logger import logger


class ModelManager:
    """Manages XTTS-v2 model loading and caching."""

    def __init__(self, config: dict[str, Any]):
        """Initialize ModelManager.

        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.model: Any | None = None
        
        # Check if device is specified in config
        config_device = config.get("model", {}).get("device", "auto")
        if config_device == "auto":
            self.device = self._detect_device()
        else:
            self.device = config_device
            logger.info(f"Using device from config: {self.device}")
        
        self.model_name = config.get("model", {}).get(
            "name", "tts_models/multilingual/multi-dataset/xtts_v2"
        )
        self.models_cache = Path(config.get("paths", {}).get("models", "./data/models"))

    def _detect_device(self) -> str:
        """Detect best available device (MPS/CUDA/CPU).

        Returns:
            Device string: "mps", "cuda", or "cpu"
        """
        # Check for MPS (Apple Silicon)
        if sys.platform == "darwin":
            try:
                import torch

                if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
                    logger.info("Using Metal Performance Shaders (MPS)")
                    return "mps"
            except ImportError:
                pass

        # Check for CUDA
        try:
            import torch

            if torch.cuda.is_available():
                logger.info(f"Using CUDA: {torch.cuda.get_device_name(0)}")
                return "cuda"
        except ImportError:
            pass

        # Fallback to CPU
        logger.info("Using CPU (slower performance)")
        return "cpu"

    def load_model(self) -> bool:
        """Load XTTS-v2 model.

        Downloads model if not cached, then loads into memory.

        Returns:
            True if successful, False otherwise
        """
        if self.model is not None:
            logger.info("Model already loaded")
            return True

        try:
            # Import TTS
            try:
                from TTS.api import TTS
            except ImportError:
                logger.error(
                    "TTS library not installed. Install with: pip install TTS>=0.22.0"
                )
                return False

            # Create cache directory
            self.models_cache.mkdir(parents=True, exist_ok=True)

            logger.info(f"Loading model: {self.model_name}")
            logger.info(f"Device: {self.device}")
            logger.info(f"Cache directory: {self.models_cache}")

            # Initialize TTS with progress
            self.model = TTS(
                model_name=self.model_name,
                progress_bar=True,
            ).to(self.device)

            logger.info("✓ Model loaded successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            self.model = None
            return False

    def unload_model(self) -> None:
        """Unload model from memory."""
        if self.model is not None:
            del self.model
            self.model = None

            # Clear CUDA cache if available
            try:
                import torch

                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
            except ImportError:
                pass

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
