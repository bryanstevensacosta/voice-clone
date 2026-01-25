"""
Manual test script for batch processing handler.

This script helps manually test the batch processing functionality
in the Gradio UI without running the full application.

Usage:
    python tests/gradio_ui/manual_test_batch.py
"""

from pathlib import Path

from gradio_ui.handlers.batch_handler import batch_process_handler


def create_test_script():
    """Create a test script file."""
    script_dir = Path("data/scripts")
    script_dir.mkdir(parents=True, exist_ok=True)

    script_content = """[INTRO]
Hola, bienvenidos a este tutorial sobre inteligencia artificial.

[SECTION_1]
Hoy vamos a hablar sobre redes neuronales y cómo funcionan.

[SECTION_2]
Las redes neuronales son modelos computacionales inspirados en el cerebro humano.

[OUTRO]
Gracias por ver este video. No olvides suscribirte al canal.
"""

    script_path = script_dir / "test_script.txt"
    with open(script_path, "w") as f:
        f.write(script_content)

    print(f"✓ Created test script: {script_path}")
    return script_path


def test_validation_errors():
    """Test validation error scenarios."""
    print("\n" + "=" * 60)
    print("Testing Validation Errors")
    print("=" * 60)

    # Test 1: No profile selected
    print("\n1. Testing with no profile selected...")
    files, info = batch_process_handler("", "script.txt")
    print(f"   Result: {len(files)} files")
    print(f"   Info:\n{info}")
    assert files == []
    assert "No profile selected" in info
    print("   ✓ Passed")

    # Test 2: No script file
    print("\n2. Testing with no script file...")
    files, info = batch_process_handler("test_profile", None)
    print(f"   Result: {len(files)} files")
    print(f"   Info:\n{info}")
    assert files == []
    assert "No script file uploaded" in info
    print("   ✓ Passed")

    # Test 3: Profile not found
    print("\n3. Testing with non-existent profile...")
    files, info = batch_process_handler("nonexistent", "script.txt")
    print(f"   Result: {len(files)} files")
    print(f"   Info:\n{info}")
    assert files == []
    assert "Profile not found" in info
    print("   ✓ Passed")


def test_script_parsing():
    """Test script parsing."""
    print("\n" + "=" * 60)
    print("Testing Script Parsing")
    print("=" * 60)

    script_path = create_test_script()

    print("\nScript content:")
    with open(script_path) as f:
        content = f.read()
        print(content)

    print("\nExpected segments:")
    print("  1. INTRO")
    print("  2. SECTION_1")
    print("  3. SECTION_2")
    print("  4. OUTRO")


def test_with_real_profile():
    """Test with a real profile if available."""
    print("\n" + "=" * 60)
    print("Testing with Real Profile (if available)")
    print("=" * 60)

    # Check if any profiles exist
    profiles_dir = Path("data/profiles")
    if not profiles_dir.exists():
        print("\n⚠️  No profiles directory found")
        print("   Create a profile in the Gradio UI first")
        return

    profiles = list(profiles_dir.glob("*.json"))
    if not profiles:
        print("\n⚠️  No profiles found")
        print("   Create a profile in the Gradio UI first")
        return

    # Use the first profile
    profile_path = profiles[0]
    profile_name = profile_path.stem

    print(f"\n✓ Found profile: {profile_name}")

    # Create test script
    script_path = create_test_script()

    print("\n⚠️  This would attempt real batch processing")
    print(f"   Profile: {profile_name}")
    print(f"   Script: {script_path}")
    print("\n   To test for real, uncomment the code below")

    # Uncomment to test for real:
    # print("\nProcessing batch...")
    # files, info = batch_process_handler(profile_name, str(script_path))
    # print(f"\nResult: {len(files)} files generated")
    # print(f"Info:\n{info}")
    # if files:
    #     print("\nGenerated files:")
    #     for f in files:
    #         print(f"  - {f}")


def main():
    """Run all manual tests."""
    print("=" * 60)
    print("Manual Test Suite for Batch Processing Handler")
    print("=" * 60)

    try:
        # Run validation tests
        test_validation_errors()

        # Test script parsing
        test_script_parsing()

        # Test with real profile (if available)
        test_with_real_profile()

        print("\n" + "=" * 60)
        print("All Manual Tests Completed Successfully!")
        print("=" * 60)
        print("\nNote: These tests verify error handling and validation.")
        print("To test actual batch processing, you need:")
        print("  1. A real voice profile with valid audio samples")
        print("  2. The Qwen3-TTS model downloaded and configured")
        print("  3. Uncomment the real processing code in test_with_real_profile()")
        print("  4. Or run the full Gradio UI: voice-clone ui")

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
