# Getting Started with Voice Cloning

## 🎉 Congratulations!

You've successfully set up your voice cloning system and generated your first test audio! Here's what you've accomplished:

- ✅ Converted 13 M4A recordings to WAV format (207 seconds total)
- ✅ Validated all audio samples (100% valid)
- ✅ Created your voice profile: `bryan_voice_profile.json`
- ✅ Generated your first cloned voice test: `test_output.wav`

## 📊 Your Voice Profile Stats

- **Name**: Bryan
- **Samples**: 13 audio files
- **Total Duration**: 207 seconds (~3.5 minutes)
- **Sample Rate**: 22050 Hz (optimal for XTTS-v2)
- **Format**: Mono, 16-bit WAV
- **Location**: `data/bryan_voice_profile.json`

## 🚀 Quick Start Guide

### 1. Interactive Mode (Recommended)

Start the interactive CLI for easy navigation:

```bash
voice-clone
```

This will launch a menu-driven interface where you can:
- Generate speech from text
- Process batch scripts
- Manage voice profiles
- View settings

### 2. Command Line Mode

For quick tasks, use direct commands:

```bash
# Generate speech from text
voice-clone generate \
  --profile ./data/bryan_voice_profile.json \
  --text "Hola, este es un ejemplo de mi voz clonada" \
  --output ./data/outputs/ejemplo.wav

# Process a batch script
voice-clone batch \
  --profile ./data/bryan_voice_profile.json \
  --input ./data/scripts/mi_script.txt \
  --output-dir ./data/outputs/video_001

# Quick test
voice-clone test --profile ./data/bryan_voice_profile.json
```

## 📝 Creating Content

### Single Text Generation

```bash
voice-clone generate \
  --profile ./data/bryan_voice_profile.json \
  --text "Tu texto aquí. Usa puntuación correcta para mejor entonación." \
  --output ./data/outputs/mi_audio.wav
```

### Batch Processing for Videos

1. Create a script file (e.g., `data/scripts/video_001.txt`):

```
[INTRO]
Bienvenidos a este tutorial sobre inteligencia artificial.

[SECTION_1]
Hoy vamos a explorar cómo funcionan las redes neuronales.

[SECTION_2]
Las redes neuronales son modelos inspirados en el cerebro humano.

[OUTRO]
Gracias por ver este video. No olvides suscribirte.
```

2. Generate all segments:

```bash
voice-clone batch \
  --profile ./data/bryan_voice_profile.json \
  --input ./data/scripts/video_001.txt \
  --output-dir ./data/outputs/video_001
```

3. Find your generated files in `data/outputs/video_001/`:
   - `intro.wav`
   - `section_1.wav`
   - `section_2.wav`
   - `outro.wav`

## ⚙️ Configuration

### Current Setup

Your system is configured to use **CPU** for generation due to MPS compatibility issues with XTTS-v2. This is slower but works reliably.

**Performance on M1 Pro (CPU)**:
- Model loading: ~40 seconds (first time)
- Generation: ~20-30 seconds per minute of audio
- Real-time factor: ~3-4x (1 minute of audio takes 3-4 minutes to generate)

### Configuration File

Your personal config is at `config/config.yaml`:

```yaml
model:
  device: "cpu"  # Force CPU due to MPS compatibility issues

performance:
  use_gpu: false
  fp16: false  # CPU doesn't support fp16
```

To modify settings, edit this file or use the interactive mode's Settings menu.

## 🎯 Tips for Best Results

### Text Formatting

1. **Use proper punctuation** - It affects intonation:
   ```
   ✅ "Hola, ¿cómo estás? Espero que bien."
   ❌ "hola como estas espero que bien"
   ```

2. **Keep chunks under 400 characters** - Better quality:
   ```
   ✅ Short paragraphs (2-3 sentences)
   ❌ Very long paragraphs (10+ sentences)
   ```

3. **Use ellipsis for pauses**:
   ```
   "Primero... vamos a ver esto. Segundo... esto otro."
   ```

### Audio Quality

1. **Normalize output** (optional):
   ```bash
   ffmpeg -i input.wav -af "loudnorm=I=-16:TP=-1.5:LRA=11" output_normalized.wav
   ```

2. **Add fade in/out** (optional):
   ```bash
   ffmpeg -i input.wav -af "afade=t=in:d=0.5,afade=t=out:st=9:d=1" output_faded.wav
   ```

3. **Convert to video format** (for editing):
   ```bash
   ffmpeg -i input.wav -codec:a aac -b:a 192k output.m4a
   ```

## 📁 Project Structure

```
voice-clone/
├── data/
│   ├── samples/              # Your 13 voice samples
│   ├── outputs/              # Generated audio files
│   │   └── test_output.wav  # Your first test!
│   ├── scripts/              # Text scripts for batch processing
│   └── bryan_voice_profile.json  # Your voice profile
├── config/
│   ├── default.yaml          # Default settings
│   └── config.yaml           # Your personal settings
└── recordings-from-iphone/   # Original M4A files (backup)
```

## 🎬 Workflow for YouTube Videos

### Step 1: Write Your Script

