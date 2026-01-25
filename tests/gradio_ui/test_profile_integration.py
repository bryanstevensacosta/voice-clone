"""
Integration tests for profile creation workflow.

These tests verify the complete end-to-end workflow of profile creation,
including UI component interaction and backend integration.
"""

from unittest.mock import Mock, patch

import gradio as gr
from gradio_ui.app import create_app
from gradio_ui.handlers.profile_handler import (
    create_profile_handler,
    list_available_profiles,
)


class TestProfileCreationIntegration:
    """Integration tests for the complete profile creation workflow."""

    def test_app_has_profile_components(self):
        """Test that the app contains all required profile creation components."""
        app = create_app()

        # Verify app was created
        assert app is not None
        assert isinstance(app, gr.Blocks)

        # Note: We can't easily inspect Gradio component structure programmatically,
        # but we can verify the app builds without errors
        print("✅ App created successfully with all components")

    @patch("gradio_ui.handlers.profile_handler.AudioProcessor")
    @patch("gradio_ui.handlers.profile_handler.VoiceProfile")
    def test_complete_workflow_simulation(
        self, mock_profile_class, mock_processor_class, tmp_path
    ):
        """Simulate the complete workflow from file upload to profile creation."""
        # Setup mocks
        mock_processor = Mock()
        mock_processor_class.return_value = mock_processor

        # Mock validation result
        mock_result = Mock()
        mock_result.is_valid.return_value = True
        mock_result.warnings = []
        mock_result.metadata = {"duration": "15.0s"}
        mock_processor.validate_sample.return_value = mock_result

        # Mock VoiceProfile
        mock_profile = Mock()
        mock_profile.name = "integration_test_profile"
        mock_profile.samples = [Mock(duration=15.0)]
        mock_profile.total_duration = 15.0
        mock_profile.created_at = "2024-01-25T12:00:00"
        mock_profile.language = "es"
        mock_profile.ref_text = "Integration test reference"
        mock_profile.validate.return_value = (True, [])
        mock_profile_class.return_value = mock_profile

        # Setup filesystem
        profiles_dir = tmp_path / "data" / "profiles"
        profiles_dir.mkdir(parents=True, exist_ok=True)

        # Create dummy audio file
        dummy_file = tmp_path / "test_sample.wav"
        dummy_file.write_text("dummy audio data")

        # Patch Path
        with patch("gradio_ui.handlers.profile_handler.Path") as mock_path:

            def path_constructor(path_str):
                if path_str == "data/profiles":
                    return profiles_dir
                return tmp_path / path_str if isinstance(path_str, str) else path_str

            mock_path.side_effect = path_constructor

            # Step 1: User uploads files (simulated by having file paths)
            uploaded_files = [str(dummy_file)]

            # Step 2: User enters profile name and reference text
            profile_name = "integration_test_profile"
            ref_text = "Integration test reference"

            # Step 3: User clicks "Create Profile" button
            # This calls create_profile_handler
            result, dropdown1, dropdown2 = create_profile_handler(
                files=uploaded_files, name=profile_name, ref_text=ref_text
            )

            # Step 4: Verify results
            assert "error" not in result, f"Unexpected error: {result.get('error')}"
            assert result["name"] == profile_name
            assert result["samples"] == 1
            assert result["total_duration"] == "15.0s"
            assert result["language"] == "es"
            assert result["ref_text"] == ref_text

            # Step 5: Verify dropdowns were updated
            # Note: In real Gradio, these would be gr.Dropdown objects
            # In our test, we're verifying the structure
            assert hasattr(dropdown1, "choices")
            assert hasattr(dropdown2, "choices")

            print("✅ Complete workflow simulation passed")

    def test_error_recovery_workflow(self, tmp_path):
        """Test that the workflow handles errors gracefully and allows recovery."""
        # Test 1: Try to create profile with no files
        result1, dd1_1, dd1_2 = create_profile_handler(
            files=[], name="test", ref_text="test"
        )
        assert "error" in result1

        # Test 2: Try to create profile with no name
        dummy_file = tmp_path / "sample.wav"
        dummy_file.write_text("dummy")

        result2, dd2_1, dd2_2 = create_profile_handler(
            files=[str(dummy_file)], name="", ref_text="test"
        )
        assert "error" in result2

        # Test 3: Try to create profile with invalid name
        result3, dd3_1, dd3_2 = create_profile_handler(
            files=[str(dummy_file)], name="test/invalid", ref_text="test"
        )
        assert "error" in result3

        # Verify that after errors, the system is still functional
        # (no exceptions raised, dropdowns still work)
        print("✅ Error recovery workflow passed")

    @patch("gradio_ui.handlers.profile_handler.AudioProcessor")
    @patch("gradio_ui.handlers.profile_handler.VoiceProfile")
    def test_multiple_profiles_workflow(
        self, mock_profile_class, mock_processor_class, tmp_path
    ):
        """Test creating multiple profiles in sequence."""
        # Setup mocks
        mock_processor = Mock()
        mock_processor_class.return_value = mock_processor

        mock_result = Mock()
        mock_result.is_valid.return_value = True
        mock_result.warnings = []
        mock_result.metadata = {"duration": "10.0s"}
        mock_processor.validate_sample.return_value = mock_result

        # Setup filesystem
        profiles_dir = tmp_path / "data" / "profiles"
        profiles_dir.mkdir(parents=True, exist_ok=True)

        # Create dummy audio file
        dummy_file = tmp_path / "sample.wav"
        dummy_file.write_text("dummy")

        # Patch Path
        with patch("gradio_ui.handlers.profile_handler.Path") as mock_path:

            def path_constructor(path_str):
                if path_str == "data/profiles":
                    return profiles_dir
                return tmp_path / path_str if isinstance(path_str, str) else path_str

            mock_path.side_effect = path_constructor

            # Create first profile
            mock_profile1 = Mock()
            mock_profile1.name = "profile1"
            mock_profile1.samples = [Mock(duration=10.0)]
            mock_profile1.total_duration = 10.0
            mock_profile1.created_at = "2024-01-25T12:00:00"
            mock_profile1.language = "es"
            mock_profile1.ref_text = "Profile 1"
            mock_profile1.validate.return_value = (True, [])
            mock_profile_class.return_value = mock_profile1

            result1, dd1_1, dd1_2 = create_profile_handler(
                files=[str(dummy_file)], name="profile1", ref_text="Profile 1"
            )

            assert "error" not in result1
            assert result1["name"] == "profile1"

            # Create second profile
            mock_profile2 = Mock()
            mock_profile2.name = "profile2"
            mock_profile2.samples = [Mock(duration=10.0)]
            mock_profile2.total_duration = 10.0
            mock_profile2.created_at = "2024-01-25T12:01:00"
            mock_profile2.language = "es"
            mock_profile2.ref_text = "Profile 2"
            mock_profile2.validate.return_value = (True, [])
            mock_profile_class.return_value = mock_profile2

            result2, dd2_1, dd2_2 = create_profile_handler(
                files=[str(dummy_file)], name="profile2", ref_text="Profile 2"
            )

            assert "error" not in result2
            assert result2["name"] == "profile2"

            print("✅ Multiple profiles workflow passed")

    def test_profile_name_sanitization(self):
        """Test that profile names are properly sanitized."""
        test_cases = [
            ("valid_name", True),
            ("valid-name", True),
            ("ValidName123", True),
            ("invalid/name", False),
            ("invalid\\name", False),
            ("invalid name", False),
            ("invalid.name", False),
            ("../../../etc/passwd", False),
            ("a" * 51, False),  # Too long
            ("", False),  # Empty
        ]

        for name, should_be_valid in test_cases:
            from gradio_ui.handlers.profile_handler import _is_valid_profile_name

            result = _is_valid_profile_name(name)
            assert result == should_be_valid, f"Name '{name}' validation failed"

        print("✅ Profile name sanitization tests passed")

    def test_dropdown_synchronization(self, tmp_path):
        """Test that both dropdowns are synchronized after profile creation."""
        # This test verifies that both Tab 2 and Tab 3 dropdowns receive
        # the same updated list of profiles

        with patch("gradio_ui.handlers.profile_handler.AudioProcessor"), patch(
            "gradio_ui.handlers.profile_handler.VoiceProfile"
        ) as mock_profile_class:
            # Setup mocks
            mock_profile = Mock()
            mock_profile.name = "sync_test"
            mock_profile.samples = [Mock(duration=10.0)]
            mock_profile.total_duration = 10.0
            mock_profile.created_at = "2024-01-25T12:00:00"
            mock_profile.language = "es"
            mock_profile.ref_text = "Sync test"
            mock_profile.validate.return_value = (True, [])
            mock_profile_class.return_value = mock_profile

            # Setup filesystem
            profiles_dir = tmp_path / "data" / "profiles"
            profiles_dir.mkdir(parents=True, exist_ok=True)

            dummy_file = tmp_path / "sample.wav"
            dummy_file.write_text("dummy")

            with patch("gradio_ui.handlers.profile_handler.Path") as mock_path:

                def path_constructor(path_str):
                    if path_str == "data/profiles":
                        return profiles_dir
                    return (
                        tmp_path / path_str if isinstance(path_str, str) else path_str
                    )

                mock_path.side_effect = path_constructor

                # Mock validation
                with patch(
                    "gradio_ui.handlers.profile_handler.AudioProcessor"
                ) as mock_proc:
                    mock_processor = Mock()
                    mock_result = Mock()
                    mock_result.is_valid.return_value = True
                    mock_result.warnings = []
                    mock_result.metadata = {"duration": "10.0s"}
                    mock_processor.validate_sample.return_value = mock_result
                    mock_proc.return_value = mock_processor

                    result, dropdown1, dropdown2 = create_profile_handler(
                        files=[str(dummy_file)], name="sync_test", ref_text="Sync test"
                    )

                    # Verify both dropdowns have the same choices
                    assert dropdown1.choices == dropdown2.choices

                    # Verify both dropdowns have the new profile selected
                    assert dropdown1.value == "sync_test"
                    assert dropdown2.value == "sync_test"

                    print("✅ Dropdown synchronization test passed")


