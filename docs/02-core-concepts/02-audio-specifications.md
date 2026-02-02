---
inclusion: always
---

# Audio Specifications - Technical Reference

## Quick Reference Card

```
Qwen3-TTS Native Format:
├── Sample Rate: 12000 Hz
├── Channels: Mono (1)
├── Bit Depth: 16-bit
├── Format: WAV (PCM)
└── Language: Spanish

Optimal Input Samples:
├── Duration: 3-30 seconds each
├── Total: 1-3 samples recommended
├── Quality: Clean, no background noise
└── Variety: Different emotions/tones

Generation Limits:
├── Max text length: ~2048 tokens (optimal)
├── Max audio length: No hard limit (chunking recommended)
├── Memory usage: ~4-6GB during inference
└── Generation speed: ~15-25s per minute (M1 Pro)
```

---

## Supported Formats

### Input Formats (Reference Samples)

#### Recommended (Native)
```bash
WAV (PCM)
├── Sample Rate: 12000 Hz
├── Channels: Mono
├── Bit Depth: 16-bit
└── Codec: PCM uncompressed
```

#### Accepted (Will be converted)
```bash
# El sistema puede aceptar y convertir automáticamente:
- WAV (cualquier sample rate)
- MP3 (será convertido a WAV)
- M4A/AAC (será convertido a WAV)
- FLAC (será convertido a WAV)
- OGG (será convertido a WAV)

# Conversión automática a formato nativo
Input → Resample to 12000Hz → Convert to Mono → 16-bit PCM
```

### Output Formats (Generated Audio)

#### Default Output
```bash
WAV (PCM)
├── Sample Rate: 12000 Hz
├── Channels: Mono
├── Bit Depth: 16-bit
└── Size: ~1.4 MB per minute
```

#### Optional Exports
```bash
# Configurables via CLI flags
--format wav     # Default, sin compresión
--format mp3     # Comprimido, ~1 MB/min
--format m4a     # AAC, mejor para video
--format flac    # Lossless compression
```

---

## Sample Rates

### Qwen3-TTS Native: 12000 Hz
```bash
# Por qué 12000 Hz?
- Óptimo para voz humana (rango 80-6000 Hz)
- Balance entre calidad y tamaño
- Nativo del modelo (no requiere resampling)
- Suficiente para YouTube/TikTok

# Nyquist frequency: 6000 Hz
# Cubre todo el rango de voz humana
```

### Comparison Table
```
Sample Rate | Quality      | Use Case              | File Size
------------|--------------|----------------------|------------
8000 Hz     | Teléfono     | Llamadas             | Pequeño
12000 Hz    | Buena (Qwen3)| YouTube, TikTok      | Óptimo ✓
16000 Hz    | Aceptable    | Podcasts básicos     | Mediano
22050 Hz    | Muy buena    | Audio profesional    | Grande
44100 Hz    | CD Quality   | Música, audio pro    | Muy grande
48000 Hz    | Professional | Video production     | Muy grande
```

### When to Use Different Sample Rates

#### Stick with 12000 Hz (Recommended)
```bash
✓ Narración de videos
✓ Tutoriales
✓ Podcasts
✓ Contenido de redes sociales
✓ Audiolibros
```

#### Consider 44100 Hz (Advanced)
```bash
# Solo si necesitas:
- Mezclar con música de alta calidad
- Post-procesamiento extenso
- Distribución en plataformas de audio premium

# Nota: Requiere upsampling después de generación
ffmpeg -i input_12k.wav -ar 44100 output_44k.wav
```

---

## Bit Depth

### 16-bit (Standard)
```bash
# Qwen3-TTS native
Bit Depth: 16-bit
Dynamic Range: 96 dB
Quality: Más que suficiente para voz
Size: 1.4 MB per minute (12000 Hz, mono)
```

### Comparison
```
Bit Depth | Dynamic Range | Use Case           | Recommended
----------|---------------|--------------------|--------------
8-bit     | 48 dB        | Retro/Lo-fi        | ❌
16-bit    | 96 dB        | Voz, podcasts      | ✓ (Qwen3)
24-bit    | 144 dB       | Música pro         | ❌ (overkill)
32-bit    | 192 dB       | Mastering          | ❌ (overkill)
```

### Why 16-bit is Enough
- Rango dinámico de voz humana: ~40-60 dB
- 16-bit provee 96 dB (mucho margen)
- Archivos más pequeños
- Compatible con todos los editores

