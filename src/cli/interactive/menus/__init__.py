"""
Menu System for Interactive CLI.

This module contains all menu classes for the interactive CLI mode.
Each menu handles a specific aspect of the voice cloning workflow.

Available menus:
- MainMenu: Primary navigation hub
- ProfileMenu: Voice profile management
- SamplesMenu: Audio sample validation
- GenerationMenu: Audio generation
- SettingsMenu: Configuration management
"""

__all__ = [
    "BaseMenu",
    "MainMenu",
    "ProfileMenu",
    "SamplesMenu",
    "GenerationMenu",
    "SettingsMenu",
]

from cli.interactive.menus.base import BaseMenu
from cli.interactive.menus.generation_menu import GenerationMenu
from cli.interactive.menus.main_menu import MainMenu
from cli.interactive.menus.profile_menu import ProfileMenu
from cli.interactive.menus.samples_menu import SamplesMenu
from cli.interactive.menus.settings_menu import SettingsMenu