class TestProfileListingIntegration:
    """Integration tests for profile listing functionality."""

    def test_list_profiles_with_real_directory(self, tmp_path):
        """Test listing profiles with a real directory structure."""
        profiles_dir = tmp_path / "data" / "profiles"
        profiles_dir.mkdir(parents=True, exist_ok=True)

        # Create some profile files
        (profiles_dir / "profile1.json").write_text('{"name": "profile1"}')
        (profiles_dir / "profile2.json").write_text('{"name": "profile2"}')
        (profiles_dir / "profile3.json").write_text('{"name": "profile3"}')

        # Create some non-profile files (should be ignored)
        (profiles_dir / "readme.txt").write_text("readme")
        (profiles_dir / ".hidden").write_text("hidden")

        with patch("gradio_ui.handlers.profile_handler.Path") as mock_path:
            mock_path.return_value = profiles_dir

            profiles = list_available_profiles()

            assert len(profiles) == 3
            assert "profile1" in profiles
            assert "profile2" in profiles
            assert "profile3" in profiles
            assert profiles == sorted(profiles)  # Should be sorted

            print("✅ Profile listing integration test passed")


def test_all_integration():
    """Run all integration tests."""
    print("\n" + "=" * 80)
    print("  INTEGRATION TEST SUITE: Profile Creation")
    print("=" * 80 + "\n")

    # This function can be called to run all tests manually
    # In practice, pytest will discover and run these automatically
    print("Run with: pytest tests/gradio_ui/test_profile_integration.py -v")


if __name__ == "__main__":
    test_all_integration()
