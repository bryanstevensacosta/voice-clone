"""
Manual test script for audio generation handler.

This script helps manually test the audio generation functionality
in the Gradio UI without running the full application.

Usage:
    python tests/gradio_ui/manual_test_generation.py
"""

import json
from pathlib import Path

from gradio_ui.handlers.generation_handler import generate_audio_handler


def setup_test_profile():
    """Create a test profile for manual testing."""
    profiles_dir = Path("data/profiles")
    profiles_dir.mkdir(parents=True, exist_ok=True)

    # Create a simple test profile
    profile_data = {
        "name": "manual_test_profile",
        "created_at": "2024-01-25T00:00:00",
        "language": "es",
        "total_duration": 30.0,
        "ref_text": "Esta es una muestra de voz para clonación de prueba.",
        "sample_rate": 12000,
        "samples": [
            {
                "path": "data/samples/test_sample.wav",
                "duration": 10.0,
                "emotion": "neutral",
                "quality_score": 1.0,
            }
        ],
    }

    profile_path = profiles_dir / "manual_test_profile.json"
    with open(profile_path, "w") as f:
        json.dump(profile_data, f, indent=2)

    print(f"✓ Created test profile: {profile_path}")
    return profile_path


def test_validation_errors():
    """Test validation error scenarios."""
    print("\n" + "=" * 60)
    print("Testing Validation Errors")
    print("=" * 60)

    # Test 1: No profile selected
    print("\n1. Testing with no profile selected...")
    audio_path, info = generate_audio_handler("", "Some text", 0.75, 1.0)
    print(f"   Result: {audio_path}")
    print(f"   Info:\n{info}")
    assert audio_path is None
    assert "No profile selected" in info
    print("   ✓ Passed")

    # Test 2: No text provided
    print("\n2. Testing with no text...")
    audio_path, info = generate_audio_handler("test_profile", "", 0.75, 1.0)
    print(f"   Result: {audio_path}")
    print(f"   Info:\n{info}")
    assert audio_path is None
    assert "No text provided" in info
    print("   ✓ Passed")

    # Test 3: Profile not found
    print("\n3. Testing with non-existent profile...")
    audio_path, info = generate_audio_handler(
        "nonexistent_profile", "Some text", 0.75, 1.0
    )
    print(f"   Result: {audio_path}")
    print(f"   Info:\n{info}")
    assert audio_path is None
    assert "Profile not found" in info
    print("   ✓ Passed")


def test_parameter_ranges():
    """Test different parameter values."""
    print("\n" + "=" * 60)
    print("Testing Parameter Ranges")
    print("=" * 60)

    test_cases = [
        ("Minimum temperature", 0.5, 1.0),
        ("Maximum temperature", 1.0, 1.0),
        ("Minimum speed", 0.75, 0.8),
        ("Maximum speed", 0.75, 1.2),
        ("Default values", 0.75, 1.0),
    ]

    for name, temp, speed in test_cases:
        print(f"\n{name}: temp={temp}, speed={speed}")
        # This will fail (no real profile), but shouldn't crash
        audio_path, info = generate_audio_handler("test_profile", "Text", temp, speed)
        print(f"   Result: {audio_path}")
        print(f"   Info (first 100 chars): {info[:100]}...")
        print("   ✓ No crash")


def test_text_lengths():
    """Test different text lengths."""
    print("\n" + "=" * 60)
    print("Testing Text Lengths")
    print("=" * 60)

    test_cases = [
        ("Short text", "Hola"),
        ("Medium text", "Hola, este es un texto de prueba de longitud media."),
        ("Long text", "A" * 500),
        ("Very long text", "A" * 600),
    ]

    for name, text in test_cases:
        print(f"\n{name}: {len(text)} characters")
        audio_path, info = generate_audio_handler("test_profile", text, 0.75, 1.0)
        print(f"   Result: {audio_path}")
        print(f"   Info (first 100 chars): {info[:100]}...")
        print("   ✓ No crash")


def main():
    """Run all manual tests."""
    print("=" * 60)
    print("Manual Test Suite for Audio Generation Handler")
    print("=" * 60)

    try:
        # Run validation tests
        test_validation_errors()

        # Run parameter tests
        test_parameter_ranges()

        # Run text length tests
        test_text_lengths()

        print("\n" + "=" * 60)
        print("All Manual Tests Completed Successfully!")
        print("=" * 60)
        print("\nNote: These tests verify error handling and validation.")
        print("To test actual audio generation, you need:")
        print("  1. A real voice profile with valid audio samples")
        print("  2. The Qwen3-TTS model downloaded and configured")
        print("  3. Run the full Gradio UI: voice-clone ui")

    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback

        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