---

## Channels (Mono vs Stereo)

### Mono (Required for Qwen3-TTS)
```bash
Channels: 1 (Mono)
Reason: Modelo entrenado con mono
Size: 1.4 MB per minute (12000 Hz, 16-bit)
```

### Converting Stereo to Mono
```bash
# FFmpeg: Mix stereo to mono
ffmpeg -i stereo.wav -ac 1 mono.wav

# FFmpeg: Use only left channel
ffmpeg -i stereo.wav -map_channel 0.0.0 mono.wav

# FFmpeg: Use only right channel
ffmpeg -i stereo.wav -map_channel 0.0.1 mono.wav

# SoX: Mix stereo to mono
sox stereo.wav mono.wav channels 1
```

### When to Convert to Stereo (Post-Production)
```bash
# Después de generación, para mezclar con música stereo
ffmpeg -i mono_voice.wav -ac 2 stereo_voice.wav

# Nota: No mejora calidad, solo compatibilidad
```

---

## Format Conversions

### Common Conversions (FFmpeg)

#### WAV to MP3
```bash
# High quality (320 kbps)
ffmpeg -i input.wav -codec:a libmp3lame -b:a 320k output.mp3

# Good quality (192 kbps) - Recommended
ffmpeg -i input.wav -codec:a libmp3lame -b:a 192k output.mp3

# Variable bitrate (V0 = highest VBR)
ffmpeg -i input.wav -codec:a libmp3lame -qscale:a 0 output.mp3
```

#### WAV to AAC/M4A (Best for Video)
```bash
# High quality AAC
ffmpeg -i input.wav -codec:a aac -b:a 192k output.m4a

# Variable bitrate AAC
ffmpeg -i input.wav -codec:a aac -vbr 5 output.m4a

# For Final Cut Pro / iMovie
ffmpeg -i input.wav -codec:a aac -b:a 256k -ar 48000 output.m4a
```

#### WAV to FLAC (Lossless)
```bash
# Lossless compression (~50% size reduction)
ffmpeg -i input.wav -codec:a flac output.flac

# With compression level (0-12, 5 is default)
ffmpeg -i input.wav -codec:a flac -compression_level 8 output.flac
```

#### MP3/M4A to WAV (for Qwen3-TTS input)
```bash
# Convert to Qwen3-TTS native format
ffmpeg -i input.mp3 -ar 12000 -ac 1 -sample_fmt s16 output.wav

# From M4A
ffmpeg -i input.m4a -ar 12000 -ac 1 -sample_fmt s16 output.wav

# From any format (auto-detect)
ffmpeg -i input.* -ar 12000 -ac 1 -sample_fmt s16 output.wav
```

### Batch Conversions

#### Convert all MP3 to WAV
```bash
for file in *.mp3; do
  ffmpeg -i "$file" -ar 12000 -ac 1 -sample_fmt s16 "${file%.mp3}.wav"
done
```

#### Convert all WAV to M4A
```bash
for file in *.wav; do
  ffmpeg -i "$file" -codec:a aac -b:a 192k "${file%.wav}.m4a"
done
```

#### Normalize and convert
```bash
for file in *.wav; do
  ffmpeg -i "$file" \
    -af "loudnorm=I=-16:TP=-1.5:LRA=11" \
    -codec:a aac -b:a 192k \
    "normalized/${file%.wav}.m4a"
done
```

---

## Audio Processing Commands

### Normalization (Loudness)

#### EBU R128 Loudness Normalization (Recommended)
```bash
# Standard for broadcast (-16 LUFS)
ffmpeg -i input.wav -af "loudnorm=I=-16:TP=-1.5:LRA=11" output.wav

# For YouTube (-14 LUFS)
ffmpeg -i input.wav -af "loudnorm=I=-14:TP=-1:LRA=11" output.wav

# For podcasts (-19 LUFS)
ffmpeg -i input.wav -af "loudnorm=I=-19:TP=-2:LRA=11" output.wav
```

#### Peak Normalization (Simple)
```bash
# Normalize to 0 dB peak
ffmpeg -i input.wav -af "volume=0dB" output.wav

# Normalize to -3 dB peak (safer)
ffmpeg -i input.wav -af "volume=-3dB" output.wav
```

### Fade In/Out

