"""
Audio visualization handler for Gradio UI.

This module provides handlers for generating audio visualizations
(spectrograms, waveforms) from uploaded samples.
"""

from pathlib import Path

import matplotlib.pyplot as plt

from gradio_ui.utils.audio_viz import (
    close_figure,
    generate_combined_visualization,
    generate_spectrogram,
    generate_waveform,
)


def generate_sample_visualization(
    files: list[str], viz_type: str = "combined"
) -> plt.Figure | None:
    """
    Generate visualization for the first uploaded audio sample.

    Args:
        files: List of file paths from Gradio File component
        viz_type: Type of visualization:
                  - "spectrogram": Mel spectrogram only
                  - "waveform": Waveform only
                  - "combined": Both waveform and spectrogram (default)

    Returns:
        matplotlib Figure object or None if no files or error
    """
    # Handle empty file list
    if not files:
        return None

    # Get first file
    file_path = Path(files[0])

    # Check if file exists
    if not file_path.exists():
        return None

    try:
        # Generate visualization based on type
        if viz_type == "spectrogram":
            fig = generate_spectrogram(file_path)
        elif viz_type == "waveform":
            fig = generate_waveform(file_path)
        else:  # combined
            fig = generate_combined_visualization(file_path)

        return fig

    except Exception as e:
        print(f"Error generating visualization: {e}")
        return None


def generate_all_spectrograms(files: list[str]) -> list[plt.Figure]:
    """
    Generate spectrograms for all uploaded audio samples.

    Args:
        files: List of file paths from Gradio File component

    Returns:
        List of matplotlib Figure objects (one per file)
    """
    figures = []

    for file_path in files:
        path = Path(file_path)

        if not path.exists():
            continue

        try:
            fig = generate_spectrogram(path)
            if fig is not None:
                figures.append(fig)
        except Exception as e:
            print(f"Error generating spectrogram for {path.name}: {e}")
            continue

    return figures


def cleanup_figures(figures: list[plt.Figure]) -> None:
    """
    Close all matplotlib figures to free memory.

    Args:
        figures: List of matplotlib Figure objects
    """
    for fig in figures:
        close_figure(fig)
