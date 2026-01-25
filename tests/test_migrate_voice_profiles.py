"""Tests for voice profile migration script."""

import json
import subprocess
import sys
from pathlib import Path

import pytest


class TestMigrateVoiceProfiles:
    """Test voice profile migration script."""

    def test_migrate_single_profile(self, tmp_path: Path) -> None:
        """Test migrating a single profile file."""
        # Create old profile without ref_text
        old_profile = {
            "name": "test_profile",
            "created_at": "2024-01-01T00:00:00",
            "language": "es",
            "total_duration": 60.0,
            "samples": [
                {
                    "path": "sample1.wav",
                    "duration": 10.0,
                    "emotion": "neutral",
                    "quality_score": 1.0,
                }
            ],
        }

        input_path = tmp_path / "old_profile.json"
        with open(input_path, "w") as f:
            json.dump(old_profile, f)

        output_path = tmp_path / "migrated_profile.json"

        # Run migration script
        result = subprocess.run(
            [
                sys.executable,
                "scripts/migrate_voice_profiles.py",
                str(input_path),
                "--output",
                str(output_path),
                "--ref-text",
                "This is the reference text",
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert output_path.exists()

        # Verify migrated profile
        with open(output_path) as f:
            migrated = json.load(f)

        assert "ref_text" in migrated
        assert migrated["ref_text"] == "This is the reference text"
        assert "sample_rate" in migrated
        assert migrated["sample_rate"] == 12000

    def test_migrate_directory(self, tmp_path: Path) -> None:
        """Test migrating a directory of profiles."""
        # Create directory with multiple profiles
        profiles_dir = tmp_path / "profiles"
        profiles_dir.mkdir()

        for i in range(3):
            profile = {
                "name": f"profile_{i}",
                "created_at": "2024-01-01T00:00:00",
                "language": "es",
                "total_duration": 60.0,
                "samples": [],
            }

            profile_path = profiles_dir / f"profile_{i}.json"
            with open(profile_path, "w") as f:
                json.dump(profile, f)

        output_dir = tmp_path / "migrated"

        # Run migration script
        result = subprocess.run(
            [
                sys.executable,
                "scripts/migrate_voice_profiles.py",
                str(profiles_dir),
                "--output",
                str(output_dir),
                "--ref-text",
                "Reference text for all profiles",
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert output_dir.exists()

        # Verify all profiles were migrated
        migrated_files = list(output_dir.glob("*.json"))
        assert len(migrated_files) == 3

        for migrated_file in migrated_files:
            with open(migrated_file) as f:
                migrated = json.load(f)

            assert "ref_text" in migrated
            assert migrated["ref_text"] == "Reference text for all profiles"
            assert "sample_rate" in migrated

    def test_migrate_already_migrated_profile(self, tmp_path: Path) -> None:
        """Test that already migrated profiles are skipped."""
        # Create already migrated profile
        migrated_profile = {
            "name": "test_profile",
            "created_at": "2024-01-01T00:00:00",
            "language": "es",
            "total_duration": 60.0,
            "ref_text": "Already has ref_text",
            "sample_rate": 12000,
            "samples": [],
        }

        input_path = tmp_path / "migrated_profile.json"
        with open(input_path, "w") as f:
            json.dump(migrated_profile, f)

        output_path = tmp_path / "output_profile.json"

        # Run migration script
        result = subprocess.run(
            [
                sys.executable,
                "scripts/migrate_voice_profiles.py",
                str(input_path),
                "--output",
                str(output_path),
                "--ref-text",
                "New ref text",
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "already migrated" in result.stdout

    def test_migrate_in_place(self, tmp_path: Path) -> None:
        """Test in-place migration (overwriting original files)."""
        # Create old profile
        old_profile = {
            "name": "test_profile",
            "created_at": "2024-01-01T00:00:00",
            "language": "es",
            "total_duration": 60.0,
            "samples": [],
        }

        profile_path = tmp_path / "profile.json"
        with open(profile_path, "w") as f:
            json.dump(old_profile, f)

        # Run migration script with --in-place
        result = subprocess.run(
            [
                sys.executable,
                "scripts/migrate_voice_profiles.py",
                str(profile_path),
                "--ref-text",
                "In-place migration",
                "--in-place",
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0

        # Verify original file was updated
        with open(profile_path) as f:
            migrated = json.load(f)

        assert "ref_text" in migrated
        assert migrated["ref_text"] == "In-place migration"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