#### Basic Fade
```bash
# Fade in: 0.5s, Fade out: 1s
ffmpeg -i input.wav -af "afade=t=in:st=0:d=0.5,afade=t=out:st=9:d=1" output.wav

# Variables
# t=in|out (type)
# st=X (start time in seconds)
# d=X (duration in seconds)
```

#### Dynamic Fade (based on duration)
```bash
# Get duration
duration=$(ffprobe -v error -show_entries format=duration \
  -of default=noprint_wrappers=1:nokey=1 input.wav)

# Calculate fade out start (duration - 1s)
fade_start=$(echo "$duration - 1" | bc)

# Apply fade
ffmpeg -i input.wav \
  -af "afade=t=in:st=0:d=0.5,afade=t=out:st=$fade_start:d=1" \
  output.wav
```

### Silence Removal

#### Remove Leading/Trailing Silence
```bash
# Remove silence at start and end
ffmpeg -i input.wav -af "silenceremove=start_periods=1:stop_periods=-1:detection=peak" output.wav

# More aggressive (remove quieter parts)
ffmpeg -i input.wav -af "silenceremove=start_periods=1:start_threshold=-50dB:stop_periods=-1:stop_threshold=-50dB" output.wav
```

#### Remove Long Pauses (>1s)
```bash
# Remove silences longer than 1 second
ffmpeg -i input.wav -af "silenceremove=stop_periods=-1:stop_duration=1:stop_threshold=-50dB" output.wav
```

### Noise Reduction

#### High-pass Filter (Remove Low Rumble)
```bash
# Remove frequencies below 80 Hz
ffmpeg -i input.wav -af "highpass=f=80" output.wav

# More aggressive (below 100 Hz)
ffmpeg -i input.wav -af "highpass=f=100" output.wav
```

#### Low-pass Filter (Remove High Hiss)
```bash
# Remove frequencies above 8000 Hz
ffmpeg -i input.wav -af "lowpass=f=8000" output.wav
```

#### Band-pass Filter (Voice Range Only)
```bash
# Keep only 80-8000 Hz (voice range)
ffmpeg -i input.wav -af "highpass=f=80,lowpass=f=8000" output.wav
```

### Compression (Dynamic Range)

#### Basic Compression
```bash
# Compress dynamic range (make quiet parts louder)
ffmpeg -i input.wav -af "acompressor=threshold=-20dB:ratio=4:attack=200:release=1000" output.wav

# Gentle compression (for voice)
ffmpeg -i input.wav -af "acompressor=threshold=-18dB:ratio=3:attack=100:release=500" output.wav
```

### Speed/Pitch Adjustment

#### Change Speed (affects pitch)
```bash
# 10% faster
ffmpeg -i input.wav -af "atempo=1.1" output.wav

# 10% slower
ffmpeg -i input.wav -af "atempo=0.9" output.wav

# Note: atempo range is 0.5-2.0
# For larger changes, chain multiple atempo filters
```

#### Change Pitch (without speed change)
```bash
# Requires rubberband (install via brew)
brew install rubberband

# Pitch up 2 semitones
rubberband -p 2 input.wav output.wav

# Pitch down 2 semitones
rubberband -p -2 input.wav output.wav
```

### Concatenation

#### Join Multiple Audio Files
```bash
# Create file list
cat > filelist.txt << EOF
file 'segment_01.wav'
file 'segment_02.wav'
file 'segment_03.wav'
EOF

# Concatenate
ffmpeg -f concat -safe 0 -i filelist.txt -c copy output.wav
```

#### Join with Crossfade
```bash
# Crossfade 1 second between two files
ffmpeg -i input1.wav -i input2.wav \
  -filter_complex "[0][1]acrossfade=d=1:c1=tri:c2=tri" \
  output.wav
```

### Trimming/Cutting

#### Extract Segment
```bash
# Extract from 5s to 15s (10 seconds)
ffmpeg -i input.wav -ss 5 -t 10 output.wav

# Extract from 5s to end
ffmpeg -i input.wav -ss 5 output.wav

# Extract first 10 seconds
ffmpeg -i input.wav -t 10 output.wav
```

---

## Qwen3-TTS Model Limits

### Text Input Limits

#### Optimal Text Length
```
Recommended: 200-500 characters per generation
Maximum: ~2048 tokens (quality may degrade)
Minimum: 10 characters (too short = unnatural)
```

