"""Unit tests for Qwen3Generator."""

from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from voice_clone.model.qwen3_generator import Qwen3Generator
from voice_clone.model.qwen3_manager import Qwen3ModelManager


class TestQwen3GeneratorInitialization:
    """Test Qwen3Generator initialization."""

    def test_initialization_with_config(self) -> None:
        """Test Qwen3Generator initializes with config."""
        config: dict[str, Any] = {
            "model": {},
            "paths": {},
            "generation": {
                "max_length": 400,
                "language": "Spanish",
                "max_new_tokens": 2048,
            },
        }

        manager = Qwen3ModelManager(config)
        generator = Qwen3Generator(manager, config)

        assert generator.model_manager == manager
        assert generator.config == config
        assert generator.max_chunk_size == 400
        assert generator.language == "Spanish"
        assert generator.max_new_tokens == 2048

    def test_initialization_with_default_values(self) -> None:
        """Test initialization uses default values when not in config."""
        config: dict[str, Any] = {"model": {}, "paths": {}}

        manager = Qwen3ModelManager(config)
        generator = Qwen3Generator(manager, config)

        assert generator.max_chunk_size == 400  # Default
        assert generator.language == "Spanish"  # Default
        assert generator.max_new_tokens == 2048  # Default


class TestTextChunking:
    """Test text chunking functionality."""

    def test_chunk_text_short_text(self) -> None:
        """Test that short text is not chunked."""
        config: dict[str, Any] = {"model": {}, "paths": {}}
        manager = Qwen3ModelManager(config)
        generator = Qwen3Generator(manager, config)

        text = "This is a short text."
        chunks = generator._chunk_text(text)

        assert len(chunks) == 1
        assert chunks[0] == text

    def test_chunk_text_long_text(self) -> None:
        """Test that long text is chunked at sentence boundaries."""
        config: dict[str, Any] = {
            "model": {},
            "paths": {},
            "generation": {"max_length": 50},
        }
        manager = Qwen3ModelManager(config)
        generator = Qwen3Generator(manager, config)

        text = (
            "This is the first sentence. This is the second sentence. "
            "This is the third sentence. This is the fourth sentence."
        )
        chunks = generator._chunk_text(text)

        assert len(chunks) > 1
        # Each chunk should be under max_length
        for chunk in chunks:
            assert len(chunk) <= 50 or " " not in chunk  # Allow single long words

    def test_chunk_text_preserves_content(self) -> None:
        """Test that chunking preserves all content."""
        config: dict[str, Any] = {
            "model": {},
            "paths": {},
            "generation": {"max_length": 50},
        }
        manager = Qwen3ModelManager(config)
        generator = Qwen3Generator(manager, config)

        text = "First sentence. Second sentence. Third sentence."
        chunks = generator._chunk_text(text)

        # Joining chunks should give back original text (approximately)
        joined = " ".join(chunks)
        # Remove extra spaces for comparison
        assert text.replace("  ", " ") in joined or joined in text


