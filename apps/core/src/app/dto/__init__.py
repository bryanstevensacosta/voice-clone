"""Data Transfer Objects (DTOs) for the application layer.

DTOs are used to transfer data between layers and serialize/deserialize
data for external interfaces.
"""

from .batch_dto import BatchRequestDTO, BatchResultDTO
from .generation_dto import GenerationRequestDTO, GenerationResultDTO
from .voice_profile_dto import VoiceProfileDTO

__all__ = [
    "VoiceProfileDTO",
    "GenerationRequestDTO",
    "GenerationResultDTO",
    "BatchRequestDTO",
    "BatchResultDTO",
]
