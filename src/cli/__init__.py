"""
CLI Package for Voice Clone Tool.

This package contains the command-line interface for the voice cloning tool,
separated from the core voice_clone package for better maintainability.

The CLI provides:
- Interactive mode with menu-driven interface
- Direct commands for all voice cloning operations
- Integration with Gradio UI

Usage:
    voice-clone [command] [options]
    voice-clone interactive
    voice-clone ui
"""

__version__ = "0.2.0"
__all__ = ["cli"]

from cli.cli import cli
