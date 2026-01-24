"""Tests for CLI module."""

from click.testing import CliRunner
from voice_clone.cli import cli


def test_cli_help() -> None:
    """Test that CLI help command works."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Voice cloning" in result.output or "voice" in result.output.lower()


def test_cli_version() -> None:
    """Test that CLI version command works."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "0.1.0" in result.output


def test_cli_commands_exist() -> None:
    """Test that CLI commands are available."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "validate-samples" in result.output
    assert "prepare" in result.output
    assert "generate" in result.output
    assert "batch" in result.output
    assert "test" in result.output
