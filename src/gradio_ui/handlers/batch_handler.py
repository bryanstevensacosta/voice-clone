"""
Batch processing handler for Gradio UI.

This module provides handlers for processing multiple text segments from a script file
and generating audio for each segment using voice profiles with the Qwen3-TTS model.
"""

import re
from pathlib import Path

from voice_clone.config import ConfigManager
from voice_clone.model.profile import VoiceProfile
from voice_clone.model.qwen3_generator import Qwen3Generator
from voice_clone.model.qwen3_manager import Qwen3ModelManager
from voice_clone.utils.logger import logger


def batch_process_handler(
    profile_name: str,
    script_file: str | None,
) -> tuple[list[str], str]:
    """
    Process a script file in batch mode.

    This handler loads the voice profile, parses the script file into segments,
    generates audio for each segment, and returns the list of generated audio files
    along with processing information.

    Args:
        profile_name: Name of the voice profile to use
        script_file: Path to the script file (.txt or .md)

    Returns:
        Tuple of:
        - List of audio file paths (list[str]) or empty list if error
        - Info markdown (str) with processing details or error message
    """
    # Validate inputs - profile selected
    if not profile_name or len(profile_name.strip()) == 0:
        return [], _format_error(
            "No profile selected",
            "Please select a voice profile from the dropdown.",
        )

    # Validate inputs - script file uploaded
    if not script_file:
        return [], _format_error(
            "No script file uploaded",
            "Please upload a script file (.txt or .md) with text segments to process.",
        )

    try:
        # Load VoiceProfile from file
        profiles_dir = Path("data/profiles")
        profile_path = profiles_dir / f"{profile_name}.json"

        if not profile_path.exists():
            return [], _format_error(
                "Profile not found",
                f"The profile '{profile_name}' does not exist. It may have been deleted. Please create a new profile or select a different one.",
            )

        logger.info(f"Loading voice profile: {profile_name}")
        profile = VoiceProfile.from_json(profile_path)

        # Validate profile has required data
        if not profile.samples or len(profile.samples) == 0:
            return [], _format_error(
                "Invalid profile",
                f"Profile '{profile_name}' has no audio samples. Please recreate the profile.",
            )

        if not profile.ref_text or len(profile.ref_text.strip()) == 0:
            return [], _format_error(
                "Missing reference text",
                f"Profile '{profile_name}' is missing reference text required for voice cloning. Please recreate the profile with reference text.",
            )

        # Get the first sample as reference audio
        ref_sample = profile.samples[0]
        ref_audio_path = Path(ref_sample.path)

        if not ref_audio_path.exists():
            return [], _format_error(
                "Reference audio not found",
                f"Reference audio file not found: {ref_audio_path}. The sample files may have been moved or deleted.",
            )

        # Parse script file
        script_path = Path(script_file)
        if not script_path.exists():
            return [], _format_error(
                "Script file not found",
                f"The script file could not be found: {script_path}",
            )

        logger.info(f"Parsing script file: {script_path.name}")
        segments = _parse_script_file(script_path)

        if not segments:
            return [], _format_error(
                "Empty script",
                "The script file contains no valid segments. Please check the format:\n\n"
                "```\n[SEGMENT_NAME]\nText content here...\n```",
            )

        logger.info(f"Found {len(segments)} segments to process")

        # Load configuration
        config = ConfigManager.load_config()

        # Create output directory
        output_dir = Path("data/outputs") / f"batch_{profile_name}"
        output_dir.mkdir(parents=True, exist_ok=True)

        # Initialize model manager and generator
        logger.info("Initializing Qwen3-TTS model...")
        model_manager = Qwen3ModelManager(config)

        # Load model if not already loaded
        if not model_manager.is_loaded():
            logger.info("Loading Qwen3-TTS model (this may take 30-60 seconds)...")
            success = model_manager.load_model()
            if not success:
                return [], _format_error(
                    "Model loading failed",
                    "Failed to load the Qwen3-TTS model. Please check the logs for details.",
                )

        generator = Qwen3Generator(model_manager, config)

        # Process all segments
        logger.info(f"Processing {len(segments)} segments...")
        results = []
        output_files = []

        for i, (segment_name, segment_text) in enumerate(segments, 1):
            logger.info(f"Processing segment {i}/{len(segments)}: {segment_name}")

            # Generate output filename
            safe_name = _sanitize_filename(segment_name)
            output_path = output_dir / f"{i:02d}_{safe_name}.wav"

            try:
                # Generate audio for this segment
                success = generator.generate_to_file(
                    text=segment_text,
                    ref_audio=ref_audio_path,
                    ref_text=profile.ref_text,
                    output_path=output_path,
                    language=profile.language,
                )

                if success:
                    results.append({"name": segment_name, "success": True})
                    output_files.append(str(output_path))
                    logger.info(f"✓ Generated: {output_path.name}")
                else:
                    results.append({"name": segment_name, "success": False})
                    logger.warning(f"✗ Failed: {segment_name}")

            except Exception as e:
                logger.error(f"Error processing segment {segment_name}: {e}")
                results.append({"name": segment_name, "success": False})

        # Count successes and failures
        successful = sum(1 for r in results if r["success"])
        failed = len(results) - successful

        # Format results info
        info = _format_success(
            profile_name=profile_name,
            total_segments=len(segments),
            successful=successful,
            failed=failed,
            output_dir=output_dir,
        )

        logger.info(
            f"✓ Batch processing complete: {successful}/{len(segments)} successful"
        )
        return output_files, info

    except MemoryError:
        return [], _format_error(
            "Out of memory",
            "Not enough memory to process batch. Try processing fewer segments or closing other applications.",
        )

    except PermissionError as e:
        return [], _format_error(
            "Permission denied",
            f"Cannot write to output directory: {str(e)}",
        )

    except OSError as e:
        return [], _format_error(
            "File system error",
            f"Error accessing files: {str(e)}",
        )

    except Exception as e:
        logger.exception("Unexpected error during batch processing")
        return [], _format_error(
            "Unexpected error",
            f"An unexpected error occurred: {str(e)}. Please check the logs for details.",
        )


