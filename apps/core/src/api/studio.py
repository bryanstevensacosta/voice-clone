"""TTS Studio API - Main entry point for the core library.

This module provides the main API class that wires together all components
of the hexagonal architecture and exposes a simple interface for external
consumers (primarily the Tauri desktop backend).
"""

import logging
from pathlib import Path
from typing import Any

from app.dto.generation_dto import GenerationRequestDTO
from app.use_cases.create_voice_profile import CreateVoiceProfileUseCase
from app.use_cases.generate_audio import GenerateAudioUseCase
from app.use_cases.list_voice_profiles import ListVoiceProfilesUseCase
from app.use_cases.process_batch import ProcessBatchUseCase
from app.use_cases.validate_audio_samples import ValidateAudioSamplesUseCase
from domain.ports.config_provider import ConfigProvider
from infra.audio.processor_adapter import LibrosaAudioProcessor
from infra.config.yaml_config import YAMLConfigProvider
from infra.engines.qwen3.adapter import Qwen3Adapter
from infra.persistence.file_profile_repository import FileProfileRepository

logger = logging.getLogger(__name__)


class TTSStudio:
    """Main API for TTS Studio core library.

    This class is the primary entry point for external consumers.
    It initializes all adapters (infrastructure) and use cases (application),
    following the hexagonal architecture pattern with dependency injection.

    Example usage:
        >>> from api.studio import TTSStudio
        >>> studio = TTSStudio()
        >>> result = studio.create_voice_profile(
        ...     name="my_voice",
        ...     sample_paths=["sample1.wav", "sample2.wav"]
        ... )
        >>> print(result["status"])  # "success"
    """

    _config: ConfigProvider  # Type annotation for mypy

    def __init__(
        self,
        config_path: Path | None = None,
        config_dict: dict[str, Any] | None = None,
    ):
        """Initialize TTS Studio API.

        Args:
            config_path: Optional path to config file. If None, uses default config.
            config_dict: Optional config dictionary (for testing, bypasses file loading).
        """
        logger.info("Initializing TTS Studio API")

        # Initialize configuration
        self._init_config(config_path, config_dict)

        # Initialize infrastructure adapters
        self._init_adapters()

        # Initialize use cases
        self._init_use_cases()

        logger.info("TTS Studio API initialized successfully")

    def _init_config(
        self, config_path: Path | None, config_dict: dict[str, Any] | None
    ) -> None:
        """Initialize configuration provider.

        Args:
            config_path: Optional path to config file
            config_dict: Optional config dictionary (for testing)
        """
        # If config_dict provided, use DictConfigProvider (for testing)
        if config_dict is not None:
            from infra.config.dict_config import DictConfigProvider

            self._config = DictConfigProvider(config_dict)
            logger.debug("Configuration loaded from dictionary")
            return

        # Default config paths (relative to apps/core/)
        default_config = Path(__file__).parent.parent.parent / "config" / "default.yaml"
        user_config = Path(__file__).parent.parent.parent / "config" / "config.yaml"

        if config_path:
            user_config = config_path

        self._config = YAMLConfigProvider(
            default_config_path=default_config,
            user_config_path=user_config if user_config.exists() else None,
        )

        logger.debug(f"Configuration loaded from {default_config}")

    def _init_adapters(self) -> None:
        """Initialize infrastructure adapters (ports implementations)."""
        # Audio processor adapter
        sample_rate = self._config.get("audio.sample_rate", 12000)
        self._audio_processor = LibrosaAudioProcessor(sample_rate=sample_rate)
        logger.debug("Audio processor adapter initialized")

        # Profile repository adapter
        profiles_dir = Path(self._config.get("paths.profiles", "./data/profiles"))
        self._profile_repository = FileProfileRepository(profiles_dir=profiles_dir)
        logger.debug(f"Profile repository initialized at {profiles_dir}")

        # TTS engine adapter
        engine_config = {
            "model_name": self._config.get(
                "model.name", "Qwen/Qwen3-TTS-12Hz-1.7B-Base"
            ),
            "device": self._config.get("model.device", "cpu"),
            "dtype": self._config.get("model.dtype", "float32"),
            "cache_dir": self._config.get("paths.models_cache", "./data/models"),
        }
        self._tts_engine = Qwen3Adapter(config=engine_config)
        logger.debug("TTS engine adapter initialized")

    def _init_use_cases(self) -> None:
        """Initialize application use cases."""
        # Create voice profile use case
        self._create_profile_uc = CreateVoiceProfileUseCase(
            audio_processor=self._audio_processor,
            profile_repository=self._profile_repository,
        )

        # Generate audio use case
        self._generate_audio_uc = GenerateAudioUseCase(
            tts_engine=self._tts_engine,
            profile_repository=self._profile_repository,
        )

        # List profiles use case
        self._list_profiles_uc = ListVoiceProfilesUseCase(
            profile_repository=self._profile_repository,
        )

        # Validate samples use case
        self._validate_samples_uc = ValidateAudioSamplesUseCase(
            audio_processor=self._audio_processor,
        )

        # Process batch use case
        self._process_batch_uc = ProcessBatchUseCase(
            tts_engine=self._tts_engine,
            profile_repository=self._profile_repository,
        )

        logger.debug("Use cases initialized")

    def create_voice_profile(
        self,
        name: str,
        sample_paths: list[str],
        language: str = "es",
        reference_text: str | None = None,
    ) -> dict[str, Any]:
        """Create a new voice profile from audio samples.

        Args:
            name: Name for the voice profile
            sample_paths: List of paths to audio sample files
            language: Language code (default: "es")
            reference_text: Optional reference text describing the samples

        Returns:
            Dictionary with status and profile data:
            {
                "status": "success" | "error",
                "profile": {...} | None,
                "error": str | None
            }
        """
        try:
            logger.info(f"Creating voice profile: {name}")

            # Convert string paths to Path objects
            paths = [Path(p) for p in sample_paths]

            # Execute use case
            profile_dto = self._create_profile_uc.execute(
                name=name,
                sample_paths=paths,
                language=language,
                reference_text=reference_text,
            )

            logger.info(f"Voice profile created successfully: {profile_dto.id}")

            return {
                "status": "success",
                "profile": profile_dto.to_dict(),
                "error": None,
            }

        except Exception as e:
            logger.error(f"Failed to create voice profile: {e}", exc_info=True)
            return {
                "status": "error",
                "profile": None,
                "error": str(e),
            }

    def generate_audio(
        self,
        profile_id: str,
        text: str,
        output_path: str | None = None,
        temperature: float = 0.75,
        speed: float = 1.0,
        language: str | None = None,
        mode: str = "clone",
    ) -> dict[str, Any]:
        """Generate audio from text using a voice profile.

        Args:
            profile_id: ID of the voice profile to use
            text: Text to convert to speech
            output_path: Optional path to save audio (auto-generated if None)
            temperature: Sampling temperature (0.5-1.0, default: 0.75)
            speed: Speaking speed multiplier (0.8-1.2, default: 1.0)
            language: Language code (default: from config)
            mode: Generation mode (default: "clone")

        Returns:
            Dictionary with status and generation results:
            {
                "status": "success" | "error",
                "output_path": str | None,
                "duration": float | None,
                "generation_time": float | None,
                "error": str | None
            }
        """
        try:
            logger.info(f"Generating audio for profile: {profile_id}")

            # Create generation request
            request = GenerationRequestDTO(
                profile_id=profile_id,
                text=text,
                output_path=Path(output_path) if output_path else None,
                temperature=temperature,
                speed=speed,
                language=language or self._config.get("generation.language", "es"),
                mode=mode,
            )

            # Execute use case
            result = self._generate_audio_uc.execute(request)

            if result.success:
                logger.info(f"Audio generated successfully: {result.output_path}")
                return {
                    "status": "success",
                    "output_path": (
                        str(result.output_path) if result.output_path else None
                    ),
                    "duration": result.duration,
                    "generation_time": result.generation_time,
                    "error": None,
                }
            else:
                logger.error(f"Audio generation failed: {result.error}")
                return {
                    "status": "error",
                    "output_path": None,
                    "duration": None,
                    "generation_time": None,
                    "error": result.error,
                }

        except Exception as e:
            logger.error(f"Failed to generate audio: {e}", exc_info=True)
            return {
                "status": "error",
                "output_path": None,
                "duration": None,
                "generation_time": None,
                "error": str(e),
            }

    def list_voice_profiles(self) -> dict[str, Any]:
        """List all available voice profiles.

        Returns:
            Dictionary with status and profiles list:
            {
                "status": "success" | "error",
                "profiles": [...] | None,
                "count": int,
                "error": str | None
            }
        """
        try:
            logger.info("Listing voice profiles")

            # Execute use case
            profiles = self._list_profiles_uc.execute()

            logger.info(f"Found {len(profiles)} voice profiles")

            return {
                "status": "success",
                "profiles": [p.to_dict() for p in profiles],
                "count": len(profiles),
                "error": None,
            }

        except Exception as e:
            logger.error(f"Failed to list profiles: {e}", exc_info=True)
            return {
                "status": "error",
                "profiles": None,
                "count": 0,
                "error": str(e),
            }

    def delete_voice_profile(self, profile_id: str) -> dict[str, Any]:
        """Delete a voice profile.

        Args:
            profile_id: ID of the profile to delete

        Returns:
            Dictionary with status:
            {
                "status": "success" | "error",
                "deleted": bool,
                "error": str | None
            }
        """
        try:
            logger.info(f"Deleting voice profile: {profile_id}")

            # Delete profile
            deleted = self._profile_repository.delete(profile_id)

            if deleted:
                logger.info(f"Profile deleted successfully: {profile_id}")
                return {
                    "status": "success",
                    "deleted": True,
                    "error": None,
                }
            else:
                logger.warning(f"Profile not found: {profile_id}")
                return {
                    "status": "error",
                    "deleted": False,
                    "error": f"Profile not found: {profile_id}",
                }

        except Exception as e:
            logger.error(f"Failed to delete profile: {e}", exc_info=True)
            return {
                "status": "error",
                "deleted": False,
                "error": str(e),
            }

    def validate_samples(self, sample_paths: list[str]) -> dict[str, Any]:
        """Validate audio samples for voice cloning.

        Args:
            sample_paths: List of paths to audio files to validate

        Returns:
            Dictionary with validation results:
            {
                "status": "success" | "error",
                "results": [...],
                "all_valid": bool,
                "error": str | None
            }
        """
        try:
            logger.info(f"Validating {len(sample_paths)} audio samples")

            # Convert string paths to Path objects
            paths = [Path(p) for p in sample_paths]

            # Execute use case
            summary = self._validate_samples_uc.execute(paths)

            # Convert results to dict format
            results_dict = [
                {
                    "path": str(r.path),
                    "valid": r.valid,
                    "error": r.error,
                    "duration": r.duration,
                    "sample_rate": r.sample_rate,
                    "channels": r.channels,
                    "bit_depth": r.bit_depth,
                }
                for r in summary.results
            ]

            logger.info(f"Validation complete: {summary.all_valid}")

            return {
                "status": "success",
                "results": results_dict,
                "all_valid": summary.all_valid,
                "total_samples": summary.total_samples,
                "valid_samples": summary.valid_samples,
                "invalid_samples": summary.invalid_samples,
                "total_duration": summary.total_duration,
                "error": None,
            }

        except Exception as e:
            logger.error(f"Failed to validate samples: {e}", exc_info=True)
            return {
                "status": "error",
                "results": [],
                "all_valid": False,
                "error": str(e),
            }

    def get_config(self, key: str, default: Any = None) -> Any:
        """Get a configuration value.

        Args:
            key: Configuration key (supports dot notation)
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        return self._config.get(key, default)

    def reload_config(self) -> dict[str, Any]:
        """Reload configuration from files.

        Returns:
            Dictionary with status:
            {
                "status": "success" | "error",
                "error": str | None
            }
        """
        try:
            logger.info("Reloading configuration")
            self._config.reload()
            logger.info("Configuration reloaded successfully")

            return {
                "status": "success",
                "error": None,
            }

        except Exception as e:
            logger.error(f"Failed to reload config: {e}", exc_info=True)
            return {
                "status": "error",
                "error": str(e),
            }
