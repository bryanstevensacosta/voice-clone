# Qwen3-TTS Setup and Testing Guide

## Quick Start

### 1. Installation

```bash
# Run the automated setup script
bash scripts/setup_qwen3_tts.sh
```

This script will:
- Install `qwen-tts` package
- Optionally install `flash-attention` for better GPU performance
- Create necessary directories
- Optionally pre-download models

### 2. Manual Installation

If you prefer manual installation:

```bash
# Activate your virtual environment
source venv/bin/activate

# Install qwen-tts
pip install -U qwen-tts

# Optional: Install flash-attention (for NVIDIA GPUs)
# On systems with <96GB RAM:
MAX_JOBS=4 pip install -U flash-attn --no-build-isolation

# Or skip if you don't have compatible hardware
```

---

## Testing Qwen3-TTS

### Test Voice Cloning

```bash
# Test voice cloning with your reference samples
python scripts/test_qwen3_tts.py --mode clone
```

**Requirements:**
- Reference audio in `data/samples/` directory
- Update `ref_text` variable in script with actual transcript

### Test Custom Speakers

```bash
# Test with predefined speakers (no reference needed)
python scripts/test_qwen3_tts.py --mode custom
```

Available speakers:
- **Vivian** - Bright, slightly edgy young female voice (Chinese)
- **Serena** - Warm, gentle young female voice (Chinese)
- **Ryan** - Dynamic male voice with strong rhythmic drive (English)
- **Aiden** - Sunny American male voice (English)
- And 5 more...

### Test Both

```bash
# Run all tests
python scripts/test_qwen3_tts.py --mode both
```

---

## Comparing XTTS-v2 vs Qwen3-TTS

### Run Comparison

```bash
# Compare both models side-by-side
python scripts/compare_tts_models.py
```

This will:
1. Load both XTTS-v2 and Qwen3-TTS models
2. Generate audio for the same test cases
3. Measure performance (speed, quality)
4. Save results to `data/comparison_results/`

### Expected Output

```
📊 Performance Comparison
════════════════════════════════════════════════════════════════════════════════
Test Case          XTTS-v2 Time  Qwen3-TTS Time  XTTS Speed  Qwen3 Speed  Winner
────────────────────────────────────────────────────────────────────────────────
neutral_short            3.45s           2.89s       0.87x        1.04x   Qwen3
neutral_medium           8.23s           7.12s       0.73x        0.84x   Qwen3
question                 4.12s           3.67s       0.92x        1.03x   Qwen3
technical                9.45s           8.34s       0.63x        0.71x   Qwen3
numbers                  5.67s           4.89s       0.79x        0.92x   Qwen3
────────────────────────────────────────────────────────────────────────────────

Average Generation Time:
  XTTS-v2:   6.18s
  Qwen3-TTS: 5.38s
  → Qwen3-TTS is 1.15x faster
```

---

## Model Options

### Available Models

Qwen3-TTS offers multiple models for different use cases:

#### Base Models (Voice Cloning)
```python
# Smaller, faster (600MB)
"Qwen/Qwen3-TTS-12Hz-0.6B-Base"

# Larger, better quality (1.7GB) - Recommended
"Qwen/Qwen3-TTS-12Hz-1.7B-Base"
```

#### CustomVoice Models (Predefined Speakers)
```python
# With 9 premium speakers
"Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice"
"Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice"
```

#### VoiceDesign Model (Text-to-Voice)
```python
# Create voices from text descriptions
"Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign"
```

### Choosing a Model

**For voice cloning (like XTTS-v2):**
- Use `Qwen3-TTS-12Hz-1.7B-Base`
- Similar size to XTTS-v2
- Best quality

**For faster generation:**
- Use `Qwen3-TTS-12Hz-0.6B-Base`
- 3x smaller
- Still good quality

**For predefined speakers:**
- Use `Qwen3-TTS-12Hz-1.7B-CustomVoice`
- No reference audio needed
- 9 high-quality voices

---

## Python API Examples

### Basic Voice Cloning

```python
import torch
import soundfile as sf
from qwen_tts import Qwen3TTSModel

# Load model
model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-Base",
    device_map="cuda:0",  # or "mps" for Apple Silicon, "cpu" for CPU
    dtype=torch.bfloat16,  # or torch.float32 for MPS/CPU
)

# Generate with voice clone
wavs, sr = model.generate_voice_clone(
    text="Hola, esta es una prueba de mi voz clonada.",
    language="Spanish",
    ref_audio="data/samples/sample_01.wav",
    ref_text="Transcripción del audio de referencia",
    max_new_tokens=2048,
)

# Save output
sf.write("output.wav", wavs[0], sr)
```

### Batch Processing

