"""
Gradio UI for Voice Clone Tool.

This package provides a web-based user interface for the voice cloning tool,
built with Gradio. It offers an intuitive way to:
- Upload and validate voice samples
- Create voice profiles
- Generate audio from text
- Process scripts in batch mode
"""

__version__ = "0.1.0"
__author__ = "Bryan Stevens Acosta"

from .app import create_app, main

__all__ = ["create_app", "main"]
