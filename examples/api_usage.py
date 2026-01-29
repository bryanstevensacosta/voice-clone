"""Example usage of TTS Studio API.

This example demonstrates how to use the TTSStudio API to:
1. Validate audio samples
2. Create a voice profile
3. Generate audio from text
4. List available profiles
5. Delete a profile

This is the recommended way to interact with the TTS Studio core library.
"""

import sys
from pathlib import Path

from api.studio import TTSStudio

# Add apps/core/src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "apps" / "core" / "src"))


def main():
    """Main example function."""
    print("=" * 60)
    print("TTS Studio API Usage Example")
    print("=" * 60)
    print()

    # Initialize the API
    print("1. Initializing TTS Studio API...")
    studio = TTSStudio()
    print("   ✓ API initialized successfully")
    print()

    # Example sample paths (replace with your actual samples)
    sample_paths = [
        "./data/samples/neutral_01.wav",
        "./data/samples/neutral_02.wav",
        "./data/samples/happy_01.wav",
    ]

    # Step 1: Validate samples
    print("2. Validating audio samples...")
    validation_result = studio.validate_samples(sample_paths=sample_paths)

    if validation_result["status"] == "success":
        print(f"   ✓ Validated {validation_result['total_samples']} samples")
        print(f"   ✓ Valid: {validation_result['valid_samples']}")
        print(f"   ✓ Invalid: {validation_result['invalid_samples']}")
        print(f"   ✓ Total duration: {validation_result['total_duration']:.1f}s")

        if not validation_result["all_valid"]:
            print("   ⚠ Some samples are invalid:")
            for result in validation_result["results"]:
                if not result["valid"]:
                    print(f"     - {result['path']}: {result['error']}")
            print()
            print("   Please fix invalid samples before creating profile.")
            return
    else:
        print(f"   ✗ Validation failed: {validation_result['error']}")
        return
    print()

    # Step 2: Create voice profile
    print("3. Creating voice profile...")
    profile_result = studio.create_voice_profile(
        name="my_voice",
        sample_paths=sample_paths,
        language="es",
        reference_text="Samples de mi voz para clonación",
    )

    if profile_result["status"] == "success":
        profile = profile_result["profile"]
        print("   ✓ Profile created successfully")
        print(f"   ✓ Profile ID: {profile['id']}")
        print(f"   ✓ Name: {profile['name']}")
        print(f"   ✓ Language: {profile['language']}")
        print(f"   ✓ Samples: {len(profile['samples'])}")
        print(f"   ✓ Total duration: {profile['total_duration']:.1f}s")
        profile_id = profile["id"]
    else:
        print(f"   ✗ Profile creation failed: {profile_result['error']}")
        return
    print()

    # Step 3: Generate audio
    print("4. Generating audio from text...")
    text = "Hola, bienvenidos a este ejemplo de TTS Studio. Esta es mi voz clonada."

    generation_result = studio.generate_audio(
        profile_id=profile_id,
        text=text,
        temperature=0.75,
        speed=1.0,
        mode="clone",
    )

    if generation_result["status"] == "success":
        print("   ✓ Audio generated successfully")
        print(f"   ✓ Output: {generation_result['output_path']}")
        print(f"   ✓ Duration: {generation_result['duration']:.1f}s")
        print(f"   ✓ Generation time: {generation_result['generation_time']:.1f}s")
    else:
        print(f"   ✗ Generation failed: {generation_result['error']}")
    print()

    # Step 4: List all profiles
    print("5. Listing all voice profiles...")
    list_result = studio.list_voice_profiles()

    if list_result["status"] == "success":
        print(f"   ✓ Found {list_result['count']} profile(s)")
        for profile in list_result["profiles"]:
            print(f"     - {profile['name']} (ID: {profile['id']})")
    else:
        print(f"   ✗ Listing failed: {list_result['error']}")
    print()

    # Step 5: Delete profile (optional)
    print("6. Deleting voice profile...")
    delete_result = studio.delete_voice_profile(profile_id=profile_id)

    if delete_result["status"] == "success":
        print("   ✓ Profile deleted successfully")
    else:
        print(f"   ✗ Deletion failed: {delete_result['error']}")
    print()

    print("=" * 60)
    print("Example completed!")
    print("=" * 60)


def example_error_handling():
    """Example of error handling with the API."""
    print("\n" + "=" * 60)
    print("Error Handling Example")
    print("=" * 60)
    print()

    studio = TTSStudio()

    # Example 1: Invalid sample path
    print("1. Handling invalid sample path...")
    result = studio.validate_samples(sample_paths=["nonexistent.wav"])

    if result["status"] == "success":
        if not result["all_valid"]:
            print("   ⚠ Sample validation failed:")
            for sample_result in result["results"]:
                if not sample_result["valid"]:
                    print(f"     Error: {sample_result['error']}")
    print()

    # Example 2: Non-existent profile
    print("2. Handling non-existent profile...")
    result = studio.generate_audio(profile_id="nonexistent_profile", text="Test text")

    if result["status"] == "error":
        print(f"   ⚠ Expected error: {result['error']}")
    print()

    # Example 3: Empty text
    print("3. Handling empty text...")
    result = studio.generate_audio(profile_id="any_profile", text="")

    if result["status"] == "error":
        print(f"   ⚠ Expected error: {result['error']}")
    print()


def example_configuration():
    """Example of configuration management."""
    print("\n" + "=" * 60)
    print("Configuration Management Example")
    print("=" * 60)
    print()

    studio = TTSStudio()

    # Get configuration values
    print("1. Reading configuration...")
    sample_rate = studio.get_config("audio.sample_rate", 12000)
    language = studio.get_config("generation.language", "es")
    device = studio.get_config("model.device", "cpu")

    print(f"   Sample rate: {sample_rate} Hz")
    print(f"   Language: {language}")
    print(f"   Device: {device}")
    print()

    # Reload configuration
    print("2. Reloading configuration...")
    result = studio.reload_config()

    if result["status"] == "success":
        print("   ✓ Configuration reloaded successfully")
    else:
        print(f"   ✗ Reload failed: {result['error']}")
    print()


if __name__ == "__main__":
    # Run main example
    main()

    # Run error handling example
    example_error_handling()

    # Run configuration example
    example_configuration()
