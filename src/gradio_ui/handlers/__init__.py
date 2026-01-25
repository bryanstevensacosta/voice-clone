"""
Event Handlers for Gradio UI.

This module contains handler functions that process user interactions
and connect the UI to the backend voice cloning functionality.

Handlers are responsible for:
- Validating user inputs
- Calling backend services
- Formatting responses for display
- Error handling and user feedback
"""

# Import handlers as they are created
from .sample_handler import validate_samples_handler

# from .profile_handler import create_profile_handler, list_available_profiles
# from .generation_handler import generate_audio_handler
# from .batch_handler import batch_process_handler

__all__ = [
    "validate_samples_handler",
]
