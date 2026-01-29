# UI Guide

> **⚠️ DEPRECATED**: This guide is no longer valid. The Gradio UI has been removed from the project.
>
> **Current Architecture**: The project now uses a **Python API** for the core library, with a **Tauri desktop application** (React + TypeScript + Rust) planned for the UI.
>
> **For API Usage**: See [API Documentation](api.md)
>
> **For Desktop App**: Coming soon in Phase 8 of the project roadmap
>
> **Date Deprecated**: 2026-01-29

---

## Migration Notes

If you were using the Gradio UI, you can now use the Python API directly:

```python
from api.studio import TTSStudio

# Initialize the API
studio = TTSStudio()

# Create a voice profile
result = studio.create_voice_profile(
    name="my_voice",
    sample_paths=["sample1.wav", "sample2.wav"],
    reference_text="This is my voice sample"
)

# Generate audio
result = studio.generate_audio(
    profile_name="my_voice",
    text="Hello, this is a test",
    temperature=0.75,
    speed=1.0
)
```

For more details, see the [API Documentation](api.md).
