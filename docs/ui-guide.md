# Gradio UI User Guide

## Overview

The Voice Clone Gradio UI provides a web-based interface for voice cloning and text-to-speech generation. This guide will walk you through all features and workflows.

---

## Getting Started

### Launching the UI

```bash
# Start the UI (default port 7860)
voice-clone ui

# Use custom port
voice-clone ui --port 8080

# Create public shareable link
voice-clone ui --share
```

The UI will be available at `http://localhost:7860` (or your custom port).

---

## Tab 1: Prepare Voice Profile

### Purpose
Create a voice profile from audio samples that will be used for voice cloning.

### Step-by-Step Guide

#### 1. Upload Audio Samples

**Requirements:**
- 1-3 audio files
- Supported formats: WAV, MP3, M4A, FLAC
- Duration: 10-20 seconds per sample (optimal)
- Quality: Clear audio, no background noise
- Variety: Different emotions/tones recommended

**How to Upload:**
1. Click the file upload area or drag & drop files
2. Select 1-3 audio files from your computer
3. Wait for files to upload
4. **View automatic spectrogram visualization** in the right panel

**Tips:**
- Use samples with different emotions (neutral, happy, serious)
- Ensure consistent audio quality across all samples
- Avoid samples with background noise or echo
- Check the spectrogram to verify audio quality visually

#### 2. Audio Visualization

**Automatic Display:**
- When you upload audio files, a spectrogram is automatically generated
- Shows both waveform (top) and mel spectrogram (bottom)
- Helps you visually verify audio quality

**What to Look For:**
- **Waveform**: Should show clear amplitude variations
- **Spectrogram**: Should show rich frequency content (colorful patterns)
- **Red flags**:
  - Flat waveform = audio too quiet
  - Clipped waveform = audio too loud (distortion)
  - Sparse spectrogram = poor audio quality
  - Horizontal lines = background noise

#### 3. Validate Samples (Optional but Recommended)

1. Click **"🔍 Validate Samples"** button
2. Review validation results:
   - ✅ Green checkmarks = Valid samples
   - ❌ Red X = Issues found
3. Fix any issues before creating profile

**Common Issues:**
- Wrong sample rate → Convert to 12000 Hz
- Stereo audio → Convert to mono
- Too short/long → Use 10-20 second clips
- Poor spectrogram quality → Re-record with better equipment/environment

#### 4. Enter Profile Information

**Profile Name:**
- Enter a descriptive name (e.g., "my_voice", "narrator_voice")
- Use only letters, numbers, underscores
- Must be unique

**Reference Text (Optional):**
- Describe the content of your samples
- Example: "Hola, esta es una muestra de mi voz para clonación."
- Helps improve voice cloning quality

#### 5. Create Profile

1. Click **"✨ Create Voice Profile"** button
2. Wait for processing (may take a few seconds)
3. Check results in the right panel:
   - Profile info displayed as JSON
   - Dropdowns in other tabs updated automatically

**Success Indicators:**
- Profile info shows in JSON panel
- Profile name appears in Tab 2 and Tab 3 dropdowns

---

## Tab 2: Generate Audio

### Purpose
Convert text to speech using your cloned voice.

### Step-by-Step Guide

#### 1. Select Voice Profile

1. Click the **"Select Voice Profile"** dropdown
2. Choose a previously created profile
3. If no profiles available, create one in Tab 1 first

#### 2. Enter Text

1. Type or paste text in the text box
2. Maximum 500 characters recommended for best quality
3. Character counter shows current length

**Text Tips:**
- Use proper punctuation for natural pauses
- Break long texts into shorter segments
- Use "..." for longer pauses
- Add commas for natural breathing points

**Example Texts:**
```
Hola, bienvenidos a este tutorial sobre inteligencia artificial.

La tecnología está transformando el mundo de maneras increíbles.

Gracias por ver este video. No olvides suscribirte al canal.
```

#### 3. Adjust Advanced Settings (Optional)

Click **"⚙️ Advanced Settings"** to expand:

**Temperature (0.5 - 1.0):**
- Lower (0.5-0.7): More consistent, less variation
- Higher (0.8-1.0): More varied, more expressive
- Default: 0.75 (recommended)

**Speed (0.8 - 1.2):**
- Lower (0.8-0.9): Slower, more deliberate
- Higher (1.1-1.2): Faster, more energetic
- Default: 1.0 (normal speed)

#### 4. Generate Audio

1. Click **"🎙️ Generate Audio"** button
2. Wait for generation (15-30 seconds typically)
3. Progress bar shows processing status