#### Chunking Strategy
```python
# Pseudo-code for chunking
def chunk_text(text, max_chars=400):
    """Split text at sentence boundaries"""
    sentences = text.split('. ')
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) < max_chars:
            current_chunk += sentence + ". "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

# Example
text = "Very long text here..."
chunks = chunk_text(text, max_chars=400)
# Generate each chunk separately, then concatenate
```

### Audio Duration Limits

#### Reference Samples (Input)
```
Minimum: 3 seconds (shorter = poor quality)
Optimal: 10-20 seconds per sample
Maximum: 30 seconds (longer = diminishing returns)
Total samples: 1-3 samples recommended
Total duration: 10-60 seconds of reference audio
```

#### Generated Audio (Output)
```
No hard limit on output duration
Recommended: Generate in chunks, concatenate
Memory consideration: ~4-6GB per generation
Batch processing: Keep model loaded between generations
```

### Memory Requirements

#### Model Loading
```
Model size: ~1.8 GB (weights)
Runtime memory: ~4-6 GB during inference
Peak memory: ~8 GB (loading + generation)
Minimum RAM: 8 GB (tight)
Recommended RAM: 16 GB (comfortable) ✓
Optimal RAM: 32 GB (multiple models)
```

#### M1 Pro Specific (16GB Unified Memory)
```
Available for Qwen3-TTS: ~10-12 GB (after OS + apps)
Concurrent generations: 1 at a time
Batch processing: Keep model loaded, process sequentially
Memory pressure: Monitor Activity Monitor
```

### File Size Limits

#### Input Samples
```
Individual file: No hard limit
Recommended: <10 MB per sample
Total samples: <100 MB combined
Format: WAV preferred (no decompression overhead)
```

#### Output Files
```
1 minute audio: ~1.4 MB (WAV, 12000 Hz, mono, 16-bit)
10 minutes: ~14 MB
1 hour: ~84 MB

Compressed (MP3 192kbps): ~1.4 MB per minute
Compressed (AAC 192kbps): ~1.4 MB per minute
```

---

## Quality Guidelines

### Input Sample Quality Checklist
```
✓ No background noise (AC, traffic, keyboard)
✓ No echo or reverb
✓ No clipping (distortion)
✓ Consistent volume across samples
✓ Clear pronunciation
✓ Natural speaking pace
✓ Variety of emotions/tones
✓ Different sentence structures
```

### Output Quality Expectations
```
✓ Natural-sounding voice (80-90% similarity)
✓ Correct pronunciation (95%+ accuracy)
✓ Appropriate intonation (context-dependent)
✓ Minimal artifacts (occasional glitches possible)
✓ Consistent voice across generations
✗ Not perfect (some robotic moments)
✗ May struggle with rare words
✗ Emotion control is limited
```

### Quality Metrics

#### Subjective Quality Scale
```
5/5 - Indistinguishable from real voice
4/5 - Very good, minor artifacts
3/5 - Good, usable for content
2/5 - Acceptable, noticeable issues
1/5 - Poor, needs improvement
```

#### Typical Qwen3-TTS Results
```
With good samples: 3.5-4.5/5
With poor samples: 2-3/5
After optimization: 4-4.5/5
```

---

## Platform-Specific Requirements

### YouTube
```
Recommended:
├── Format: AAC (M4A) or MP3
├── Sample Rate: 48000 Hz (upsampled) or 44100 Hz
├── Bit Rate: 192-320 kbps
├── Channels: Stereo (converted from mono)
└── Loudness: -14 LUFS (YouTube normalization target)

Command:
ffmpeg -i input_22k.wav \
  -ar 48000 -ac 2 \
  -af "loudnorm=I=-14:TP=-1:LRA=11" \
  -codec:a aac -b:a 192k \
  output_youtube.m4a
```

### TikTok
```
Recommended:
├── Format: AAC (M4A) or MP3
├── Sample Rate: 44100 Hz
├── Bit Rate: 128-192 kbps
├── Channels: Stereo
└── Loudness: -14 LUFS

Command:
ffmpeg -i input_22k.wav \
  -ar 44100 -ac 2 \
  -af "loudnorm=I=-14:TP=-1:LRA=11" \
  -codec:a aac -b:a 128k \
  output_tiktok.m4a
```

### Podcasts (Apple Podcasts, Spotify)
```
Recommended:
├── Format: MP3 or AAC
├── Sample Rate: 44100 Hz
├── Bit Rate: 128-192 kbps (mono) or 192-256 kbps (stereo)
├── Channels: Mono (voice only) or Stereo (with music)
└── Loudness: -16 to -19 LUFS

Command:
ffmpeg -i input_22k.wav \
  -ar 44100 -ac 1 \
  -af "loudnorm=I=-16:TP=-2:LRA=11" \
  -codec:a libmp3lame -b:a 128k \
  output_podcast.mp3
```

