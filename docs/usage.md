# Usage Guide

This guide covers how to use Voice Clone CLI for voice cloning and text-to-speech synthesis.

## Quick Start

```bash
# Clone a voice from audio samples
voice-clone train --samples data/samples/my_voice/ --output data/models/my_voice

# Generate speech from text
voice-clone synthesize --model data/models/my_voice --text "Hello, world!" --output output.wav

# Interactive REPL mode
voice-clone repl --model data/models/my_voice
```

## Command Overview

Voice Clone CLI provides three main commands:

- `train` - Train a voice model from audio samples
- `synthesize` - Generate speech from text
- `repl` - Interactive mode for real-time synthesis

## Training a Voice Model

### Basic Training

```bash
voice-clone train \
  --samples data/samples/my_voice/ \
  --output data/models/my_voice
```

### Training Options

```bash
voice-clone train \
  --samples data/samples/my_voice/ \
  --output data/models/my_voice \
  --language en \
  --min-duration 1.0 \
  --max-duration 10.0 \
  --sample-rate 22050
```

**Parameters**:
- `--samples`: Directory containing audio samples (WAV, MP3, FLAC)
- `--output`: Output path for the trained model
- `--language`: Language code (en, es, fr, de, etc.)
- `--min-duration`: Minimum audio duration in seconds (default: 1.0)
- `--max-duration`: Maximum audio duration in seconds (default: 10.0)
- `--sample-rate`: Audio sample rate in Hz (default: 22050)

### Audio Sample Requirements

For best results:
- **Duration**: 5-30 seconds per sample
- **Quantity**: 10-30 samples minimum (more is better)
- **Quality**: Clear audio, minimal background noise
- **Format**: WAV, MP3, or FLAC
- **Content**: Natural speech, varied intonation
- **Consistency**: Same speaker, similar recording conditions

### Example Training Workflow

```bash
# 1. Prepare audio samples
mkdir -p data/samples/my_voice
cp ~/recordings/*.wav data/samples/my_voice/

# 2. Train the model
voice-clone train \
  --samples data/samples/my_voice/ \
  --output data/models/my_voice \
  --language en

# 3. Verify model creation
ls -lh data/models/my_voice/
```

## Synthesizing Speech

### Basic Synthesis

```bash
# From text string
voice-clone synthesize \
  --model data/models/my_voice \
  --text "Hello, this is a test." \
  --output output.wav

# From text file
voice-clone synthesize \
  --model data/models/my_voice \
  --text-file script.txt \
  --output output.wav
```

### Synthesis Options

```bash
voice-clone synthesize \
  --model data/models/my_voice \
  --text "Hello, world!" \
  --output output.wav \
  --language en \
  --speed 1.0 \
  --temperature 0.7 \
  --sample-rate 22050
```

**Parameters**:
- `--model`: Path to trained voice model
- `--text`: Text to synthesize (use quotes for multiple words)
- `--text-file`: Path to text file (alternative to --text)
- `--output`: Output audio file path
- `--language`: Language code (default: en)
- `--speed`: Speech speed multiplier (0.5-2.0, default: 1.0)
- `--temperature`: Synthesis temperature (0.1-1.0, default: 0.7)
- `--sample-rate`: Output sample rate in Hz (default: 22050)

### Temperature and Speed

**Temperature** controls synthesis randomness:
- Lower (0.1-0.5): More consistent, less expressive
- Medium (0.6-0.8): Balanced, natural-sounding
- Higher (0.9-1.0): More varied, potentially less stable

**Speed** controls speech rate:
- Slower (0.5-0.9): Clearer, more deliberate
- Normal (1.0): Natural pace
- Faster (1.1-2.0): Quicker, may reduce clarity

### Batch Processing

Process multiple texts:

```bash
# Create a text file with one sentence per line
cat > texts.txt << EOF
Hello, this is the first sentence.
This is the second sentence.
And this is the third.
EOF

# Process each line
while IFS= read -r line; do
  voice-clone synthesize \
    --model data/models/my_voice \
    --text "$line" \
    --output "output_$(date +%s).wav"
done < texts.txt
```

## Interactive REPL Mode

