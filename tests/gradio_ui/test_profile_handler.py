"""
Unit tests for profile creation handler.

Tests the create_profile_handler and list_available_profiles functions
with various scenarios including success cases and error handling.
"""

from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

from gradio_ui.handlers.profile_handler import (
    _infer_emotion_from_filename,
    _is_valid_profile_name,
    create_profile_handler,
    list_available_profiles,
)


class TestCreateProfileHandler:
    """Tests for create_profile_handler function."""

    def test_empty_files_list(self):
        """Test handler with empty files list."""
        result, dropdown1, dropdown2 = create_profile_handler(
            files=[], name="test_profile", ref_text="Test reference"
        )

        assert "error" in result
        assert result["error"] == "No audio files uploaded"
        assert dropdown1.choices == []
        assert dropdown2.choices == []

    def test_missing_profile_name(self, tmp_path):
        """Test handler with missing profile name."""
        # Create a dummy file
        dummy_file = tmp_path / "sample.wav"
        dummy_file.write_text("dummy")

        result, dropdown1, dropdown2 = create_profile_handler(
            files=[str(dummy_file)], name="", ref_text="Test reference"
        )

        assert "error" in result
        assert result["error"] == "Profile name required"
        assert dropdown1.choices == []
        assert dropdown2.choices == []

    def test_whitespace_only_profile_name(self, tmp_path):
        """Test handler with whitespace-only profile name."""
        dummy_file = tmp_path / "sample.wav"
        dummy_file.write_text("dummy")

        result, dropdown1, dropdown2 = create_profile_handler(
            files=[str(dummy_file)], name="   ", ref_text="Test reference"
        )

        assert "error" in result
        assert result["error"] == "Profile name required"

    def test_invalid_profile_name_special_chars(self, tmp_path):
        """Test handler with invalid profile name (special characters)."""
        dummy_file = tmp_path / "sample.wav"
        dummy_file.write_text("dummy")

        result, dropdown1, dropdown2 = create_profile_handler(
            files=[str(dummy_file)],
            name="test/profile",  # Contains slash
            ref_text="Test reference",
        )

        assert "error" in result
        assert result["error"] == "Invalid profile name"

    def test_invalid_profile_name_too_long(self, tmp_path):
        """Test handler with profile name that's too long."""
        dummy_file = tmp_path / "sample.wav"
        dummy_file.write_text("dummy")

        result, dropdown1, dropdown2 = create_profile_handler(
            files=[str(dummy_file)],
            name="a" * 51,  # 51 characters (max is 50)
            ref_text="Test reference",
        )

        assert "error" in result
        assert result["error"] == "Invalid profile name"

    @patch("gradio_ui.handlers.profile_handler.AudioProcessor")
    @patch("gradio_ui.handlers.profile_handler.VoiceProfile")
    def test_duplicate_profile_name(
        self, mock_profile_class, mock_processor_class, tmp_path
    ):
        """Test handler with duplicate profile name."""
        # Setup: Create existing profile
        profiles_dir = tmp_path / "data" / "profiles"
        profiles_dir.mkdir(parents=True, exist_ok=True)
        existing_profile = profiles_dir / "test_profile.json"
        existing_profile.write_text('{"name": "test_profile"}')

        # Create dummy file
        dummy_file = tmp_path / "sample.wav"
        dummy_file.write_text("dummy")

        # Patch Path to use tmp_path
        with patch("gradio_ui.handlers.profile_handler.Path") as mock_path:
            # Make Path constructor return appropriate paths
            def path_constructor(path_str):
                if path_str == "data/profiles":
                    return profiles_dir
                return Path(path_str)

            mock_path.side_effect = path_constructor

            result, dropdown1, dropdown2 = create_profile_handler(
                files=[str(dummy_file)], name="test_profile", ref_text="Test reference"
            )

            assert "error" in result
            assert result["error"] == "Profile already exists"

    @patch("gradio_ui.handlers.profile_handler.AudioProcessor")
    @patch("gradio_ui.handlers.profile_handler.VoiceProfile")
    def test_successful_profile_creation(
        self, mock_profile_class, mock_processor_class, tmp_path, monkeypatch
    ):
        """Test successful profile creation."""
        # Setup mocks
        mock_processor = Mock()
        mock_processor_class.return_value = mock_processor

        # Mock validation result
        mock_result = Mock()
        mock_result.is_valid.return_value = True
        mock_result.warnings = []
        mock_result.metadata = {"duration": "10.5s"}
        mock_processor.validate_sample.return_value = mock_result

        # Mock VoiceProfile
        mock_profile = Mock()
        mock_profile.name = "test_profile"
        mock_profile.samples = [Mock(duration=10.5)]
        mock_profile.total_duration = 10.5
        mock_profile.created_at = "2024-01-01T00:00:00"
        mock_profile.language = "es"
        mock_profile.ref_text = "Test reference"
        mock_profile.validate.return_value = (True, [])
        mock_profile_class.return_value = mock_profile

        # Setup filesystem
        profiles_dir = tmp_path / "data" / "profiles"
        profiles_dir.mkdir(parents=True, exist_ok=True)

        # Create dummy audio file
        dummy_file = tmp_path / "sample.wav"
        dummy_file.write_text("dummy")

        # Patch Path to use tmp_path
        with patch("gradio_ui.handlers.profile_handler.Path") as mock_path:
            # Make Path() return paths relative to tmp_path
            def path_constructor(path_str):
                if path_str == "data/profiles":
                    return profiles_dir
                return tmp_path / path_str

            mock_path.side_effect = path_constructor

            # Execute handler
            result, dropdown1, dropdown2 = create_profile_handler(
                files=[str(dummy_file)], name="test_profile", ref_text="Test reference"
            )

            # Verify result
            assert "error" not in result
            assert result["name"] == "test_profile"
            assert result["samples"] == 1
            assert "total_duration" in result
            assert result["language"] == "es"
            assert result["ref_text"] == "Test reference"

    @patch("gradio_ui.handlers.profile_handler.AudioProcessor")
    def test_no_valid_samples(self, mock_processor_class, tmp_path):
        """Test handler when all samples are invalid."""
        # Setup mock
        mock_processor = Mock()
        mock_processor_class.return_value = mock_processor

        # Mock validation result (invalid)
        mock_result = Mock()
        mock_result.is_valid.return_value = False
        mock_processor.validate_sample.return_value = mock_result

        # Create dummy file
        dummy_file = tmp_path / "sample.wav"
        dummy_file.write_text("dummy")

        # Patch Path
        with patch("gradio_ui.handlers.profile_handler.Path") as mock_path:
            profiles_dir = tmp_path / "data" / "profiles"
            profiles_dir.mkdir(parents=True, exist_ok=True)

            def path_constructor(path_str):
                if path_str == "data/profiles":
                    return profiles_dir
                return Path(path_str)

            mock_path.side_effect = path_constructor

            result, dropdown1, dropdown2 = create_profile_handler(
                files=[str(dummy_file)], name="test_profile", ref_text="Test reference"
            )

            assert "error" in result
            assert result["error"] == "No valid audio samples"

    def test_permission_error(self, tmp_path, monkeypatch):
        """Test handler with permission error."""
        # Create dummy file
        dummy_file = tmp_path / "sample.wav"
        dummy_file.write_text("dummy")

        # Mock Path.mkdir to raise PermissionError
        with patch("gradio_ui.handlers.profile_handler.Path") as mock_path:
            mock_profiles_dir = MagicMock()
            mock_profiles_dir.mkdir.side_effect = PermissionError("Permission denied")
            mock_profiles_dir.exists.return_value = False
            mock_profiles_dir.__truediv__.return_value.exists.return_value = False

            def path_constructor(path_str):
                if path_str == "data/profiles":
                    return mock_profiles_dir
                return Path(path_str)

            mock_path.side_effect = path_constructor

            result, dropdown1, dropdown2 = create_profile_handler(
                files=[str(dummy_file)], name="test_profile", ref_text="Test reference"
            )

            assert "error" in result
            assert result["error"] == "Permission denied"


