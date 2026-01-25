"""
Audio generation handler for Gradio UI.

This module provides handlers for generating audio from text using voice profiles
with the Qwen3-TTS model.
"""

from pathlib import Path

from voice_clone.config import ConfigManager
from voice_clone.model.profile import VoiceProfile
from voice_clone.model.qwen3_generator import Qwen3Generator
from voice_clone.model.qwen3_manager import Qwen3ModelManager
from voice_clone.utils.logger import logger


def generate_audio_handler(
    profile_name: str,
    text: str,
    temperature: float,
    speed: float,
) -> tuple[str | None, str]:
    """
    Generate audio from text using selected voice profile.

    This handler loads the voice profile, initializes the Qwen3-TTS model,
    generates audio from the provided text, and returns the audio file path
    along with generation information.

    Args:
        profile_name: Name of the voice profile to use
        text: Text to convert to speech
        temperature: Generation temperature (0.5-1.0, controls variability)
        speed: Speaking speed multiplier (0.8-1.2)

    Returns:
        Tuple of:
        - Audio file path (str) or None if error
        - Info markdown (str) with generation details or error message
    """
    # Validate inputs - profile selected
    if not profile_name or len(profile_name.strip()) == 0:
        return None, _format_error(
            "No profile selected",
            "Please select a voice profile from the dropdown.",
        )

    # Validate inputs - text not empty
    if not text or len(text.strip()) == 0:
        return None, _format_error(
            "No text provided",
            "Please enter the text you want to convert to speech.",
        )

    # Validate text length (warn if too long)
    text = text.strip()
    if len(text) > 500:
        logger.warning(
            f"Text length ({len(text)} chars) exceeds recommended 500 characters. Quality may degrade."
        )

    try:
        # Load VoiceProfile from file
        profiles_dir = Path("data/profiles")
        profile_path = profiles_dir / f"{profile_name}.json"

        if not profile_path.exists():
            return None, _format_error(
                "Profile not found",
                f"The profile '{profile_name}' does not exist. It may have been deleted. Please create a new profile or select a different one.",
            )

        logger.info(f"Loading voice profile: {profile_name}")
        profile = VoiceProfile.from_json(profile_path)

        # Validate profile has required data for Qwen3-TTS
        if not profile.samples or len(profile.samples) == 0:
            return None, _format_error(
                "Invalid profile",
                f"Profile '{profile_name}' has no audio samples. Please recreate the profile.",
            )

        if not profile.ref_text or len(profile.ref_text.strip()) == 0:
            return None, _format_error(
                "Missing reference text",
                f"Profile '{profile_name}' is missing reference text required for voice cloning. Please recreate the profile with reference text.",
            )

        # Get the first sample as reference audio (Qwen3-TTS uses one reference)
        ref_sample = profile.samples[0]
        ref_audio_path = Path(ref_sample.path)

        if not ref_audio_path.exists():
            return None, _format_error(
                "Reference audio not found",
                f"Reference audio file not found: {ref_audio_path}. The sample files may have been moved or deleted.",
            )

        # Load configuration
        config = ConfigManager.load_config()

        # Create output directory if needed
        output_dir = Path("data/outputs")
        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate unique output filename
        output_path = output_dir / f"generated_{profile_name}.wav"

        # Initialize model manager and generator
        logger.info("Initializing Qwen3-TTS model...")
        model_manager = Qwen3ModelManager(config)

        # Load model if not already loaded
        if not model_manager.is_loaded():
            logger.info("Loading Qwen3-TTS model (this may take 30-60 seconds)...")
            success = model_manager.load_model()
            if not success:
                return None, _format_error(
                    "Model loading failed",
                    "Failed to load the Qwen3-TTS model. Please check the logs for details.",
                )

        generator = Qwen3Generator(model_manager, config)

        # Generate audio
        logger.info(f"Generating audio for text: {text[:50]}...")
        success = generator.generate_to_file(
            text=text,
            ref_audio=ref_audio_path,
            ref_text=profile.ref_text,
            output_path=output_path,
            language=profile.language,
        )

        if not success:
            return None, _format_error(
                "Generation failed",
                "Audio generation failed. Please check the logs for details. Try with shorter text or different parameters.",
            )

        # Calculate audio duration (approximate)
        import soundfile as sf

        audio_data, sample_rate = sf.read(output_path)
        duration = len(audio_data) / sample_rate

        # Format generation info
        info = _format_success(
            profile_name=profile_name,
            text_length=len(text),
            temperature=temperature,
            speed=speed,
            output_file=output_path.name,
            duration=duration,
        )

        logger.info(f"✓ Audio generated successfully: {output_path}")
        return str(output_path), info

    except MemoryError:
        return None, _format_error(
            "Out of memory",
            "Not enough memory to generate audio. Try closing other applications or using shorter text.",
        )

    except PermissionError as e:
        return None, _format_error(
            "Permission denied",
            f"Cannot write to output directory: {str(e)}",
        )

    except OSError as e:
        return None, _format_error(
            "File system error",
            f"Error accessing files: {str(e)}",
        )

    except Exception as e:
        logger.exception("Unexpected error during audio generation")
        return None, _format_error(
            "Unexpected error",
            f"An unexpected error occurred: {str(e)}. Please check the logs for details.",
        )


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
    text_length: int,
    temperature: float,
    speed: float,
    output_file: str,
    duration: float,
) -> str:
    """
    Format success message as Markdown.

    Args:
        profile_name: Name of voice profile used
        text_length: Length of input text in characters
        temperature: Temperature parameter used
        speed: Speed parameter used
        output_file: Name of output file
        duration: Duration of generated audio in seconds

    Returns:
        Formatted Markdown string
    """
    return f"""
## ✅ Audio Generated Successfully!

- **Profile**: {profile_name}
- **Text Length**: {text_length} characters
- **Temperature**: {temperature}
- **Speed**: {speed}x
- **Duration**: {duration:.2f} seconds
- **Output**: `{output_file}`

You can listen to the audio above and download it using the download button.
"""