**What Happens:**
- Model loads (first time: 30-60 seconds)
- Audio is generated
- File is saved to `data/outputs/`

#### 5. Listen and Download

1. Audio player appears with generated audio
2. Click play button to listen
3. Click download button to save file
4. Generation info shows details (duration, settings, etc.)

**Generation Info Includes:**
- Profile used
- Text length
- Temperature and speed settings
- Audio duration
- Output filename

---

## Tab 3: Batch Processing

### Purpose
Process multiple text segments from a script file and generate audio for each segment.

### Step-by-Step Guide

#### 1. Prepare Script File

Create a text file with this format:

```
[INTRO]
Hola, bienvenidos a este tutorial sobre inteligencia artificial.

[SECTION_1]
Hoy vamos a hablar sobre redes neuronales y cómo funcionan.

[SECTION_2]
Las redes neuronales son modelos computacionales inspirados en el cerebro humano.

[OUTRO]
Gracias por ver este video. No olvides suscribirte al canal.
```

**Format Rules:**
- Segment markers: `[SEGMENT_NAME]`
- Use uppercase letters, numbers, underscores in names
- Text follows immediately after marker
- Blank line between segments (optional)
- Supported formats: `.txt`, `.md`

**Example Segment Names:**
- `[INTRO]`
- `[SECTION_1]`
- `[CHAPTER_2]`
- `[OUTRO]`
- `[CALL_TO_ACTION]`

#### 2. Select Voice Profile

1. Click the **"Select Voice Profile"** dropdown
2. Choose a previously created profile
3. Same profile will be used for all segments

#### 3. Upload Script File

1. Click **"Upload Script File (.txt)"** area
2. Select your script file
3. File is uploaded and ready for processing

#### 4. Process Batch

1. Click **"⚡ Process Batch"** button
2. Wait for processing (varies by segment count)
3. Progress bar shows overall status

**Processing Time:**
- Model loading: 30-60 seconds (first time)
- Per segment: 15-30 seconds
- 3 segments: ~1-2 minutes
- 10 segments: ~3-5 minutes

#### 5. Download Results

1. All generated files appear in download area
2. Click individual files to download
3. Or download all as a batch
4. Processing info shows summary

**Output Files:**
- Named: `01_intro.wav`, `02_section_1.wav`, etc.
- Saved to: `data/outputs/batch_{profile_name}/`
- Format: WAV, 12000 Hz, mono, 16-bit

**Processing Info Includes:**
- Profile used
- Total segments
- Successful count
- Failed count (if any)
- Output directory

---

## Troubleshooting

### Profile Creation Issues

**Problem: "No files uploaded"**
- Solution: Upload 1-3 audio files before creating profile

**Problem: "Profile name required"**
- Solution: Enter a profile name in the text box

**Problem: Validation fails**
- Solution: Check validation results and fix issues:
  - Convert to 12000 Hz sample rate
  - Convert to mono (1 channel)
  - Ensure 10-20 second duration
  - Remove background noise

### Audio Generation Issues

**Problem: "No profile selected"**
- Solution: Select a profile from dropdown or create one in Tab 1

**Problem: "No text provided"**
- Solution: Enter text in the text box

**Problem: Generation takes too long**
- Solution:
  - First generation loads model (30-60 seconds)
  - Subsequent generations are faster
  - Close other applications to free memory

**Problem: "Out of memory"**
- Solution:
  - Close other applications
  - Use shorter text
  - Restart the UI

**Problem: Audio quality is poor**
- Solution:
  - Use higher quality input samples
  - Add more samples with variety
  - Adjust temperature (try 0.7-0.8)
  - Use proper punctuation in text

### Batch Processing Issues

**Problem: "Empty script"**
- Solution: Check script format:
  - Use `[SEGMENT_NAME]` markers
  - Add text after each marker
  - Ensure proper formatting

**Problem: Some segments fail**
- Solution:
  - Check logs for specific errors
  - Verify text in failed segments
  - Try shorter text per segment
  - Regenerate failed segments individually in Tab 2

**Problem: Script not parsing correctly**
- Solution:
  - Use uppercase letters in segment names
  - Ensure markers are on their own line
  - Check for special characters
  - Save file as UTF-8 encoding

---

## Best Practices

### For Best Voice Quality

1. **High-Quality Samples:**
   - Record in quiet environment
   - Use good microphone
   - Clear pronunciation
   - Natural speaking pace

2. **Sample Variety:**
   - Include different emotions
   - Vary sentence structures
   - Different speaking speeds
   - Multiple tones

