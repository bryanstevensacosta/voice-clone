---
inclusion: always
---

# Voice Samples Guide - Recording Quality Reference

## Critical Truth
**La calidad de tus samples determina el 80% del resultado final.**

No importa qué tan bien configures el modelo, si tus samples son malos, la voz clonada será mala. Invierte tiempo en grabar samples de calidad desde el principio.

---

## Quick Start Checklist

```
Antes de grabar:
├── [ ] Ambiente silencioso (sin ruido de fondo)
├── [ ] Micrófono funcionando correctamente
├── [ ] Distancia correcta (15-20cm del micrófono)
├── [ ] Nivel de volumen apropiado (no muy bajo, no clipping)
├── [ ] Lista de textos preparada
├── [ ] Voz descansada (no grabar con voz cansada/ronca)
└── [ ] Agua a mano (mantener garganta hidratada)

Durante la grabación:
├── [ ] Hablar con volumen natural
├── [ ] Pronunciación clara
├── [ ] Velocidad natural (no muy rápido ni lento)
├── [ ] Variar emociones entre samples
└── [ ] Evitar ruidos (respiraciones fuertes, clicks)

Después de grabar:
├── [ ] Validar formato (22050 Hz, mono, 16-bit)
├── [ ] Verificar duración (6-30 segundos)
├── [ ] Escuchar cada sample (sin ruido, sin clipping)
├── [ ] Limpiar si es necesario
└── [ ] Nombrar apropiadamente
```

---

## Hardware Setup

### Microphone Options

#### Option 1: Built-in MacBook Pro Microphone (Acceptable)
```
Pros:
✓ Ya lo tienes
✓ Calidad decente para voz
✓ Cero setup

Cons:
✗ Capta ruido del teclado
✗ Menos control de dirección
✗ Calidad inferior a micrófonos dedicados

Best for: Testing inicial, prototipos
Quality: 6/10
```

#### Option 2: USB Microphone (Recommended)
```
Examples:
- Blue Yeti (~$100)
- Audio-Technica ATR2100x (~$80)
- Rode NT-USB Mini (~$100)
- Samson Q2U (~$70)

Pros:
✓ Excelente calidad de audio
✓ Plug & play (USB)
✓ Control de ganancia
✓ Patrón direccional (rechaza ruido lateral)

Cons:
✗ Costo adicional
✗ Requiere espacio

Best for: Producción seria
Quality: 8-9/10
```

#### Option 3: XLR Microphone + Audio Interface (Professional)
```
Examples:
- Shure SM7B + Focusrite Scarlett (~$500)
- Rode PodMic + Behringer U-Phoria (~$200)

Pros:
✓ Calidad profesional
✓ Máximo control
✓ Mejor rechazo de ruido

Cons:
✗ Caro
✗ Setup más complejo
✗ Overkill para voice cloning

Best for: Producción profesional, podcasts
Quality: 9-10/10
```

### Recommended Setup for This Project
```
Minimum: MacBook Pro built-in mic
Recommended: USB microphone (~$80-100)
Optimal: USB mic + pop filter + boom arm

Investment: $100-150 total
ROI: Dramática mejora en calidad de voz clonada
```

### Accessories

#### Pop Filter ($10-20)
```
Purpose: Reduce plosives (P, B, T sounds)
Impact: Significant improvement
Necessary: Highly recommended
DIY: Pantyhose stretched over wire hanger works
```

#### Boom Arm ($20-40)
```
Purpose: Position mic optimally, reduce desk vibrations
Impact: Moderate improvement
Necessary: Nice to have
Alternative: Stack of books to elevate mic
```

#### Acoustic Treatment (Optional)
```
Purpose: Reduce room echo
Options:
- Foam panels ($30-50)
- DIY: Blankets, pillows
- Record in closet (clothes absorb sound)
Impact: Moderate to significant
Necessary: Only if room has bad echo
```

---

## Recording Environment

### Ideal Environment
```
✓ Quiet room (no traffic, AC, appliances)
✓ Soft surfaces (carpet, curtains, furniture)
✓ Small to medium room (not empty large room)
✓ Door closed
✓ Windows closed
✓ Notifications silenced
✓ Pets in another room
```

### Common Noise Sources to Eliminate
```
✗ Air conditioning / heating
✗ Refrigerator hum
✗ Computer fans (use laptop, not desktop nearby)
✗ Traffic outside
✗ People talking in other rooms
✗ Phone notifications
✗ Clock ticking
✗ Keyboard/mouse clicks
```

