"""Settings and configuration menu."""

from typing import Optional

import questionary
from rich.table import Table

from voice_clone.cli.menus.base import BaseMenu, console


class SettingsMenu(BaseMenu):
    """Menu for settings and configuration."""

    def run(self) -> Optional[str]:
        """Run settings menu loop."""
        while True:
            choice = questionary.select(
                "Settings",
                choices=[
                    "ℹ️  View Current Configuration",
                    "🔧 Model Settings",
                    "💾 Memory Management",
                    "📊 System Information",
                    questionary.Separator(),
                    "← Back to Main Menu",
                ],
                style=self.style,
            ).ask()

            if choice is None or choice == "← Back to Main Menu":
                break

            if choice == "ℹ️  View Current Configuration":
                self._view_configuration()
            elif choice == "🔧 Model Settings":
                self._model_settings()
            elif choice == "💾 Memory Management":
                self._memory_management()
            elif choice == "📊 System Information":
                self._system_info()

        return None

    def _view_configuration(self) -> None:
        """View current configuration."""
        config = self.state.load_config()

        console.print("\n[bold cyan]Current Configuration[/bold cyan]\n")

        # Model settings
        console.print("[bold]Model Settings:[/bold]")
        model_table = Table(show_header=False, box=None, padding=(0, 2))
        model_table.add_column("Key", style="cyan")
        model_table.add_column("Value", style="white")

        model_config = config.get("model", {})
        model_table.add_row("Name", model_config.get("name", "N/A"))
        model_table.add_row("Device", model_config.get("device", "N/A"))

        console.print(model_table)

        # Audio settings
        console.print("\n[bold]Audio Settings:[/bold]")
        audio_table = Table(show_header=False, box=None, padding=(0, 2))
        audio_table.add_column("Key", style="cyan")
        audio_table.add_column("Value", style="white")

        audio_config = config.get("audio", {})
        audio_table.add_row("Sample Rate", str(audio_config.get("sample_rate", "N/A")))
        audio_table.add_row("Format", audio_config.get("format", "N/A"))
        audio_table.add_row("Mono", str(audio_config.get("mono", "N/A")))

        console.print(audio_table)

        # Generation settings
        console.print("\n[bold]Generation Settings:[/bold]")
        gen_table = Table(show_header=False, box=None, padding=(0, 2))
        gen_table.add_column("Key", style="cyan")
        gen_table.add_column("Value", style="white")

        gen_config = config.get("generation", {})
        gen_table.add_row("Language", gen_config.get("language", "N/A"))
        gen_table.add_row("Temperature", str(gen_config.get("temperature", "N/A")))
        gen_table.add_row("Max Length", str(gen_config.get("max_length", "N/A")))

        console.print(gen_table)
        console.print()

        self.pause()

    def _model_settings(self) -> None:
        """Manage model settings."""
        while True:
            # Show current model status
            if self.state.model_loaded:
                status = "[green]✓ Loaded[/green]"
            else:
                status = "[dim]Not loaded[/dim]"

            console.print(f"\n[cyan]Model Status: {status}[/cyan]\n")

            choice = questionary.select(
                "Model Settings",
                choices=[
                    "🔄 Load Model" if not self.state.model_loaded else "🔄 Reload Model",
                    "🗑️  Unload Model" if self.state.model_loaded else None,
                    "ℹ️  Model Information",
                    questionary.Separator(),
                    "← Back",
                ],
                style=self.style,
            ).ask()

            if choice is None or choice == "← Back":
                break

            if choice and "Load Model" in choice:
                self._load_model()
            elif choice == "🗑️  Unload Model":
                self._unload_model()
            elif choice == "ℹ️  Model Information":
                self._model_info()

    def _load_model(self) -> None:
        """Load TTS model."""
        if self.state.model_loaded:
            if not self.confirm("Model is already loaded. Reload?"):
                return
            self.state.unload_model()

        try:
            from rich.progress import Progress, SpinnerColumn, TextColumn

            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                task = progress.add_task(
                    "Loading TTS model (this may take a while)...", total=None
                )

                if self.state.load_model():
                    self.show_success("Model loaded successfully!")
                else:
                    self.show_error("Failed to load model")

            self.pause()

        except Exception as e:
            self.show_error(f"Failed to load model: {str(e)}")
            self.pause()

    def _unload_model(self) -> None:
        """Unload TTS model."""
        if not self.state.model_loaded:
            self.show_warning("Model is not loaded")
            self.pause()
            return

        if self.confirm("Unload TTS model to free memory?"):
            self.state.unload_model()
            self.show_success("Model unloaded successfully!")
            self.pause()

    def _model_info(self) -> None:
        """Show model information."""
        config = self.state.load_config()
        model_config = config.get("model", {})

        console.print("\n[bold cyan]Model Information[/bold cyan]\n")

        table = Table(show_header=False, box=None)
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="white")

        table.add_row("Model Name", model_config.get("name", "N/A"))
        table.add_row("Device", model_config.get("device", "N/A"))
        table.add_row(
            "Status",
            "[green]Loaded[/green]" if self.state.model_loaded else "[dim]Not loaded[/dim]",
        )

        if self.state.model_manager:
            table.add_row("Model Type", "XTTS-v2")
            table.add_row("Multilingual", "Yes")
            table.add_row("Supported Languages", "Spanish, English, French, German, etc.")

        console.print(table)
        console.print()
        self.pause()

    def _memory_management(self) -> None:
        """Memory management options."""
        console.print("\n[bold cyan]Memory Management[/bold cyan]\n")

        choice = questionary.select(
            "What would you like to do?",
            choices=[
                "🗑️  Unload Model (Free ~4-6GB)",
                "🔄 Clear Cache",
                "📊 View Memory Usage",
                questionary.Separator(),
                "← Back",
            ],
            style=self.style,
        ).ask()

        if choice is None or choice == "← Back":
            return

        if choice == "🗑️  Unload Model (Free ~4-6GB)":
            self._unload_model()
        elif choice == "🔄 Clear Cache":
            self.show_info("Cache clearing feature coming soon!")
            self.pause()
        elif choice == "📊 View Memory Usage":
            self._view_memory_usage()

    def _view_memory_usage(self) -> None:
        """View memory usage information."""
        import psutil

        console.print("\n[bold cyan]Memory Usage[/bold cyan]\n")

        # Get memory info
        memory = psutil.virtual_memory()

        table = Table(show_header=False, box=None)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="white")

        table.add_row("Total Memory", f"{memory.total / (1024**3):.1f} GB")
        table.add_row("Available", f"{memory.available / (1024**3):.1f} GB")
        table.add_row("Used", f"{memory.used / (1024**3):.1f} GB")
        table.add_row("Usage", f"{memory.percent}%")

        console.print(table)

        # Model memory estimate
        if self.state.model_loaded:
            console.print("\n[yellow]Estimated Model Memory: ~4-6 GB[/yellow]")

        console.print()
        self.pause()

    def _system_info(self) -> None:
        """Show system information."""
        import platform
        import sys

        console.print("\n[bold cyan]System Information[/bold cyan]\n")

        table = Table(show_header=False, box=None)
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="white")

        table.add_row("OS", platform.system())
        table.add_row("OS Version", platform.version())
        table.add_row("Architecture", platform.machine())
        table.add_row("Python Version", sys.version.split()[0])
        table.add_row("Platform", platform.platform())

        console.print(table)
        console.print()
        self.pause()
