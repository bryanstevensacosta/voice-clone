"""Main menu for interactive CLI."""

from typing import TYPE_CHECKING, Any

import questionary
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from voice_clone.cli.menus.base import BaseMenu
from voice_clone.cli.menus.generation_menu import GenerationMenu
from voice_clone.cli.menus.profile_menu import ProfileMenu
from voice_clone.cli.menus.samples_menu import SamplesMenu
from voice_clone.cli.menus.settings_menu import SettingsMenu

if TYPE_CHECKING:
    from voice_clone.cli.state import CLIState

console = Console()


class MainMenu(BaseMenu):
    """Main menu screen."""

    def __init__(self, state: "CLIState", style: Any) -> None:
        """Initialize main menu."""
        super().__init__(state, style)
        self.samples_menu = SamplesMenu(state, style)
        self.profile_menu = ProfileMenu(state, style)
        self.generation_menu = GenerationMenu(state, style)
        self.settings_menu = SettingsMenu(state, style)

    def run(self) -> str | None:
        """Run main menu loop."""
        while True:
            # Show current state
            self._show_status()

            # Show menu options
            choice = questionary.select(
                "What would you like to do?",
                choices=[
                    "📁 Manage Audio Samples",
                    "👤 Manage Voice Profiles",
                    "🎙️  Generate Speech",
                    "⚙️  Settings",
                    questionary.Separator(),
                    "❌ Exit",
                ],
                style=self.style,
            ).ask()

            if choice is None or choice == "❌ Exit":
                break

            # Route to appropriate menu
            if choice == "📁 Manage Audio Samples":
                self.samples_menu.run()
            elif choice == "👤 Manage Voice Profiles":
                self.profile_menu.run()
            elif choice == "🎙️  Generate Speech":
                self.generation_menu.run()
            elif choice == "⚙️  Settings":
                self.settings_menu.run()

        return None

    def _show_status(self) -> None:
        """Show current CLI status."""
        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_column("Key", style="cyan")
        table.add_column("Value", style="white")

        # Voice profile status
        if self.state.current_profile:
            profile_status = f"[green]✓[/green] {self.state.current_profile.name}"
            table.add_row("Voice Profile", profile_status)
            table.add_row(
                "  Samples", f"{len(self.state.current_profile.samples)} samples"
            )
            table.add_row(
                "  Duration", f"{self.state.current_profile.total_duration:.1f}s"
            )
        else:
            table.add_row("Voice Profile", "[yellow]Not loaded[/yellow]")

        # Model status
        if self.state.model_loaded:
            table.add_row("TTS Model", "[green]✓ Loaded[/green]")
        else:
            table.add_row("TTS Model", "[dim]Not loaded[/dim]")

        panel = Panel(table, title="[bold]Current Status[/bold]", border_style="cyan")
        console.print(panel)
        console.print()
