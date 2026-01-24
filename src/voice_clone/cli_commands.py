"""Command-line interface for voice cloning.

This module provides both:
1. Traditional CLI commands (voice-clone <command>)
2. Interactive mode (voice-clone interactive or just voice-clone)
"""

import sys
from pathlib import Path

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from voice_clone.audio.processor import AudioProcessor
from voice_clone.batch.processor import BatchProcessor
from voice_clone.config import ConfigManager
from voice_clone.model.generator import VoiceGenerator
from voice_clone.model.manager import ModelManager
from voice_clone.model.profile import VoiceProfile

console = Console()


@click.group(invoke_without_command=True)
@click.pass_context
@click.version_option(version="0.1.0")
def cli(ctx: click.Context) -> None:
    """Voice cloning CLI tool using XTTS-v2.

    Run without arguments to start interactive mode.
    """
    # If no subcommand is provided, start interactive mode
    if ctx.invoked_subcommand is None:
        from voice_clone.cli.app import InteractiveCLI

        app = InteractiveCLI()
        app.run()


@cli.command()
def interactive() -> None:
    """Start interactive mode with menu navigation."""
    from voice_clone.cli.app import InteractiveCLI

    app = InteractiveCLI()
    app.run()


@cli.command()
@click.option(
    "--dir",
    "samples_dir",
    required=True,
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    help="Directory containing audio samples",
)
def validate_samples(samples_dir: Path) -> None:
    """Validate audio samples for voice cloning.

    Checks sample rate, channels, duration, and quality.
    """
    try:
        processor = AudioProcessor()

        # Find all WAV files
        wav_files = list(samples_dir.glob("*.wav"))

        if not wav_files:
            console.print(f"[red]✗ No WAV files found in {samples_dir}[/red]")
            sys.exit(1)

        console.print(f"\n[cyan]Validating {len(wav_files)} samples...[/cyan]\n")

        # Create results table
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("File", style="white")
        table.add_column("Status", style="white")
        table.add_column("Issues", style="white")

        valid_count = 0
        for wav_file in sorted(wav_files):
            result = processor.validate_sample(wav_file)

            if result.is_valid():
                status = "[green]✓ Valid[/green]"
                valid_count += 1
            else:
                status = "[red]✗ Invalid[/red]"

            # Collect issues
            issues = []
            for error in result.errors:
                issues.append(f"[red]ERROR: {error}[/red]")
            for warning in result.warnings:
                issues.append(f"[yellow]WARNING: {warning}[/yellow]")

            issues_text = "\n".join(issues) if issues else "[green]None[/green]"
            table.add_row(wav_file.name, status, issues_text)

        console.print(table)
        console.print(f"\n[cyan]{valid_count}/{len(wav_files)} samples valid[/cyan]\n")

        if valid_count < len(wav_files):
            sys.exit(1)

    except Exception as e:
        console.print(f"[red]✗ Error: {str(e)}[/red]")
        sys.exit(1)


@cli.command()
@click.option(
    "--samples",
    "samples_dir",
    required=True,
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    help="Directory containing audio samples",
)
@click.option(
    "--output",
    "output_path",
    required=True,
    type=click.Path(path_type=Path),
    help="Output path for voice profile JSON",
)
@click.option(
    "--name",
    "profile_name",
    required=True,
    help="Name for the voice profile",
)
def prepare(samples_dir: Path, output_path: Path, profile_name: str) -> None:
    """Create voice profile from audio samples."""
    try:
        console.print(f"\n[cyan]Creating voice profile: {profile_name}[/cyan]\n")

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Processing samples...", total=None)

            # Create profile
            profile = VoiceProfile.from_directory(profile_name, samples_dir)

            if not profile.samples:
                console.print("[red]✗ No valid samples found[/red]")
                sys.exit(1)

            progress.update(task, description="Validating profile...")

            # Validate profile
            is_valid, warnings = profile.validate()

            if not is_valid:
                console.print("[red]✗ Profile validation failed[/red]")
                sys.exit(1)

            progress.update(task, description="Saving profile...")

            # Save profile
            profile.to_json(output_path)

        # Show warnings
        if warnings:
            console.print("\n[yellow]Warnings:[/yellow]")
            for warning in warnings:
                console.print(f"  [yellow]⚠ {warning}[/yellow]")

        # Show success
        console.print("\n[green]✓ Voice profile created successfully![/green]\n")

        # Create info table
        table = Table(show_header=False, box=None)
        table.add_column("Key", style="cyan")
        table.add_column("Value", style="white")
        table.add_row("Samples", str(len(profile.samples)))
        table.add_row("Duration", f"{profile.total_duration:.1f}s")
        table.add_row("Language", profile.language)
        table.add_row("Output", str(output_path))

        console.print(table)
        console.print()

    except Exception as e:
        console.print(f"[red]✗ Error: {str(e)}[/red]")
        sys.exit(1)


