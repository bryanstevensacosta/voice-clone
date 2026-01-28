"""Main interactive CLI application."""

import sys

from rich.console import Console

from cli.interactive.menus.main_menu import MainMenu
from cli.interactive.state import CLIState
from cli.interactive.styles import get_custom_style

console = Console()


class InteractiveCLI:
    """Interactive CLI application for voice cloning."""

    def __init__(self) -> None:
        """Initialize the interactive CLI."""
        self.state = CLIState()
        self.style = get_custom_style()
        self.main_menu = MainMenu(self.state, self.style)

    def run(self) -> None:
        """Run the interactive CLI application."""
        try:
            # Show welcome banner
            self._show_welcome()

            # Run main menu loop
            self.main_menu.run()

            # Show goodbye message
            self._show_goodbye()

        except KeyboardInterrupt:
            console.print("\n\n[yellow]👋 Interrupted by user. Goodbye![/yellow]\n")
            sys.exit(0)
        except Exception as e:
            console.print(f"\n[red]✗ Unexpected error: {str(e)}[/red]\n")
            sys.exit(1)

    def _show_welcome(self) -> None:
        """Show welcome banner."""
        console.print("\n" + "=" * 60)
        console.print("[bold cyan]🎙️  Voice Clone CLI - Interactive Mode[/bold cyan]")
        console.print("=" * 60)
        console.print("[dim]Navigate with arrow keys, select with Enter[/dim]")
        console.print("[dim]Press Ctrl+C to exit at any time[/dim]")
        console.print("=" * 60 + "\n")

    def _show_goodbye(self) -> None:
        """Show goodbye message."""
        console.print("\n[cyan]👋 Thank you for using Voice Clone CLI![/cyan]\n")


def main() -> None:
    """Entry point for interactive CLI."""
    app = InteractiveCLI()
    app.run()


if __name__ == "__main__":
    main()
