"""
Audio visualization utilities for Gradio UI.
"""

from pathlib import Path

import librosa
import librosa.display
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# Use non-interactive backend for server-side rendering
matplotlib.use("Agg")


def generate_spectrogram(
    audio_path: str | Path, figsize: tuple = (10, 4), cmap: str = "viridis"
) -> plt.Figure | None:
    """
    Generate a mel spectrogram visualization from an audio file.

    Args:
        audio_path: Path to the audio file
        figsize: Figure size (width, height) in inches
        cmap: Colormap for the spectrogram

    Returns:
        matplotlib Figure object or None if error
    """
    try:
        # Load audio file
        y, sr = librosa.load(audio_path, sr=None)

        # Compute mel spectrogram
        mel_spec = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)

        # Convert to dB scale
        mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)

        # Create figure
        fig, ax = plt.subplots(figsize=figsize)

        # Display spectrogram
        img = librosa.display.specshow(
            mel_spec_db, x_axis="time", y_axis="mel", sr=sr, fmax=8000, ax=ax, cmap=cmap
        )

        # Add colorbar
        fig.colorbar(img, ax=ax, format="%+2.0f dB")

        # Set title and labels
        ax.set_title("Mel Spectrogram", fontsize=14, fontweight="bold")
        ax.set_xlabel("Time (s)", fontsize=11)
        ax.set_ylabel("Frequency (Hz)", fontsize=11)

        # Tight layout
        plt.tight_layout()

        return fig

    except Exception as e:
        print(f"Error generating spectrogram: {e}")
        return None


def generate_waveform(
    audio_path: str | Path, figsize: tuple = (10, 3)
) -> plt.Figure | None:
    """
    Generate a waveform visualization from an audio file.

    Args:
        audio_path: Path to the audio file
        figsize: Figure size (width, height) in inches

    Returns:
        matplotlib Figure object or None if error
    """
    try:
        # Load audio file
        y, sr = librosa.load(audio_path, sr=None)

        # Create figure
        fig, ax = plt.subplots(figsize=figsize)

        # Display waveform
        librosa.display.waveshow(y, sr=sr, ax=ax, color="#1f77b4")

        # Set title and labels
        ax.set_title("Waveform", fontsize=14, fontweight="bold")
        ax.set_xlabel("Time (s)", fontsize=11)
        ax.set_ylabel("Amplitude", fontsize=11)
        ax.grid(True, alpha=0.3)

        # Tight layout
        plt.tight_layout()

        return fig

    except Exception as e:
        print(f"Error generating waveform: {e}")
        return None


def generate_combined_visualization(
    audio_path: str | Path, figsize: tuple = (10, 8)
) -> plt.Figure | None:
    """
    Generate combined waveform and spectrogram visualization.

    Args:
        audio_path: Path to the audio file
        figsize: Figure size (width, height) in inches

    Returns:
        matplotlib Figure object or None if error
    """
    try:
        # Load audio file
        y, sr = librosa.load(audio_path, sr=None)

        # Create figure with 2 subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize)

        # Plot waveform
        librosa.display.waveshow(y, sr=sr, ax=ax1, color="#1f77b4")
        ax1.set_title("Waveform", fontsize=12, fontweight="bold")
        ax1.set_xlabel("Time (s)", fontsize=10)
        ax1.set_ylabel("Amplitude", fontsize=10)
        ax1.grid(True, alpha=0.3)

        # Compute and plot mel spectrogram
        mel_spec = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)
        mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)

        img = librosa.display.specshow(
            mel_spec_db,
            x_axis="time",
            y_axis="mel",
            sr=sr,
            fmax=8000,
            ax=ax2,
            cmap="viridis",
        )

        ax2.set_title("Mel Spectrogram", fontsize=12, fontweight="bold")
        ax2.set_xlabel("Time (s)", fontsize=10)
        ax2.set_ylabel("Frequency (Hz)", fontsize=10)

        # Add colorbar
        fig.colorbar(img, ax=ax2, format="%+2.0f dB")

        # Tight layout
        plt.tight_layout()

        return fig

    except Exception as e:
        print(f"Error generating combined visualization: {e}")
        return None


def close_figure(fig: plt.Figure | None) -> None:
    """
    Close a matplotlib figure to free memory.

    Args:
        fig: matplotlib Figure object
    """
    if fig is not None:
        plt.close(fig)