### Best Times to Record
```
✓ Early morning (less traffic)
✓ Late evening (neighbors quiet)
✗ Avoid: Rush hour, lunch time, weekends with neighbors
```

### Quick Environment Test
```bash
# Grabar 10 segundos de silencio
# Escuchar con volumen alto
# ¿Escuchas ruido de fondo?

# Si sí: Mejorar ambiente antes de grabar samples
# Si no: Listo para grabar
```

---

## Recording Settings

### macOS QuickTime Player (Simple)
```
1. Open QuickTime Player
2. File → New Audio Recording
3. Click dropdown next to record button
4. Select microphone
5. Set quality to "Maximum"
6. Adjust input volume (middle range, not max)
7. Record
8. File → Export → Audio Only
```

### Audacity (More Control)
```
1. Download Audacity (free)
   brew install --cask audacity

2. Preferences → Audio Settings:
   - Sample Rate: 22050 Hz
   - Channels: 1 (Mono)

3. Select correct input device

4. Set recording level:
   - Test recording
   - Aim for -12 to -6 dB peak
   - Avoid red (clipping)

5. Record

6. Export:
   File → Export → Export as WAV
   - Format: WAV (Microsoft) signed 16-bit PCM
   - Sample Rate: 22050 Hz
```

### Recording Level Guidelines
```
Too Quiet: Peak < -20 dB
├── Problem: Noise floor becomes audible
└── Solution: Increase gain/volume

Optimal: Peak between -12 and -6 dB
├── Good headroom
├── Clean signal
└── Easy to normalize later

Too Loud: Peak > -3 dB or clipping
├── Problem: Distortion, unusable
└── Solution: Reduce gain/volume immediately
```

---

## What to Record: Content Strategy

### Minimum Viable Samples (6 samples)
```
1. neutral_01.wav (10-15s)
   "Hola, mi nombre es [nombre]. Hoy vamos a hablar sobre
   tecnología y programación. Es un tema muy interesante."

2. neutral_02.wav (15-20s)
   "La inteligencia artificial está transformando el mundo.
   Desde asistentes virtuales hasta vehículos autónomos,
   la IA está presente en nuestra vida diaria."

3. happy_01.wav (10-15s)
   "¡Hola a todos! ¡Bienvenidos a este nuevo video!
   Hoy tengo algo muy especial para compartir.
   ¡Esto va a ser genial!"

4. serious_01.wav (15-20s)
   "Es importante analizar estos datos con detenimiento.
   Las decisiones estratégicas deben basarse en evidencia sólida.
   No podemos ignorar estos indicadores."

5. calm_01.wav (10-15s)
   "Tómate un momento para respirar profundamente.
   Relájate y escucha con atención.
   Todo va a estar bien."

6. question_01.wav (10-15s)
   "¿Alguna vez te has preguntado cómo funciona esto?
   ¿Qué pasaría si intentamos algo diferente?
   ¿No es fascinante?"
```

### Recommended Set (10 samples)
```
Add to minimum set:

7. excited_01.wav (10-15s)
   "¡No puedo creer que esto funcione tan bien!
   ¡Es increíble! ¡Mira estos resultados!
   ¡Esto supera todas mis expectativas!"

8. emphasis_01.wav (15-20s)
   "Esto es fundamental. Muy importante.
   Presta mucha atención a este punto.
   No puedo enfatizar esto lo suficiente."

9. conversational_01.wav (15-20s)
   "Entonces, como te decía, la cosa es así.
   Básicamente, lo que pasa es que necesitamos
   entender bien el contexto antes de continuar."

10. narrative_01.wav (20-25s)
    "Había una vez un desarrollador que quería crear
    algo especial. Trabajó día y noche, enfrentando
    desafíos y superando obstáculos. Al final,
    lo logró."
```

### Advanced Set (15+ samples)
```
Add more variety:

11. technical_01.wav
    Technical explanation with jargon

12. tutorial_01.wav
    Step-by-step instructions

13. fast_paced_01.wav
    Faster speaking speed

14. slow_paced_01.wav
    Slower, deliberate speaking

15. whisper_01.wav (optional)
    Soft, intimate tone
```

---

## Spanish Phoneme Coverage

### Essential Phonemes to Include

#### Vowels (Critical)
```
a - casa, mapa, hablar
e - este, verde, entender
i - inicio, vivir, escribir
o - como, solo, otro
u - uno, futuro, usar
```

