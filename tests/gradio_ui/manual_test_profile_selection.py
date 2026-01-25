"""
Manual test script for profile selection functionality.

This script launches the Gradio UI and allows manual testing of:
1. Profile selection dropdown in Tab 2
2. Profile selection dropdown in Tab 3
3. Empty profile list handling
4. Profile selection after creation

Run this script and test the following scenarios:
- Initial state with no profiles (should show warning message)
- Create a profile in Tab 1
- Verify dropdowns in Tab 2 and Tab 3 update with new profile
- Select profile in Tab 2 and Tab 3
"""

import sys
from pathlib import Path

from gradio_ui.app import create_app

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))  # noqa: E402


def main():
    """Launch the Gradio UI for manual testing."""
    print("=" * 80)
    print("Manual Test: Profile Selection")
    print("=" * 80)
    print()
    print("Test Scenarios:")
    print("1. Check Tab 2 - Profile dropdown should show available profiles")
    print("2. Check Tab 3 - Profile dropdown should show same profiles")
    print("3. If no profiles exist, info text should show warning")
    print("4. Create a profile in Tab 1")
    print("5. Verify dropdowns in Tab 2 and Tab 3 update automatically")
    print("6. Select a profile in Tab 2 dropdown")
    print("7. Select a profile in Tab 3 dropdown")
    print()
    print("=" * 80)
    print()

    # Create and launch app
    app = create_app()
    app.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        show_error=True,
    )


if __name__ == "__main__":
    main()
