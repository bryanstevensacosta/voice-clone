"""Process Batch Use Case.

Use case for processing multiple text segments in batch.
"""

from app.dto.batch_dto import BatchRequestDTO, BatchResultDTO
from app.dto.generation_dto import GenerationResultDTO
from domain.ports.profile_repository import ProfileRepository
from domain.ports.tts_engine import TTSEngine

from .generate_audio import GenerateAudioUseCase


class ProcessBatchUseCase:
    """Use case for batch processing multiple text segments.

    Processes multiple text segments using the same voice profile,
    generating audio for each segment.
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
        self._generate_audio = GenerateAudioUseCase(tts_engine, profile_repository)

    def execute(self, request: BatchRequestDTO) -> BatchResultDTO:
        """Execute the use case to process batch.

        Args:
            request: Batch request with all segments and parameters

        Returns:
            BatchResultDTO with results for all segments
        """
        # Ensure output directory exists
        request.output_dir.mkdir(parents=True, exist_ok=True)

        # Convert batch request to individual generation requests
        generation_requests = request.to_generation_requests()

        # Process each segment
        results: list[GenerationResultDTO] = []
        for gen_request in generation_requests:
            result = self._generate_audio.execute(gen_request)
            results.append(result)

        # Create batch result from individual results
        return BatchResultDTO.from_results(results)
