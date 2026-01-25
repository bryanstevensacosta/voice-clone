# Gradio UI Handlers

This directory contains event handlers that connect the Gradio UI to the backend voice cloning functionality.

## Overview

Handlers act as **adapters** between the Gradio UI layer and the backend business logic. They:

1. **Receive inputs** from Gradio components (files, text, selections)
2. **Validate inputs** at the UI level
3. **Call backend services** (AudioProcessor, VoiceProfile, VoiceGenerator, etc.)
4. **Format outputs** for display (Markdown, JSON, file paths)
5. **Handle errors** gracefully with user-friendly messages

## Architecture

```
Gradio UI Components
        ↓
    Handlers (this directory)
        ↓
Backend Services (voice_clone.*)
```

## Available Handlers

### 1. Sample Handler (`sample_handler.py`)

**Purpose**: Validate uploaded audio samples against Qwen3-TTS requirements.

**Function**: `validate_samples_handler(files: List[str]) -> str`

**Input**: List of file paths from `gr.File` component

**Output**: Markdown-formatted validation results with:
- ✅ for valid samples
- ❌ for invalid samples
- Detailed metadata (duration, sample rate, channels, bit depth)
- Error and warning messages
- Summary statistics

**Example Usage**:
```python
import gradio as gr
from gradio_ui.handlers import validate_samples_handler

with gr.Blocks() as app:
    files = gr.File(file_count="multiple", file_types=[".wav", ".mp3"])
    output = gr.Markdown()
    btn = gr.Button("Validate")

    btn.click(
        fn=validate_samples_handler,
        inputs=[files],
        outputs=[output]
    )
```

**Backend Integration**:
- Uses `AudioProcessor.validate_sample()` from `voice_clone.audio.processor`
- Returns `ValidationResult` with success status, errors, warnings, and metadata

**Error Handling**:
- Empty file list → User-friendly message with requirements
- File not found → Clear error message
- Invalid audio format → Graceful error with suggestion
- Processing errors → Caught and formatted for display

**Testing**: See `tests/gradio_ui/test_sample_handler.py`

---

### 2. Profile Handler (`profile_handler.py`) - TODO

**Purpose**: Create and manage voice profiles.

**Functions**:
- `create_profile_handler()` - Create new voice profile from samples
- `list_available_profiles()` - Get list of existing profiles

---

### 3. Generation Handler (`generation_handler.py`) - TODO

**Purpose**: Generate audio from text using voice profiles.

**Function**: `generate_audio_handler()` - Convert text to speech

---

### 4. Batch Handler (`batch_handler.py`) - TODO

**Purpose**: Process multiple text segments in batch mode.

**Function**: `batch_process_handler()` - Process script file

---

## Design Principles

### 1. Separation of Concerns

**Handlers should NOT**:
- Contain business logic (that's in the backend)
- Directly manipulate files (use backend services)
- Implement audio processing (use AudioProcessor)
- Manage model state (use VoiceGenerator)

**Handlers SHOULD**:
- Validate UI-level inputs (empty strings, null values)
- Transform data formats (Gradio types ↔ backend types)
- Format outputs for display (Markdown, JSON)
- Provide user-friendly error messages

### 2. Error Handling

All handlers follow this pattern:

```python
def handler(input):
    # 1. Validate inputs
    if not input:
        return None, "⚠️ **Please provide input**"

    # 2. Try processing
    try:
        result = backend_service.process(input)
        return result, "✅ **Success!**"

    # 3. Handle specific errors
    except FileNotFoundError as e:
        return None, f"❌ **File not found**: {e.filename}"

    # 4. Handle general errors
    except Exception as e:
        return None, f"❌ **Error**: {str(e)}"
```

### 3. Output Formatting

**Markdown Format** (for display):
- Use `##` for section headers
- Use `###` for subsections
- Use `**bold**` for emphasis
- Use emojis: ✅ ❌ ⚠️ 🎤 📁 🔊
- Use lists for structured data
- Use `---` for separators

**JSON Format** (for structured data):
```python
{
    "name": "profile_name",
    "samples": 3,
    "duration": "45.2s",
    "created_at": "2024-01-25T10:30:00"
}
```

### 4. Type Hints

All handlers use type hints for clarity:

```python
from typing import List, Tuple, Optional, Dict, Any

def handler(
    files: List[str],
    name: str,
    settings: Dict[str, Any]
) -> Tuple[Optional[str], str]:
    """Handler with clear type hints."""
    pass
```

### 5. Documentation

Each handler includes:
- Module docstring explaining purpose
- Function docstring with Args, Returns, Examples
- Inline comments for complex logic
- Error handling documentation

## Testing

### Unit Tests

Each handler has corresponding tests in `tests/gradio_ui/`:

```python
# tests/gradio_ui/test_sample_handler.py
def test_validate_samples_empty():
    """Test with no files."""
    result = validate_samples_handler([])
    assert "No files uploaded" in result

def test_validate_samples_valid():
    """Test with valid sample."""
    result = validate_samples_handler(["/path/to/valid.wav"])
    assert "✅" in result
```

### Integration Tests

Test handlers with actual Gradio components:

```python
def test_handler_integration():
    """Test handler with Gradio app."""
    app = create_app()
    # Test interactions
```

### Manual Testing

Use example scripts in `examples/`:

```bash
python examples/test_validation_handler.py
```

## Adding New Handlers

To add a new handler:

1. **Create handler file**: `src/gradio_ui/handlers/new_handler.py`

2. **Implement handler function**:
```python
def new_handler(input: str) -> str:
    """Handler description.

    Args:
        input: Input description

    Returns:
        Output description
    """
    # Implementation
    pass
```

3. **Export in `__init__.py`**:
```python
from .new_handler import new_handler

__all__ = [
    "validate_samples_handler",
    "new_handler",  # Add here
]
```

4. **Write tests**: `tests/gradio_ui/test_new_handler.py`

5. **Update this README**: Document the new handler

6. **Create example**: `examples/test_new_handler.py`

## Best Practices

### ✅ Do

- Keep handlers simple and focused
- Use backend services for business logic
- Provide clear, actionable error messages
- Format outputs consistently (Markdown/JSON)
- Handle all error cases gracefully
- Write comprehensive tests
- Document with type hints and docstrings

### ❌ Don't

- Put business logic in handlers
- Directly manipulate files or models
- Return raw exceptions to users
- Mix formatting styles
- Ignore error cases
- Skip testing
- Leave code undocumented

## Examples

See `examples/` directory for working examples:

- `test_validation_handler.py` - Sample validation examples
- More examples coming as handlers are implemented

## Resources

- [Gradio Documentation](https://www.gradio.app/docs)
- [Design Document](../../../.kiro/specs/gradio-integration/design.md)
- [Tasks List](../../../.kiro/specs/gradio-integration/tasks.md)
- [Backend API](../../voice_clone/)

---

**Status**: In Progress
**Last Updated**: 2025-01-25
**Maintainer**: Development Team
