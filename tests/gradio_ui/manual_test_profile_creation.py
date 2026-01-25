"""
Manual test script for profile creation workflow.

This script provides a manual testing guide for the profile creation feature
in the Gradio UI. Run this to verify the complete workflow works as expected.

Usage:
    python tests/gradio_ui/manual_test_profile_creation.py
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

# Import after path modification
from gradio_ui.handlers.profile_handler import (  # noqa: E402
    create_profile_handler,
    list_available_profiles,
)


def print_section(title: str) -> None:
    """Print a section header."""
    print(f"\n{'=' * 80}")
    print(f"  {title}")
    print(f"{'=' * 80}\n")


def test_list_profiles():
    """Test listing available profiles."""
    print_section("TEST 1: List Available Profiles")

    profiles = list_available_profiles()
    print(f"Found {len(profiles)} profiles:")
    for profile in profiles:
        print(f"  - {profile}")

    return profiles


def test_create_profile_no_files():
    """Test creating profile with no files."""
    print_section("TEST 2: Create Profile with No Files (Should Fail)")

    result, dropdown1, dropdown2 = create_profile_handler(
        files=[], name="test_profile", ref_text="Test reference"
    )

    print("Result:")
    print(f"  Error: {result.get('error', 'None')}")
    print(f"  Message: {result.get('message', 'None')}")
    print(f"  Dropdown 1 choices: {dropdown1.choices}")
    print(f"  Dropdown 2 choices: {dropdown2.choices}")

    assert "error" in result
    print("\n✅ Test passed: Error correctly returned for no files")


def test_create_profile_no_name():
    """Test creating profile with no name."""
    print_section("TEST 3: Create Profile with No Name (Should Fail)")

    # Create a dummy file
    dummy_file = Path("tests/fixtures/test_sample.wav")
    if not dummy_file.exists():
        print(f"⚠️  Warning: Test file {dummy_file} not found, skipping test")
        return

    result, dropdown1, dropdown2 = create_profile_handler(
        files=[str(dummy_file)], name="", ref_text="Test reference"
    )

    print("Result:")
    print(f"  Error: {result.get('error', 'None')}")
    print(f"  Message: {result.get('message', 'None')}")

    assert "error" in result
    print("\n✅ Test passed: Error correctly returned for missing name")


def test_create_profile_invalid_name():
    """Test creating profile with invalid name."""
    print_section("TEST 4: Create Profile with Invalid Name (Should Fail)")

    dummy_file = Path("tests/fixtures/test_sample.wav")
    if not dummy_file.exists():
        print(f"⚠️  Warning: Test file {dummy_file} not found, skipping test")
        return

    result, dropdown1, dropdown2 = create_profile_handler(
        files=[str(dummy_file)],
        name="test/profile",  # Invalid: contains slash
        ref_text="Test reference",
    )

    print("Result:")
    print(f"  Error: {result.get('error', 'None')}")
    print(f"  Message: {result.get('message', 'None')}")

    assert "error" in result
    print("\n✅ Test passed: Error correctly returned for invalid name")


def test_create_profile_success():
    """Test successful profile creation."""
    print_section("TEST 5: Create Profile Successfully")

    # Check if we have test samples
    samples_dir = Path("data/samples")
    if not samples_dir.exists() or not list(samples_dir.glob("*.wav")):
        print("⚠️  Warning: No audio samples found in data/samples/")
        print("   Please add some .wav files to data/samples/ to test profile creation")
        return

    # Get first 3 samples
    sample_files = list(samples_dir.glob("*.wav"))[:3]
    print(f"Using {len(sample_files)} sample files:")
    for f in sample_files:
        print(f"  - {f.name}")

    result, dropdown1, dropdown2 = create_profile_handler(
        files=[str(f) for f in sample_files],
        name="manual_test_profile",
        ref_text="This is a manual test profile",
    )

    print("\nResult:")
    if "error" in result:
        print(f"  ❌ Error: {result['error']}")
        print(f"  Message: {result['message']}")
    else:
        print("  ✅ Profile created successfully!")
        print(f"  Name: {result['name']}")
        print(f"  Samples: {result['samples']}")
        print(f"  Total Duration: {result['total_duration']}")
        print(f"  Language: {result['language']}")
        print(f"  Reference Text: {result['ref_text']}")
        print(f"  Path: {result['path']}")

        if "warnings" in result:
            print("\n  Warnings:")
            for warning in result["warnings"]:
                print(f"    - {warning}")

        print(f"\n  Dropdown 1 choices: {dropdown1.choices}")
        print(f"  Dropdown 1 value: {dropdown1.value}")
        print(f"  Dropdown 2 choices: {dropdown2.choices}")
        print(f"  Dropdown 2 value: {dropdown2.value}")

        assert "manual_test_profile" in dropdown1.choices
        assert dropdown1.value == "manual_test_profile"
        print("\n✅ Test passed: Profile created and dropdowns updated")


def test_create_duplicate_profile():
    """Test creating duplicate profile."""
    print_section("TEST 6: Create Duplicate Profile (Should Fail)")

    # Check if manual_test_profile exists
    profile_path = Path("data/profiles/manual_test_profile.json")
    if not profile_path.exists():
        print("⚠️  Skipping: manual_test_profile doesn't exist yet")
        return

    samples_dir = Path("data/samples")
    if not samples_dir.exists() or not list(samples_dir.glob("*.wav")):
        print("⚠️  Warning: No audio samples found")
        return

    sample_files = list(samples_dir.glob("*.wav"))[:1]

    result, dropdown1, dropdown2 = create_profile_handler(
        files=[str(f) for f in sample_files],
        name="manual_test_profile",  # Duplicate name
        ref_text="Duplicate test",
    )

    print("Result:")
    print(f"  Error: {result.get('error', 'None')}")
    print(f"  Message: {result.get('message', 'None')}")

    assert "error" in result
    assert result["error"] == "Profile already exists"
    print("\n✅ Test passed: Duplicate profile correctly rejected")


def cleanup():
    """Clean up test profile."""
    print_section("CLEANUP: Remove Test Profile")

    profile_path = Path("data/profiles/manual_test_profile.json")
    if profile_path.exists():
        profile_path.unlink()
        print("✅ Removed manual_test_profile.json")
    else:
        print("ℹ️  No test profile to clean up")


def main():
    """Run all manual tests."""
    print("\n" + "=" * 80)
    print("  MANUAL TEST SUITE: Profile Creation")
    print("=" * 80)

    try:
        # Test 1: List profiles
        initial_profiles = test_list_profiles()

        # Test 2: No files
        test_create_profile_no_files()

        # Test 3: No name
        test_create_profile_no_name()

        # Test 4: Invalid name
        test_create_profile_invalid_name()

        # Test 5: Success
        test_create_profile_success()

        # Test 6: Duplicate
        test_create_duplicate_profile()

        # Final check: List profiles again
        final_profiles = test_list_profiles()

        print_section("SUMMARY")
        print(f"Initial profiles: {len(initial_profiles)}")
        print(f"Final profiles: {len(final_profiles)}")

        if len(final_profiles) > len(initial_profiles):
            print(
                f"\n✅ New profile created: {set(final_profiles) - set(initial_profiles)}"
            )

        print("\n" + "=" * 80)
        print("  ALL TESTS COMPLETED")
        print("=" * 80)

        # Ask if user wants to cleanup
        print("\nDo you want to remove the test profile? (y/n): ", end="")
        response = input().strip().lower()
        if response == "y":
            cleanup()
        else:
            print("ℹ️  Test profile kept for inspection")

    except Exception as e:
        print(f"\n❌ Test failed with exception: {e}")
        import traceback

        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