```python
# Generate multiple texts at once
texts = [
    "Primera oración.",
    "Segunda oración.",
    "Tercera oración.",
]

wavs, sr = model.generate_voice_clone(
    text=texts,
    language=["Spanish"] * len(texts),
    ref_audio="data/samples/sample_01.wav",
    ref_text="Transcripción",
)

# Save each output
for i, wav in enumerate(wavs):
    sf.write(f"output_{i}.wav", wav, sr)
```

### Reusable Voice Prompts (Efficient)

```python
# Create prompt once
prompt = model.create_voice_clone_prompt(
    ref_audio="data/samples/sample_01.wav",
    ref_text="Transcripción",
)

# Reuse for multiple generations (faster!)
for i, text in enumerate(texts):
    wavs, sr = model.generate_voice_clone(
        text=text,
        language="Spanish",
        voice_clone_prompt=prompt,  # Reuse!
    )
    sf.write(f"output_{i}.wav", wavs[0], sr)
```

### Custom Speakers

```python
# Load CustomVoice model
model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice",
    device_map="cuda:0",
    dtype=torch.bfloat16,
)

# Generate with predefined speaker
wavs, sr = model.generate_custom_voice(
    text="Hello, welcome to this tutorial!",
    language="English",
    speaker="ryan",  # or "serena", "vivian", etc.
    instruct="Speak in a cheerful and energetic tone",  # Optional
)

sf.write("output_ryan.wav", wavs[0], sr)
```

### Voice Design (Text-to-Voice)

```python
# Load VoiceDesign model
model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign",
    device_map="cuda:0",
    dtype=torch.bfloat16,
)

# Create voice from description
wavs, sr = model.generate_voice_design(
    text="Hola, ¿cómo estás?",
    language="Spanish",
    instruct="Voz femenina joven, alegre y energética, con tono cálido",
)

sf.write("output_designed.wav", wavs[0], sr)
```

---

## Hardware Optimization

### NVIDIA GPU (CUDA)

```python
model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-Base",
    device_map="cuda:0",
    dtype=torch.bfloat16,
    attn_implementation="flash_attention_2",  # If installed
)
```

### Apple Silicon (M1/M2/M3)

```python
model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-Base",
    device_map="mps",
    dtype=torch.float32,  # MPS doesn't support bfloat16 well
)
```

### CPU Only

```python
model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-Base",
    device_map="cpu",
    dtype=torch.float32,
)
```

---

## Troubleshooting

### Issue: qwen-tts not found

```bash
# Solution
pip install qwen-tts
```

### Issue: Flash Attention installation fails

```bash
# Solution 1: Install with limited jobs
MAX_JOBS=4 pip install flash-attn --no-build-isolation

# Solution 2: Skip flash attention (optional)
# Model will work without it, just slightly slower
```

### Issue: Out of memory

```bash
# Solution 1: Use smaller model
model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-0.6B-Base",  # Smaller
    device_map="cuda:0",
)

# Solution 2: Use CPU
model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-Base",
    device_map="cpu",
)
```

### Issue: Poor voice cloning quality

```python
# Solution 1: Provide accurate transcript
wavs, sr = model.generate_voice_clone(
    text="...",
    ref_audio="ref.wav",
    ref_text="Exact transcript of ref.wav",  # Important!
    x_vector_only_mode=False,
)

# Solution 2: Use longer reference (6-10s)
# Solution 3: Use cleaner reference audio
```

### Issue: Slow on Apple Silicon

```python
# Ensure using MPS
import torch

device = "mps" if torch.backends.mps.is_available() else "cpu"
model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-Base",
    device_map=device,
    dtype=torch.float32,  # Important for MPS
)
```

---

## Next Steps

1. **Run setup:**
   ```bash
   bash scripts/setup_qwen3_tts.sh
   ```

2. **Test voice cloning:**
   ```bash
   python scripts/test_qwen3_tts.py --mode clone
   ```

3. **Compare with XTTS-v2:**
   ```bash
   python scripts/compare_tts_models.py
   ```

4. **Evaluate results:**
   - Listen to generated audio
   - Compare quality
   - Compare speed
   - Decide which model to use

5. **Read full comparison:**
   - See `docs/QWEN_VS_XTTS_COMPARISON.md` (Spanish)
   - Detailed feature comparison
   - Benchmarks and recommendations

---

## Resources

- [Qwen3-TTS HuggingFace](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-Base)
- [Qwen3-TTS GitHub](https://github.com/QwenLM/Qwen3-TTS)
- [Qwen3-TTS Technical Report](https://arxiv.org/abs/2601.15621)
- [Python Package Documentation](https://pypi.org/project/qwen-tts/)

---

**Last Updated**: January 2025