#### Common Consonants
```
b/v - bien, voz, haber
c/k - casa, que, tecnología
d - día, todo, poder
f - fue, café, información
g - gato, seguir, programa
h - (silent) hola, ahora
j - juego, mejor, trabajar
l - la, el, hablar
ll - llamar, desarrollar
m - más, mismo, tiempo
n - no, en, entonces
ñ - año, español, mañana
p - para, tipo, ejemplo
r - pero, crear, tres
rr - perro, desarrollo, error
s - si, es, sistema
t - tu, este, importante
x - éxito, texto, explicar
y - yo, hoy, proyecto
z - hacer, vez, comenzar
```

#### Consonant Clusters (Important)
```
bl - hablar, tabla, problema
br - sobre, nombre,iembre
cl - clase, incluir, declarar
cr - crear, escribir, incrementar
dr - padre, cuadro,andro
fl - flujo, reflexión
fr - frase, frecuencia
gl - inglés, regla
gr - grande, programa, integrar
pl - ejemplo, aplicar, completo
pr - primero, proceso, programar
tr - tres, trabajo, encontrar
```

### Sample Text with Good Phoneme Coverage
```
"Hola, mi nombre es [nombre] y trabajo en desarrollo de software.
La programación es una habilidad muy valiosa en el mundo actual.
Desde aplicaciones móviles hasta inteligencia artificial,
las posibilidades son prácticamente ilimitadas.
Hoy vamos a explorar conceptos fundamentales como variables,
funciones, y estructuras de datos. ¿Estás listo para comenzar?"

Covers: All vowels, most consonants, common clusters, questions
Duration: ~20 seconds
Emotion: Neutral/informative
```

---

## Recording Technique

### Microphone Distance
```
Too Close (< 10cm):
✗ Plosives (P, B) too strong
✗ Breathing audible
✗ Proximity effect (too much bass)

Optimal (15-20cm):
✓ Clear voice
✓ Minimal plosives
✓ Natural tone
✓ About a hand's width away

Too Far (> 30cm):
✗ Room reverb increases
✗ Noise floor more audible
✗ Voice sounds distant
```

### Speaking Technique

#### Volume
```
Too Quiet:
✗ Noise becomes prominent
✗ Lacks presence

Optimal:
✓ Natural speaking volume
✓ As if talking to someone 2 meters away
✓ Not whispering, not shouting

Too Loud:
✗ Risk of clipping
✗ Sounds aggressive
```

#### Speed
```
Too Fast:
✗ Words blend together
✗ Pronunciation suffers

Optimal:
✓ Natural conversational pace
✓ Clear pronunciation
✓ Comfortable to listen to
✓ ~150-160 words per minute

Too Slow:
✗ Sounds unnatural
✗ Loses energy
```

#### Articulation
```
✓ Clear pronunciation of each word
✓ Don't mumble
✓ Open mouth properly
✓ Enunciate consonants
✗ Don't over-articulate (sounds robotic)
```

#### Breathing
```
✓ Breathe naturally
✓ Breathe between sentences
✗ Don't breathe mid-sentence if possible
✗ Don't breathe directly into mic
✗ Don't hold breath (sounds strained)
```

### Common Mistakes to Avoid

#### Mouth Noises
```
✗ Lip smacks (drink water before recording)
✗ Tongue clicks
✗ Saliva sounds (stay hydrated)
✗ Teeth clicks

Prevention:
- Drink water 5 minutes before
- Don't eat right before recording
- Practice mouth movements before recording
```

#### Plosives (P, B, T, K sounds)
```
Problem: Burst of air hits microphone
Solution:
- Use pop filter
- Angle mic slightly off-axis
- Speak across mic, not directly into it
- Reduce gain slightly
```

#### Sibilance (S, Z, SH sounds)
```
Problem: Harsh "sss" sounds
Solution:
- Don't speak too close to mic
- Angle mic slightly
- Can be fixed in post-processing
- De-esser plugin in Audacity
```

---

## Duration Guidelines

### Per Sample
```
Too Short (< 6 seconds):
✗ Not enough data for model
✗ Sounds unnatural

Optimal (10-20 seconds):
✓ Enough context
✓ Natural phrasing
✓ Complete thoughts
✓ Good for training

Acceptable (6-30 seconds):
✓ Still usable
⚠ Very long samples (>25s) have diminishing returns

Too Long (> 30 seconds):
✗ Diminishing returns
✗ Harder to maintain consistency
✗ More chance of mistakes
```

