# UI Integration Guide - Text Length Validation

## Overview

This guide explains how the UI should integrate with the backend's text length validation system. The system uses a **defense in depth** approach with validation at both UI and backend layers.

## Architecture: Defense in Depth

```
┌─────────────────────────────────────────────────────────┐
│                    UI Layer (React)                      │
│  - Query engine capabilities                             │
│  - Enforce limits proactively                            │
│  - Provide real-time feedback                            │
│  - Prevent invalid submissions                           │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              Backend Layer (Python API)                  │
│  - Validate against engine capabilities                  │
│  - Soft limit: Log warning, allow generation             │
│  - Hard limit: Raise error, block generation             │
│  - Protect against bugs and direct API calls             │
└─────────────────────────────────────────────────────────┘
```

## Engine Capabilities

Each TTS engine reports its capabilities via `get_capabilities()`:

```python
@dataclass
class EngineCapabilities:
    max_text_length: int              # Hard limit (error if exceeded)
    recommended_text_length: int      # Soft limit (warning if exceeded)
    supports_streaming: bool          # Future: streaming generation
    min_sample_duration: float        # Minimum seconds per sample
    max_sample_duration: float        # Maximum seconds per sample
```

### Example: Qwen3-TTS Capabilities

```python
EngineCapabilities(
    max_text_length=2048,           # Absolute maximum
    recommended_text_length=400,    # Best quality range
    supports_streaming=False,
    min_sample_duration=3.0,
    max_sample_duration=30.0,
)
```

## UI Implementation

### 1. Query Engine Capabilities

When the UI loads or when the user selects a voice profile, query the engine capabilities:

```typescript
// Tauri command to get capabilities
const capabilities = await invoke<EngineCapabilities>('get_engine_capabilities', {
  profileId: selectedProfile.id
});

// TypeScript interface
interface EngineCapabilities {
  max_text_length: number;
  recommended_text_length: number;
  supports_streaming: boolean;
  min_sample_duration: number;
  max_sample_duration: number;
}
```

### 2. Real-Time Character Counter

Display a character counter that updates as the user types:

```typescript
const [text, setText] = useState('');
const [capabilities, setCapabilities] = useState<EngineCapabilities | null>(null);

const textLength = text.length;
const isWithinRecommended = textLength <= capabilities.recommended_text_length;
const isWithinMax = textLength <= capabilities.max_text_length;

// Character counter component
<div className="character-counter">
  <span className={getCounterColor()}>
    {textLength} / {capabilities.recommended_text_length}
  </span>
  <span className="text-muted">
    (max: {capabilities.max_text_length})
  </span>
</div>
```

### 3. Visual Feedback

Provide visual feedback based on text length:

```typescript
function getCounterColor(): string {
  if (!isWithinMax) {
    return 'text-red-600';      // Over hard limit - error
  }
  if (!isWithinRecommended) {
    return 'text-yellow-600';   // Over soft limit - warning
  }
  return 'text-green-600';      // Within recommended - good
}

function getWarningMessage(): string | null {
  if (!isWithinMax) {
    return `Text exceeds maximum limit of ${capabilities.max_text_length} characters. Please shorten your text.`;
  }
  if (!isWithinRecommended) {
    return `Text exceeds recommended limit of ${capabilities.recommended_text_length} characters. Quality may be degraded.`;
  }
  return null;
}
```

### 4. Disable Submit Button

Disable the generate button when text exceeds hard limit:

```typescript
<button
  onClick={handleGenerate}
  disabled={!isWithinMax || isGenerating}
  className={`btn ${!isWithinMax ? 'btn-disabled' : 'btn-primary'}`}
>
  {isGenerating ? 'Generating...' : 'Generate Audio'}
</button>
```

### 5. Warning Dialog for Soft Limit

Show a confirmation dialog when text exceeds recommended limit but is within max:

```typescript
async function handleGenerate() {
  // Check if exceeds recommended but within max
  if (!isWithinRecommended && isWithinMax) {
    const confirmed = await showConfirmDialog({
      title: 'Quality Warning',
      message: `Your text (${textLength} characters) exceeds the recommended limit of ${capabilities.recommended_text_length} characters. This may result in degraded audio quality. Continue anyway?`,
      confirmText: 'Generate Anyway',
      cancelText: 'Edit Text',
    });

    if (!confirmed) {
      return; // User chose to edit
    }
  }

  // Proceed with generation
  await generateAudio(text, selectedProfile);
}
```

## Complete UI Example

