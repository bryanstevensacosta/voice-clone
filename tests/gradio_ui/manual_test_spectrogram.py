"""
Manual test for audio spectrogram visualization.

Run this script to test the spectrogram generation functionality.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from gradio_ui.utils.audio_viz import (
    generate_combined_visualization,
    generate_spectrogram,
    generate_waveform,
)


def test_spectrogram_generation():
    """Test spectrogram generation with a sample audio file."""

    # Look for sample audio files
    samples_dir = Path("data/samples")

    if not samples_dir.exists():
        print("❌ No samples directory found at data/samples")
        print("Please create some audio samples first using Tab 1 of the UI")
        return

    # Find first audio file
    audio_files = list(samples_dir.glob("*.wav")) + list(samples_dir.glob("*.mp3"))

    if not audio_files:
        print("❌ No audio files found in data/samples")
        print("Please add some audio samples first")
        return

    audio_file = audio_files[0]
    print(f"📁 Testing with: {audio_file.name}")

    # Test spectrogram generation
    print("\n1️⃣ Testing spectrogram generation...")
    fig_spec = generate_spectrogram(audio_file)
    if fig_spec:
        print("✅ Spectrogram generated successfully")
        output_path = Path("data/outputs/test_spectrogram.png")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig_spec.savefig(output_path, dpi=100, bbox_inches="tight")
        print(f"   Saved to: {output_path}")
    else:
        print("❌ Failed to generate spectrogram")

    # Test waveform generation
    print("\n2️⃣ Testing waveform generation...")
    fig_wave = generate_waveform(audio_file)
    if fig_wave:
        print("✅ Waveform generated successfully")
        output_path = Path("data/outputs/test_waveform.png")
        fig_wave.savefig(output_path, dpi=100, bbox_inches="tight")
        print(f"   Saved to: {output_path}")
    else:
        print("❌ Failed to generate waveform")

    # Test combined visualization
    print("\n3️⃣ Testing combined visualization...")
    fig_combined = generate_combined_visualization(audio_file)
    if fig_combined:
        print("✅ Combined visualization generated successfully")
        output_path = Path("data/outputs/test_combined.png")
        fig_combined.savefig(output_path, dpi=100, bbox_inches="tight")
        print(f"   Saved to: {output_path}")
    else:
        print("❌ Failed to generate combined visualization")

    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("Check data/outputs/ for generated images")
    print("=" * 60)


if __name__ == "__main__":
    test_spectrogram_generation()
