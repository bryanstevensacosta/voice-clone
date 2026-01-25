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
from voice_clone.model.profile import VoiceProfile
from voice_clone.model.qwen3_generator import Qwen3Generator
from voice_clone.model.qwen3_manager import Qwen3ModelManager

console = Console()


@click.group(invoke_without_command=True)
@click.pass_context
@click.version_option(version="0.1.0")
def cli(ctx: click.Context) -> None:
    """Voice cloning CLI tool using Qwen3-TTS.

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
@click.option(
    "--ref-text",
    "ref_text",
    required=True,
    help="Transcript of the reference audio (required for Qwen3-TTS)",
)
def prepare(
    samples_dir: Path, output_path: Path, profile_name: str, ref_text: str
) -> None:
    """Create voice profile from audio samples.

    Note: Qwen3-TTS requires a transcript (ref_text) of the reference audio.
    """
    try:
        console.print(f"\n[cyan]Creating voice profile: {profile_name}[/cyan]\n")

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Processing samples...", total=None)

            # Create profile with ref_text
            profile = VoiceProfile.from_directory(
                profile_name, samples_dir, ref_text=ref_text
            )

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
        table.add_row("Sample Rate", f"{profile.sample_rate} Hz")
        table.add_row(
            "Reference Text", ref_text[:50] + "..." if len(ref_text) > 50 else ref_text
        )
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
    """Generate speech from text using voice profile (Qwen3-TTS)."""
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
                task,
                description="Initializing Qwen3-TTS model (this may take a while)...",
            )
            model_manager = Qwen3ModelManager(config)

            if not model_manager.load_model():
                console.print("[red]✗ Failed to load Qwen3-TTS model[/red]")
                sys.exit(1)

            # Generate
            progress.update(task, description="Generating speech with Qwen3-TTS...")
            generator = Qwen3Generator(model_manager, config)

            success = generator.generate_to_file(
                text=text,
                ref_audio=profile.samples[0].path,  # Use path from VoiceSample
                ref_text=profile.ref_text,
                output_path=output_path,
                language=profile.language,
            )

        if success:
            console.print("\n[green]✓ Audio generated successfully![/green]")
            console.print(f"[cyan]Output: {output_path}[/cyan]")
            console.print("[dim]Sample rate: 12000 Hz (Qwen3-TTS native)[/dim]\n")
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
    """Process script file and generate audio for all segments (Qwen3-TTS)."""
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
                task,
                description="Initializing Qwen3-TTS model (this may take a while)...",
            )
            model_manager = Qwen3ModelManager(config)

            if not model_manager.load_model():
                console.print("[red]✗ Failed to load Qwen3-TTS model[/red]")
                sys.exit(1)

            # Process batch
            progress.update(task, description="Processing script...")
            generator = Qwen3Generator(model_manager, config)
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
        table.add_row("Sample rate", "12000 Hz (Qwen3-TTS native)")

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
    default="Hola, esta es una prueba de mi voz clonada con Qwen3-TTS. ¿Suena natural?",
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
    """Quick test of voice cloning with Qwen3-TTS."""
    if output_path is None:
        output_path = Path("./test_output.wav")

    try:
        console.print("\n[cyan]Running Qwen3-TTS voice cloning test...[/cyan]\n")
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
                task,
                description="Initializing Qwen3-TTS model (this may take a while)...",
            )
            model_manager = Qwen3ModelManager(config)

            if not model_manager.load_model():
                console.print("[red]✗ Failed to load Qwen3-TTS model[/red]")
                sys.exit(1)

            # Generate
            progress.update(task, description="Generating test audio with Qwen3-TTS...")
            generator = Qwen3Generator(model_manager, config)
            success = generator.generate_to_file(
                text=text,
                ref_audio=profile.samples[0].path,  # Use path from VoiceSample
                ref_text=profile.ref_text,
                output_path=output_path,
                language=profile.language,
            )

        if success:
            console.print("\n[green]✓ Test audio generated successfully![/green]")
            console.print(f"[cyan]Output: {output_path}[/cyan]")
            console.print("[dim]Sample rate: 12000 Hz (Qwen3-TTS native)[/dim]")
            console.print(f"\n[yellow]Play with: afplay {output_path}[/yellow]\n")
        else:
            console.print("\n[red]✗ Generation failed[/red]")
            sys.exit(1)

    except Exception as e:
        console.print(f"[red]✗ Error: {str(e)}[/red]")
        sys.exit(1)


@cli.command()
def info() -> None:
    """Display Qwen3-TTS model and system information."""
    try:
        import torch

        console.print("\n[bold cyan]Voice Clone CLI - System Information[/bold cyan]\n")

        # Create info table
        table = Table(show_header=False, box=None)
        table.add_column("Key", style="cyan", width=25)
        table.add_column("Value", style="white")

        # TTS Engine
        table.add_row("TTS Engine", "Qwen3-TTS")
        table.add_row("Model", "Qwen/Qwen3-TTS-12Hz-1.7B-Base")

        # Device info
        if torch.backends.mps.is_available():
            device = "MPS (Metal Performance Shaders)"
            device_status = "[green]✓ Available[/green]"
        elif torch.cuda.is_available():
            device = f"CUDA (GPU: {torch.cuda.get_device_name(0)})"
            device_status = "[green]✓ Available[/green]"
        else:
            device = "CPU"
            device_status = "[yellow]⚠ GPU not available[/yellow]"

        table.add_row("Device", device)
        table.add_row("Device Status", device_status)

        # PyTorch info
        table.add_row("PyTorch Version", torch.__version__)
        table.add_row(
            "MPS Available",
            "[green]Yes[/green]"
            if torch.backends.mps.is_available()
            else "[red]No[/red]",
        )
        table.add_row(
            "CUDA Available",
            "[green]Yes[/green]" if torch.cuda.is_available() else "[red]No[/red]",
        )

        # Audio specs
        table.add_row("Native Sample Rate", "12000 Hz")
        table.add_row("Min Sample Duration", "3 seconds")
        table.add_row("Output Format", "WAV (mono, 16-bit)")

        # Config
        try:
            config_manager = ConfigManager()
            config = config_manager.load_config()

            model_config = config.get("model", {})
            table.add_row("Config Device", model_config.get("device", "auto"))
            table.add_row("Config Dtype", model_config.get("dtype", "float32"))

            paths = config.get("paths", {})
            table.add_row("Models Cache", paths.get("models", "./data/qwen3_models"))
        except Exception:
            table.add_row("Config", "[yellow]Not loaded[/yellow]")

        console.print(table)
        console.print()

    except Exception as e:
        console.print(f"[red]✗ Error: {str(e)}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    cli()
