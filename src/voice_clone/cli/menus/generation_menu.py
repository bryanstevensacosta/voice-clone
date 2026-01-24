"""Speech generation menu."""

from pathlib import Path
from typing import Optional

import questionary
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from voice_clone.audio.processor import AudioProcessor
from voice_clone.batch.processor import BatchProcessor
from voice_clone.cli.menus.base import BaseMenu, console
from voice_clone.model.generator import VoiceGenerator


class GenerationMenu(BaseMenu):
    """Menu for speech generation."""

    def run(self) -> Optional[str]:
        """Run generation menu loop."""
        while True:
            choice = questionary.select(
                "Speech Generation",
                choices=[
                    "🎤 Generate from Text",
                    "📝 Batch Process Script",
                    "🧪 Quick Test",
                    questionary.Separator(),
                    "← Back to Main Menu",
                ],
                style=self.style,
            ).ask()

            if choice is None or choice == "← Back to Main Menu":
                break

            if choice == "🎤 Generate from Text":
                self._generate_from_text()
            elif choice == "📝 Batch Process Script":
                self._batch_process()
            elif choice == "🧪 Quick Test":
                self._quick_test()

        return None

    def _generate_from_text(self) -> None:
        """Generate speech from user-provided text."""
        # Check if profile is loaded
        if not self.state.current_profile:
            self.show_error("No voice profile loaded. Please load a profile first.")
            self.pause()
            return

        console.print("\n[bold cyan]Generate Speech from Text[/bold cyan]\n")

        # Ask for text
        text = questionary.text(
            "Enter text to convert to speech:",
            multiline=True,
            style=self.style,
        ).ask()

        if not text or not text.strip():
            return

        # Ask for output path
        output_path = questionary.path(
            "Enter output path for audio file:",
            default=str(self.state.recent_output_dir or "./data/outputs") + "/output.wav",
            style=self.style,
        ).ask()

        if not output_path:
            return

        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Remember output directory
        self.state.recent_output_dir = output_file.parent

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
                # Load model if needed
                if not self.state.model_loaded:
                    task = progress.add_task(
                        "Loading TTS model (this may take a while)...", total=None
                    )
                    if not self.state.load_model():
                        self.show_error("Failed to load TTS model")
                        self.pause()
                        return
                    progress.remove_task(task)

                # Generate speech
                task = progress.add_task("Generating speech...", total=None)
                generator = VoiceGenerator(self.state.model_manager, self.state.config)
                success = generator.generate(
                    text, self.state.current_profile, output_file
                )

            if success:
                self.show_success("Audio generated successfully!")
                console.print(f"[cyan]Output: {output_file}[/cyan]")
                console.print(f"[dim]Play with: afplay {output_file}[/dim]\n")
            else:
                self.show_error("Generation failed")

            self.pause()

        except Exception as e:
            self.show_error(f"Generation failed: {str(e)}")
            self.pause()

    def _batch_process(self) -> None:
        """Process a script file with multiple segments."""
        # Check if profile is loaded
        if not self.state.current_profile:
            self.show_error("No voice profile loaded. Please load a profile first.")
            self.pause()
            return

        console.print("\n[bold cyan]Batch Process Script[/bold cyan]\n")

        # Ask for script path
        script_path = questionary.path(
            "Enter path to script file:",
            default="./data/scripts/",
            style=self.style,
        ).ask()

        if not script_path:
            return

        script_file = Path(script_path)
        if not script_file.exists():
            self.show_error(f"File not found: {script_file}")
            self.pause()
            return

        # Ask for output directory
        output_dir = questionary.path(
            "Enter output directory:",
            default=str(self.state.recent_output_dir or "./data/outputs") + "/batch",
            only_directories=True,
            style=self.style,
        ).ask()

        if not output_dir:
            return

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Remember output directory
        self.state.recent_output_dir = output_path

        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                # Load model if needed
                if not self.state.model_loaded:
                    task = progress.add_task(
                        "Loading TTS model (this may take a while)...", total=None
                    )
                    if not self.state.load_model():
                        self.show_error("Failed to load TTS model")
                        self.pause()
                        return
                    progress.remove_task(task)

                # Process batch
                task = progress.add_task("Processing script...", total=None)
                generator = VoiceGenerator(self.state.model_manager, self.state.config)
                processor = AudioProcessor()
                batch_processor = BatchProcessor(generator, processor)

                results = batch_processor.process_script(
                    script_file, self.state.current_profile, output_path
                )

            # Show results
            self.show_success("Batch processing complete!")

            table = Table(show_header=False, box=None)
            table.add_column("Key", style="cyan")
            table.add_column("Value", style="white")
            table.add_row("Total segments", str(results["total"]))
            table.add_row("Successful", f"[green]{results['successful']}[/green]")
            table.add_row(
                "Failed",
                f"[red]{results['failed']}[/red]" if results["failed"] > 0 else "0",
            )
            table.add_row("Output directory", str(output_path))

            console.print(table)
            console.print()

            self.pause()

        except Exception as e:
            self.show_error(f"Batch processing failed: {str(e)}")
            self.pause()

    def _quick_test(self) -> None:
        """Quick test with default text."""
        # Check if profile is loaded
        if not self.state.current_profile:
            self.show_error("No voice profile loaded. Please load a profile first.")
            self.pause()
            return

        console.print("\n[bold cyan]Quick Voice Test[/bold cyan]\n")

        # Default test text
        default_text = "Hola, esta es una prueba de mi voz clonada. ¿Suena natural?"

        # Ask if user wants to use default or custom text
        use_default = self.confirm(
            f"Use default test text?\n'{default_text}'", default=True
        )

        if use_default:
            text = default_text
        else:
            text = questionary.text(
                "Enter custom test text:",
                default=default_text,
                style=self.style,
            ).ask()

            if not text:
                return

        # Generate to default location
        output_file = Path("./test_output.wav")

        try:
            console.print(f"\n[white]Text: {text}[/white]\n")

            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                # Load model if needed
                if not self.state.model_loaded:
                    task = progress.add_task(
                        "Loading TTS model (this may take a while)...", total=None
                    )
                    if not self.state.load_model():
                        self.show_error("Failed to load TTS model")
                        self.pause()
                        return
                    progress.remove_task(task)

                # Generate speech
                task = progress.add_task("Generating test audio...", total=None)
                generator = VoiceGenerator(self.state.model_manager, self.state.config)
                success = generator.generate(
                    text, self.state.current_profile, output_file
                )

            if success:
                self.show_success("Test audio generated successfully!")
                console.print(f"[cyan]Output: {output_file}[/cyan]")
                console.print(f"[yellow]Play with: afplay {output_file}[/yellow]\n")
            else:
                self.show_error("Generation failed")

            self.pause()

        except Exception as e:
            self.show_error(f"Test failed: {str(e)}")
            self.pause()