### Video Editing (Final Cut Pro, Premiere)
```
Recommended:
├── Format: WAV (uncompressed) or AAC
├── Sample Rate: 48000 Hz (video standard)
├── Bit Depth: 16-bit or 24-bit
├── Channels: Mono or Stereo
└── Loudness: -23 LUFS (broadcast standard)

Command:
ffmpeg -i input_22k.wav \
  -ar 48000 -sample_fmt s24 \
  -af "loudnorm=I=-23:TP=-2:LRA=11" \
  output_video.wav
```

---

## Troubleshooting Audio Issues

### Issue: Clipping/Distortion
```bash
# Check for clipping
ffmpeg -i input.wav -af "astats" -f null -

# Fix: Reduce volume
ffmpeg -i input.wav -af "volume=-3dB" output.wav
```

### Issue: Background Noise
```bash
# Apply noise gate
ffmpeg -i input.wav -af "agate=threshold=-50dB:ratio=3:attack=10:release=100" output.wav

# High-pass filter (remove rumble)
ffmpeg -i input.wav -af "highpass=f=80" output.wav
```

### Issue: Inconsistent Volume
```bash
# Normalize loudness
ffmpeg -i input.wav -af "loudnorm=I=-16:TP=-1.5:LRA=11" output.wav

# Compress dynamic range
ffmpeg -i input.wav -af "acompressor=threshold=-20dB:ratio=4" output.wav
```

### Issue: File Too Large
```bash
# Convert to MP3 (smaller)
ffmpeg -i input.wav -codec:a libmp3lame -b:a 128k output.mp3

# Convert to AAC (smaller, better quality)
ffmpeg -i input.wav -codec:a aac -b:a 128k output.m4a
```

### Issue: Wrong Format for Editor
```bash
# Convert to video editing standard
ffmpeg -i input.wav -ar 48000 -ac 2 -sample_fmt s24 output.wav
```

---

## Quick Command Reference

### Essential FFmpeg Commands
```bash
# Get audio info
ffprobe -i input.wav

# Convert to Qwen3-TTS format
ffmpeg -i input.* -ar 12000 -ac 1 -sample_fmt s16 output.wav

# Normalize
ffmpeg -i input.wav -af "loudnorm=I=-16:TP=-1.5:LRA=11" output.wav

# Fade in/out
ffmpeg -i input.wav -af "afade=t=in:d=0.5,afade=t=out:st=9:d=1" output.wav

# Convert to MP3
ffmpeg -i input.wav -codec:a libmp3lame -b:a 192k output.mp3

# Convert to AAC
ffmpeg -i input.wav -codec:a aac -b:a 192k output.m4a

# Concatenate files
ffmpeg -f concat -safe 0 -i filelist.txt -c copy output.wav

# Trim audio
ffmpeg -i input.wav -ss 5 -t 10 output.wav
```

### Validation Commands
```bash
# Check sample rate
ffprobe -v error -select_streams a:0 -show_entries stream=sample_rate -of default=noprint_wrappers=1:nokey=1 input.wav

# Check channels
ffprobe -v error -select_streams a:0 -show_entries stream=channels -of default=noprint_wrappers=1:nokey=1 input.wav

# Check duration
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 input.wav

# Check bit depth
ffprobe -v error -select_streams a:0 -show_entries stream=bits_per_sample -of default=noprint_wrappers=1:nokey=1 input.wav
```

---

## Best Practices Summary

### For Input Samples
- ✅ Use 12000 Hz, mono, 16-bit WAV
- ✅ 10-20 seconds per sample
- ✅ 1-3 samples total
- ✅ Clean, no background noise
- ✅ Variety of emotions

### For Generated Output
- ✅ Keep as WAV for editing
- ✅ Convert to AAC/MP3 for final delivery
- ✅ Normalize loudness (-16 LUFS)
- ✅ Apply fade in/out
- ✅ Upsample to 48kHz for video if needed

### For Processing
- ✅ Always backup originals
- ✅ Process in lossless (WAV) until final export
- ✅ Use loudnorm instead of peak normalization
- ✅ Test on target platform before batch processing
- ✅ Document settings that work well