class TestListAvailableProfiles:
    """Tests for list_available_profiles function."""

    def test_empty_directory(self, tmp_path, monkeypatch):
        """Test with empty profiles directory."""
        profiles_dir = tmp_path / "data" / "profiles"
        profiles_dir.mkdir(parents=True, exist_ok=True)

        with patch("gradio_ui.handlers.profile_handler.Path") as mock_path:
            mock_path.return_value = profiles_dir
            result = list_available_profiles()

            assert result == []

    def test_nonexistent_directory(self):
        """Test with nonexistent profiles directory."""
        with patch("gradio_ui.handlers.profile_handler.Path") as mock_path:
            mock_dir = MagicMock()
            mock_dir.exists.return_value = False
            mock_path.return_value = mock_dir

            result = list_available_profiles()

            assert result == []

    def test_multiple_profiles(self, tmp_path):
        """Test with multiple profile files."""
        profiles_dir = tmp_path / "data" / "profiles"
        profiles_dir.mkdir(parents=True, exist_ok=True)

        # Create profile files
        (profiles_dir / "profile1.json").write_text("{}")
        (profiles_dir / "profile2.json").write_text("{}")
        (profiles_dir / "profile3.json").write_text("{}")

        with patch("gradio_ui.handlers.profile_handler.Path") as mock_path:
            mock_path.return_value = profiles_dir
            result = list_available_profiles()

            assert len(result) == 3
            assert "profile1" in result
            assert "profile2" in result
            assert "profile3" in result
            assert result == sorted(result)  # Should be sorted

    def test_ignores_non_json_files(self, tmp_path):
        """Test that non-JSON files are ignored."""
        profiles_dir = tmp_path / "data" / "profiles"
        profiles_dir.mkdir(parents=True, exist_ok=True)

        # Create various files
        (profiles_dir / "profile1.json").write_text("{}")
        (profiles_dir / "readme.txt").write_text("readme")
        (profiles_dir / "config.yaml").write_text("config")

        with patch("gradio_ui.handlers.profile_handler.Path") as mock_path:
            mock_path.return_value = profiles_dir
            result = list_available_profiles()

            assert len(result) == 1
            assert result == ["profile1"]


