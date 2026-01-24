"""Unit tests for VoiceGenerator."""

from typing import Any

from voice_clone.model.generator import VoiceGenerator
from voice_clone.model.manager import ModelManager


def test_voice_generator_initialization() -> None:
    """Test VoiceGenerator initializes with config."""
    config: dict[str, Any] = {
        "model": {},
        "paths": {},
        "generation": {"max_length": 400, "language": "es"},
    }
    model_manager = ModelManager(config)
    generator = VoiceGenerator(model_manager, config)

    assert generator.model_manager == model_manager
    assert generator.config == config
    assert generator.max_chunk_size == 400
    assert generator.language == "es"


def test_chunk_text_short_text() -> None:
    """Test chunking with text shorter than max size."""
    config: dict[str, Any] = {
        "model": {},
        "paths": {},
        "generation": {"max_length": 400},
    }
    model_manager = ModelManager(config)
    generator = VoiceGenerator(model_manager, config)

    text = "This is a short text."
    chunks = generator._chunk_text(text)

    assert len(chunks) == 1
    assert chunks[0] == text


def test_chunk_text_long_text() -> None:
    """Test chunking with text longer than max size."""
    config: dict[str, Any] = {
        "model": {},
        "paths": {},
        "generation": {"max_length": 50},
    }
    model_manager = ModelManager(config)
    generator = VoiceGenerator(model_manager, config)

    text = "This is the first sentence. This is the second sentence. This is the third sentence."
    chunks = generator._chunk_text(text)

    # Should split into multiple chunks
    assert len(chunks) > 1
    # Each chunk should be under max size
    for chunk in chunks:
        assert len(chunk) <= 50 + 30  # Allow some margin for sentence boundaries


def test_chunk_text_at_sentence_boundaries() -> None:
    """Test that chunking respects sentence boundaries."""
    config: dict[str, Any] = {
        "model": {},
        "paths": {},
        "generation": {"max_length": 100},
    }
    model_manager = ModelManager(config)
    generator = VoiceGenerator(model_manager, config)

    text = "First sentence. Second sentence! Third sentence? Fourth sentence."
    chunks = generator._chunk_text(text)

    # Each chunk should end with sentence punctuation
    for chunk in chunks:
        assert chunk.rstrip()[-1] in ".!?"