class TestGenerate:
    """Test audio generation functionality."""

    def test_generate_success(self) -> None:
        """Test successful audio generation."""
        config: dict[str, Any] = {"model": {}, "paths": {}}
        manager = Qwen3ModelManager(config)
        generator = Qwen3Generator(manager, config)

        # Mock model
        mock_model = MagicMock()
        mock_audio = np.array([0.1, 0.2, 0.3])
        mock_sample_rate = 12000
        mock_model.generate_voice_clone.return_value = (mock_audio, mock_sample_rate)

        manager.model = mock_model

        result = generator.generate(
            text="Test text",
            ref_audio="ref.wav",
            ref_text="Reference text",
        )

        assert result is not None
        audio, sample_rate = result
        assert isinstance(audio, np.ndarray)
        assert sample_rate == 12000
        mock_model.generate_voice_clone.assert_called_once()

    def test_generate_with_custom_parameters(self) -> None:
        """Test generation with custom language and max_new_tokens."""
        config: dict[str, Any] = {"model": {}, "paths": {}}
        manager = Qwen3ModelManager(config)
        generator = Qwen3Generator(manager, config)

        mock_model = MagicMock()
        mock_audio = np.array([0.1, 0.2, 0.3])
        mock_sample_rate = 12000
        mock_model.generate_voice_clone.return_value = (mock_audio, mock_sample_rate)

        manager.model = mock_model

        result = generator.generate(
            text="Test text",
            ref_audio="ref.wav",
            ref_text="Reference text",
            language="English",
            max_new_tokens=1024,
        )

        assert result is not None
        # Verify custom parameters were passed
        call_args = mock_model.generate_voice_clone.call_args
        assert call_args[1]["language"] == "English"
        assert call_args[1]["max_new_tokens"] == 1024

    def test_generate_model_not_loaded(self) -> None:
        """Test generation fails gracefully when model not loaded."""
        config: dict[str, Any] = {"model": {}, "paths": {}}
        manager = Qwen3ModelManager(config)
        generator = Qwen3Generator(manager, config)

        # Model not loaded
        result = generator.generate(
            text="Test text",
            ref_audio="ref.wav",
            ref_text="Reference text",
        )

        assert result is None

    def test_generate_exception_handling(self) -> None:
        """Test generation handles exceptions gracefully."""
        config: dict[str, Any] = {"model": {}, "paths": {}}
        manager = Qwen3ModelManager(config)
        generator = Qwen3Generator(manager, config)

        mock_model = MagicMock()
        mock_model.generate_voice_clone.side_effect = RuntimeError("Generation failed")

        manager.model = mock_model

        result = generator.generate(
            text="Test text",
            ref_audio="ref.wav",
            ref_text="Reference text",
        )

        assert result is None

    def test_generate_with_path_object(self) -> None:
        """Test generation accepts Path objects for ref_audio."""
        config: dict[str, Any] = {"model": {}, "paths": {}}
        manager = Qwen3ModelManager(config)
        generator = Qwen3Generator(manager, config)

        mock_model = MagicMock()
        mock_audio = np.array([0.1, 0.2, 0.3])
        mock_sample_rate = 12000
        mock_model.generate_voice_clone.return_value = (mock_audio, mock_sample_rate)

        manager.model = mock_model

        result = generator.generate(
            text="Test text",
            ref_audio=Path("ref.wav"),
            ref_text="Reference text",
        )

        assert result is not None
        # Verify Path was converted to string
        call_args = mock_model.generate_voice_clone.call_args
        assert isinstance(call_args[1]["ref_audio"], str)


class TestGenerateBatch:
    """Test batch generation functionality."""

    def test_generate_batch_success(self) -> None:
        """Test successful batch generation."""
        config: dict[str, Any] = {"model": {}, "paths": {}}
        manager = Qwen3ModelManager(config)
        generator = Qwen3Generator(manager, config)

        mock_model = MagicMock()
        mock_audio = np.array([0.1, 0.2, 0.3])
        mock_sample_rate = 12000
        mock_model.generate_voice_clone.return_value = (mock_audio, mock_sample_rate)

        manager.model = mock_model

        texts = ["Text 1", "Text 2", "Text 3"]
        results = generator.generate_batch(
            texts=texts,
            ref_audio="ref.wav",
            ref_text="Reference text",
        )

        assert len(results) == 3
        for audio, sample_rate in results:
            assert isinstance(audio, np.ndarray)
            assert sample_rate == 12000

        # Verify generate_voice_clone was called 3 times
        assert mock_model.generate_voice_clone.call_count == 3

    def test_generate_batch_partial_failure(self) -> None:
        """Test batch generation continues on partial failures."""
        config: dict[str, Any] = {"model": {}, "paths": {}}
        manager = Qwen3ModelManager(config)
        generator = Qwen3Generator(manager, config)

        mock_model = MagicMock()
        mock_audio = np.array([0.1, 0.2, 0.3])
        mock_sample_rate = 12000

        # First call succeeds, second fails, third succeeds
        mock_model.generate_voice_clone.side_effect = [
            (mock_audio, mock_sample_rate),
            RuntimeError("Failed"),
            (mock_audio, mock_sample_rate),
        ]

        manager.model = mock_model

        texts = ["Text 1", "Text 2", "Text 3"]
        results = generator.generate_batch(
            texts=texts,
            ref_audio="ref.wav",
            ref_text="Reference text",
        )

        # Should have 2 successful results (1st and 3rd)
        assert len(results) == 2

    def test_generate_batch_empty_list(self) -> None:
        """Test batch generation with empty list."""
        config: dict[str, Any] = {"model": {}, "paths": {}}
        manager = Qwen3ModelManager(config)
        generator = Qwen3Generator(manager, config)

        results = generator.generate_batch(
            texts=[],
            ref_audio="ref.wav",
            ref_text="Reference text",
        )

        assert len(results) == 0


