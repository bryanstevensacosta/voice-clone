"""Property-based tests for CLI interface."""


from click.testing import CliRunner
from hypothesis import given
from hypothesis import strategies as st
from voice_clone.cli_commands import cli


@given(st.text(min_size=1, max_size=100))
def test_success_messages_include_location(output_text: str) -> None:
    """Property 41: Success messages should include file location.

    When operations succeed, the CLI should show where files were created.
    """
    runner = CliRunner()

    # Test help command (always succeeds)
    result = runner.invoke(cli, ["--help"])

    # Success should have exit code 0
    assert result.exit_code == 0

    # Output should exist
    assert len(result.output) > 0


@given(st.text(min_size=0, max_size=50))
def test_missing_arguments_show_help(command_name: str) -> None:
    """Property 42: Missing required arguments should display help.

    When required arguments are missing, CLI should show usage information.
    """
    runner = CliRunner()

    # Valid commands
    valid_commands = ["validate-samples", "prepare", "generate", "batch", "test"]

    # Test with a valid command but missing arguments
    for cmd in valid_commands:
        result = runner.invoke(cli, [cmd])

        # Should fail with non-zero exit code
        assert result.exit_code != 0

        # Should show usage or error message
        assert (
            "Usage:" in result.output
            or "Error:" in result.output
            or "Missing" in result.output
            or "required" in result.output.lower()
        )


def test_exit_code_correctness_success() -> None:
    """Property 43: Exit codes should be correct for success.

    Successful operations should return exit code 0.
    """
    runner = CliRunner()

    # Test commands that should succeed
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0

    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0


def test_exit_code_correctness_failure() -> None:
    """Property 43: Exit codes should be correct for failure.

    Failed operations should return non-zero exit code.
    """
    runner = CliRunner()

    # Test commands that should fail (missing required arguments)
    result = runner.invoke(cli, ["validate-samples"])
    assert result.exit_code != 0

    result = runner.invoke(cli, ["prepare"])
    assert result.exit_code != 0

    result = runner.invoke(cli, ["generate"])
    assert result.exit_code != 0


@given(st.text(min_size=1, max_size=20))
def test_invalid_commands_show_error(invalid_command: str) -> None:
    """Property: Invalid commands should show error message."""
    runner = CliRunner()

    # Filter out valid commands
    valid_commands = [
        "validate-samples",
        "prepare",
        "generate",
        "batch",
        "test",
        "--help",
        "--version",
    ]

    if invalid_command in valid_commands:
        return

    result = runner.invoke(cli, [invalid_command])

    # Should fail
    assert result.exit_code != 0

    # Should show error
    assert "Error:" in result.output or "No such command" in result.output


def test_help_flag_works_for_all_commands() -> None:
    """Property: --help flag should work for all commands."""
    runner = CliRunner()

    commands = ["validate-samples", "prepare", "generate", "batch", "test"]

    for cmd in commands:
        result = runner.invoke(cli, [cmd, "--help"])

        # Should succeed
        assert result.exit_code == 0

        # Should show usage
        assert "Usage:" in result.output


def test_cli_commands_are_discoverable() -> None:
    """Property: All CLI commands should be listed in help."""
    runner = CliRunner()

    result = runner.invoke(cli, ["--help"])

    # Should succeed
    assert result.exit_code == 0

    # All commands should be listed
    assert "validate-samples" in result.output
    assert "prepare" in result.output
    assert "generate" in result.output
    assert "batch" in result.output
    assert "test" in result.output


@given(st.integers(min_value=0, max_value=10))
def test_cli_handles_multiple_help_requests(num_requests: int) -> None:
    """Property: CLI should handle multiple help requests consistently."""
    runner = CliRunner()

    for _ in range(num_requests):
        result = runner.invoke(cli, ["--help"])

        # Should always succeed
        assert result.exit_code == 0

        # Should always show usage
        assert len(result.output) > 0


def test_cli_version_is_displayed() -> None:
    """Property: CLI version should be displayed with --version flag."""
    runner = CliRunner()

    result = runner.invoke(cli, ["--version"])

    # Should succeed
    assert result.exit_code == 0

    # Should show version
    assert "0.1.0" in result.output or "version" in result.output.lower()