### Total Sample Duration
```
Minimum: 60 seconds total (6 samples × 10s)
├── Will work, but limited quality
└── Good for testing

Recommended: 120-180 seconds (8-10 samples × 15s)
├── Good quality results
├── Enough variety
└── Optimal for XTTS-v2

Optimal: 180-300 seconds (10-15 samples × 20s)
├── Best quality
├── Maximum variety
└── Diminishing returns beyond this

Overkill: > 300 seconds
├── No significant improvement
└── Time better spent on quality, not quantity
```

---

## Emotion & Tone Variety

### Why Variety Matters
```
Single emotion (e.g., only neutral):
✗ Generated voice sounds monotone
✗ Can't express different contexts
✗ Robotic feeling

Multiple emotions:
✓ Natural variation
✓ Appropriate for different content
✓ More human-like
```

### Essential Emotions to Capture

#### 1. Neutral/Informative (40% of samples)
```
Use case: Tutorials, explanations, narration
Characteristics:
- Even tone
- Clear pronunciation
- Moderate pace
- Professional

Example: "La inteligencia artificial es una tecnología
que permite a las máquinas aprender de datos."
```

#### 2. Happy/Enthusiastic (20% of samples)
```
Use case: Intros, exciting announcements
Characteristics:
- Higher energy
- Upward inflection
- Faster pace
- Smile while speaking (yes, it affects sound!)

Example: "¡Hola a todos! ¡Bienvenidos!
¡Hoy tengo algo increíble para compartir!"
```

#### 3. Serious/Professional (20% of samples)
```
Use case: Important information, analysis
Characteristics:
- Lower pitch
- Deliberate pace
- Authoritative
- Measured

Example: "Es fundamental analizar estos datos
con detenimiento antes de tomar decisiones."
```

#### 4. Calm/Relaxed (10% of samples)
```
Use case: Meditations, soothing content
Characteristics:
- Soft tone
- Slower pace
- Gentle
- Reassuring

Example: "Tómate un momento para respirar.
Todo va a estar bien."
```

#### 5. Curious/Questioning (10% of samples)
```
Use case: Questions, engagement
Characteristics:
- Upward inflection
- Inquisitive tone
- Engaging
- Conversational

Example: "¿Alguna vez te has preguntado cómo funciona?
¿No es fascinante?"
```

### Emotion Recording Tips
```
✓ Actually feel the emotion (method acting)
✓ Smile for happy samples (changes voice)
✓ Stand up for energetic samples
✓ Sit relaxed for calm samples
✓ Think of real scenarios
✗ Don't fake it (sounds artificial)
✗ Don't exaggerate (sounds cartoonish)
```

---

## Audio Cleanup & Processing

### When to Clean Audio
```
Always:
✓ Remove silence at start/end
✓ Normalize volume
✓ Check for clipping

If Needed:
⚠ Noise reduction (only if noticeable noise)
⚠ De-essing (only if sibilance is harsh)
⚠ EQ (only if tone is off)

Never:
✗ Don't over-process
✗ Don't add effects (reverb, echo, etc.)
✗ Don't compress too much
```

### Basic Cleanup in Audacity

#### 1. Remove Silence
```
1. Select audio
2. Effect → Truncate Silence
3. Settings:
   - Detect: -40 dB
   - Duration: 0.5 seconds
   - Truncate to: 0.1 seconds
4. Apply
```

#### 2. Normalize Volume
```
1. Select audio
2. Effect → Normalize
3. Settings:
   - Normalize peak amplitude to: -3 dB
   - ✓ Normalize stereo channels independently
4. Apply
```

#### 3. Noise Reduction (if needed)
```
1. Select 1-2 seconds of "silence" (background noise)
2. Effect → Noise Reduction
3. Click "Get Noise Profile"
4. Select entire audio
5. Effect → Noise Reduction
6. Settings:
   - Noise reduction: 12 dB (start conservative)
   - Sensitivity: 6.00
   - Frequency smoothing: 3 bands
7. Preview, then Apply

⚠ Warning: Too much noise reduction = robotic sound
```

#### 4. De-essing (if needed)
```
1. Select audio
2. Effect → Equalization
3. Reduce 6-8 kHz by 3-6 dB
4. Preview, then Apply

Or use De-esser plugin if available
```

### FFmpeg Cleanup Commands

#### Normalize
```bash
ffmpeg -i input.wav -af "loudnorm=I=-16:TP=-1.5:LRA=11" output.wav
```

