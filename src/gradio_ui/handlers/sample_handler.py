"""
Sample validation handler for Gradio UI.

This module provides handlers for validating audio samples uploaded by users.
It integrates with the backend AudioProcessor to perform validation and
formats results for display in the Gradio interface.
"""

from pathlib import Path

from voice_clone.audio.processor import AudioProcessor


def validate_samples_handler(files: list[str]) -> str:
    """
    Validate uploaded audio samples.

    This handler validates audio files against Qwen3-TTS requirements:
    - Sample rate (12000 Hz recommended)
    - Channels (mono required)
    - Bit depth (16-bit recommended)
    - Duration (3-30 seconds optimal)
    - No clipping/distortion

    Args:
        files: List of file paths from Gradio File component.
               Can be empty if no files uploaded.

    Returns:
        Markdown-formatted validation results with:
        - ✅ for valid samples
        - ❌ for invalid samples
        - Detailed metadata and error/warning messages

    Examples:
        >>> validate_samples_handler([])
        '⚠️ **No files uploaded**\\n\\nPlease upload 1-3 audio samples...'

        >>> validate_samples_handler(['/path/to/valid.wav'])
        '## Validation Results\\n\\n### ✅ valid.wav\\n- Duration: 12.3s...'
    """
    # Handle empty file list
    if not files:
        return """⚠️ **No files uploaded**

Please upload 1-3 audio samples to continue.

**Requirements:**
- Format: WAV, MP3, M4A, or FLAC
- Duration: 3-30 seconds per sample
- Quality: Clear audio, no background noise
- Channels: Mono preferred (stereo will be converted)
"""

    # Initialize audio processor with Qwen3-TTS defaults
    processor = AudioProcessor(
        sample_rate=12000,  # Qwen3-TTS native
        channels=1,  # Mono required
        bit_depth=16,  # Standard quality
    )

    # Build results header
    results = ["## Validation Results\n"]

    # Validate each file
    for file_path in files:
        try:
            # Convert to Path object
            path = Path(file_path)

            # Check if file exists
            if not path.exists():
                results.append(f"### ❌ {path.name}")
                results.append(f"- ⚠️ **File not found**: {file_path}")
                results.append("")
                continue

            # Validate the sample
            validation_result = processor.validate_sample(path)

            # Format results based on validation outcome
            if validation_result.is_valid():
                # Valid sample - show success with metadata
                results.append(f"### ✅ {path.name}")

                # Add metadata
                if "duration" in validation_result.metadata:
                    results.append(
                        f"- **Duration**: {validation_result.metadata['duration']}"
                    )
                if "sample_rate" in validation_result.metadata:
                    results.append(
                        f"- **Sample Rate**: {validation_result.metadata['sample_rate']} Hz"
                    )
                if "channels" in validation_result.metadata:
                    results.append(
                        f"- **Channels**: {validation_result.metadata['channels']}"
                    )
                if "bit_depth" in validation_result.metadata:
                    results.append(
                        f"- **Bit Depth**: {validation_result.metadata['bit_depth']}"
                    )
                if "max_amplitude" in validation_result.metadata:
                    results.append(
                        f"- **Max Amplitude**: {validation_result.metadata['max_amplitude']}"
                    )

                # Add warnings if any
                if validation_result.warnings:
                    results.append("")
                    results.append("**Warnings:**")
                    for warning in validation_result.warnings:
                        results.append(f"- ⚠️ {warning}")

            else:
                # Invalid sample - show errors
                results.append(f"### ❌ {path.name}")

                # Add errors
                if validation_result.errors:
                    results.append("")
                    results.append("**Errors:**")
                    for error in validation_result.errors:
                        results.append(f"- ❌ {error}")

                # Add warnings if any
                if validation_result.warnings:
                    results.append("")
                    results.append("**Warnings:**")
                    for warning in validation_result.warnings:
                        results.append(f"- ⚠️ {warning}")

                # Add metadata if available
                if validation_result.metadata:
                    results.append("")
                    results.append("**Current values:**")
                    if "duration" in validation_result.metadata:
                        results.append(
                            f"- Duration: {validation_result.metadata['duration']}"
                        )
                    if "sample_rate" in validation_result.metadata:
                        results.append(
                            f"- Sample Rate: {validation_result.metadata['sample_rate']} Hz"
                        )
                    if "channels" in validation_result.metadata:
                        results.append(
                            f"- Channels: {validation_result.metadata['channels']}"
                        )

            # Add blank line between files
            results.append("")

        except FileNotFoundError:
            # Handle file not found specifically
            results.append(f"### ❌ {Path(file_path).name}")
            results.append(f"- ⚠️ **File not found**: {file_path}")
            results.append(
                "- The file may have been moved or deleted. Please upload again."
            )
            results.append("")

        except Exception as e:
            # Handle any other errors gracefully
            results.append(f"### ❌ {Path(file_path).name}")
            results.append(f"- ⚠️ **Error processing file**: {str(e)}")
            results.append(
                "- Please ensure the file is a valid audio file (WAV, MP3, M4A, FLAC)."
            )
            results.append("")

    # Add summary footer
    total_files = len(files)
    valid_count = sum(
        1
        for file_path in files
        if Path(file_path).exists()
        and processor.validate_sample(Path(file_path)).is_valid()
    )

    results.append("---\n")
    results.append(
        f"**Summary**: {valid_count}/{total_files} samples passed validation"
    )

    if valid_count == total_files and total_files > 0:
        results.append(
            "\n✅ **All samples are valid!** You can proceed to create a voice profile."
        )
    elif valid_count > 0:
        results.append(
            "\n⚠️ **Some samples have issues.** Fix the errors above or remove invalid samples before creating a profile."
        )
    else:
        results.append(
            "\n❌ **No valid samples found.** Please upload valid audio files that meet the requirements."
        )

    return "\n".join(results)
