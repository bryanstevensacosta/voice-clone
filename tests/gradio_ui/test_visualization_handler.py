"""
Unit tests for audio visualization handler.
"""

import tempfile
from pathlib import Path

import numpy as np
import pytest
import soundfile as sf

from gradio_ui.handlers.visualization_handler import (
    cleanup_figures,
    generate_all_spectrograms,
    generate_sample_visualization,
)


@pytest.fixture
def temp_audio_file():
    """Create a temporary audio file for testing."""
    # Generate 1 second of sine wave at 440 Hz
    sample_rate = 12000
    duration = 1.0
    frequency = 440.0

    t = np.linspace(0, duration, int(sample_rate * duration))
    audio_data = np.sin(2 * np.pi * frequency * t)

    # Create temporary file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        temp_path = Path(f.name)
        sf.write(temp_path, audio_data, sample_rate)

    yield str(temp_path)

    # Cleanup
    if temp_path.exists():
        temp_path.unlink()


class TestGenerateSampleVisualization:
    """Tests for generate_sample_visualization function."""

    def test_empty_file_list(self):
        """Test with empty file list."""
        result = generate_sample_visualization([])
        assert result is None

    def test_nonexistent_file(self):
        """Test with nonexistent file."""
        result = generate_sample_visualization(["/nonexistent/file.wav"])
        assert result is None

    def test_valid_audio_file_combined(self, temp_audio_file):
        """Test with valid audio file - combined visualization."""
        result = generate_sample_visualization([temp_audio_file], viz_type="combined")
        assert result is not None
        # Cleanup
        if result:
            import matplotlib.pyplot as plt

            plt.close(result)

    def test_valid_audio_file_spectrogram(self, temp_audio_file):
        """Test with valid audio file - spectrogram only."""
        result = generate_sample_visualization(
            [temp_audio_file], viz_type="spectrogram"
        )
        assert result is not None
        # Cleanup
        if result:
            import matplotlib.pyplot as plt

            plt.close(result)

    def test_valid_audio_file_waveform(self, temp_audio_file):
        """Test with valid audio file - waveform only."""
        result = generate_sample_visualization([temp_audio_file], viz_type="waveform")
        assert result is not None
        # Cleanup
        if result:
            import matplotlib.pyplot as plt

            plt.close(result)

    def test_multiple_files_uses_first(self, temp_audio_file):
        """Test that only first file is visualized when multiple provided."""
        result = generate_sample_visualization(
            [temp_audio_file, temp_audio_file], viz_type="waveform"
        )
        assert result is not None
        # Cleanup
        if result:
            import matplotlib.pyplot as plt

            plt.close(result)


class TestGenerateAllSpectrograms:
    """Tests for generate_all_spectrograms function."""

    def test_empty_file_list(self):
        """Test with empty file list."""
        result = generate_all_spectrograms([])
        assert result == []

    def test_nonexistent_files(self):
        """Test with nonexistent files."""
        result = generate_all_spectrograms(
            ["/nonexistent/file1.wav", "/nonexistent/file2.wav"]
        )
        assert result == []

    def test_valid_audio_files(self, temp_audio_file):
        """Test with valid audio files."""
        result = generate_all_spectrograms([temp_audio_file])
        assert len(result) == 1
        assert result[0] is not None
        # Cleanup
        cleanup_figures(result)

    def test_mixed_valid_invalid_files(self, temp_audio_file):
        """Test with mix of valid and invalid files."""
        result = generate_all_spectrograms([temp_audio_file, "/nonexistent/file.wav"])
        assert len(result) == 1
        # Cleanup
        cleanup_figures(result)


class TestCleanupFigures:
    """Tests for cleanup_figures function."""

    def test_cleanup_empty_list(self):
        """Test cleanup with empty list."""
        # Should not raise any errors
        cleanup_figures([])

    def test_cleanup_valid_figures(self, temp_audio_file):
        """Test cleanup with valid figures."""
        figures = generate_all_spectrograms([temp_audio_file])
        assert len(figures) > 0

        # Cleanup should not raise errors
        cleanup_figures(figures)

    def test_cleanup_none_in_list(self):
        """Test cleanup with None values in list."""
        # Should handle None gracefully
        cleanup_figures([None, None])


class TestIntegration:
    """Integration tests for visualization workflow."""

    def test_full_workflow(self, temp_audio_file):
        """Test complete workflow: generate -> use -> cleanup."""
        # Generate visualization
        fig = generate_sample_visualization([temp_audio_file])
        assert fig is not None

        # Simulate using the figure (e.g., displaying in Gradio)
        # In real usage, Gradio would handle the figure

        # Cleanup
        import matplotlib.pyplot as plt

        plt.close(fig)

    def test_multiple_generations(self, temp_audio_file):
        """Test generating multiple visualizations."""
        figs = []

        # Generate multiple times
        for _ in range(3):
            fig = generate_sample_visualization([temp_audio_file])
            assert fig is not None
            figs.append(fig)

        # Cleanup all
        import matplotlib.pyplot as plt

        for fig in figs:
            plt.close(fig)
