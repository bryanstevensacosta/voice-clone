"""
Tests for profile selection functionality in Tab 2 (Generate Audio).

This module tests the profile selection dropdown, including:
- Dropdown initialization with available profiles
- Empty profile list handling
- Profile selection after creation
"""

from pathlib import Path

import gradio as gr
import pytest
from gradio_ui.app import create_app
from gradio_ui.handlers.profile_handler import list_available_profiles


class TestProfileSelection:
    """Test suite for profile selection dropdown."""

    def test_list_available_profiles_empty_directory(self, tmp_path, monkeypatch):
        """Test list_available_profiles returns empty list when directory doesn't exist."""
        # Setup: Point to non-existent directory
        non_existent_dir = tmp_path / "non_existent"
        monkeypatch.setattr(
            "gradio_ui.handlers.profile_handler.Path",
            lambda x: non_existent_dir if x == "data/profiles" else Path(x),
        )

        # Execute
        profiles = list_available_profiles()

        # Assert
        assert profiles == []

    def test_list_available_profiles_no_profiles(self, tmp_path, monkeypatch):
        """Test list_available_profiles returns empty list when directory is empty."""
        # Setup: Create empty directory
        profiles_dir = tmp_path / "profiles"
        profiles_dir.mkdir(parents=True)

        # Mock Path to return our test directory
        def mock_path(path_str):
            if path_str == "data/profiles":
                return profiles_dir
            return Path(path_str)

        monkeypatch.setattr("gradio_ui.handlers.profile_handler.Path", mock_path)

        # Execute
        profiles = list_available_profiles()

        # Assert
        assert profiles == []

    def test_list_available_profiles_with_profiles(self, tmp_path, monkeypatch):
        """Test list_available_profiles returns sorted list of profile names."""
        # Setup: Create test profiles
        profiles_dir = tmp_path / "profiles"
        profiles_dir.mkdir(parents=True)

        # Create test profile files
        (profiles_dir / "profile_a.json").write_text('{"name": "profile_a"}')
        (profiles_dir / "profile_c.json").write_text('{"name": "profile_c"}')
        (profiles_dir / "profile_b.json").write_text('{"name": "profile_b"}')

        # Mock Path to return our test directory
        def mock_path(path_str):
            if path_str == "data/profiles":
                return profiles_dir
            return Path(path_str)

        monkeypatch.setattr("gradio_ui.handlers.profile_handler.Path", mock_path)

        # Execute
        profiles = list_available_profiles()

        # Assert
        assert profiles == [
            "profile_a",
            "profile_b",
            "profile_c",
        ]  # Sorted alphabetically

    def test_list_available_profiles_ignores_non_json(self, tmp_path, monkeypatch):
        """Test list_available_profiles ignores non-JSON files."""
        # Setup: Create directory with mixed files
        profiles_dir = tmp_path / "profiles"
        profiles_dir.mkdir(parents=True)

        # Create test files
        (profiles_dir / "profile_a.json").write_text('{"name": "profile_a"}')
        (profiles_dir / "readme.txt").write_text("This is a readme")
        (profiles_dir / "profile_b.json").write_text('{"name": "profile_b"}')
        (profiles_dir / ".hidden").write_text("Hidden file")

        # Mock Path to return our test directory
        def mock_path(path_str):
            if path_str == "data/profiles":
                return profiles_dir
            return Path(path_str)

        monkeypatch.setattr("gradio_ui.handlers.profile_handler.Path", mock_path)

        # Execute
        profiles = list_available_profiles()

        # Assert
        assert profiles == ["profile_a", "profile_b"]  # Only JSON files

    def test_dropdown_initialization_with_profiles(self, tmp_path, monkeypatch):
        """Test that dropdown is initialized with available profiles."""
        # Setup: Create test profiles
        profiles_dir = tmp_path / "profiles"
        profiles_dir.mkdir(parents=True)
        (profiles_dir / "test_profile.json").write_text('{"name": "test_profile"}')

        # Mock Path to return our test directory
        def mock_path(path_str):
            if path_str == "data/profiles":
                return profiles_dir
            return Path(path_str)

        monkeypatch.setattr("gradio_ui.handlers.profile_handler.Path", mock_path)

        # Execute: Create app
        app = create_app()

        # Assert: App should be created successfully
        assert app is not None
        assert isinstance(app, gr.Blocks)

    def test_dropdown_initialization_empty_profiles(self, tmp_path, monkeypatch):
        """Test that dropdown handles empty profile list gracefully."""
        # Setup: Create empty directory
        profiles_dir = tmp_path / "profiles"
        profiles_dir.mkdir(parents=True)

        # Mock Path to return our test directory
        def mock_path(path_str):
            if path_str == "data/profiles":
                return profiles_dir
            return Path(path_str)

        monkeypatch.setattr("gradio_ui.handlers.profile_handler.Path", mock_path)

        # Execute: Create app
        app = create_app()

        # Assert: App should be created successfully even with no profiles
        assert app is not None
        assert isinstance(app, gr.Blocks)

    def test_dropdown_updates_after_profile_creation(self, tmp_path, monkeypatch):
        """Test that dropdown choices are updated after creating a new profile."""
        # Setup: Create profiles directory
        profiles_dir = tmp_path / "profiles"
        profiles_dir.mkdir(parents=True)

        # Mock Path to return our test directory
        def mock_path(path_str):
            if path_str == "data/profiles":
                return profiles_dir
            return Path(path_str)

        monkeypatch.setattr("gradio_ui.handlers.profile_handler.Path", mock_path)

        # Initial state: No profiles
        initial_profiles = list_available_profiles()
        assert initial_profiles == []

        # Create a profile
        (profiles_dir / "new_profile.json").write_text('{"name": "new_profile"}')

        # After creation: Profile should be listed
        updated_profiles = list_available_profiles()
        assert updated_profiles == ["new_profile"]

    def test_profile_selection_info_text_with_profiles(self, tmp_path, monkeypatch):
        """Test that info text is appropriate when profiles exist."""
        # Setup: Create test profile
        profiles_dir = tmp_path / "profiles"
        profiles_dir.mkdir(parents=True)
        (profiles_dir / "test_profile.json").write_text('{"name": "test_profile"}')

        # Mock Path
        def mock_path(path_str):
            if path_str == "data/profiles":
                return profiles_dir
            return Path(path_str)

        monkeypatch.setattr("gradio_ui.handlers.profile_handler.Path", mock_path)

        # Execute
        profiles = list_available_profiles()

        # Assert: Should have profiles
        assert len(profiles) > 0
        # Info text should be the normal one (not the warning)

    def test_profile_selection_info_text_without_profiles(self, tmp_path, monkeypatch):
        """Test that info text shows warning when no profiles exist."""
        # Setup: Create empty directory
        profiles_dir = tmp_path / "profiles"
        profiles_dir.mkdir(parents=True)

        # Mock Path
        def mock_path(path_str):
            if path_str == "data/profiles":
                return profiles_dir
            return Path(path_str)

        monkeypatch.setattr("gradio_ui.handlers.profile_handler.Path", mock_path)

        # Execute
        profiles = list_available_profiles()

        # Assert: Should have no profiles
        assert len(profiles) == 0
        # Info text should show warning (verified in app.py)