class TestGenerateToFile:
    """Test file generation functionality."""

    def test_generate_to_file_success(self, tmp_path: Path) -> None:
        """Test successful generation to file."""
        config: dict[str, Any] = {"model": {}, "paths": {}}
        manager = Qwen3ModelManager(config)
        generator = Qwen3Generator(manager, config)

        mock_model = MagicMock()
        mock_audio = np.array([0.1, 0.2, 0.3])
        mock_sample_rate = 12000
        mock_model.generate_voice_clone.return_value = (mock_audio, mock_sample_rate)

        manager.model = mock_model

        # Create a temporary reference audio file
        ref_audio = tmp_path / "ref.wav"
        ref_audio.touch()

        output_path = tmp_path / "output.wav"

        with patch("soundfile.write"):
            result = generator.generate_to_file(
                text="Test text",
                ref_audio=str(ref_audio),
                ref_text="Reference text",
                output_path=output_path,
            )

            assert result is True

    def test_generate_to_file_empty_text(self, tmp_path: Path) -> None:
        """Test generation fails with empty text."""
        config: dict[str, Any] = {"model": {}, "paths": {}}
        manager = Qwen3ModelManager(config)
        generator = Qwen3Generator(manager, config)

        manager.model = MagicMock()

        ref_audio = tmp_path / "ref.wav"
        ref_audio.touch()

        output_path = tmp_path / "output.wav"

        result = generator.generate_to_file(
            text="",
            ref_audio=str(ref_audio),
            ref_text="Reference text",
            output_path=output_path,
        )

        assert result is False

    def test_generate_to_file_missing_ref_audio(self, tmp_path: Path) -> None:
        """Test generation fails when reference audio doesn't exist."""
        config: dict[str, Any] = {"model": {}, "paths": {}}
        manager = Qwen3ModelManager(config)
        generator = Qwen3Generator(manager, config)

        manager.model = MagicMock()

        output_path = tmp_path / "output.wav"

        result = generator.generate_to_file(
            text="Test text",
            ref_audio="nonexistent.wav",
            ref_text="Reference text",
            output_path=output_path,
        )

        assert result is False

    def test_generate_to_file_empty_ref_text(self, tmp_path: Path) -> None:
        """Test generation fails with empty reference text."""
        config: dict[str, Any] = {"model": {}, "paths": {}}
        manager = Qwen3ModelManager(config)
        generator = Qwen3Generator(manager, config)

        manager.model = MagicMock()

        ref_audio = tmp_path / "ref.wav"
        ref_audio.touch()

        output_path = tmp_path / "output.wav"

        result = generator.generate_to_file(
            text="Test text",
            ref_audio=str(ref_audio),
            ref_text="",
            output_path=output_path,
        )

        assert result is False

    def test_generate_to_file_model_not_loaded(self, tmp_path: Path) -> None:
        """Test generation fails when model not loaded."""
        config: dict[str, Any] = {"model": {}, "paths": {}}
        manager = Qwen3ModelManager(config)
        generator = Qwen3Generator(manager, config)

        # Model not loaded

        ref_audio = tmp_path / "ref.wav"
        ref_audio.touch()

        output_path = tmp_path / "output.wav"

        result = generator.generate_to_file(
            text="Test text",
            ref_audio=str(ref_audio),
            ref_text="Reference text",
            output_path=output_path,
        )

        assert result is False

    def test_generate_to_file_creates_parent_directory(self, tmp_path: Path) -> None:
        """Test that parent directories are created if they don't exist."""
        config: dict[str, Any] = {"model": {}, "paths": {}}
        manager = Qwen3ModelManager(config)
        generator = Qwen3Generator(manager, config)

        mock_model = MagicMock()
        mock_audio = np.array([0.1, 0.2, 0.3])
        mock_sample_rate = 12000
        mock_model.generate_voice_clone.return_value = (mock_audio, mock_sample_rate)

        manager.model = mock_model

        ref_audio = tmp_path / "ref.wav"
        ref_audio.touch()

        # Output path with non-existent parent directory
        output_path = tmp_path / "subdir" / "output.wav"

        with patch("soundfile.write"):
            result = generator.generate_to_file(
                text="Test text",
                ref_audio=str(ref_audio),
                ref_text="Reference text",
                output_path=output_path,
            )

            assert result is True
            assert output_path.parent.exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
