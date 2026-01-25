#!/usr/bin/env python3
"""Migrate existing voice profiles to Qwen3-TTS format.

This script updates old voice profiles to include:
- ref_text field (required for Qwen3-TTS)
- sample_rate field (12000 Hz for Qwen3-TTS)
"""

import argparse
import json
import sys
from pathlib import Path


def migrate_profile(input_path: Path, output_path: Path, ref_text: str) -> bool:
    """Migrate a single voice profile.

    Args:
        input_path: Path to old profile JSON
        output_path: Path to save migrated profile
        ref_text: Reference text for voice cloning

    Returns:
        True if successful, False otherwise
    """
    try:
        # Load old profile
        with open(input_path) as f:
            data = json.load(f)

        # Check if already migrated
        if "ref_text" in data and "sample_rate" in data:
            print(f"✓ {input_path.name} already migrated")
            return True

        # Add new fields
        data["ref_text"] = ref_text
        data["sample_rate"] = data.get("sample_rate", 12000)

        # Save migrated profile
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)

        print(f"✓ Migrated {input_path.name} → {output_path.name}")
        return True

    except Exception as e:
        print(f"✗ Failed to migrate {input_path.name}: {e}")
        return False


def migrate_directory(
    profiles_dir: Path, output_dir: Path, ref_text: str, in_place: bool = False
) -> tuple[int, int]:
    """Migrate all profiles in a directory.

    Args:
        profiles_dir: Directory containing profile JSON files
        output_dir: Directory to save migrated profiles
        ref_text: Reference text for voice cloning
        in_place: If True, overwrite original files

    Returns:
        Tuple of (successful_count, failed_count)
    """
    if not profiles_dir.exists():
        print(f"Error: Directory not found: {profiles_dir}")
        return 0, 0

    # Find all JSON files
    profile_files = list(profiles_dir.glob("*.json"))

    if not profile_files:
        print(f"No profile files found in {profiles_dir}")
        return 0, 0

    print(f"Found {len(profile_files)} profile(s) to migrate")
    print(f"Reference text: {ref_text[:50]}..." if len(ref_text) > 50 else ref_text)
    print()

    successful = 0
    failed = 0

    for profile_file in profile_files:
        if in_place:
            output_path = profile_file
        else:
            output_path = output_dir / profile_file.name

        if migrate_profile(profile_file, output_path, ref_text):
            successful += 1
        else:
            failed += 1

    return successful, failed


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Migrate voice profiles to Qwen3-TTS format"
    )
    parser.add_argument(
        "input",
        type=Path,
        help="Input profile file or directory",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output file or directory (default: same as input with _migrated suffix)",
    )
    parser.add_argument(
        "--ref-text",
        type=str,
        required=True,
        help="Reference text (transcript of reference audio)",
    )
    parser.add_argument(
        "--in-place",
        action="store_true",
        help="Overwrite original files (use with caution)",
    )

    args = parser.parse_args()

    # Determine input type
    if args.input.is_file():
        # Single file migration
        if args.output:
            output_path = args.output
        elif args.in_place:
            output_path = args.input
        else:
            output_path = args.input.parent / f"{args.input.stem}_migrated.json"

        success = migrate_profile(args.input, output_path, args.ref_text)
        return 0 if success else 1

    elif args.input.is_dir():
        # Directory migration
        if args.output:
            output_dir = args.output
        elif args.in_place:
            output_dir = args.input
        else:
            output_dir = args.input.parent / f"{args.input.name}_migrated"

        successful, failed = migrate_directory(
            args.input, output_dir, args.ref_text, args.in_place
        )

        print()
        print(f"Migration complete: {successful} successful, {failed} failed")

        return 0 if failed == 0 else 1

    else:
        print(f"Error: {args.input} is not a file or directory")
        return 1


if __name__ == "__main__":
    sys.exit(main())
