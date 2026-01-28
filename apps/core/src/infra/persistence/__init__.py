"""Persistence infrastructure adapters.

This module contains adapters for persisting domain entities.
All adapters implement ports defined in the domain layer.
"""

from .file_profile_repository import FileProfileRepository
from .json_serializer import JSONSerializer

__all__ = ["FileProfileRepository", "JSONSerializer"]
