# Generating Audio

Learn how to generate speech from text using voice profiles.

## Basic Generation

```python
from api.studio import TTSStudio

studio = TTSStudio()

# Generate speech from text
result = studio.generate_audio(
    profile_id="my_voice",
    text="Hola, esta es una prueba de mi voz clonada.",
    output_path="./data/outputs/output.wav"
)

if result["status"] == "success":
    print(f"✓ Audio generated: {result['output_path']}")
    print(f"  Duration: {result['duration']}s")
else:
    print(f"✗ Error: {result['error']}")
```

## Generation Options

```python
# Generate with all options
result = studio.generate_audio(
    profile_id="my_voice",
    text="Hola, ¿cómo estás?",
    output_path="./data/outputs/output.wav",
    temperature=0.75,  # Sampling temperature (0.5-1.0)
    speed=1.0,  # Speaking speed multiplier (0.8-1.2)
    language="es",  # Language code
    mode="clone"  # Generation mode
)
```

**Parameters**:
- `profile_id`: ID of the voice profile to use (required)
- `text`: Text to convert to speech (required)
- `output_path`: Path to save audio (auto-generated if None)
- `temperature`: Sampling temperature (0.5-1.0, default: 0.75)
- `speed`: Speaking speed multiplier (0.8-1.2, default: 1.0)
- `language`: Language code (default: from config)
- `mode`: Generation mode (default: "clone")

## Temperature and Speed

**Temperature** controls synthesis randomness:
- Lower (0.5-0.6): More consistent, less expressive
- Medium (0.7-0.8): Balanced, natural-sounding (recommended)
- Higher (0.9-1.0): More varied, potentially less stable

**Speed** controls speech rate:
- Slower (0.8-0.9): Clearer, more deliberate
- Normal (1.0): Natural pace
- Faster (1.1-1.2): Quicker, may reduce clarity

## Batch Processing

Process multiple texts:

```python
texts = [
    "Hola, esta es la primera oración.",
    "Esta es la segunda oración.",
    "Y esta es la tercera."
]

# Generate each text
for i, text in enumerate(texts):
    result = studio.generate_audio(
        profile_id="my_voice",
        text=text,
        output_path=f"./data/outputs/output_{i:03d}.wav"
    )

    if result["status"] == "success":
        print(f"✓ Generated {i+1}/{len(texts)}")
    else:
        print(f"✗ Error {i+1}/{len(texts)}: {result['error']}")
```

## Best Practices

### For Speech Generation
- Start with default parameters (temperature=0.75, speed=1.0)
- Use temperature 0.7-0.8 for balanced results
- Keep text length reasonable (<500 characters per generation)
- Test different speeds for optimal clarity
- Use appropriate language code

### Text Formatting
- Use proper punctuation for natural pauses
- Break long texts into shorter segments
- Include question marks for questions
- Use ellipsis (...) for longer pauses

## Troubleshooting

### Voice Sounds Robotic
- Add more samples with emotional variety
- Ensure samples are high quality and natural
- Try adjusting temperature (0.7-0.9)
- Record samples with natural expression

### Slow Processing
- Enable GPU support (MPS for M1/M2, CUDA for NVIDIA)
- First generation is slower (model loading)
- Process shorter text segments
- Check device configuration in config.yaml

## Next Steps

- [Batch Processing](04-batch-processing.md) - Process multiple segments
- [Post-Processing](05-post-processing.md) - Enhance generated audio
- [API Reference](../04-api-reference/01-python-api.md) - Explore the full API
