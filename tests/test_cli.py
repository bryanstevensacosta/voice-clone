"""Tests for CLI module."""

from pathlib import Path

from click.testing import CliRunner
from voice_clone.cli_commands import cli


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


# Task 15.3: Unit tests for CLI commands


def test_validate_samples_missing_dir() -> None:
    """Test validate-samples command with missing --dir argument."""
    runner = CliRunner()
    result = runner.invoke(cli, ["validate-samples"])

    # Should fail with non-zero exit code
    assert result.exit_code != 0

    # Should show error about missing argument
    assert "Missing option" in result.output or "required" in result.output.lower()


def test_validate_samples_help() -> None:
    """Test validate-samples --help flag."""
    runner = CliRunner()
    result = runner.invoke(cli, ["validate-samples", "--help"])

    # Should succeed
    assert result.exit_code == 0

    # Should show usage
    assert "Usage:" in result.output
    assert "--dir" in result.output


def test_prepare_missing_arguments() -> None:
    """Test prepare command with missing arguments."""
    runner = CliRunner()
    result = runner.invoke(cli, ["prepare"])

    # Should fail
    assert result.exit_code != 0

    # Should show error
    assert "Missing option" in result.output or "required" in result.output.lower()


def test_prepare_help() -> None:
    """Test prepare --help flag."""
    runner = CliRunner()
    result = runner.invoke(cli, ["prepare", "--help"])

    # Should succeed
    assert result.exit_code == 0

    # Should show usage
    assert "Usage:" in result.output
    assert "--samples" in result.output
    assert "--output" in result.output
    assert "--name" in result.output


def test_generate_missing_arguments() -> None:
    """Test generate command with missing arguments."""
    runner = CliRunner()
    result = runner.invoke(cli, ["generate"])

    # Should fail
    assert result.exit_code != 0

    # Should show error
    assert "Missing option" in result.output or "required" in result.output.lower()


def test_generate_help() -> None:
    """Test generate --help flag."""
    runner = CliRunner()
    result = runner.invoke(cli, ["generate", "--help"])

    # Should succeed
    assert result.exit_code == 0

    # Should show usage
    assert "Usage:" in result.output
    assert "--profile" in result.output
    assert "--text" in result.output
    assert "--output" in result.output


def test_batch_missing_arguments() -> None:
    """Test batch command with missing arguments."""
    runner = CliRunner()
    result = runner.invoke(cli, ["batch"])

    # Should fail
    assert result.exit_code != 0

    # Should show error
    assert "Missing option" in result.output or "required" in result.output.lower()


def test_batch_help() -> None:
    """Test batch --help flag."""
    runner = CliRunner()
    result = runner.invoke(cli, ["batch", "--help"])

    # Should succeed
    assert result.exit_code == 0

    # Should show usage
    assert "Usage:" in result.output
    assert "--profile" in result.output
    assert "--input" in result.output
    assert "--output-dir" in result.output


def test_test_command_missing_profile() -> None:
    """Test test command with missing --profile argument."""
    runner = CliRunner()
    result = runner.invoke(cli, ["test"])

    # Should fail
    assert result.exit_code != 0

    # Should show error
    assert "Missing option" in result.output or "required" in result.output.lower()


def test_test_command_help() -> None:
    """Test test command --help flag."""
    runner = CliRunner()
    result = runner.invoke(cli, ["test", "--help"])

    # Should succeed
    assert result.exit_code == 0

    # Should show usage
    assert "Usage:" in result.output
    assert "--profile" in result.output


def test_validate_samples_with_nonexistent_dir() -> None:
    """Test validate-samples with non-existent directory."""
    runner = CliRunner()
    result = runner.invoke(cli, ["validate-samples", "--dir", "/nonexistent/path"])

    # Should fail
    assert result.exit_code != 0

    # Should show error about path
    assert (
        "does not exist" in result.output.lower() or "invalid" in result.output.lower()
    )


def test_validate_samples_with_valid_dir(tmp_path: Path) -> None:
    """Test validate-samples with valid directory but no WAV files."""
    runner = CliRunner()

    # Create empty directory
    test_dir = tmp_path / "samples"
    test_dir.mkdir()

    result = runner.invoke(cli, ["validate-samples", "--dir", str(test_dir)])

    # Should fail (no WAV files)
    assert result.exit_code != 0

    # Should show error about no files
    assert "No WAV files" in result.output or "no" in result.output.lower()


def test_prepare_with_nonexistent_samples_dir() -> None:
    """Test prepare with non-existent samples directory."""
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "prepare",
            "--samples",
            "/nonexistent/path",
            "--output",
            "profile.json",
            "--name",
            "test",
        ],
    )

    # Should fail
    assert result.exit_code != 0

    # Should show error
    assert (
        "does not exist" in result.output.lower() or "invalid" in result.output.lower()
    )


def test_generate_with_nonexistent_profile() -> None:
    """Test generate with non-existent profile file."""
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "generate",
            "--profile",
            "/nonexistent/profile.json",
            "--text",
            "test",
            "--output",
            "out.wav",
        ],
    )

    # Should fail
    assert result.exit_code != 0

    # Should show error
    assert (
        "does not exist" in result.output.lower() or "invalid" in result.output.lower()
    )


def test_exit_code_success_for_help() -> None:
    """Test that help commands return exit code 0."""
    runner = CliRunner()

    commands = ["validate-samples", "prepare", "generate", "batch", "test"]

    for cmd in commands:
        result = runner.invoke(cli, [cmd, "--help"])
        assert result.exit_code == 0, f"Help for {cmd} should return exit code 0"


def test_exit_code_failure_for_missing_args() -> None:
    """Test that missing arguments return non-zero exit code."""
    runner = CliRunner()

    commands = ["validate-samples", "prepare", "generate", "batch", "test"]

    for cmd in commands:
        result = runner.invoke(cli, [cmd])
        assert (
            result.exit_code != 0
        ), f"{cmd} without args should return non-zero exit code"