#### Remove Silence
```bash
ffmpeg -i input.wav -af "silenceremove=start_periods=1:stop_periods=-1:detection=peak" output.wav
```

#### High-pass Filter (remove rumble)
```bash
ffmpeg -i input.wav -af "highpass=f=80" output.wav
```

#### Complete Cleanup Pipeline
```bash
ffmpeg -i input.wav \
  -af "highpass=f=80,silenceremove=start_periods=1:stop_periods=-1,loudnorm=I=-16:TP=-1.5:LRA=11" \
  -ar 22050 -ac 1 -sample_fmt s16 \
  output_clean.wav
```

---

## Quality Checklist

### Before Using Samples

#### Technical Validation
```bash
# Run validation script
voice-clone validate-samples --dir ./data/samples

Check:
├── [ ] Sample rate: 22050 Hz
├── [ ] Channels: Mono (1)
├── [ ] Bit depth: 16-bit
├── [ ] Format: WAV
├── [ ] Duration: 6-30 seconds each
└── [ ] Total duration: 60-300 seconds
```

#### Listening Test (Critical!)
```
Listen to each sample with headphones:

Audio Quality:
├── [ ] No background noise
├── [ ] No clipping/distortion
├── [ ] No echo/reverb
├── [ ] No mouth noises
├── [ ] No breathing sounds
└── [ ] Consistent volume

Voice Quality:
├── [ ] Clear pronunciation
├── [ ] Natural speaking pace
├── [ ] Appropriate emotion
├── [ ] Complete sentences
└── [ ] No mistakes/stutters

If ANY sample fails: Re-record it
Don't compromise on quality!
```

#### Variety Check
```
Across all samples:
├── [ ] Multiple emotions represented
├── [ ] Different sentence structures
├── [ ] Variety of phonemes covered
├── [ ] Questions and statements
├── [ ] Different pacing
└── [ ] Consistent voice (same person, same mic)
```

---

## Good vs Bad Samples

### Example: Good Sample ✓
```
Characteristics:
✓ Clear voice, no background noise
✓ Consistent volume (-12 to -6 dB peak)
✓ Natural speaking pace
✓ Complete thoughts
✓ Appropriate emotion
✓ 15 seconds duration
✓ Good pronunciation
✓ No mouth noises

Waveform:
- Consistent amplitude
- No clipping (flat tops)
- Minimal silence
- Clean signal

Result: Excellent voice cloning quality
```

### Example: Bad Sample ✗
```
Problems:
✗ Background noise (AC, traffic)
✗ Inconsistent volume
✗ Too fast or too slow
✗ Incomplete sentences
✗ Monotone
✗ Too short (3 seconds)
✗ Mumbled words
✗ Lip smacks, breathing

Waveform:
- Erratic amplitude
- Clipping visible
- Long silences
- Noisy signal

Result: Poor voice cloning quality
```

### Common Issues & Fixes

#### Issue: Background Hum
```
Cause: AC, refrigerator, computer fans
Fix:
- Record in different location
- Turn off appliances
- Use noise reduction (last resort)
```

#### Issue: Echo/Reverb
```
Cause: Large empty room, hard surfaces
Fix:
- Record in smaller room
- Add soft materials (blankets, pillows)
- Record in closet
```

#### Issue: Plosives (P, B sounds)
```
Cause: Air hitting microphone
Fix:
- Use pop filter
- Increase mic distance
- Angle mic slightly
```

#### Issue: Inconsistent Volume
```
Cause: Moving closer/farther from mic
Fix:
- Mark mic position
- Stay consistent distance
- Use boom arm or stand
```

#### Issue: Mouth Noises
```
Cause: Dry mouth, lip smacks
Fix:
- Drink water before recording
- Don't eat right before
- Practice mouth movements
```

---

## Recording Session Workflow

### Preparation (5-10 minutes)
```
1. [ ] Choose quiet time/location
2. [ ] Set up microphone
3. [ ] Test recording levels
4. [ ] Prepare text list
5. [ ] Drink water
6. [ ] Silence notifications
7. [ ] Close windows/doors
```

### Recording (20-30 minutes)
```
For each sample:
1. [ ] Read text silently first
2. [ ] Take breath
3. [ ] Start recording
4. [ ] Speak naturally
5. [ ] Stop recording
6. [ ] Listen back immediately
7. [ ] Re-record if needed
8. [ ] Save with descriptive name

Take breaks:
- Every 5-6 samples
- Drink water
- Rest voice
```