```typescript
import { useState, useEffect } from 'react';
import { invoke } from '@tauri-apps/api/tauri';

interface EngineCapabilities {
  max_text_length: number;
  recommended_text_length: number;
  supports_streaming: boolean;
  min_sample_duration: number;
  max_sample_duration: number;
}

export function AudioGenerationForm() {
  const [text, setText] = useState('');
  const [capabilities, setCapabilities] = useState<EngineCapabilities | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [selectedProfile, setSelectedProfile] = useState<string | null>(null);

  // Load capabilities when profile changes
  useEffect(() => {
    if (selectedProfile) {
      loadCapabilities(selectedProfile);
    }
  }, [selectedProfile]);

  async function loadCapabilities(profileId: string) {
    try {
      const caps = await invoke<EngineCapabilities>('get_engine_capabilities', {
        profileId
      });
      setCapabilities(caps);
    } catch (error) {
      console.error('Failed to load capabilities:', error);
    }
  }

  async function handleGenerate() {
    if (!capabilities || !selectedProfile) return;

    const textLength = text.length;

    // Hard limit check (should be prevented by disabled button, but double-check)
    if (textLength > capabilities.max_text_length) {
      alert(`Text exceeds maximum limit of ${capabilities.max_text_length} characters.`);
      return;
    }

    // Soft limit warning
    if (textLength > capabilities.recommended_text_length) {
      const confirmed = confirm(
        `Your text (${textLength} characters) exceeds the recommended limit of ${capabilities.recommended_text_length} characters. Quality may be degraded. Continue?`
      );
      if (!confirmed) return;
    }

    // Generate audio
    setIsGenerating(true);
    try {
      const result = await invoke('generate_audio', {
        text,
        profileId: selectedProfile,
      });
      console.log('Generation successful:', result);
    } catch (error) {
      // Backend validation error
      if (error.includes('exceeds maximum limit')) {
        alert('Text is too long. Please shorten your text and try again.');
      } else {
        alert(`Generation failed: ${error}`);
      }
    } finally {
      setIsGenerating(false);
    }
  }

  if (!capabilities) {
    return <div>Loading...</div>;
  }

  const textLength = text.length;
  const isWithinRecommended = textLength <= capabilities.recommended_text_length;
  const isWithinMax = textLength <= capabilities.max_text_length;

  return (
    <div className="audio-generation-form">
      <h2>Generate Audio</h2>

      {/* Text Input */}
      <div className="form-group">
        <label htmlFor="text-input">Text to Generate</label>
        <textarea
          id="text-input"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Enter the text you want to convert to speech..."
          rows={8}
          className={`form-control ${!isWithinMax ? 'border-red-500' : ''}`}
        />

        {/* Character Counter */}
        <div className="character-counter mt-2">
          <span className={
            !isWithinMax ? 'text-red-600' :
            !isWithinRecommended ? 'text-yellow-600' :
            'text-green-600'
          }>
            {textLength} / {capabilities.recommended_text_length}
          </span>
          <span className="text-gray-500 ml-2">
            (max: {capabilities.max_text_length})
          </span>
        </div>

        {/* Warning Messages */}
        {!isWithinMax && (
          <div className="alert alert-error mt-2">
            ⚠️ Text exceeds maximum limit of {capabilities.max_text_length} characters.
            Please shorten your text.
          </div>
        )}
        {isWithinMax && !isWithinRecommended && (
          <div className="alert alert-warning mt-2">
            ⚠️ Text exceeds recommended limit of {capabilities.recommended_text_length} characters.
            Quality may be degraded.
          </div>
        )}
      </div>

      {/* Generate Button */}
      <button
        onClick={handleGenerate}
        disabled={!isWithinMax || isGenerating || !text.trim()}
        className={`btn ${!isWithinMax || !text.trim() ? 'btn-disabled' : 'btn-primary'}`}
      >
        {isGenerating ? 'Generating...' : 'Generate Audio'}
      </button>
    </div>
  );
}
```

## Backend Error Handling

The backend will return errors if validation fails:

### Hard Limit Error (> max_text_length)

```json
{
  "status": "error",
  "error_type": "validation_error",
  "error": "Text length (3000 characters) exceeds maximum limit of 2048 characters for this engine. Please split your text into smaller segments."
}
```

### UI should handle this error:

```typescript
try {
  await invoke('generate_audio', { text, profileId });
} catch (error) {
  if (error.includes('exceeds maximum limit')) {
    // Show user-friendly error
    showError('Text is too long', 'Please split your text into smaller segments.');
  }
}
```

## Best Practices

### ✅ Do's

1. **Query capabilities on profile selection** - Different engines may have different limits
2. **Show real-time character counter** - Let users know where they stand
3. **Provide visual feedback** - Colors (green/yellow/red) help users understand status
4. **Disable submit when over hard limit** - Prevent invalid submissions
5. **Warn when over soft limit** - Let users make informed decisions
6. **Handle backend errors gracefully** - Backend is the final authority

### ❌ Don'ts

1. **Don't assume fixed limits** - Always query capabilities dynamically
2. **Don't allow submission over hard limit** - Backend will reject it anyway
3. **Don't silently truncate text** - User should control what gets generated
4. **Don't skip backend validation** - UI can have bugs, backend is safety net
5. **Don't ignore soft limit warnings** - Quality degradation is real

## Testing Checklist

- [ ] Character counter updates in real-time
- [ ] Visual feedback changes at recommended and max limits
- [ ] Generate button disabled when over max limit
- [ ] Warning dialog shows when over recommended limit
- [ ] Backend errors are handled gracefully
- [ ] Capabilities are queried when profile changes
- [ ] Works with different engines (Qwen3, future XTTS, etc.)

## Summary

The double validation approach provides:

1. **Better UX** - UI prevents errors proactively
2. **Safety** - Backend guarantees limits are enforced
3. **Flexibility** - Dynamic limits per engine
4. **Quality** - Users are warned about quality degradation
5. **Robustness** - Protects against bugs and direct API calls

This is superior to automatic chunking because:
- ✅ No quality degradation from automatic splitting
- ✅ User controls where to split text
- ✅ Clear feedback about limits
- ✅ Each segment is coherent and complete