@cli.command()
@click.option(
    "--profile",
    "profile_path",
    required=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="Path to voice profile JSON",
)
@click.option(
    "--text",
    required=True,
    help="Text to convert to speech",
)
@click.option(
    "--output",
    "output_path",
    required=True,
    type=click.Path(path_type=Path),
    help="Output path for generated audio",
)
def generate(profile_path: Path, text: str, output_path: Path) -> None:
    """Generate speech from text using voice profile."""
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            # Load config
            task = progress.add_task("Loading configuration...", total=None)
            config_manager = ConfigManager()
            config = config_manager.load_config()

            # Load profile
            progress.update(task, description="Loading voice profile...")
            profile = VoiceProfile.from_json(profile_path)

            # Initialize model
            progress.update(
                task, description="Initializing model (this may take a while)..."
            )
            model_manager = ModelManager(config)

            if not model_manager.load_model():
                console.print("[red]✗ Failed to load model[/red]")
                sys.exit(1)

            # Generate
            progress.update(task, description="Generating speech...")
            generator = VoiceGenerator(model_manager, config)

            success = generator.generate(text, profile, output_path)

        if success:
            console.print("\n[green]✓ Audio generated successfully![/green]")
            console.print(f"[cyan]Output: {output_path}[/cyan]\n")
        else:
            console.print("\n[red]✗ Generation failed[/red]")
            sys.exit(1)

    except Exception as e:
        console.print(f"[red]✗ Error: {str(e)}[/red]")
        sys.exit(1)


@cli.command()
@click.option(
    "--profile",
    "profile_path",
    required=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="Path to voice profile JSON",
)
@click.option(
    "--input",
    "script_path",
    required=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="Path to script file with [MARKERS]",
)
@click.option(
    "--output-dir",
    "output_dir",
    required=True,
    type=click.Path(path_type=Path),
    help="Output directory for generated audio files",
)
def batch(profile_path: Path, script_path: Path, output_dir: Path) -> None:
    """Process script file and generate audio for all segments."""
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            # Load config
            task = progress.add_task("Loading configuration...", total=None)
            config_manager = ConfigManager()
            config = config_manager.load_config()

            # Load profile
            progress.update(task, description="Loading voice profile...")
            profile = VoiceProfile.from_json(profile_path)

            # Initialize model
            progress.update(
                task, description="Initializing model (this may take a while)..."
            )
            model_manager = ModelManager(config)

            if not model_manager.load_model():
                console.print("[red]✗ Failed to load model[/red]")
                sys.exit(1)

            # Process batch
            progress.update(task, description="Processing script...")
            generator = VoiceGenerator(model_manager, config)
            processor = AudioProcessor()
            batch_processor = BatchProcessor(generator, processor)

            results = batch_processor.process_script(script_path, profile, output_dir)

        # Show results
        console.print("\n[green]✓ Batch processing complete![/green]\n")

        table = Table(show_header=False, box=None)
        table.add_column("Key", style="cyan")
        table.add_column("Value", style="white")
        table.add_row("Total segments", str(results["total"]))
        table.add_row("Successful", f"[green]{results['successful']}[/green]")
        table.add_row(
            "Failed",
            f"[red]{results['failed']}[/red]" if results["failed"] > 0 else "0",
        )
        table.add_row("Output directory", str(output_dir))

        console.print(table)
        console.print()

        if results["failed"] > 0:
            sys.exit(1)

    except Exception as e:
        console.print(f"[red]✗ Error: {str(e)}[/red]")
        sys.exit(1)


@cli.command()
@click.option(
    "--profile",
    "profile_path",
    required=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="Path to voice profile JSON",
)
@click.option(
    "--text",
    default="Hola, esta es una prueba de mi voz clonada. ¿Suena natural?",
    help="Test text (default: Spanish test phrase)",
)
@click.option(
    "--output",
    "output_path",
    type=click.Path(path_type=Path),
    default=None,
    help="Output path (default: ./test_output.wav)",
)
def test(profile_path: Path, text: str, output_path: Path | None) -> None:
    """Quick test of voice cloning with default text."""
    if output_path is None:
        output_path = Path("./test_output.wav")

    try:
        console.print("\n[cyan]Running voice cloning test...[/cyan]\n")
        console.print(f"[white]Text: {text}[/white]\n")

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            # Load config
            task = progress.add_task("Loading configuration...", total=None)
            config_manager = ConfigManager()
            config = config_manager.load_config()

            # Load profile
            progress.update(task, description="Loading voice profile...")
            profile = VoiceProfile.from_json(profile_path)

            # Initialize model
            progress.update(
                task, description="Initializing model (this may take a while)..."
            )
            model_manager = ModelManager(config)

            if not model_manager.load_model():
                console.print("[red]✗ Failed to load model[/red]")
                sys.exit(1)

            # Generate
            progress.update(task, description="Generating test audio...")
            generator = VoiceGenerator(model_manager, config)
            success = generator.generate(text, profile, output_path)

        if success:
            console.print("\n[green]✓ Test audio generated successfully![/green]")
            console.print(f"[cyan]Output: {output_path}[/cyan]")
            console.print(f"\n[yellow]Play with: afplay {output_path}[/yellow]\n")
        else:
            console.print("\n[red]✗ Generation failed[/red]")
            sys.exit(1)

    except Exception as e:
        console.print(f"[red]✗ Error: {str(e)}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    cli()
