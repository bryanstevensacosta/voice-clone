"""
Profile creation and management handlers for Gradio UI.

This module provides handlers for creating voice profiles from uploaded audio samples
and managing the list of available profiles.
"""

from pathlib import Path
from typing import Any

import gradio as gr

from voice_clone.audio.processor import AudioProcessor
from voice_clone.model.profile import VoiceProfile, VoiceSample


def create_profile_handler(
    files: list[str], name: str, ref_text: str
) -> tuple[dict[str, Any], gr.Dropdown, gr.Dropdown]:
    """
    Create voice profile from uploaded samples.

    This handler creates a voice profile from the uploaded audio samples,
    saves it to disk, and updates the profile dropdowns in both Tab 2 and Tab 3.

    Args:
        files: List of audio file paths from Gradio File component
        name: Profile name (user input)
        ref_text: Reference text describing the audio samples (optional)

    Returns:
        Tuple of:
        - Profile info dict (for JSON display) or error dict
        - Updated dropdown for Tab 2 (with new profile selected)
        - Updated dropdown for Tab 3 (with new profile selected)
    """
    # Validate inputs - empty files
    if not files or len(files) == 0:
        error_dict = {
            "error": "No audio files uploaded",
            "message": "Please upload 1-3 audio samples to create a voice profile.",
        }
        empty_dropdown = gr.Dropdown(choices=[])
        return error_dict, empty_dropdown, empty_dropdown

    # Validate inputs - missing profile name
    if not name or len(name.strip()) == 0:
        error_dict = {
            "error": "Profile name required",
            "message": "Please provide a name for your voice profile.",
        }
        empty_dropdown = gr.Dropdown(choices=[])
        return error_dict, empty_dropdown, empty_dropdown

    # Sanitize profile name (alphanumeric, underscore, hyphen only)
    name = name.strip()
    if not _is_valid_profile_name(name):
        error_dict = {
            "error": "Invalid profile name",
            "message": "Profile name must contain only letters, numbers, underscores, and hyphens (max 50 characters).",
        }
        empty_dropdown = gr.Dropdown(choices=[])
        return error_dict, empty_dropdown, empty_dropdown

    # Check for duplicate profile names
    profiles_dir = Path("data/profiles")
    profile_path = profiles_dir / f"{name}.json"

    if profile_path.exists():
        error_dict = {
            "error": "Profile already exists",
            "message": f"A profile named '{name}' already exists. Please choose a different name or delete the existing profile.",
        }
        # Still return current profiles in dropdowns
        available_profiles = list_available_profiles()
        return (
            error_dict,
            gr.Dropdown(choices=available_profiles),
            gr.Dropdown(choices=available_profiles),
        )

    try:
        # Create profiles directory if it doesn't exist
        profiles_dir.mkdir(parents=True, exist_ok=True)

        # Process audio samples and create VoiceSample objects
        processor = AudioProcessor()
        samples = []

        for file_path in files:
            file_path_obj = Path(file_path)

            # Validate the sample
            result = processor.validate_sample(file_path_obj)

            if not result.is_valid():
                # Skip invalid samples but continue with others
                continue

            # Get duration from validation result
            duration_str = result.metadata.get("duration", "0s")
            duration = float(duration_str.rstrip("s"))

            # Infer emotion from filename (basic heuristic)
            emotion = _infer_emotion_from_filename(file_path_obj.stem)

            # Create VoiceSample
            sample = VoiceSample(
                path=str(file_path_obj),
                duration=duration,
                emotion=emotion,
                quality_score=1.0 if not result.warnings else 0.8,
            )
            samples.append(sample)

        # Check if we have at least one valid sample
        if len(samples) == 0:
            error_dict = {
                "error": "No valid audio samples",
                "message": "None of the uploaded files are valid audio samples. Please check the file formats and try again.",
            }
            empty_dropdown = gr.Dropdown(choices=[])
            return error_dict, empty_dropdown, empty_dropdown

        # Create VoiceProfile
        profile = VoiceProfile(
            name=name,
            samples=samples,
            language="es",  # Default to Spanish
            ref_text=ref_text if ref_text else "Voice sample for cloning",
        )

        # Calculate total duration
        profile.total_duration = sum(s.duration for s in samples)

        # Save profile to JSON
        profile.to_json(profile_path)

        # Get updated list of available profiles
        available_profiles = list_available_profiles()

        # Create profile info dict for display
        profile_info = {
            "name": profile.name,
            "samples": len(profile.samples),
            "total_duration": f"{profile.total_duration:.1f}s",
            "created_at": profile.created_at,
            "language": profile.language,
            "ref_text": profile.ref_text,
            "path": str(profile_path),
        }

        # Validate profile and add warnings if any
        is_valid, warnings = profile.validate()
        if warnings:
            profile_info["warnings"] = warnings

        # Return profile info and updated dropdowns (with new profile selected)
        return (
            profile_info,
            gr.Dropdown(choices=available_profiles, value=name),
            gr.Dropdown(choices=available_profiles, value=name),
        )

    except PermissionError as e:
        error_dict = {
            "error": "Permission denied",
            "message": f"Cannot write to profiles directory: {str(e)}",
        }
        empty_dropdown = gr.Dropdown(choices=[])
        return error_dict, empty_dropdown, empty_dropdown

    except OSError as e:
        error_dict = {
            "error": "File system error",
            "message": f"Error saving profile: {str(e)}",
        }
        empty_dropdown = gr.Dropdown(choices=[])
        return error_dict, empty_dropdown, empty_dropdown

    except Exception as e:
        error_dict = {
            "error": "Unexpected error",
            "message": f"Failed to create profile: {str(e)}",
        }
        empty_dropdown = gr.Dropdown(choices=[])
        return error_dict, empty_dropdown, empty_dropdown


def list_available_profiles() -> list[str]:
    """
    Get list of available voice profiles.

    Scans the data/profiles directory and returns a list of profile names
    (without the .json extension).

    Returns:
        List of profile names (strings)
    """
    profiles_dir = Path("data/profiles")

    # Return empty list if directory doesn't exist
    if not profiles_dir.exists():
        return []

    # Get all .json files and extract names (without extension)
    try:
        profiles = [p.stem for p in profiles_dir.glob("*.json")]
        return sorted(profiles)  # Return sorted for consistent ordering
    except Exception:
        # Return empty list if there's any error reading the directory
        return []


def _is_valid_profile_name(name: str) -> bool:
    """
    Validate profile name format.

    Profile names must:
    - Be 1-50 characters long
    - Contain only alphanumeric characters, underscores, and hyphens
    - Not contain path traversal characters

    Args:
        name: Profile name to validate

    Returns:
        True if valid, False otherwise
    """
    import re

    if not name or len(name) > 50:
        return False

    # Only allow alphanumeric, underscore, and hyphen
    return bool(re.match(r"^[a-zA-Z0-9_-]+$", name))


def _infer_emotion_from_filename(filename: str) -> str:
    """
    Infer emotion from filename using simple heuristics.

    Args:
        filename: Filename (without extension)

    Returns:
        Emotion string (neutral, happy, sad, angry, calm, serious, excited)
    """
    filename_lower = filename.lower()

    if "happy" in filename_lower or "excited" in filename_lower:
        return "happy"
    elif "sad" in filename_lower:
        return "sad"
    elif "angry" in filename_lower:
        return "angry"
    elif "calm" in filename_lower or "relaxed" in filename_lower:
        return "calm"
    elif "serious" in filename_lower or "professional" in filename_lower:
        return "serious"
    else:
        return "neutral"