def _parse_script_file(script_path: Path) -> list[tuple[str, str]]:
    """
    Parse script file into segments.

    Expected format:
    ```
    [SEGMENT_NAME]
    Text content here...

    [ANOTHER_SEGMENT]
    More text here...
    ```

    Args:
        script_path: Path to script file

    Returns:
        List of (segment_name, segment_text) tuples
    """
    try:
        with open(script_path, encoding="utf-8") as f:
            content = f.read()

        # Pattern to match [SEGMENT_NAME] followed by text
        pattern = r"\[([^\]]+)\]\s*\n((?:(?!\[)[^\n].*\n?)*)"
        matches = re.findall(pattern, content, re.MULTILINE)

        segments = []
        for segment_name, segment_text in matches:
            # Clean up text
            text = segment_text.strip()
            if text:  # Only add non-empty segments
                segments.append((segment_name.strip(), text))

        return segments

    except UnicodeDecodeError:
        logger.error(f"Failed to decode script file: {script_path}")
        return []
    except Exception as e:
        logger.error(f"Error parsing script file: {e}")
        return []


def _sanitize_filename(name: str) -> str:
    """
    Sanitize segment name for use in filename.

    Args:
        name: Segment name

    Returns:
        Sanitized filename-safe string
    """
    # Replace spaces with underscores
    name = name.replace(" ", "_")

    # Remove or replace invalid characters
    name = re.sub(r'[<>:"/\\|?*]', "", name)

    # Limit length
    if len(name) > 50:
        name = name[:50]

    # Convert to lowercase
    name = name.lower()

    return name


def _format_error(title: str, message: str) -> str:
    """
    Format error message as Markdown.

    Args:
        title: Error title
        message: Error message

    Returns:
        Formatted Markdown string
    """
    return f"""
❌ **{title}**

{message}
"""


def _format_success(
    profile_name: str,
    total_segments: int,
    successful: int,
    failed: int,
    output_dir: Path,
) -> str:
    """
    Format success message as Markdown.

    Args:
        profile_name: Name of voice profile used
        total_segments: Total number of segments processed
        successful: Number of successful generations
        failed: Number of failed generations
        output_dir: Output directory path

    Returns:
        Formatted Markdown string
    """
    status_emoji = "✅" if failed == 0 else "⚠️"

    return f"""
## {status_emoji} Batch Processing Complete!

- **Profile**: {profile_name}
- **Total Segments**: {total_segments}
- **Successful**: {successful} ✅
- **Failed**: {failed} {"❌" if failed > 0 else ""}
- **Output Directory**: `{output_dir.name}`

{"All segments processed successfully! " if failed == 0 else f"{failed} segment(s) failed. Check logs for details. "}You can download the generated files below.
"""
