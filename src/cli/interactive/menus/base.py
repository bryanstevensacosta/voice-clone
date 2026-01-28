"""Base menu class for all CLI menus."""

from abc import ABC, abstractmethod

import questionary
from questionary import Style
from rich.console import Console

from cli.interactive.state import CLIState

console = Console()


class BaseMenu(ABC):
    """Base class for all menu screens."""

    def __init__(self, state: CLIState, style: Style) -> None:
        """Initialize base menu.

        Args:
            state: Shared CLI state
            style: Questionary style for prompts
        """
        self.state = state
        self.style = style

    @abstractmethod
    def run(self) -> str | None:
        """Run the menu and return action or None to go back.

        Returns:
            Action string or None to return to previous menu
        """
        pass

    def confirm(self, message: str, default: bool = True) -> bool:
        """Show confirmation prompt.

        Args:
            message: Confirmation message
            default: Default value

        Returns:
            True if confirmed, False otherwise
        """
        result = questionary.confirm(message, default=default, style=self.style).ask()
        return bool(result) if result is not None else False

    def show_error(self, message: str) -> None:
        """Show error message.

        Args:
            message: Error message to display
        """
        console.print(f"\n[red]✗ {message}[/red]\n")

    def show_success(self, message: str) -> None:
        """Show success message.

        Args:
            message: Success message to display
        """
        console.print(f"\n[green]✓ {message}[/green]\n")

    def show_info(self, message: str) -> None:
        """Show info message.

        Args:
            message: Info message to display
        """
        console.print(f"\n[cyan]ℹ {message}[/cyan]\n")

    def show_warning(self, message: str) -> None:
        """Show warning message.

        Args:
            message: Warning message to display
        """
        console.print(f"\n[yellow]⚠ {message}[/yellow]\n")

    def pause(self, message: str = "Press Enter to continue...") -> None:
        """Pause and wait for user input.

        Args:
            message: Message to display
        """
        questionary.press_any_key_to_continue(message, style=self.style).ask()