Create `data/scripts/video_tutorial.txt`:

```
[INTRO]
¡Hola a todos! Bienvenidos a este nuevo tutorial.

[MAIN_CONTENT]
Hoy vamos a aprender sobre [tema]. Es muy importante entender...

[OUTRO]
Gracias por ver este video. No olvides suscribirte y activar la campanita.
```

### Step 2: Generate Audio

```bash
voice-clone batch \
  --profile ./data/bryan_voice_profile.json \
  --input ./data/scripts/video_tutorial.txt \
  --output-dir ./data/outputs/video_tutorial
```

### Step 3: Post-Process (Optional)

```bash
# Normalize all files
for file in data/outputs/video_tutorial/*.wav; do
  ffmpeg -i "$file" -af "loudnorm=I=-16:TP=-1.5:LRA=11" "${file%.wav}_normalized.wav"
done

# Convert to AAC for video editing
for file in data/outputs/video_tutorial/*_normalized.wav; do
  ffmpeg -i "$file" -codec:a aac -b:a 192k "${file%.wav}.m4a"
done
```

### Step 4: Import to Video Editor

1. Open Final Cut Pro / Premiere / DaVinci Resolve
2. Import the M4A files from `data/outputs/video_tutorial/`
3. Sync with your video footage
4. Export final video

## 🔧 Troubleshooting

### Generation is Slow

**Expected**: CPU generation is 3-4x slower than real-time
- 1 minute of audio = 3-4 minutes to generate
- This is normal for CPU-based generation

**Solution**: Be patient or consider using a cloud GPU service for faster generation

### Voice Doesn't Sound Natural

**Possible causes**:
1. Text formatting issues (missing punctuation)
2. Need more varied samples
3. Text too long (>400 characters)

**Solutions**:
1. Add proper punctuation: commas, periods, question marks
2. Record 2-3 more samples with different emotions
3. Split long texts into smaller chunks

### Audio Has Artifacts

**Possible causes**:
1. Original samples had noise
2. Text has unusual words

**Solutions**:
1. Re-record samples in quieter environment
2. Use phonetic spelling for difficult words

## 📚 Next Steps

### Improve Your Voice Profile

1. **Add more samples** (optional):
   - Record 2-3 more samples with different emotions
   - Place in `data/samples/`
   - Recreate profile:
     ```bash
     voice-clone prepare \
       --samples ./data/samples \
       --output ./data/bryan_voice_profile_v2.json \
       --name "Bryan_v2"
     ```

2. **Test different settings**:
   - Try different temperature values (0.5-0.9)
   - Adjust speed (0.8-1.2)
   - Experiment with text formatting

### Create Your First Video

1. Write a complete script
2. Generate all audio segments
3. Post-process (normalize, convert)
4. Import to video editor
5. Sync with visuals
6. Export and publish!

### Automate Your Workflow

Create a script for your common tasks:

```bash
#!/bin/bash
# generate_video.sh

SCRIPT_FILE=$1
OUTPUT_DIR=$2

# Generate audio
voice-clone batch \
  --profile ./data/bryan_voice_profile.json \
  --input "$SCRIPT_FILE" \
  --output-dir "$OUTPUT_DIR"

# Normalize
for file in "$OUTPUT_DIR"/*.wav; do
  ffmpeg -i "$file" -af "loudnorm=I=-16:TP=-1.5:LRA=11" "${file%.wav}_normalized.wav"
done

# Convert to AAC
for file in "$OUTPUT_DIR"/*_normalized.wav; do
  ffmpeg -i "$file" -codec:a aac -b:a 192k "${file%.wav}.m4a"
done

echo "✓ All audio generated and processed!"
```

## 🎓 Learning Resources

- **Interactive CLI Guide**: `CLI_INTERACTIVE_GUIDE.md`
- **Complete Workflow**: `.kiro/steering/workflow.md`
- **Audio Specifications**: `.kiro/steering/audio_specs.md`
- **Sample Recording Guide**: `.kiro/steering/samples_guide.md`
- **Prompt Examples**: `.kiro/steering/prompts_examples.md`

## 💡 Pro Tips

1. **Keep original samples**: Never delete `recordings-from-iphone/` - they're your backup
2. **Version your profiles**: Create v2, v3 as you improve
3. **Document what works**: Note which settings produce best results
4. **Batch process**: Generate multiple videos at once to save time
5. **Test before production**: Always generate a test before full batch

## 🎉 You're Ready!

You now have everything you need to start creating content with your cloned voice. Start small, experiment, and iterate. The more you use it, the better you'll understand what works best for your voice and content style.

**Happy creating! 🎙️**

---

## Quick Reference Commands

```bash
# Interactive mode
voice-clone

# Generate single audio
voice-clone generate --profile ./data/bryan_voice_profile.json --text "Tu texto" --output output.wav

# Batch process
voice-clone batch --profile ./data/bryan_voice_profile.json --input script.txt --output-dir ./outputs

# Quick test
voice-clone test --profile ./data/bryan_voice_profile.json

# Validate samples
voice-clone validate-samples --dir ./data/samples

# Play audio (macOS)
afplay output.wav
```