Launch interactive mode for real-time synthesis:

```bash
voice-clone repl --model data/models/my_voice
```

### REPL Commands

Once in REPL mode:

```
> Hello, world!
[Generates and plays audio]

> :speed 1.2
Speed set to 1.2

> :temperature 0.8
Temperature set to 0.8

> :save output.wav
Last output saved to output.wav

> :help
[Shows available commands]

> :quit
[Exits REPL]
```

**Available REPL commands**:
- `:speed <value>` - Set speech speed (0.5-2.0)
- `:temperature <value>` - Set temperature (0.1-1.0)
- `:language <code>` - Set language (en, es, fr, etc.)
- `:save <path>` - Save last output to file
- `:help` - Show help message
- `:quit` or `:exit` - Exit REPL

## Configuration File

Create a configuration file for default settings:

```yaml
# config/config.yaml
model:
  default_path: data/models/my_voice

synthesis:
  language: en
  speed: 1.0
  temperature: 0.7
  sample_rate: 22050

training:
  min_duration: 1.0
  max_duration: 10.0
  sample_rate: 22050

output:
  default_dir: data/outputs
```

Use configuration file:

```bash
voice-clone synthesize \
  --config config/config.yaml \
  --text "Hello, world!"
```

## Environment Variables

Set environment variables for common options:

```bash
# Set default model path
export VOICE_CLONE_MODEL=data/models/my_voice

# Set output directory
export VOICE_CLONE_OUTPUT_DIR=data/outputs

# Use GPU (if available)
export CUDA_VISIBLE_DEVICES=0

# Use CPU only
export CUDA_VISIBLE_DEVICES=""
```

## Examples

### Example 1: Personal Voice Assistant

```bash
# Train your voice
voice-clone train \
  --samples data/samples/my_voice/ \
  --output data/models/my_voice

# Create responses
voice-clone synthesize \
  --model data/models/my_voice \
  --text "Your meeting starts in 5 minutes." \
  --output reminder.wav
```

### Example 2: Audiobook Narration

```bash
# Train narrator voice
voice-clone train \
  --samples data/samples/narrator/ \
  --output data/models/narrator

# Generate chapter audio
voice-clone synthesize \
  --model data/models/narrator \
  --text-file chapter1.txt \
  --output chapter1.wav \
  --speed 0.9
```

### Example 3: Multi-Language Support

```bash
# English synthesis
voice-clone synthesize \
  --model data/models/my_voice \
  --text "Hello, how are you?" \
  --language en \
  --output hello_en.wav

# Spanish synthesis
voice-clone synthesize \
  --model data/models/my_voice \
  --text "Hola, ¿cómo estás?" \
  --language es \
  --output hello_es.wav
```

## Best Practices

### For Training
- Use high-quality audio recordings
- Ensure consistent recording environment
- Include varied speech patterns and emotions
- Remove long silences and background noise
- Use 10-30 samples of 5-30 seconds each

### For Synthesis
- Start with default parameters and adjust as needed
- Use temperature 0.7 for balanced results
- Keep text length reasonable (< 500 characters per synthesis)
- Test different speeds for optimal clarity

### For Production Use
- Always obtain proper consent before cloning voices
- Respect voice rights and ethical guidelines
- Test thoroughly before deploying
- Monitor output quality regularly

## Troubleshooting

### Poor Voice Quality
- Increase number of training samples
- Improve audio sample quality
- Adjust temperature (try 0.6-0.8)
- Check for background noise in samples

### Slow Processing
- Enable GPU support (see [Installation Guide](installation.md))
- Reduce sample rate (e.g., 16000 Hz)
- Process shorter text segments

### Out of Memory Errors
- Use CPU mode: `export CUDA_VISIBLE_DEVICES=""`
- Reduce batch size in configuration
- Process shorter audio segments

## Next Steps

- Explore [API Documentation](api.md) for programmatic usage
- Check [Development Guide](development.md) for contributing
- Review [README](../README.md) for project overview

## Getting Help

- Check [GitHub Issues](https://github.com/yourusername/voice-clone-cli/issues)
- Read [FAQ](../README.md#faq)
- Open a new issue with details and examples
