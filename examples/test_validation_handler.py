"""
Example demonstrating the validation handler.

This script shows how the validate_samples_handler works with different inputs.
Run this to see the Markdown-formatted output that will be displayed in Gradio.
"""

from gradio_ui.handlers.sample_handler import validate_samples_handler


def print_section(title: str) -> None:
    """Print a section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def main() -> None:
    """Run validation examples."""

    # Example 1: Empty file list
    print_section("Example 1: No files uploaded")
    result = validate_samples_handler([])
    print(result)

    # Example 2: Non-existent file
    print_section("Example 2: File not found")
    result = validate_samples_handler(["/path/to/nonexistent.wav"])
    print(result)

    # Example 3: Multiple non-existent files
    print_section("Example 3: Multiple files (not found)")
    result = validate_samples_handler(
        [
            "/path/to/sample1.wav",
            "/path/to/sample2.wav",
            "/path/to/sample3.wav",
        ]
    )
    print(result)

    print("\n" + "=" * 80)
    print("  To test with real audio files:")
    print("  1. Place some WAV files in data/samples/")
    print("  2. Update this script with the actual paths")
    print("  3. Run again to see validation results")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
