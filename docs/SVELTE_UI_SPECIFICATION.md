# Svelte UI Specification - Voice Clone Tool

## Document Overview

This document provides a comprehensive specification for replacing the current Gradio UI with a modern Svelte + Django frontend. It includes:
- Complete UI design specification
- Google Stitch prompt for initial HTML/CSS generation
- Component structure for Svelte
- Django API endpoint design
- Color palette and styling guidelines
- Responsive design requirements
- Accessibility requirements

**Last Updated**: 2025-01-25
**Version**: 1.0.0
**Status**: Design Phase

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Google Stitch Prompt](#google-stitch-prompt)
3. [UI Design Specification](#ui-design-specification)
4. [Component Architecture](#component-architecture)
5. [Django API Design](#django-api-design)
6. [Color Palette & Styling](#color-palette--styling)
7. [Responsive Design](#responsive-design)
8. [Accessibility Requirements](#accessibility-requirements)
9. [Implementation Roadmap](#implementation-roadmap)

---

## Executive Summary

### Current State
- Gradio-based UI with 3 tabs (Profile Creation, Generation, Batch Processing)
- Python backend with Qwen3-TTS integration
- Functional but limited customization options

### Target State
- Modern Svelte single-page application
- Django REST API backend
- Custom UI with enhanced user experience
- Single-screen workflow with 3 main cards
- No authentication required (local tool)

### Key Constraints
- **Model Limitation**: Uses exactly 1 audio file + 1 reference text (not multiple samples)
- **Local Only**: No cloud deployment, runs on localhost
- **Simple Auth**: No user authentication or sessions needed
- **Performance**: Must work smoothly on M1 Pro MacBook (16GB RAM)


---

## Google Stitch Prompt

### Complete Prompt for Google Stitch

```
Create a modern, single-page voice cloning web application with the following specifications:

LAYOUT:
- Single page with 3 main cards arranged horizontally
- Clean, modern design with blue color scheme
- Generous white space and clear visual hierarchy
- Rounded corners

CARD 1: REFERENCE AUDIO (🎵)
Header:
- Title: "🎵 Reference Audio" (left side)
- Action icons (right side): Upload New, Edit Reference Text

Content:
- Large horizontal audio waveform visualization (center)
- Waveform should be prominent and visually appealing
- Show frequency spectrum with blue gradient colors
- Drag & drop for audio file upload

Controls (bottom):
- Playback controls: Rewind, Play/Pause, Forward
- Timeline scrubber with current time / total duration
- Volume control
- Trim/Cut tools (scissors icon)

Reference Text Section:
- Collapsible/expandable text area
- Placeholder: "Enter the transcript of your reference audio..."
- Character counter
- Save button

CARD 2: TARGET TEXT (📝)
Header:
- Title: "📝 Target Text"
- Character counter: "0 / 500 characters"

Content:
- Large text area (textarea)
- Placeholder: "Enter the text you want to convert to speech (max 500 characters)..."
- Real-time character counter
- Language dropdown selector (Spanish, English, etc.)

Advanced Settings (collapsible):
- Temperature slider (0.5 - 1.0)
- Speed slider (0.8 - 1.2)
- Tooltips explaining each parameter

Action Button:
- Large, prominent "Generate Audio" button
- Blue gradient background
- Disabled state when no text entered

CARD 3: OUTPUT AUDIO (🔊)
Header:
- Title: "🔊 Generated Audio"
- Status indicator (Processing / Finished / Error)

Status Display:
- Progress bar during generation
- Status messages: "Processing...", "Finished!", "Error: ..."
- Estimated time remaining

Audio Player:
- Waveform visualization of generated audio
- Standard playback controls
- Download button
- Share button (optional)

Generation Info:
- Duration
- Generation time
- Settings used (temperature, speed)

COLOR SCHEME:
- Primary: Blue (#0171E3)
- Secondary: Gray (#F5F5F7)
- Background: White (#FFFFFF)
- Cards: gray (#F5F5F7) with subtle shadow
- Text: Dark gray (#2C3E50)
- Accent: Bright blue for CTAs

TYPOGRAPHY:
- Headers: Inter or SF Pro Display (bold, 24-32px)
- Body: Inter or SF Pro Text (regular, 14-16px)
- Monospace: SF Mono or Fira Code (for technical info)

INTERACTIONS:
- Drag & drop for audio file upload

ICONS:
- Use modern icon set
- Consistent icon style throughout
```

### Usage Instructions

1. **Copy the prompt above** to Google Stitch
2. **Review generated HTML/CSS** - Stitch will create initial markup
3. **Export to Figma** (optional) - For design refinement
4. **Download HTML/CSS** - Use as base for Svelte components
5. **Adapt to Svelte** - Convert HTML to Svelte component structure


---

## UI Design Specification

### Overall Layout

```
┌─────────────────────────────────────────────────────────────┐
│  Header: Voice Clone Tool                          [?] [⚙️]  │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ 🎵 Reference Audio              [📤 Upload] [✏️ Edit] │  │
│  │                                                         │  │
│  │  ╔═══════════════════════════════════════════════╗    │  │
│  │  ║  [Waveform/Spectrogram Visualization]        ║    │  │
│  │  ║  ▁▂▃▅▇█▇▅▃▂▁▂▃▅▇█▇▅▃▂▁▂▃▅▇█▇▅▃▂▁▂▃▅▇█▇▅▃▂▁  ║    │  │
│  │  ╚═══════════════════════════════════════════════╝    │  │
│  │                                                         │  │
│  │  [⏮] [▶️] [⏭]  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │  │
│  │  0:00 / 0:15                              [🔊] [✂️]   │  │
│  │                                                         │  │
│  │  📝 Reference Text (click to expand)                   │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ 📝 Target Text                      0 / 500 characters │  │
│  │                                                         │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │ Enter the text you want to convert to speech... │  │  │
│  │  │                                                   │  │  │
│  │  │                                                   │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  │                                                         │  │
│  │  Language: [Spanish ▼]    ⚙️ Advanced Settings        │  │
│  │                                                         │  │
│  │         [🎙️ Generate Audio]                           │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ 🔊 Output Audio                    ⏳ Processing...    │  │
│  │                                                         │  │
│  │  ╔═══════════════════════════════════════════════╗    │  │
│  │  ║  [Generated Audio Waveform]                   ║    │  │
│  │  ║  ▁▂▃▅▇█▇▅▃▂▁▂▃▅▇█▇▅▃▂▁▂▃▅▇█▇▅▃▂▁▂▃▅▇█▇▅▃▂▁  ║    │  │
│  │  ╚═══════════════════════════════════════════════╝    │  │
│  │                                                         │  │
│  │  [▶️] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │  │
│  │  0:00 / 0:12                    [⬇️ Download] [🔗]    │  │
│  │                                                         │  │
│  │  ℹ️ Duration: 12.3s | Generated in 18.5s              │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                               │
│                                          [💾 Save Profile]   │
└─────────────────────────────────────────────────────────────┘
```

### Card 1: Reference Audio - Detailed Specification

#### Header Section
```html
<div class="card-header">
  <h2 class="card-title">
    <span class="icon">🎵</span>
    Reference Audio
  </h2>
  <div class="card-actions">
    <button class="btn-icon" title="Upload New Audio">
      <svg><!-- Upload icon --></svg>
    </button>
    <button class="btn-icon" title="Edit Reference Text">
      <svg><!-- Edit icon --></svg>
    </button>
  </div>
</div>
```

**Styling:**
- Title: 24px, bold, dark gray (#2C3E50)
- Icons: 20px, blue (#0066B4) on hover
- Background: White with subtle shadow

#### Waveform/Spectrogram Visualization
```html
<div class="audio-visualization">
  <canvas id="waveform-canvas" width="800" height="200"></canvas>
  <canvas id="spectrogram-canvas" width="800" height="200"></canvas>
</div>
```

**Features:**
- Dual visualization: Waveform (top) + Spectrogram (bottom)
- Real-time rendering using Web Audio API
- Blue/cyan gradient colors
- Interactive: Click to seek position
- Zoom controls (optional)

**Technical:**
- Use `wavesurfer.js` or custom Canvas API
- FFT size: 2048 for spectrogram
- Update rate: 60fps for smooth animation
- Responsive: Scale to container width

#### Playback Controls
```html
<div class="playback-controls">
  <div class="control-buttons">
    <button class="btn-control" id="rewind">⏮</button>
    <button class="btn-control btn-play" id="play">▶️</button>
    <button class="btn-control" id="forward">⏭</button>
  </div>

  <div class="timeline">
    <input type="range" class="timeline-slider" min="0" max="100" value="0">
    <span class="time-current">0:00</span>
    <span class="time-separator">/</span>
    <span class="time-total">0:00</span>
  </div>

  <div class="additional-controls">
    <button class="btn-icon" id="volume">🔊</button>
    <button class="btn-icon" id="trim">✂️</button>
  </div>
</div>
```

**Interactions:**
- Play/Pause toggle
- Rewind: -5 seconds
- Forward: +5 seconds
- Timeline: Draggable scrubber
- Volume: Popup slider (0-100%)
- Trim: Opens trim modal

#### Reference Text Section
```html
<div class="reference-text-section" data-expanded="false">
  <button class="expand-toggle">
    📝 Reference Text (click to expand)
    <svg class="chevron"><!-- Down arrow --></svg>
  </button>

  <div class="reference-text-content" hidden>
    <textarea
      class="reference-text-input"
      placeholder="Enter the transcript of your reference audio..."
      maxlength="500"
    ></textarea>
    <div class="text-footer">
      <span class="char-count">0 / 500</span>
      <button class="btn-primary btn-sm">Save</button>
    </div>
  </div>
</div>
```

**Behavior:**
- Collapsed by default
- Smooth expand/collapse animation (300ms)
- Auto-save on blur (optional)
- Character counter updates in real-time


### Card 2: Target Text - Detailed Specification

#### Header Section
```html
<div class="card-header">
  <h2 class="card-title">
    <span class="icon">📝</span>
    Target Text
  </h2>
  <div class="char-counter">
    <span class="count">0</span> / <span class="max">500</span> characters
  </div>
</div>
```

**Styling:**
- Character counter: 14px, gray when under limit, orange when near limit (>450), red when at limit
- Real-time update on input

#### Text Input Area
```html
<div class="text-input-container">
  <textarea
    class="target-text-input"
    placeholder="Enter the text you want to convert to speech (max 500 characters)..."
    maxlength="500"
    rows="6"
  ></textarea>
</div>
```

**Features:**
- Auto-resize based on content (min 6 rows, max 12 rows)
- Syntax highlighting for punctuation (optional)
- Paste detection with warning if >500 chars
- Undo/Redo support (Ctrl+Z / Ctrl+Y)

#### Language & Settings
```html
<div class="input-options">
  <div class="language-selector">
    <label for="language">Language:</label>
    <select id="language" class="select-input">
      <option value="es" selected>Spanish</option>
      <option value="en">English</option>
      <option value="pt">Portuguese</option>
    </select>
  </div>

  <button class="btn-text" id="advanced-toggle">
    ⚙️ Advanced Settings
    <svg class="chevron"><!-- Down arrow --></svg>
  </button>
</div>

<div class="advanced-settings" hidden>
  <div class="setting-group">
    <label for="temperature">
      Temperature
      <span class="tooltip-icon" title="Controls variability. Lower = more consistent, Higher = more varied">ℹ️</span>
    </label>
    <input type="range" id="temperature" min="0.5" max="1.0" step="0.05" value="0.75">
    <span class="setting-value">0.75</span>
  </div>

  <div class="setting-group">
    <label for="speed">
      Speed
      <span class="tooltip-icon" title="Speaking speed multiplier">ℹ️</span>
    </label>
    <input type="range" id="speed" min="0.8" max="1.2" step="0.05" value="1.0">
    <span class="setting-value">1.0x</span>
  </div>
</div>
```

**Interactions:**
- Advanced settings: Smooth slide-down animation
- Sliders: Show value on drag
- Tooltips: Appear on hover (delay 500ms)

#### Generate Button
```html
<div class="action-container">
  <button class="btn-generate" id="generate-btn" disabled>
    <svg class="btn-icon"><!-- Microphone icon --></svg>
    Generate Audio
  </button>
</div>
```

**States:**
- Disabled: Gray, cursor not-allowed (when no text or no reference audio)
- Enabled: Blue gradient, hover effect
- Loading: Spinner animation, text "Generating..."
- Success: Brief green flash, then back to enabled

**Styling:**
```css
.btn-generate {
  width: 100%;
  padding: 16px 32px;
  font-size: 18px;
  font-weight: 600;
  background: linear-gradient(135deg, #0066B4 0%, #01C6FF 100%);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 200ms ease;
}

.btn-generate:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 102, 180, 0.3);
}

.btn-generate:disabled {
  background: #E0E0E0;
  color: #9E9E9E;
  cursor: not-allowed;
}
```

### Card 3: Output Audio - Detailed Specification

#### Header Section with Status
```html
<div class="card-header">
  <h2 class="card-title">
    <span class="icon">🔊</span>
    Generated Audio
  </h2>
  <div class="status-indicator" data-status="idle">
    <span class="status-icon">⏳</span>
    <span class="status-text">Ready</span>
  </div>
</div>
```

**Status States:**
- `idle`: Gray, "Ready"
- `processing`: Blue spinner, "Processing..."
- `success`: Green checkmark, "Finished!"
- `error`: Red X, "Error"

#### Progress Bar (during generation)
```html
<div class="progress-container" hidden>
  <div class="progress-bar">
    <div class="progress-fill" style="width: 0%"></div>
  </div>
  <div class="progress-info">
    <span class="progress-text">Generating audio...</span>
    <span class="progress-time">Est. 15s remaining</span>
  </div>
</div>
```

**Animation:**
- Smooth width transition (100ms)
- Pulse effect on progress fill
- Update every 500ms

#### Audio Player (after generation)
```html
<div class="output-audio-player" hidden>
  <div class="audio-visualization">
    <canvas id="output-waveform" width="800" height="150"></canvas>
  </div>

  <div class="playback-controls">
    <button class="btn-control btn-play" id="output-play">▶️</button>
    <div class="timeline">
      <input type="range" class="timeline-slider" min="0" max="100" value="0">
      <span class="time-current">0:00</span>
      <span class="time-separator">/</span>
      <span class="time-total">0:00</span>
    </div>
    <div class="action-buttons">
      <button class="btn-icon" id="download" title="Download">
        <svg><!-- Download icon --></svg>
      </button>
      <button class="btn-icon" id="share" title="Share">
        <svg><!-- Share icon --></svg>
      </button>
    </div>
  </div>
</div>
```

#### Generation Info
```html
<div class="generation-info" hidden>
  <div class="info-grid">
    <div class="info-item">
      <span class="info-label">Duration:</span>
      <span class="info-value">12.3s</span>
    </div>
    <div class="info-item">
      <span class="info-label">Generated in:</span>
      <span class="info-value">18.5s</span>
    </div>
    <div class="info-item">
      <span class="info-label">Temperature:</span>
      <span class="info-value">0.75</span>
    </div>
    <div class="info-item">
      <span class="info-label">Speed:</span>
      <span class="info-value">1.0x</span>
    </div>
  </div>
</div>
```

**Styling:**
- Grid layout: 2x2 on desktop, 1x4 on mobile
- Light gray background
- 12px font size
- Monospace for values


### Voice Profile Management

#### Floating Action Button
```html
<button class="fab" id="save-profile-btn" title="Save Voice Profile">
  <svg><!-- Save icon --></svg>
  Save Profile
</button>
```

**Position:**
- Fixed: bottom-right corner
- Offset: 24px from bottom, 24px from right
- Z-index: 1000

**Styling:**
```css
.fab {
  position: fixed;
  bottom: 24px;
  right: 24px;
  padding: 16px 24px;
  background: linear-gradient(135deg, #0066B4 0%, #01C6FF 100%);
  color: white;
  border: none;
  border-radius: 50px;
  box-shadow: 0 4px 12px rgba(0, 102, 180, 0.4);
  cursor: pointer;
  transition: all 200ms ease;
}

.fab:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0, 102, 180, 0.5);
}
```

#### Save Profile Modal
```html
<div class="modal" id="save-profile-modal" hidden>
  <div class="modal-overlay"></div>
  <div class="modal-content">
    <div class="modal-header">
      <h3>Save Voice Profile</h3>
      <button class="btn-close">×</button>
    </div>

    <div class="modal-body">
      <div class="form-group">
        <label for="profile-name">Profile Name</label>
        <input
          type="text"
          id="profile-name"
          class="input-text"
          placeholder="my_voice_profile"
          maxlength="50"
        >
      </div>

      <div class="form-group">
        <label for="profile-description">Description (optional)</label>
        <textarea
          id="profile-description"
          class="input-text"
          placeholder="Describe this voice profile..."
          rows="3"
        ></textarea>
      </div>
    </div>

    <div class="modal-footer">
      <button class="btn-secondary" id="cancel-save">Cancel</button>
      <button class="btn-primary" id="confirm-save">Save Profile</button>
    </div>
  </div>
</div>
```

#### Load Profile Modal
```html
<div class="modal" id="load-profile-modal" hidden>
  <div class="modal-overlay"></div>
  <div class="modal-content modal-large">
    <div class="modal-header">
      <h3>Load Voice Profile</h3>
      <button class="btn-close">×</button>
    </div>

    <div class="modal-body">
      <div class="profile-list">
        <!-- Profile items will be dynamically generated -->
        <div class="profile-item">
          <div class="profile-info">
            <h4 class="profile-name">my_voice_profile</h4>
            <p class="profile-meta">Created: 2025-01-25 | Duration: 15.2s</p>
            <p class="profile-description">Professional narrator voice</p>
          </div>
          <div class="profile-actions">
            <button class="btn-icon" title="Preview">
              <svg><!-- Play icon --></svg>
            </button>
            <button class="btn-icon" title="Load">
              <svg><!-- Load icon --></svg>
            </button>
            <button class="btn-icon btn-danger" title="Delete">
              <svg><!-- Trash icon --></svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="modal-footer">
      <button class="btn-secondary" id="cancel-load">Cancel</button>
    </div>
  </div>
</div>
```

**Features:**
- List all saved profiles
- Preview audio sample
- Load profile (populates Card 1)
- Delete profile with confirmation
- Search/filter profiles (if many)

---

## Component Architecture

### Svelte Component Structure

```
src/
├── lib/
│   ├── components/
│   │   ├── ReferenceAudioCard.svelte
│   │   ├── TargetTextCard.svelte
│   │   ├── OutputAudioCard.svelte
│   │   ├── AudioVisualization.svelte
│   │   ├── PlaybackControls.svelte
│   │   ├── ProfileModal.svelte
│   │   └── Toast.svelte
│   ├── stores/
│   │   ├── audioStore.js
│   │   ├── profileStore.js
│   │   └── uiStore.js
│   ├── services/
│   │   ├── api.js
│   │   ├── audioProcessor.js
│   │   └── storage.js
│   └── utils/
│       ├── validators.js
│       ├── formatters.js
│       └── constants.js
├── routes/
│   └── +page.svelte
└── app.html
```

### Component Breakdown

#### 1. ReferenceAudioCard.svelte
```svelte
<script>
  import { audioStore } from '$lib/stores/audioStore';
  import AudioVisualization from './AudioVisualization.svelte';
  import PlaybackControls from './PlaybackControls.svelte';

  let referenceAudio = null;
  let referenceText = '';
  let isExpanded = false;

  async function handleUpload(event) {
    const file = event.target.files[0];
    if (file) {
      referenceAudio = await processAudioFile(file);
      audioStore.setReference(referenceAudio);
    }
  }

  function toggleExpand() {
    isExpanded = !isExpanded;
  }
</script>

<div class="card">
  <div class="card-header">
    <h2>🎵 Reference Audio</h2>
    <div class="actions">
      <button on:click={() => fileInput.click()}>📤 Upload</button>
      <button on:click={toggleExpand}>✏️ Edit</button>
    </div>
  </div>

  {#if referenceAudio}
    <AudioVisualization audio={referenceAudio} />
    <PlaybackControls audio={referenceAudio} />
  {:else}
    <div class="empty-state">
      <p>Upload an audio file to get started</p>
      <button on:click={() => fileInput.click()}>Upload Audio</button>
    </div>
  {/if}

  {#if isExpanded}
    <div class="reference-text" transition:slide>
      <textarea bind:value={referenceText} maxlength="500" />
      <div class="footer">
        <span>{referenceText.length} / 500</span>
        <button on:click={saveReferenceText}>Save</button>
      </div>
    </div>
  {/if}
</div>

<input type="file" bind:this={fileInput} accept="audio/*" hidden />
```

#### 2. TargetTextCard.svelte
```svelte
<script>
  import { audioStore } from '$lib/stores/audioStore';

  let targetText = '';
  let language = 'es';
  let temperature = 0.75;
  let speed = 1.0;
  let showAdvanced = false;
  let isGenerating = false;

  $: charCount = targetText.length;
  $: canGenerate = charCount > 0 && $audioStore.referenceAudio !== null;

  async function generateAudio() {
    if (!canGenerate) return;

    isGenerating = true;
    try {
      const result = await api.generateAudio({
        text: targetText,
        language,
        temperature,
        speed,
        referenceAudio: $audioStore.referenceAudio,
        referenceText: $audioStore.referenceText
      });

      audioStore.setOutput(result);
    } catch (error) {
      console.error('Generation failed:', error);
      // Show error toast
    } finally {
      isGenerating = false;
    }
  }
</script>

<div class="card">
  <div class="card-header">
    <h2>📝 Target Text</h2>
    <span class="char-counter" class:warning={charCount > 450}>
      {charCount} / 500
    </span>
  </div>

  <textarea
    bind:value={targetText}
    maxlength="500"
    placeholder="Enter text to convert to speech..."
  />

  <div class="options">
    <select bind:value={language}>
      <option value="es">Spanish</option>
      <option value="en">English</option>
    </select>

    <button on:click={() => showAdvanced = !showAdvanced}>
      ⚙️ Advanced Settings
    </button>
  </div>

  {#if showAdvanced}
    <div class="advanced" transition:slide>
      <label>
        Temperature: {temperature}
        <input type="range" bind:value={temperature} min="0.5" max="1.0" step="0.05" />
      </label>
      <label>
        Speed: {speed}x
        <input type="range" bind:value={speed} min="0.8" max="1.2" step="0.05" />
      </label>
    </div>
  {/if}

  <button
    class="btn-generate"
    disabled={!canGenerate || isGenerating}
    on:click={generateAudio}
  >
    {#if isGenerating}
      <Spinner /> Generating...
    {:else}
      🎙️ Generate Audio
    {/if}
  </button>
</div>
```

#### 3. OutputAudioCard.svelte
```svelte
<script>
  import { audioStore } from '$lib/stores/audioStore';
  import AudioVisualization from './AudioVisualization.svelte';
  import PlaybackControls from './PlaybackControls.svelte';

  $: outputAudio = $audioStore.outputAudio;
  $: status = $audioStore.status;
  $: progress = $audioStore.progress;

  function downloadAudio() {
    const url = URL.createObjectURL(outputAudio.blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `generated_${Date.now()}.wav`;
    a.click();
  }
</script>

<div class="card">
  <div class="card-header">
    <h2>🔊 Generated Audio</h2>
    <div class="status" data-status={status}>
      {#if status === 'processing'}
        <Spinner /> Processing...
      {:else if status === 'success'}
        ✅ Finished!
      {:else if status === 'error'}
        ❌ Error
      {:else}
        ⏳ Ready
      {/if}
    </div>
  </div>

  {#if status === 'processing'}
    <div class="progress">
      <div class="progress-bar" style="width: {progress}%"></div>
      <p>Generating audio... Est. {estimatedTime}s remaining</p>
    </div>
  {/if}

  {#if outputAudio}
    <AudioVisualization audio={outputAudio} />
    <PlaybackControls audio={outputAudio} />

    <div class="actions">
      <button on:click={downloadAudio}>⬇️ Download</button>
      <button>🔗 Share</button>
    </div>

    <div class="info">
      <span>Duration: {outputAudio.duration}s</span>
      <span>Generated in: {outputAudio.generationTime}s</span>
    </div>
  {/if}
</div>
```


### Svelte Stores

#### audioStore.js
```javascript
import { writable, derived } from 'svelte/store';

function createAudioStore() {
  const { subscribe, set, update } = writable({
    referenceAudio: null,
    referenceText: '',
    outputAudio: null,
    status: 'idle', // idle, processing, success, error
    progress: 0,
    error: null
  });

  return {
    subscribe,
    setReference: (audio) => update(state => ({ ...state, referenceAudio: audio })),
    setReferenceText: (text) => update(state => ({ ...state, referenceText: text })),
    setOutput: (audio) => update(state => ({ ...state, outputAudio: audio, status: 'success' })),
    setStatus: (status) => update(state => ({ ...state, status })),
    setProgress: (progress) => update(state => ({ ...state, progress })),
    setError: (error) => update(state => ({ ...state, error, status: 'error' })),
    reset: () => set({
      referenceAudio: null,
      referenceText: '',
      outputAudio: null,
      status: 'idle',
      progress: 0,
      error: null
    })
  };
}

export const audioStore = createAudioStore();
```

#### profileStore.js
```javascript
import { writable } from 'svelte/store';
import { api } from '$lib/services/api';

function createProfileStore() {
  const { subscribe, set, update } = writable({
    profiles: [],
    currentProfile: null,
    loading: false
  });

  return {
    subscribe,
    loadProfiles: async () => {
      update(state => ({ ...state, loading: true }));
      try {
        const profiles = await api.getProfiles();
        update(state => ({ ...state, profiles, loading: false }));
      } catch (error) {
        console.error('Failed to load profiles:', error);
        update(state => ({ ...state, loading: false }));
      }
    },
    saveProfile: async (profile) => {
      try {
        const saved = await api.saveProfile(profile);
        update(state => ({
          ...state,
          profiles: [...state.profiles, saved],
          currentProfile: saved
        }));
        return saved;
      } catch (error) {
        console.error('Failed to save profile:', error);
        throw error;
      }
    },
    loadProfile: async (profileId) => {
      try {
        const profile = await api.getProfile(profileId);
        update(state => ({ ...state, currentProfile: profile }));
        return profile;
      } catch (error) {
        console.error('Failed to load profile:', error);
        throw error;
      }
    },
    deleteProfile: async (profileId) => {
      try {
        await api.deleteProfile(profileId);
        update(state => ({
          ...state,
          profiles: state.profiles.filter(p => p.id !== profileId),
          currentProfile: state.currentProfile?.id === profileId ? null : state.currentProfile
        }));
      } catch (error) {
        console.error('Failed to delete profile:', error);
        throw error;
      }
    }
  };
}

export const profileStore = createProfileStore();
```

---

## Django API Design

### API Endpoints

#### Base URL
```
http://localhost:8000/api/v1/
```

#### Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/audio/upload` | Upload reference audio |
| POST | `/audio/generate` | Generate audio from text |
| GET | `/profiles` | List all profiles |
| POST | `/profiles` | Create new profile |
| GET | `/profiles/:id` | Get profile details |
| PUT | `/profiles/:id` | Update profile |
| DELETE | `/profiles/:id` | Delete profile |
| GET | `/audio/:id` | Download audio file |

### Detailed API Specifications

#### 1. Upload Reference Audio
```http
POST /api/v1/audio/upload
Content-Type: multipart/form-data

Request Body:
- file: audio file (WAV, MP3, M4A, FLAC)
- reference_text: string (optional)

Response (200 OK):
{
  "id": "uuid",
  "filename": "reference_audio.wav",
  "duration": 15.2,
  "sample_rate": 12000,
  "channels": 1,
  "url": "/api/v1/audio/uuid",
  "waveform_data": [...],  // For visualization
  "spectrogram_data": [...] // For visualization
}

Response (400 Bad Request):
{
  "error": "Invalid audio format",
  "details": "Only WAV, MP3, M4A, FLAC are supported"
}
```

#### 2. Generate Audio
```http
POST /api/v1/audio/generate
Content-Type: application/json

Request Body:
{
  "text": "Hola, bienvenidos a este tutorial.",
  "reference_audio_id": "uuid",
  "reference_text": "Hola, esta es mi voz.",
  "language": "es",
  "temperature": 0.75,
  "speed": 1.0
}

Response (200 OK):
{
  "id": "uuid",
  "audio_url": "/api/v1/audio/uuid",
  "duration": 12.3,
  "generation_time": 18.5,
  "waveform_data": [...],
  "settings": {
    "temperature": 0.75,
    "speed": 1.0,
    "language": "es"
  }
}

Response (400 Bad Request):
{
  "error": "Text too long",
  "details": "Maximum 500 characters allowed"
}

Response (500 Internal Server Error):
{
  "error": "Generation failed",
  "details": "Model inference error"
}
```

#### 3. List Profiles
```http
GET /api/v1/profiles

Response (200 OK):
{
  "profiles": [
    {
      "id": "uuid",
      "name": "my_voice_profile",
      "description": "Professional narrator voice",
      "created_at": "2025-01-25T10:30:00Z",
      "reference_audio_id": "uuid",
      "reference_text": "Hola, esta es mi voz.",
      "duration": 15.2
    }
  ]
}
```

#### 4. Create Profile
```http
POST /api/v1/profiles
Content-Type: application/json

Request Body:
{
  "name": "my_voice_profile",
  "description": "Professional narrator voice",
  "reference_audio_id": "uuid",
  "reference_text": "Hola, esta es mi voz.",
  "language": "es"
}

Response (201 Created):
{
  "id": "uuid",
  "name": "my_voice_profile",
  "description": "Professional narrator voice",
  "created_at": "2025-01-25T10:30:00Z",
  "reference_audio_id": "uuid",
  "reference_text": "Hola, esta es mi voz.",
  "language": "es"
}

Response (400 Bad Request):
{
  "error": "Profile name already exists",
  "details": "Choose a different name"
}
```

#### 5. Get Profile
```http
GET /api/v1/profiles/:id

Response (200 OK):
{
  "id": "uuid",
  "name": "my_voice_profile",
  "description": "Professional narrator voice",
  "created_at": "2025-01-25T10:30:00Z",
  "reference_audio": {
    "id": "uuid",
    "url": "/api/v1/audio/uuid",
    "duration": 15.2,
    "waveform_data": [...]
  },
  "reference_text": "Hola, esta es mi voz.",
  "language": "es"
}

Response (404 Not Found):
{
  "error": "Profile not found"
}
```

#### 6. Delete Profile
```http
DELETE /api/v1/profiles/:id

Response (204 No Content):
(empty body)

Response (404 Not Found):
{
  "error": "Profile not found"
}
```

#### 7. Download Audio
```http
GET /api/v1/audio/:id

Response (200 OK):
Content-Type: audio/wav
Content-Disposition: attachment; filename="audio.wav"
(binary audio data)

Response (404 Not Found):
{
  "error": "Audio file not found"
}
```

### Django Project Structure

```
backend/
├── manage.py
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── voice_api/
│   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── services/
│       ├── __init__.py
│       ├── audio_processor.py
│       ├── generator.py
│       └── storage.py
└── requirements.txt
```

### Django Models

```python
# voice_api/models.py
from django.db import models
import uuid

class AudioFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    filename = models.CharField(max_length=255)
    file = models.FileField(upload_to='audio/')
    duration = models.FloatField()
    sample_rate = models.IntegerField()
    channels = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'audio_files'

class VoiceProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    reference_audio = models.ForeignKey(AudioFile, on_delete=models.CASCADE)
    reference_text = models.TextField()
    language = models.CharField(max_length=10, default='es')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'voice_profiles'
        ordering = ['-created_at']

class GeneratedAudio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(VoiceProfile, on_delete=models.SET_NULL, null=True)
    text = models.TextField()
    audio_file = models.ForeignKey(AudioFile, on_delete=models.CASCADE)
    temperature = models.FloatField()
    speed = models.FloatField()
    generation_time = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'generated_audio'
        ordering = ['-created_at']
```


### Django Views (API Endpoints)

```python
# voice_api/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import FileResponse
from .models import AudioFile, VoiceProfile, GeneratedAudio
from .serializers import AudioFileSerializer, VoiceProfileSerializer
from .services.audio_processor import AudioProcessor
from .services.generator import AudioGenerator

class AudioViewSet(viewsets.ViewSet):
    parser_classes = (MultiPartParser, FormParser)

    @action(detail=False, methods=['post'])
    def upload(self, request):
        """Upload reference audio file"""
        file = request.FILES.get('file')
        reference_text = request.data.get('reference_text', '')

        if not file:
            return Response(
                {'error': 'No file provided'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Process audio file
            processor = AudioProcessor()
            audio_data = processor.process_upload(file)

            # Save to database
            audio_file = AudioFile.objects.create(
                filename=file.name,
                file=file,
                duration=audio_data['duration'],
                sample_rate=audio_data['sample_rate'],
                channels=audio_data['channels']
            )

            # Generate visualization data
            waveform = processor.generate_waveform(audio_file.file.path)
            spectrogram = processor.generate_spectrogram(audio_file.file.path)

            return Response({
                'id': str(audio_file.id),
                'filename': audio_file.filename,
                'duration': audio_file.duration,
                'sample_rate': audio_file.sample_rate,
                'channels': audio_file.channels,
                'url': f'/api/v1/audio/{audio_file.id}',
                'waveform_data': waveform,
                'spectrogram_data': spectrogram
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': 'Failed to process audio', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'])
    def generate(self, request):
        """Generate audio from text"""
        text = request.data.get('text')
        reference_audio_id = request.data.get('reference_audio_id')
        reference_text = request.data.get('reference_text')
        language = request.data.get('language', 'es')
        temperature = float(request.data.get('temperature', 0.75))
        speed = float(request.data.get('speed', 1.0))

        # Validation
        if not text:
            return Response(
                {'error': 'Text is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if len(text) > 500:
            return Response(
                {'error': 'Text too long', 'details': 'Maximum 500 characters'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not reference_audio_id:
            return Response(
                {'error': 'Reference audio is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Get reference audio
            reference_audio = AudioFile.objects.get(id=reference_audio_id)

            # Generate audio
            generator = AudioGenerator()
            result = generator.generate(
                text=text,
                reference_audio_path=reference_audio.file.path,
                reference_text=reference_text,
                language=language,
                temperature=temperature,
                speed=speed
            )

            # Save generated audio
            audio_file = AudioFile.objects.create(
                filename=f'generated_{result["id"]}.wav',
                file=result['file_path'],
                duration=result['duration'],
                sample_rate=12000,
                channels=1
            )

            # Save generation record
            generated = GeneratedAudio.objects.create(
                text=text,
                audio_file=audio_file,
                temperature=temperature,
                speed=speed,
                generation_time=result['generation_time']
            )

            # Generate waveform
            processor = AudioProcessor()
            waveform = processor.generate_waveform(audio_file.file.path)

            return Response({
                'id': str(audio_file.id),
                'audio_url': f'/api/v1/audio/{audio_file.id}',
                'duration': audio_file.duration,
                'generation_time': result['generation_time'],
                'waveform_data': waveform,
                'settings': {
                    'temperature': temperature,
                    'speed': speed,
                    'language': language
                }
            }, status=status.HTTP_200_OK)

        except AudioFile.DoesNotExist:
            return Response(
                {'error': 'Reference audio not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': 'Generation failed', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, pk=None):
        """Download audio file"""
        try:
            audio_file = AudioFile.objects.get(id=pk)
            return FileResponse(
                audio_file.file.open('rb'),
                content_type='audio/wav',
                as_attachment=True,
                filename=audio_file.filename
            )
        except AudioFile.DoesNotExist:
            return Response(
                {'error': 'Audio file not found'},
                status=status.HTTP_404_NOT_FOUND
            )

class VoiceProfileViewSet(viewsets.ModelViewSet):
    queryset = VoiceProfile.objects.all()
    serializer_class = VoiceProfileSerializer

    def list(self, request):
        """List all profiles"""
        profiles = self.get_queryset()
        serializer = self.get_serializer(profiles, many=True)
        return Response({'profiles': serializer.data})

    def create(self, request):
        """Create new profile"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Get profile details"""
        try:
            profile = self.get_queryset().get(id=pk)
            serializer = self.get_serializer(profile)

            # Include reference audio data
            processor = AudioProcessor()
            waveform = processor.generate_waveform(profile.reference_audio.file.path)

            data = serializer.data
            data['reference_audio']['waveform_data'] = waveform

            return Response(data)
        except VoiceProfile.DoesNotExist:
            return Response(
                {'error': 'Profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    def destroy(self, request, pk=None):
        """Delete profile"""
        try:
            profile = self.get_queryset().get(id=pk)
            profile.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except VoiceProfile.DoesNotExist:
            return Response(
                {'error': 'Profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )
```

### Django Services

```python
# voice_api/services/audio_processor.py
import librosa
import numpy as np
import soundfile as sf
from pathlib import Path

class AudioProcessor:
    def process_upload(self, file):
        """Process uploaded audio file"""
        # Save temporarily
        temp_path = f'/tmp/{file.name}'
        with open(temp_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # Load and analyze
        audio, sr = librosa.load(temp_path, sr=None)
        duration = librosa.get_duration(y=audio, sr=sr)

        # Convert to mono if stereo
        if len(audio.shape) > 1:
            audio = librosa.to_mono(audio)

        # Resample to 12000 Hz if needed
        if sr != 12000:
            audio = librosa.resample(audio, orig_sr=sr, target_sr=12000)
            sr = 12000

        # Save processed audio
        sf.write(temp_path, audio, sr)

        return {
            'duration': duration,
            'sample_rate': sr,
            'channels': 1
        }

    def generate_waveform(self, audio_path, num_points=800):
        """Generate waveform data for visualization"""
        audio, sr = librosa.load(audio_path, sr=None)

        # Downsample for visualization
        step = len(audio) // num_points
        waveform = audio[::step][:num_points]

        # Normalize to -1 to 1
        waveform = waveform / np.max(np.abs(waveform))

        return waveform.tolist()

    def generate_spectrogram(self, audio_path, n_mels=128):
        """Generate mel spectrogram for visualization"""
        audio, sr = librosa.load(audio_path, sr=None)

        # Compute mel spectrogram
        mel_spec = librosa.feature.melspectrogram(
            y=audio,
            sr=sr,
            n_mels=n_mels,
            fmax=8000
        )

        # Convert to dB
        mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)

        # Downsample for web display
        mel_spec_db = mel_spec_db[:, ::4]  # Reduce time resolution

        return mel_spec_db.tolist()
```

```python
# voice_api/services/generator.py
from pathlib import Path
import time
from voice_clone.model.qwen3_generator import Qwen3Generator
from voice_clone.model.qwen3_manager import Qwen3ModelManager
from voice_clone.config import ConfigManager

class AudioGenerator:
    def __init__(self):
        self.config = ConfigManager.load_config()
        self.model_manager = Qwen3ModelManager(self.config)

        # Load model on initialization
        if not self.model_manager.is_loaded():
            self.model_manager.load_model()

        self.generator = Qwen3Generator(self.model_manager, self.config)

    def generate(self, text, reference_audio_path, reference_text, language='es', temperature=0.75, speed=1.0):
        """Generate audio from text"""
        start_time = time.time()

        # Generate output path
        output_dir = Path('data/outputs')
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f'generated_{int(time.time())}.wav'

        # Generate audio
        success = self.generator.generate_to_file(
            text=text,
            ref_audio=Path(reference_audio_path),
            ref_text=reference_text,
            output_path=output_path,
            language=language
        )

        if not success:
            raise Exception('Audio generation failed')

        # Calculate duration
        import soundfile as sf
        audio_data, sample_rate = sf.read(output_path)
        duration = len(audio_data) / sample_rate

        generation_time = time.time() - start_time

        return {
            'id': output_path.stem,
            'file_path': str(output_path),
            'duration': duration,
            'generation_time': generation_time
        }
```


---

## Color Palette & Styling

### Primary Colors

```css
:root {
  /* Primary Blue */
  --color-primary: #0066B4;
  --color-primary-light: #0080E0;
  --color-primary-dark: #004D8A;

  /* Secondary Cyan */
  --color-secondary: #01C6FF;
  --color-secondary-light: #33D4FF;
  --color-secondary-dark: #00A8D9;

  /* Accent */
  --color-accent: #00D9FF;

  /* Gradients */
  --gradient-primary: linear-gradient(135deg, #0066B4 0%, #01C6FF 100%);
  --gradient-secondary: linear-gradient(135deg, #01C6FF 0%, #00D9FF 100%);
}
```

### Neutral Colors

```css
:root {
  /* Background */
  --color-bg-primary: #F5F7FA;
  --color-bg-secondary: #FFFFFF;
  --color-bg-tertiary: #E8EDF2;

  /* Text */
  --color-text-primary: #2C3E50;
  --color-text-secondary: #5A6C7D;
  --color-text-tertiary: #8B9AA8;
  --color-text-inverse: #FFFFFF;

  /* Borders */
  --color-border-light: #E0E6ED;
  --color-border-medium: #CBD5E0;
  --color-border-dark: #A0AEC0;
}
```

### Semantic Colors

```css
:root {
  /* Success */
  --color-success: #10B981;
  --color-success-light: #34D399;
  --color-success-dark: #059669;

  /* Warning */
  --color-warning: #F59E0B;
  --color-warning-light: #FBBF24;
  --color-warning-dark: #D97706;

  /* Error */
  --color-error: #EF4444;
  --color-error-light: #F87171;
  --color-error-dark: #DC2626;

  /* Info */
  --color-info: #3B82F6;
  --color-info-light: #60A5FA;
  --color-info-dark: #2563EB;
}
```

### Typography

```css
:root {
  /* Font Families */
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-mono: 'SF Mono', 'Fira Code', 'Consolas', monospace;

  /* Font Sizes */
  --text-xs: 0.75rem;    /* 12px */
  --text-sm: 0.875rem;   /* 14px */
  --text-base: 1rem;     /* 16px */
  --text-lg: 1.125rem;   /* 18px */
  --text-xl: 1.25rem;    /* 20px */
  --text-2xl: 1.5rem;    /* 24px */
  --text-3xl: 1.875rem;  /* 30px */
  --text-4xl: 2.25rem;   /* 36px */

  /* Font Weights */
  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;

  /* Line Heights */
  --leading-tight: 1.25;
  --leading-normal: 1.5;
  --leading-relaxed: 1.75;
}
```

### Spacing

```css
:root {
  --space-1: 0.25rem;   /* 4px */
  --space-2: 0.5rem;    /* 8px */
  --space-3: 0.75rem;   /* 12px */
  --space-4: 1rem;      /* 16px */
  --space-5: 1.25rem;   /* 20px */
  --space-6: 1.5rem;    /* 24px */
  --space-8: 2rem;      /* 32px */
  --space-10: 2.5rem;   /* 40px */
  --space-12: 3rem;     /* 48px */
  --space-16: 4rem;     /* 64px */
}
```

### Shadows

```css
:root {
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-base: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);

  /* Colored shadows for buttons */
  --shadow-primary: 0 4px 12px rgba(0, 102, 180, 0.3);
  --shadow-primary-lg: 0 8px 20px rgba(0, 102, 180, 0.4);
}
```

### Border Radius

```css
:root {
  --radius-sm: 0.25rem;   /* 4px */
  --radius-base: 0.375rem; /* 6px */
  --radius-md: 0.5rem;    /* 8px */
  --radius-lg: 0.75rem;   /* 12px */
  --radius-xl: 1rem;      /* 16px */
  --radius-full: 9999px;  /* Fully rounded */
}
```

### Transitions

```css
:root {
  --transition-fast: 100ms ease;
  --transition-base: 200ms ease;
  --transition-slow: 300ms ease;
  --transition-slower: 500ms ease;

  --ease-in: cubic-bezier(0.4, 0, 1, 1);
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
}
```

### Component Styles

#### Card
```css
.card {
  background: var(--color-bg-secondary);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-base);
  padding: var(--space-6);
  margin-bottom: var(--space-6);
  transition: box-shadow var(--transition-base);
}

.card:hover {
  box-shadow: var(--shadow-md);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-4);
}

.card-title {
  font-size: var(--text-2xl);
  font-weight: var(--font-bold);
  color: var(--color-text-primary);
  display: flex;
  align-items: center;
  gap: var(--space-2);
}
```

#### Buttons
```css
.btn {
  padding: var(--space-3) var(--space-6);
  border-radius: var(--radius-md);
  font-weight: var(--font-semibold);
  font-size: var(--text-base);
  cursor: pointer;
  transition: all var(--transition-base);
  border: none;
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
}

.btn-primary {
  background: var(--gradient-primary);
  color: var(--color-text-inverse);
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: var(--shadow-primary);
}

.btn-secondary {
  background: var(--color-bg-tertiary);
  color: var(--color-text-primary);
}

.btn-secondary:hover:not(:disabled) {
  background: var(--color-border-medium);
}

.btn-icon {
  padding: var(--space-2);
  border-radius: var(--radius-base);
  background: transparent;
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
  border: none;
}

.btn-icon:hover {
  background: var(--color-bg-tertiary);
  color: var(--color-primary);
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
```

#### Inputs
```css
.input-text,
.textarea {
  width: 100%;
  padding: var(--space-3) var(--space-4);
  border: 1px solid var(--color-border-medium);
  border-radius: var(--radius-md);
  font-size: var(--text-base);
  font-family: var(--font-sans);
  color: var(--color-text-primary);
  background: var(--color-bg-secondary);
  transition: all var(--transition-base);
}

.input-text:focus,
.textarea:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(0, 102, 180, 0.1);
}

.textarea {
  resize: vertical;
  min-height: 120px;
}

.select-input {
  padding: var(--space-3) var(--space-4);
  border: 1px solid var(--color-border-medium);
  border-radius: var(--radius-md);
  font-size: var(--text-base);
  background: var(--color-bg-secondary);
  cursor: pointer;
}
```

---

## Responsive Design

### Breakpoints

```css
:root {
  --breakpoint-sm: 640px;   /* Mobile landscape */
  --breakpoint-md: 768px;   /* Tablet */
  --breakpoint-lg: 1024px;  /* Desktop */
  --breakpoint-xl: 1280px;  /* Large desktop */
}
```

### Mobile-First Approach

```css
/* Base styles (mobile) */
.container {
  padding: var(--space-4);
  max-width: 100%;
}

/* Tablet and up */
@media (min-width: 768px) {
  .container {
    padding: var(--space-6);
    max-width: 768px;
    margin: 0 auto;
  }
}

/* Desktop and up */
@media (min-width: 1024px) {
  .container {
    padding: var(--space-8);
    max-width: 1024px;
  }
}
```

### Responsive Card Layout

```css
/* Mobile: Stack cards vertically */
.cards-container {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

/* Tablet: Still stacked but with more spacing */
@media (min-width: 768px) {
  .cards-container {
    gap: var(--space-6);
  }
}

/* Desktop: Optional side-by-side for some cards */
@media (min-width: 1024px) {
  .cards-container {
    gap: var(--space-8);
  }

  /* Keep vertical layout for main workflow */
  /* But allow horizontal for profile management */
}
```

### Responsive Typography

```css
/* Mobile */
.card-title {
  font-size: var(--text-xl);
}

/* Tablet and up */
@media (min-width: 768px) {
  .card-title {
    font-size: var(--text-2xl);
  }
}

/* Desktop and up */
@media (min-width: 1024px) {
  .card-title {
    font-size: var(--text-3xl);
  }
}
```

### Touch-Friendly Targets

```css
/* Minimum 44x44px touch targets for mobile */
.btn-icon {
  min-width: 44px;
  min-height: 44px;
}

/* Larger tap areas on mobile */
@media (max-width: 767px) {
  .playback-controls button {
    min-width: 48px;
    min-height: 48px;
  }
}
```

---

## Accessibility Requirements

### ARIA Labels

```html
<!-- Buttons -->
<button aria-label="Upload new audio file">
  <svg aria-hidden="true"><!-- Icon --></svg>
</button>

<!-- Form inputs -->
<label for="target-text">Target Text</label>
<textarea
  id="target-text"
  aria-describedby="char-counter"
  aria-required="true"
></textarea>
<span id="char-counter" role="status" aria-live="polite">
  0 / 500 characters
</span>

<!-- Status indicators -->
<div role="status" aria-live="polite" aria-atomic="true">
  <span class="sr-only">Audio generation in progress</span>
  Processing...
</div>
```

### Keyboard Navigation

```javascript
// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
  // Space: Play/Pause
  if (e.code === 'Space' && e.target.tagName !== 'TEXTAREA') {
    e.preventDefault();
    togglePlayback();
  }

  // Ctrl/Cmd + Enter: Generate audio
  if ((e.ctrlKey || e.metaKey) && e.code === 'Enter') {
    e.preventDefault();
    generateAudio();
  }

  // Escape: Close modals
  if (e.code === 'Escape') {
    closeAllModals();
  }
});
```

### Focus Management

```css
/* Visible focus indicators */
*:focus {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* Skip to main content link */
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: var(--color-primary);
  color: white;
  padding: var(--space-2) var(--space-4);
  text-decoration: none;
  z-index: 9999;
}

.skip-link:focus {
  top: 0;
}
```

### Screen Reader Support

```html
<!-- Screen reader only text -->
<span class="sr-only">
  Audio generation completed successfully
</span>

<!-- CSS for sr-only -->
<style>
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
</style>
```

### Color Contrast

```css
/* Ensure WCAG AA compliance (4.5:1 for normal text) */
:root {
  /* Text on white background */
  --color-text-primary: #2C3E50;  /* 12.6:1 */
  --color-text-secondary: #5A6C7D; /* 7.2:1 */

  /* White text on primary blue */
  --color-primary: #0066B4;  /* 4.6:1 with white */
}

/* High contrast mode support */
@media (prefers-contrast: high) {
  :root {
    --color-text-primary: #000000;
    --color-border-medium: #000000;
  }
}
```

### Reduced Motion

```css
/* Respect user's motion preferences */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```


---

## Implementation Roadmap

### Phase 1: Setup & Foundation (Week 1)

#### 1.1 Project Initialization
- [ ] Create Svelte project with SvelteKit
- [ ] Set up Tailwind CSS (or custom CSS)
- [ ] Configure build tools (Vite)
- [ ] Set up TypeScript (optional but recommended)
- [ ] Initialize Git repository

```bash
# Create SvelteKit project
npm create svelte@latest voice-clone-ui
cd voice-clone-ui
npm install

# Install Tailwind CSS
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Install additional dependencies
npm install wavesurfer.js
npm install axios
```

#### 1.2 Django Backend Setup
- [ ] Create Django project
- [ ] Set up Django REST Framework
- [ ] Configure CORS for local development
- [ ] Create database models
- [ ] Set up media file handling

```bash
# Create Django project
django-admin startproject voice_backend
cd voice_backend
python manage.py startapp voice_api

# Install dependencies
pip install djangorestframework
pip install django-cors-headers
pip install librosa soundfile
```

#### 1.3 Project Structure
- [ ] Create component directory structure
- [ ] Set up stores (Svelte stores)
- [ ] Create service layer for API calls
- [ ] Set up routing (if needed)

### Phase 2: Core Components (Week 2)

#### 2.1 Reference Audio Card
- [ ] Create ReferenceAudioCard component
- [ ] Implement file upload functionality
- [ ] Add audio visualization (waveform + spectrogram)
- [ ] Implement playback controls
- [ ] Add reference text input section
- [ ] Connect to Django upload endpoint

#### 2.2 Target Text Card
- [ ] Create TargetTextCard component
- [ ] Implement text input with character counter
- [ ] Add language selector
- [ ] Create advanced settings panel
- [ ] Add validation logic
- [ ] Style generate button with states

#### 2.3 Output Audio Card
- [ ] Create OutputAudioCard component
- [ ] Implement status indicator
- [ ] Add progress bar for generation
- [ ] Create audio player with waveform
- [ ] Add download functionality
- [ ] Display generation info

### Phase 3: Audio Visualization (Week 3)

#### 3.1 Waveform Component
- [ ] Create AudioVisualization component
- [ ] Implement Canvas-based waveform rendering
- [ ] Add real-time playback cursor
- [ ] Implement click-to-seek functionality
- [ ] Add zoom controls (optional)

#### 3.2 Spectrogram Component
- [ ] Implement mel spectrogram visualization
- [ ] Add color gradient mapping
- [ ] Optimize rendering performance
- [ ] Add frequency axis labels

#### 3.3 Playback Controls
- [ ] Create PlaybackControls component
- [ ] Implement play/pause toggle
- [ ] Add timeline scrubber
- [ ] Implement rewind/forward buttons
- [ ] Add volume control
- [ ] Create trim/cut modal (optional)

### Phase 4: Profile Management (Week 4)

#### 4.1 Save Profile Modal
- [ ] Create ProfileModal component
- [ ] Implement save profile form
- [ ] Add validation
- [ ] Connect to Django save endpoint
- [ ] Show success/error feedback

#### 4.2 Load Profile Modal
- [ ] Create profile list view
- [ ] Implement profile preview
- [ ] Add load functionality
- [ ] Implement delete with confirmation
- [ ] Add search/filter (if many profiles)

#### 4.3 Profile Store
- [ ] Create profileStore
- [ ] Implement CRUD operations
- [ ] Add local caching
- [ ] Handle profile state management

### Phase 5: API Integration (Week 5)

#### 5.1 Django API Endpoints
- [ ] Implement upload audio endpoint
- [ ] Create generate audio endpoint
- [ ] Add profile CRUD endpoints
- [ ] Implement audio download endpoint
- [ ] Add error handling

#### 5.2 Svelte API Service
- [ ] Create API service layer
- [ ] Implement upload with progress
- [ ] Add generation with polling/websocket
- [ ] Handle errors gracefully
- [ ] Add retry logic

#### 5.3 Real-time Updates
- [ ] Implement WebSocket for generation progress (optional)
- [ ] Add polling fallback
- [ ] Update UI in real-time
- [ ] Handle connection errors

### Phase 6: Polish & Testing (Week 6)

#### 6.1 UI Polish
- [ ] Refine animations and transitions
- [ ] Add loading states
- [ ] Implement toast notifications
- [ ] Add empty states
- [ ] Improve error messages

#### 6.2 Responsive Design
- [ ] Test on mobile devices
- [ ] Optimize for tablet
- [ ] Ensure desktop experience
- [ ] Fix layout issues

#### 6.3 Accessibility
- [ ] Add ARIA labels
- [ ] Test keyboard navigation
- [ ] Verify screen reader support
- [ ] Check color contrast
- [ ] Test with accessibility tools

#### 6.4 Testing
- [ ] Write unit tests for components
- [ ] Add integration tests
- [ ] Test API endpoints
- [ ] Perform end-to-end testing
- [ ] Load testing for audio generation

### Phase 7: Deployment (Week 7)

#### 7.1 Build Optimization
- [ ] Optimize bundle size
- [ ] Implement code splitting
- [ ] Compress assets
- [ ] Add service worker (optional)

#### 7.2 Local Deployment
- [ ] Create Docker setup (optional)
- [ ] Write deployment scripts
- [ ] Document setup process
- [ ] Create user guide

#### 7.3 Documentation
- [ ] Update README
- [ ] Create API documentation
- [ ] Write component documentation
- [ ] Add troubleshooting guide

---

## Migration from Gradio

### Step-by-Step Migration

#### 1. Parallel Development
- Keep Gradio UI running during Svelte development
- Test new UI alongside old UI
- Gradually migrate features

#### 2. Feature Parity Checklist
- [ ] Upload audio samples → Reference Audio Card
- [ ] Validate samples → Integrated in upload
- [ ] Create voice profile → Save Profile Modal
- [ ] Select profile → Load Profile Modal
- [ ] Generate audio → Target Text Card + Output Card
- [ ] Batch processing → Future enhancement (not in MVP)

#### 3. Data Migration
- [ ] Convert existing voice profiles to new format
- [ ] Migrate audio files to new storage structure
- [ ] Update file paths in database

#### 4. Testing Migration
- [ ] Test with existing profiles
- [ ] Verify audio generation works
- [ ] Check file compatibility
- [ ] Validate all workflows

#### 5. Cutover
- [ ] Announce new UI to users
- [ ] Provide migration guide
- [ ] Keep Gradio as fallback (temporary)
- [ ] Monitor for issues
- [ ] Deprecate Gradio after stable period

---

## Technical Considerations

### Performance Optimization

#### 1. Audio Processing
```javascript
// Use Web Workers for heavy processing
const worker = new Worker('audio-processor.worker.js');

worker.postMessage({
  type: 'generate-waveform',
  audioData: audioBuffer
});

worker.onmessage = (e) => {
  const waveformData = e.data;
  renderWaveform(waveformData);
};
```

#### 2. Lazy Loading
```javascript
// Lazy load heavy components
const AudioVisualization = lazy(() => import('./AudioVisualization.svelte'));
const ProfileModal = lazy(() => import('./ProfileModal.svelte'));
```

#### 3. Debouncing
```javascript
// Debounce character counter updates
import { debounce } from 'lodash-es';

const updateCharCount = debounce((text) => {
  charCount = text.length;
}, 100);
```

### Error Handling

#### 1. API Errors
```javascript
async function generateAudio() {
  try {
    const result = await api.generateAudio(params);
    audioStore.setOutput(result);
  } catch (error) {
    if (error.response?.status === 400) {
      showToast('Invalid input. Please check your text.', 'error');
    } else if (error.response?.status === 500) {
      showToast('Server error. Please try again.', 'error');
    } else {
      showToast('Network error. Check your connection.', 'error');
    }
  }
}
```

#### 2. File Upload Errors
```javascript
function validateAudioFile(file) {
  const validTypes = ['audio/wav', 'audio/mp3', 'audio/m4a', 'audio/flac'];
  const maxSize = 50 * 1024 * 1024; // 50MB

  if (!validTypes.includes(file.type)) {
    throw new Error('Invalid file type. Please upload WAV, MP3, M4A, or FLAC.');
  }

  if (file.size > maxSize) {
    throw new Error('File too large. Maximum size is 50MB.');
  }
}
```

### Security Considerations

#### 1. Input Validation
```javascript
// Sanitize text input
function sanitizeText(text) {
  return text
    .trim()
    .replace(/<script[^>]*>.*?<\/script>/gi, '')
    .substring(0, 500);
}
```

#### 2. File Upload Security
```python
# Django: Validate file type
def validate_audio_file(file):
    valid_extensions = ['.wav', '.mp3', '.m4a', '.flac']
    ext = os.path.splitext(file.name)[1].lower()

    if ext not in valid_extensions:
        raise ValidationError('Invalid file type')

    # Check magic bytes
    file.seek(0)
    header = file.read(12)
    # Validate audio file header...
```

#### 3. CORS Configuration
```python
# Django settings.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Svelte dev server
    "http://localhost:3000",
]

CORS_ALLOW_CREDENTIALS = True
```

---

## Future Enhancements

### Phase 8: Advanced Features (Future)

#### 1. Batch Processing
- Upload script file
- Process multiple segments
- Download all generated files
- Progress tracking for batch

#### 2. Voice Editing
- Trim audio samples
- Adjust volume
- Remove noise
- Apply filters

#### 3. Advanced Settings
- More TTS parameters
- Voice style controls
- Emotion selection
- Prosody adjustments

#### 4. History & Library
- Generation history
- Favorite profiles
- Audio library
- Search and filter

#### 5. Export Options
- Multiple format export (MP3, AAC, FLAC)
- Quality settings
- Metadata embedding
- Batch export

#### 6. Collaboration (Optional)
- Share profiles
- Export/import profiles
- Cloud sync (optional)

---

## Conclusion

This specification provides a comprehensive blueprint for building a modern Svelte + Django voice cloning UI to replace the current Gradio implementation. The design focuses on:

- **User Experience**: Clean, intuitive single-page interface
- **Performance**: Optimized audio processing and visualization
- **Accessibility**: WCAG AA compliant with keyboard navigation
- **Maintainability**: Modular component architecture
- **Scalability**: Easy to extend with new features

### Next Steps

1. **Review this specification** with the team
2. **Use Google Stitch** to generate initial HTML/CSS
3. **Start Phase 1** (Setup & Foundation)
4. **Iterate based on feedback** during development
5. **Test thoroughly** before migration from Gradio

### Resources

- **Google Stitch**: https://stitch.google.com (for initial UI generation)
- **Svelte Documentation**: https://svelte.dev/docs
- **SvelteKit**: https://kit.svelte.dev/docs
- **Django REST Framework**: https://www.django-rest-framework.org/
- **Wavesurfer.js**: https://wavesurfer-js.org/
- **Tailwind CSS**: https://tailwindcss.com/docs

---

**Document Version**: 1.0.0
**Last Updated**: 2025-01-25
**Status**: Ready for Implementation
**Author**: Kiro AI Assistant
