"""Generate Audio Use Case.

Use case for generating audio from text using a voice profile.
"""

import time
from pathlib import Path

from app.dto.generation_dto import GenerationRequestDTO, GenerationResultDTO
from domain.exceptions import GenerationException, InvalidProfileException
from domain.ports.profile_repository import ProfileRepository
from domain.ports.tts_engine import TTSEngine


class GenerateAudioUseCase:
    """Use case for generating audio from text.

    Orchestrates the TTS engine and profile repository to generate
    audio using a specific voice profile.
    """

    def __init__(
        self,
        tts_engine: TTSEngine,
        profile_repository: ProfileRepository,
    ):
        """Initialize the use case.

        Args:
            tts_engine: TTS engine port implementation
            profile_repository: Profile repository port implementation
        """
        self._engine = tts_engine
        self._repository = profile_repository

    def execute(self, request: GenerationRequestDTO) -> GenerationResultDTO:
        """Execute the use case to generate audio.

        Args:
            request: Generation request with all parameters

        Returns:
            GenerationResultDTO with generation results
        """
        start_time = time.time()

        try:
            # Load the voice profile
            profile = self._repository.find_by_id(request.profile_id)
            if profile is None:
                return GenerationResultDTO.error_result(
                    error=f"Profile not found: {request.profile_id}",
                    profile_id=request.profile_id,
                )

            # Validate profile with engine
            if not self._engine.validate_profile(profile):
                return GenerationResultDTO.error_result(
                    error=f"Profile validation failed: {request.profile_id}",
                    profile_id=request.profile_id,
                )

            # Generate output path if not provided
            output_path = request.output_path
            if output_path is None:
                output_path = Path(f"output_{profile.id}_{int(time.time())}.wav")

            # Generate audio
            result_path = self._engine.generate_audio(
                text=request.text,
                profile=profile,
                output_path=output_path,
                temperature=request.temperature,
                speed=request.speed,
                language=request.language,
                mode=request.mode,
            )

            # Calculate generation time
            generation_time = time.time() - start_time

            # Get audio duration (approximate from file size for now)
            # In a real implementation, we'd use librosa or similar to get actual duration
            duration = 0.0  # Placeholder

            return GenerationResultDTO.success_result(
                output_path=result_path,
                duration=duration,
                profile_id=profile.id,
                text_length=len(request.text),
                generation_time=generation_time,
            )

        except InvalidProfileException as e:
            return GenerationResultDTO.error_result(
                error=f"Invalid profile: {e}",
                profile_id=request.profile_id,
            )
        except GenerationException as e:
            return GenerationResultDTO.error_result(
                error=f"Generation failed: {e}",
                profile_id=request.profile_id,
            )
        except Exception as e:
            return GenerationResultDTO.error_result(
                error=f"Unexpected error: {e}",
                profile_id=request.profile_id,
            )
