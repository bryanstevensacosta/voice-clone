"""Unit tests for BatchProcessor."""

import tempfile
from pathlib import Path
from typing import Any

from voice_clone.audio.processor import AudioProcessor
from voice_clone.batch.processor import BatchProcessor
from voice_clone.model.generator import VoiceGenerator
from voice_clone.model.manager import ModelManager


def test_batch_processor_initialization() -> None:
    """Test BatchProcessor initializes correctly."""
    config: dict[str, Any] = {"model": {}, "paths": {}, "generation": {}}
    model_manager = ModelManager(config)
    generator = VoiceGenerator(model_manager, config)
    processor = AudioProcessor()

    batch_processor = BatchProcessor(generator, processor)

    assert batch_processor.voice_generator == generator
    assert batch_processor.audio_processor == processor


def test_parse_script_with_markers() -> None:
    """Test parsing script with multiple markers."""
    config: dict[str, Any] = {"model": {}, "paths": {}, "generation": {}}
    model_manager = ModelManager(config)
    generator = VoiceGenerator(model_manager, config)
    processor = AudioProcessor()
    batch_processor = BatchProcessor(generator, processor)

    # Create test script
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write(
            """[INTRO]
This is the introduction text.

[SECTION_1]
This is section one content.

[OUTRO]
This is the outro text.
"""
        )
        script_path = Path(f.name)

    try:
        segments = batch_processor._parse_script(script_path)

        assert len(segments) == 3
        assert segments[0].marker == "INTRO"
        assert segments[0].text == "This is the introduction text."
        assert segments[0].output_filename == "intro.wav"

        assert segments[1].marker == "SECTION_1"
        assert segments[1].text == "This is section one content."
        assert segments[1].output_filename == "section_1.wav"

        assert segments[2].marker == "OUTRO"
        assert segments[2].text == "This is the outro text."
        assert segments[2].output_filename == "outro.wav"

    finally:
        script_path.unlink(missing_ok=True)


def test_parse_script_empty_segments() -> None:
    """Test parsing script ignores empty segments."""
    config: dict[str, Any] = {"model": {}, "paths": {}, "generation": {}}
    model_manager = ModelManager(config)
    generator = VoiceGenerator(model_manager, config)
    processor = AudioProcessor()
    batch_processor = BatchProcessor(generator, processor)

    # Create test script - empty segments are filtered out by the code
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write(
            "[INTRO]\nThis is the introduction text.\n\n[OUTRO]\nThis is the outro text.\n"
        )
        script_path = Path(f.name)

    try:
        segments = batch_processor._parse_script(script_path)

        # Should have 2 segments
        assert len(segments) == 2
        assert segments[0].marker == "INTRO"
        assert segments[1].marker == "OUTRO"

    finally:
        script_path.unlink(missing_ok=True)


def test_parse_script_no_markers() -> None:
    """Test parsing script with no markers returns empty list."""
    config: dict[str, Any] = {"model": {}, "paths": {}, "generation": {}}
    model_manager = ModelManager(config)
    generator = VoiceGenerator(model_manager, config)
    processor = AudioProcessor()
    batch_processor = BatchProcessor(generator, processor)

    # Create test script without markers
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write("This is just plain text without markers.")
        script_path = Path(f.name)

    try:
        segments = batch_processor._parse_script(script_path)

        assert len(segments) == 0

    finally:
        script_path.unlink(missing_ok=True)
