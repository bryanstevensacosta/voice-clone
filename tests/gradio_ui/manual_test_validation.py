"""
Manual test script for validation UI.

This script launches the Gradio UI so you can manually test:
1. Upload valid samples and click "Validate Samples"
2. Upload invalid samples and click "Validate Samples"
3. Click "Validate Samples" without uploading files

Run this script and open http://localhost:7860 in your browser.
"""

from gradio_ui.app import main

if __name__ == "__main__":
    print("=" * 80)
    print("MANUAL TEST: Validation UI")
    print("=" * 80)
    print()
    print("Instructions:")
    print("1. Open http://localhost:7860 in your browser")
    print("2. Go to Tab 1: 'Prepare Voice Profile'")
    print("3. Test the following scenarios:")
    print()
    print("   Scenario 1: Valid samples")
    print("   - Upload 1-2 files from data/samples/")
    print("   - Click 'Validate Samples'")
    print("   - Expected: Green checkmarks (✅) with metadata")
    print()
    print("   Scenario 2: No files")
    print("   - Don't upload any files")
    print("   - Click 'Validate Samples'")
    print("   - Expected: Warning message (⚠️)")
    print()
    print("   Scenario 3: Invalid file")
    print("   - Upload a non-audio file (e.g., .txt, .jpg)")
    print("   - Click 'Validate Samples'")
    print("   - Expected: Error message (❌)")
    print()
    print("=" * 80)
    print()

    # Launch the app
    main(server_port=7860, share=False)