### Post-Processing (10-15 minutes)
```
1. [ ] Validate all samples (technical specs)
2. [ ] Listen to each sample
3. [ ] Clean audio if needed
4. [ ] Trim silence
5. [ ] Normalize volume
6. [ ] Export to correct format
7. [ ] Organize in data/samples/
8. [ ] Backup originals
```

### Quality Check (5 minutes)
```
1. [ ] Run validation script
2. [ ] Listen to all samples in sequence
3. [ ] Verify variety of emotions
4. [ ] Check total duration
5. [ ] Ready for voice profile creation
```

---

## Iterative Improvement

### First Recording Session
```
Goal: Get 6-8 usable samples
Expectation: May need multiple takes
Time: 30-45 minutes
Result: Baseline voice profile
```

### After First Test Generation
```
Evaluate:
- Does it sound like you?
- What's missing?
- Which emotions work best?

Action:
- Add 2-3 more samples addressing gaps
- Re-record poor quality samples
- Test again
```

### Optimization Phase
```
After 3-4 iterations:
- Identify best samples
- Remove worst samples
- Add specific emotions needed
- Fine-tune recording technique

Goal: 10-12 high-quality samples
Result: Production-ready voice profile
```

---

## Best Practices Summary

### Do's
- ✅ Record in quiet environment
- ✅ Use consistent microphone and distance
- ✅ Speak naturally and clearly
- ✅ Include variety of emotions
- ✅ Listen to each sample immediately
- ✅ Re-record bad samples without hesitation
- ✅ Backup original recordings
- ✅ Take breaks to rest voice
- ✅ Stay hydrated
- ✅ Test voice profile after recording

### Don'ts
- ❌ Don't record with background noise
- ❌ Don't rush through recordings
- ❌ Don't use samples with mistakes
- ❌ Don't over-process audio
- ❌ Don't record when voice is tired/sick
- ❌ Don't use inconsistent recording setups
- ❌ Don't skip quality checks
- ❌ Don't settle for "good enough"
- ❌ Don't record all samples in one emotion
- ❌ Don't forget to backup

---

## Troubleshooting

### "My cloned voice sounds robotic"
```
Likely cause: Samples are too monotone
Solution:
- Add more emotional variety
- Record with more natural expression
- Actually feel the emotions while recording
```

### "Pronunciation is off"
```
Likely cause: Unclear pronunciation in samples
Solution:
- Re-record with clearer articulation
- Ensure good phoneme coverage
- Speak slower and more deliberately
```

### "Voice is inconsistent"
```
Likely cause: Samples recorded in different conditions
Solution:
- Use same microphone for all samples
- Record in same location
- Maintain consistent distance
- Check volume levels are similar
```

### "Background noise in generated audio"
```
Likely cause: Noise in original samples
Solution:
- Re-record in quieter environment
- Use noise reduction carefully
- Ensure samples are clean before training
```

---

## Quick Reference Card

```
RECORDING CHECKLIST
═══════════════════════════════════════════════════

Environment:
├── Quiet room ✓
├── Door/windows closed ✓
├── Notifications off ✓
└── Water nearby ✓

Equipment:
├── Microphone working ✓
├── Recording software ready ✓
├── Levels tested ✓
└── Pop filter (if available) ✓

Technique:
├── 15-20cm from mic ✓
├── Natural volume ✓
├── Clear pronunciation ✓
└── Appropriate emotion ✓

Per Sample:
├── 10-20 seconds ✓
├── Complete thoughts ✓
├── No mistakes ✓
└── Listen back immediately ✓

Quality:
├── No background noise ✓
├── No clipping ✓
├── Good pronunciation ✓
└── Natural delivery ✓

Total:
├── 6-10 samples minimum ✓
├── Multiple emotions ✓
├── 60-180 seconds total ✓
└── All validated ✓

═══════════════════════════════════════════════════
Remember: Quality > Quantity
One great sample > Three mediocre samples
═══════════════════════════════════════════════════
```

---

## Conclusion

**Invest time in recording quality samples.** This is the foundation of your voice cloning project.

- 30 minutes of careful recording > Hours of troubleshooting poor results
- Re-record bad samples immediately, don't settle
- Quality samples = Natural sounding voice
- Poor samples = No amount of configuration will fix it

**The 80/20 rule applies here**: 80% of your result quality comes from 20% of the effort - and that 20% is recording good samples.
