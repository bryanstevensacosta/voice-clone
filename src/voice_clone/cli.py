"""Command-line interface for voice cloning tool.

This module provides the main CLI entry point for the voice cloning application.
"""

import click


@click.group()
@click.version_option(version="0.1.0", prog_name="voice-clone")
def cli() -> None:
    """Voice Clone - Personal voice cloning CLI tool.

    Clone your voice and generate text-to-speech audio using XTTS-v2.
    """
    pass


@cli.command()
def info() -> None:
    """Display information about the voice cloning tool."""
    click.echo("Voice Clone v0.1.0")
    click.echo("Personal voice cloning CLI tool using XTTS-v2")
    click.echo("")
    click.echo("Status: Initial setup complete")
    click.echo("Next steps:")
    click.echo("  1. Record voice samples (6-10 samples, 10-20s each)")
    click.echo("  2. Prepare voice profile")
    click.echo("  3. Generate text-to-speech audio")


if __name__ == "__main__":
    cli()
