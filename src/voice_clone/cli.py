"""Command-line interface for voice cloning."""

import sys
from pathlib import Path

import click

from voice_clone.audio.processor import AudioProcessor
from voice_clone.batch.processor import BatchProcessor
from voice_clone.config import ConfigManager
from voice_clone.model.generator import VoiceGenerator
from voice_clone.model.manager import ModelManager
from voice_clone.model.profile import VoiceProfile


@click.group()
@click.version_option(version="0.1.0")
def cli() -> None:
    """Voice cloning CLI tool using XTTS-v2."""
    pass


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
            click.secho(f"✗ No WAV files found in {samples_dir}", fg="red")
            sys.exit(1)

        click.secho(f"\nValidating {len(wav_files)} samples...\n", fg="cyan")

        valid_count = 0
        for wav_file in sorted(wav_files):
            result = processor.validate_sample(wav_file)

            if result.is_valid():
                click.secho(f"✓ {wav_file.name}", fg="green")
                valid_count += 1
            else:
                click.secho(f"✗ {wav_file.name}", fg="red")

            # Show errors and warnings
            for error in result.errors:
                click.secho(f"  ERROR: {error}", fg="red")
            for warning in result.warnings:
                click.secho(f"  WARNING: {warning}", fg="yellow")

        click.secho(f"\n{valid_count}/{len(wav_files)} samples valid", fg="cyan")

        if valid_count < len(wav_files):
            sys.exit(1)

    except Exception as e:
        click.secho(f"✗ Error: {str(e)}", fg="red")
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
        click.secho(f"\nCreating voice profile: {profile_name}", fg="cyan")

        # Create profile
        profile = VoiceProfile.from_directory(profile_name, samples_dir)

        if not profile.samples:
            click.secho("✗ No valid samples found", fg="red")
            sys.exit(1)

        # Validate profile
        is_valid, warnings = profile.validate()

        if not is_valid:
            click.secho("✗ Profile validation failed", fg="red")
            sys.exit(1)

        # Show warnings
        for warning in warnings:
            click.secho(f"⚠ WARNING: {warning}", fg="yellow")

        # Save profile
        profile.to_json(output_path)

        click.secho("\n✓ Voice profile created:", fg="green")
        click.secho(f"  Samples: {len(profile.samples)}", fg="cyan")
        click.secho(f"  Duration: {profile.total_duration:.1f}s", fg="cyan")
        click.secho(f"  Output: {output_path}", fg="cyan")

    except Exception as e:
        click.secho(f"✗ Error: {str(e)}", fg="red")
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
        # Load config
        config_manager = ConfigManager()
        config = config_manager.load_config()

        # Load profile
        click.secho("\nLoading voice profile...", fg="cyan")
        profile = VoiceProfile.from_json(profile_path)
        click.secho(f"✓ Loaded profile: {profile.name}", fg="green")

        # Initialize model
        click.secho("\nInitializing model...", fg="cyan")
        model_manager = ModelManager(config)

        if not model_manager.load_model():
            click.secho("✗ Failed to load model", fg="red")
            sys.exit(1)

        # Generate
        click.secho("\nGenerating speech...", fg="cyan")
        generator = VoiceGenerator(model_manager, config)

        success = generator.generate(text, profile, output_path)

        if success:
            click.secho(f"\n✓ Audio generated: {output_path}", fg="green")
        else:
            click.secho("\n✗ Generation failed", fg="red")
            sys.exit(1)

    except Exception as e:
        click.secho(f"✗ Error: {str(e)}", fg="red")
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
        # Load config
        config_manager = ConfigManager()
        config = config_manager.load_config()

        # Load profile
        click.secho("\nLoading voice profile...", fg="cyan")
        profile = VoiceProfile.from_json(profile_path)
        click.secho(f"✓ Loaded profile: {profile.name}", fg="green")

        # Initialize model
        click.secho("\nInitializing model...", fg="cyan")
        model_manager = ModelManager(config)

        if not model_manager.load_model():
            click.secho("✗ Failed to load model", fg="red")
            sys.exit(1)

        # Process batch
        generator = VoiceGenerator(model_manager, config)
        processor = AudioProcessor()
        batch_processor = BatchProcessor(generator, processor)

        results = batch_processor.process_script(script_path, profile, output_dir)

        if results["failed"] > 0:
            sys.exit(1)

    except Exception as e:
        click.secho(f"✗ Error: {str(e)}", fg="red")
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
        # Load config
        config_manager = ConfigManager()
        config = config_manager.load_config()

        # Load profile
        click.secho("\nLoading voice profile...", fg="cyan")
        profile = VoiceProfile.from_json(profile_path)
        click.secho(f"✓ Loaded profile: {profile.name}", fg="green")

        # Initialize model
        click.secho("\nInitializing model...", fg="cyan")
        model_manager = ModelManager(config)

        if not model_manager.load_model():
            click.secho("✗ Failed to load model", fg="red")
            sys.exit(1)

        # Generate
        click.secho("\nGenerating test audio...", fg="cyan")
        click.secho(f"Text: {text}", fg="white")

        generator = VoiceGenerator(model_manager, config)
        success = generator.generate(text, profile, output_path)

        if success:
            click.secho(f"\n✓ Test audio generated: {output_path}", fg="green")
            click.secho(f"\nPlay with: afplay {output_path}", fg="cyan")
        else:
            click.secho("\n✗ Generation failed", fg="red")
            sys.exit(1)

    except Exception as e:
        click.secho(f"✗ Error: {str(e)}", fg="red")
        sys.exit(1)


if __name__ == "__main__":
    cli()
