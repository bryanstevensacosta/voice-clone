"""Audio samples management menu."""

from pathlib import Path

import questionary
from rich.table import Table

from cli.interactive.menus.base import BaseMenu, console
from voice_clone.audio.processor import AudioProcessor


class SamplesMenu(BaseMenu):
    """Menu for managing audio samples."""

    def run(self) -> str | None:
        """Run samples menu loop."""
        while True:
            choice = questionary.select(
                "Audio Samples Management",
                choices=[
                    "🔍 Validate Samples",
                    "📊 View Sample Info",
                    "🔄 Convert Samples",
                    questionary.Separator(),
                    "← Back to Main Menu",
                ],
                style=self.style,
            ).ask()

            if choice is None or choice == "← Back to Main Menu":
                break

            if choice == "🔍 Validate Samples":
                self._validate_samples()
            elif choice == "📊 View Sample Info":
                self._view_sample_info()
            elif choice == "🔄 Convert Samples":
                self._convert_samples()

        return None

    def _validate_samples(self) -> None:
        """Validate audio samples in a directory."""
        # Ask for directory
        samples_dir = questionary.path(
            "Enter path to samples directory:",
            default=str(self.state.recent_samples_dir or "./data/samples"),
            only_directories=True,
            style=self.style,
        ).ask()

        if not samples_dir:
            return

        samples_path = Path(samples_dir)
        if not samples_path.exists():
            self.show_error(f"Directory not found: {samples_path}")
            self.pause()
            return

        # Remember this directory
        self.state.recent_samples_dir = samples_path

        try:
            processor = AudioProcessor()
            wav_files = list(samples_path.glob("*.wav"))

            if not wav_files:
                self.show_warning(f"No WAV files found in {samples_path}")
                self.pause()
                return

            console.print(f"\n[cyan]Validating {len(wav_files)} samples...[/cyan]\n")

            # Create results table
            table = Table(show_header=True, header_style="bold cyan")
            table.add_column("File", style="white", no_wrap=True)
            table.add_column("Status", style="white")
            table.add_column("Duration", style="white")
            table.add_column("Issues", style="white")

            valid_count = 0
            for wav_file in sorted(wav_files):
                result = processor.validate_sample(wav_file)

                if result.is_valid():
                    status = "[green]✓[/green]"
                    valid_count += 1
                else:
                    status = "[red]✗[/red]"

                # Get duration
                duration = result.metadata.get("duration", 0)
                duration_str = f"{duration:.1f}s" if duration else "N/A"

                # Collect issues
                issues = []
                for error in result.errors[:2]:  # Show first 2 errors
                    issues.append(f"[red]{error}[/red]")
                for warning in result.warnings[:1]:  # Show first warning
                    issues.append(f"[yellow]{warning}[/yellow]")

                issues_text = "\n".join(issues) if issues else "[green]OK[/green]"
                table.add_row(wav_file.name, status, duration_str, issues_text)

            console.print(table)
            console.print(
                f"\n[cyan]Result: {valid_count}/{len(wav_files)} samples valid[/cyan]\n"
            )

            self.pause()

        except Exception as e:
            self.show_error(f"Validation failed: {str(e)}")
            self.pause()

    def _view_sample_info(self) -> None:
        """View detailed information about a specific sample."""
        # Ask for file
        sample_file = questionary.path(
            "Enter path to audio file:",
            default=str(self.state.recent_samples_dir or "./data/samples") + "/",
            style=self.style,
        ).ask()

        if not sample_file:
            return

        sample_path = Path(sample_file)
        if not sample_path.exists():
            self.show_error(f"File not found: {sample_path}")
            self.pause()
            return

        try:
            processor = AudioProcessor()
            result = processor.validate_sample(sample_path)

            # Show detailed info
            console.print(
                f"\n[bold cyan]Sample Information: {sample_path.name}[/bold cyan]\n"
            )

            table = Table(show_header=False, box=None)
            table.add_column("Property", style="cyan")
            table.add_column("Value", style="white")

            # Add metadata
            for key, value in result.metadata.items():
                table.add_row(key.replace("_", " ").title(), str(value))

            # Add validation status
            table.add_row(
                "Valid", "[green]Yes[/green]" if result.is_valid() else "[red]No[/red]"
            )

            console.print(table)

            # Show errors and warnings
            if result.errors:
                console.print("\n[red]Errors:[/red]")
                for error in result.errors:
                    console.print(f"  [red]✗ {error}[/red]")

            if result.warnings:
                console.print("\n[yellow]Warnings:[/yellow]")
                for warning in result.warnings:
                    console.print(f"  [yellow]⚠ {warning}[/yellow]")

            console.print()
            self.pause()

        except Exception as e:
            self.show_error(f"Failed to read sample: {str(e)}")
            self.pause()

    def _convert_samples(self) -> None:
        """Convert audio samples to target format."""
        self.show_info("Sample conversion feature coming soon!")
        self.show_info(
            "This will allow you to convert samples to 22050Hz, mono, 16-bit WAV"
        )
        self.pause()
