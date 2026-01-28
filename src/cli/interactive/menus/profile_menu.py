"""Voice profile management menu."""

from pathlib import Path

import questionary
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from cli.interactive.menus.base import BaseMenu, console
from voice_clone.model.profile import VoiceProfile


class ProfileMenu(BaseMenu):
    """Menu for managing voice profiles."""

    def run(self) -> str | None:
        """Run profile menu loop."""
        while True:
            choice = questionary.select(
                "Voice Profile Management",
                choices=[
                    "➕ Create New Profile",
                    "📂 Load Existing Profile",
                    "ℹ️  View Current Profile",
                    "🗑️  Unload Profile",
                    questionary.Separator(),
                    "← Back to Main Menu",
                ],
                style=self.style,
            ).ask()

            if choice is None or choice == "← Back to Main Menu":
                break

            if choice == "➕ Create New Profile":
                self._create_profile()
            elif choice == "📂 Load Existing Profile":
                self._load_profile()
            elif choice == "ℹ️  View Current Profile":
                self._view_profile()
            elif choice == "🗑️  Unload Profile":
                self._unload_profile()

        return None

    def _create_profile(self) -> None:
        """Create a new voice profile from samples."""
        console.print("\n[bold cyan]Create New Voice Profile[/bold cyan]\n")

        # Ask for profile name
        profile_name = questionary.text(
            "Enter profile name:",
            default="my_voice",
            style=self.style,
        ).ask()

        if not profile_name:
            return

        # Ask for samples directory
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

        # Ask for output path
        output_path = questionary.path(
            "Enter output path for profile JSON:",
            default=f"./data/{profile_name}_profile.json",
            style=self.style,
        ).ask()

        if not output_path:
            return

        output_file = Path(output_path)

        # Confirm if file exists
        if output_file.exists():
            if not self.confirm(f"File {output_file} already exists. Overwrite?"):
                return

        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                task = progress.add_task("Processing samples...", total=None)

                # Create profile
                profile = VoiceProfile.from_directory(profile_name, samples_path)

                if not profile.samples:
                    self.show_error("No valid samples found in directory")
                    self.pause()
                    return

                progress.update(task, description="Validating profile...")

                # Validate profile
                is_valid, warnings = profile.validate()

                if not is_valid:
                    self.show_error("Profile validation failed")
                    self.pause()
                    return

                progress.update(task, description="Saving profile...")

                # Save profile
                profile.to_json(output_file)

            # Show warnings
            if warnings:
                console.print("\n[yellow]Warnings:[/yellow]")
                for warning in warnings:
                    console.print(f"  [yellow]⚠ {warning}[/yellow]")

            # Show success
            self.show_success("Voice profile created successfully!")

            # Show profile info
            table = Table(show_header=False, box=None)
            table.add_column("Key", style="cyan")
            table.add_column("Value", style="white")
            table.add_row("Name", profile.name)
            table.add_row("Samples", str(len(profile.samples)))
            table.add_row("Duration", f"{profile.total_duration:.1f}s")
            table.add_row("Language", profile.language)
            table.add_row("Output", str(output_file))

            console.print(table)
            console.print()

            # Ask if user wants to load this profile
            if self.confirm("Load this profile now?"):
                self.state.load_profile(output_file)
                self.show_success(f"Profile '{profile.name}' loaded!")

            self.pause()

        except Exception as e:
            self.show_error(f"Failed to create profile: {str(e)}")
            self.pause()

    def _load_profile(self) -> None:
        """Load an existing voice profile."""
        # Ask for profile path
        profile_path = questionary.path(
            "Enter path to profile JSON:",
            default="./data/",
            style=self.style,
        ).ask()

        if not profile_path:
            return

        profile_file = Path(profile_path)
        if not profile_file.exists():
            self.show_error(f"File not found: {profile_file}")
            self.pause()
            return

        try:
            profile = self.state.load_profile(profile_file)
            self.show_success(f"Profile '{profile.name}' loaded successfully!")

            # Show profile info
            table = Table(show_header=False, box=None)
            table.add_column("Key", style="cyan")
            table.add_column("Value", style="white")
            table.add_row("Name", profile.name)
            table.add_row("Samples", str(len(profile.samples)))
            table.add_row("Duration", f"{profile.total_duration:.1f}s")
            table.add_row("Language", profile.language)
            table.add_row("Created", profile.created_at)

            console.print(table)
            console.print()
            self.pause()

        except Exception as e:
            self.show_error(f"Failed to load profile: {str(e)}")
            self.pause()

    def _view_profile(self) -> None:
        """View current loaded profile."""
        if not self.state.current_profile:
            self.show_warning("No profile loaded")
            self.pause()
            return

        profile = self.state.current_profile

        console.print(
            f"\n[bold cyan]Current Voice Profile: {profile.name}[/bold cyan]\n"
        )

        # General info
        table = Table(show_header=False, box=None)
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="white")
        table.add_row("Name", profile.name)
        table.add_row("Language", profile.language)
        table.add_row("Created", profile.created_at)
        table.add_row("Total Samples", str(len(profile.samples)))
        table.add_row("Total Duration", f"{profile.total_duration:.1f}s")
        table.add_row("Profile Path", str(self.state.current_profile_path or "N/A"))

        console.print(table)

        # Samples details
        if profile.samples:
            console.print("\n[bold]Samples:[/bold]\n")
            samples_table = Table(show_header=True, header_style="bold cyan")
            samples_table.add_column("File", style="white")
            samples_table.add_column("Duration", style="white")
            samples_table.add_column("Emotion", style="white")

            for sample in profile.samples:
                samples_table.add_row(
                    Path(sample.path).name,
                    f"{sample.duration:.1f}s",
                    sample.emotion or "N/A",
                )

            console.print(samples_table)

        console.print()
        self.pause()

    def _unload_profile(self) -> None:
        """Unload current profile."""
        if not self.state.current_profile:
            self.show_warning("No profile loaded")
            self.pause()
            return

        if self.confirm(f"Unload profile '{self.state.current_profile.name}'?"):
            self.state.current_profile = None
            self.state.current_profile_path = None
            self.show_success("Profile unloaded")
            self.pause()