3. **Text Formatting:**
   - Use proper punctuation
   - Break long texts into segments
   - Add commas for natural pauses
   - Use "..." for longer pauses

4. **Generation Settings:**
   - Start with defaults (temp: 0.75, speed: 1.0)
   - Adjust based on results
   - Lower temperature for consistency
   - Higher temperature for variety

### For Efficient Workflow

1. **Profile Management:**
   - Create profiles for different voices/styles
   - Use descriptive names
   - Keep samples organized
   - Backup profile files

2. **Text Preparation:**
   - Prepare scripts in advance
   - Use consistent formatting
   - Test with short texts first
   - Proofread for errors

3. **Batch Processing:**
   - Group related segments
   - Use clear segment names
   - Keep segments under 500 characters
   - Process during off-peak hours

4. **File Organization:**
   - Download files promptly
   - Organize by project
   - Keep backups
   - Clean up old files

---

## Keyboard Shortcuts

Currently, the Gradio UI uses standard browser shortcuts:

- **Tab**: Navigate between fields
- **Enter**: Submit forms (in text boxes)
- **Ctrl/Cmd + A**: Select all text
- **Ctrl/Cmd + C**: Copy text
- **Ctrl/Cmd + V**: Paste text

---

## FAQ

### General Questions

**Q: Can I use the UI and CLI at the same time?**
A: Yes, they are independent. However, they share the same data directories.

**Q: Where are my files saved?**
A:
- Profiles: `data/profiles/`
- Generated audio: `data/outputs/`
- Batch outputs: `data/outputs/batch_{profile_name}/`

**Q: Can I edit a profile after creation?**
A: Currently, no. You need to create a new profile. This feature may be added in the future.

**Q: How many profiles can I create?**
A: Unlimited. However, each profile requires disk space for samples.

### Technical Questions

**Q: What audio formats are supported?**
A: Input: WAV, MP3, M4A, FLAC. Output: WAV (12000 Hz, mono, 16-bit).

**Q: What's the maximum text length?**
A: Recommended: 500 characters. Maximum: 2048 tokens (~800 characters).

**Q: How long does generation take?**
A: First time: 30-60 seconds (model loading). Subsequent: 15-30 seconds per minute of audio.

**Q: Can I use GPU acceleration?**
A: Yes, on Apple Silicon (M1/M2/M3) via MPS. CUDA not currently supported.

**Q: What languages are supported?**
A: Spanish is primary. Other languages may work but are not officially supported.

### Troubleshooting Questions

**Q: Why is my voice robotic?**
A:
- Use higher quality samples
- Add more emotional variety
- Increase temperature (0.8-0.9)
- Ensure samples are natural

**Q: Why does generation fail?**
A: Check:
- Profile exists and is valid
- Text is not empty
- Enough memory available
- Model files are present

**Q: Why is the UI slow?**
A:
- First generation loads model (slow)
- Close other applications
- Use faster hardware (Apple Silicon recommended)
- Reduce text length

---

## Tips & Tricks

### Recording Better Samples

1. Use a quiet room
2. Speak naturally (not too fast/slow)
3. Maintain consistent distance from mic
4. Record multiple takes, keep best ones
5. Include variety (emotions, tones, speeds)

### Writing Better Text

1. Use conversational language
2. Add punctuation for natural flow
3. Break long sentences
4. Use "..." for dramatic pauses
5. Test with short texts first

### Optimizing Generation

1. Keep model loaded (don't close UI)
2. Process multiple texts in one session
3. Use batch processing for multiple segments
4. Adjust settings based on content type
5. Monitor memory usage

### Organizing Projects

1. Create separate profiles for different projects
2. Use descriptive profile names
3. Organize scripts by project
4. Keep generated files organized
5. Backup important profiles and outputs

---

## Support

### Getting Help

- **Documentation**: Check `docs/` directory
- **Issues**: Report bugs on GitHub
- **Logs**: Check console output for errors
- **Community**: Join discussions on GitHub

### Reporting Issues

When reporting issues, include:
1. Error message (if any)
2. Steps to reproduce
3. System information (OS, Python version)
4. Log output
5. Sample files (if relevant)

---

## Changelog

### Version 1.0.0 (2025-01-25)
- Initial release
- Tab 1: Voice profile creation
- Tab 2: Single text generation
- Tab 3: Batch processing
- Comprehensive error handling
- User-friendly interface

---

## Credits

- **Framework**: Gradio 4.x
- **TTS Model**: Qwen3-TTS
- **Audio Processing**: soundfile, librosa
- **UI Design**: Gradio Blocks API

---

**Last Updated**: 2025-01-25
**Version**: 1.0.0