class TestIsValidProfileName:
    """Tests for _is_valid_profile_name helper function."""

    def test_valid_names(self):
        """Test valid profile names."""
        assert _is_valid_profile_name("test_profile") is True
        assert _is_valid_profile_name("test-profile") is True
        assert _is_valid_profile_name("TestProfile123") is True
        assert _is_valid_profile_name("my_voice_2024") is True
        assert _is_valid_profile_name("a") is True

    def test_invalid_names(self):
        """Test invalid profile names."""
        assert _is_valid_profile_name("") is False
        assert _is_valid_profile_name("test/profile") is False
        assert _is_valid_profile_name("test profile") is False  # Space
        assert _is_valid_profile_name("test.profile") is False  # Dot
        assert _is_valid_profile_name("test@profile") is False  # Special char
        assert _is_valid_profile_name("a" * 51) is False  # Too long

    def test_path_traversal_prevention(self):
        """Test that path traversal attempts are blocked."""
        assert _is_valid_profile_name("../profile") is False
        assert _is_valid_profile_name("..\\profile") is False
        assert _is_valid_profile_name("../../etc/passwd") is False


class TestInferEmotionFromFilename:
    """Tests for _infer_emotion_from_filename helper function."""

    def test_happy_emotion(self):
        """Test happy emotion inference."""
        assert _infer_emotion_from_filename("happy_01") == "happy"
        assert _infer_emotion_from_filename("excited_voice") == "happy"
        assert _infer_emotion_from_filename("HAPPY_SAMPLE") == "happy"

    def test_sad_emotion(self):
        """Test sad emotion inference."""
        assert _infer_emotion_from_filename("sad_01") == "sad"
        assert _infer_emotion_from_filename("SAD_VOICE") == "sad"

    def test_angry_emotion(self):
        """Test angry emotion inference."""
        assert _infer_emotion_from_filename("angry_01") == "angry"
        assert _infer_emotion_from_filename("ANGRY_SAMPLE") == "angry"

    def test_calm_emotion(self):
        """Test calm emotion inference."""
        assert _infer_emotion_from_filename("calm_01") == "calm"
        assert _infer_emotion_from_filename("relaxed_voice") == "calm"

    def test_serious_emotion(self):
        """Test serious emotion inference."""
        assert _infer_emotion_from_filename("serious_01") == "serious"
        assert _infer_emotion_from_filename("professional_voice") == "serious"

    def test_neutral_default(self):
        """Test neutral as default emotion."""
        assert _infer_emotion_from_filename("sample_01") == "neutral"
        assert _infer_emotion_from_filename("voice_recording") == "neutral"
        assert _infer_emotion_from_filename("test") == "neutral"


class TestIntegration:
    """Integration tests for profile creation workflow."""

    @patch("gradio_ui.handlers.profile_handler.AudioProcessor")
    @patch("gradio_ui.handlers.profile_handler.VoiceProfile")
    def test_full_workflow_with_multiple_samples(
        self, mock_profile_class, mock_processor_class, tmp_path
    ):
        """Test complete workflow with multiple audio samples."""
        # Setup mocks
        mock_processor = Mock()
        mock_processor_class.return_value = mock_processor

        # Mock validation results for 3 samples
        mock_results = []
        for i in range(3):
            mock_result = Mock()
            mock_result.is_valid.return_value = True
            mock_result.warnings = []
            mock_result.metadata = {"duration": f"{10 + i}.0s"}
            mock_results.append(mock_result)

        mock_processor.validate_sample.side_effect = mock_results

        # Mock VoiceProfile
        mock_profile = Mock()
        mock_profile.name = "multi_sample_profile"
        mock_profile.samples = [
            Mock(duration=10.0),
            Mock(duration=11.0),
            Mock(duration=12.0),
        ]
        mock_profile.total_duration = 33.0
        mock_profile.created_at = "2024-01-01T00:00:00"
        mock_profile.language = "es"
        mock_profile.ref_text = "Multiple samples test"
        mock_profile.validate.return_value = (True, [])
        mock_profile_class.return_value = mock_profile

        # Setup filesystem
        profiles_dir = tmp_path / "data" / "profiles"
        profiles_dir.mkdir(parents=True, exist_ok=True)

        # Create dummy audio files
        dummy_files = []
        for i in range(3):
            dummy_file = tmp_path / f"sample_{i}.wav"
            dummy_file.write_text(f"dummy{i}")
            dummy_files.append(str(dummy_file))

        # Patch Path
        with patch("gradio_ui.handlers.profile_handler.Path") as mock_path:

            def path_constructor(path_str):
                if path_str == "data/profiles":
                    return profiles_dir
                return tmp_path / path_str if isinstance(path_str, str) else path_str

            mock_path.side_effect = path_constructor

            result, dropdown1, dropdown2 = create_profile_handler(
                files=dummy_files,
                name="multi_sample_profile",
                ref_text="Multiple samples test",
            )

            # Verify result
            assert "error" not in result
            assert result["name"] == "multi_sample_profile"
            assert result["samples"] == 3
            assert result["total_duration"] == "33.0s"