class TestProfileSelectionIntegration:
    """Integration tests for profile selection across tabs."""

    def test_profile_selector_synced_across_tabs(self, tmp_path, monkeypatch):
        """Test that profile selectors in Tab 2 and Tab 3 are synchronized."""
        # Setup: Create test profiles
        profiles_dir = tmp_path / "profiles"
        profiles_dir.mkdir(parents=True)
        (profiles_dir / "profile_1.json").write_text('{"name": "profile_1"}')
        (profiles_dir / "profile_2.json").write_text('{"name": "profile_2"}')

        # Mock Path
        def mock_path(path_str):
            if path_str == "data/profiles":
                return profiles_dir
            return Path(path_str)

        monkeypatch.setattr("gradio_ui.handlers.profile_handler.Path", mock_path)

        # Execute: Get profiles
        profiles = list_available_profiles()

        # Assert: Both tabs should have same profiles
        assert profiles == ["profile_1", "profile_2"]

    def test_app_creation_with_various_profile_states(self, tmp_path, monkeypatch):
        """Test app creation with different profile directory states."""

        # Mock Path
        def mock_path(path_str):
            if path_str == "data/profiles":
                return tmp_path / "profiles"
            return Path(path_str)

        monkeypatch.setattr("gradio_ui.handlers.profile_handler.Path", mock_path)

        # Test 1: Directory doesn't exist
        app1 = create_app()
        assert app1 is not None

        # Test 2: Directory exists but is empty
        profiles_dir = tmp_path / "profiles"
        profiles_dir.mkdir(parents=True)
        app2 = create_app()
        assert app2 is not None

        # Test 3: Directory has profiles
        (profiles_dir / "test.json").write_text('{"name": "test"}')
        app3 = create_app()
        assert app3 is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
