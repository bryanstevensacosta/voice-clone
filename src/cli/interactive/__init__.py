"""
Interactive CLI Mode.

This module provides an interactive, menu-driven interface for the voice cloning tool.
Users can navigate through menus to perform all voice cloning operations without
remembering command-line arguments.

The interactive mode includes:
- Profile management
- Sample validation
- Audio generation
- Batch processing
- Settings configuration
"""

__all__ = ["InteractiveCLI"]

from cli.interactive.app import InteractiveCLI
