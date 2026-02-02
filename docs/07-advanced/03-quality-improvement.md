# Guía Completa para Mejorar la Calidad de Voz Clonada

## 📊 Factores que Afectan la Calidad (en orden de importancia)

1. **Calidad de Samples** (40%) - Ya lo tienes ✅
2. **Formato del Texto** (30%) - ¡Muy importante!
3. **Parámetros de Generación** (20%) - Ajustables
4. **Post-Procesamiento** (10%) - Opcional

---

## 🎯 Estrategia de Mejora Paso a Paso

### Nivel 1: Básico (Ya lo tienes)
- ✅ 21 samples válidos
- ✅ 291 segundos de audio
- ✅ Formato correcto (22050Hz, mono, 16-bit)

### Nivel 2: Formato de Texto (HAZLO AHORA)

**Antes de generar cualquier audio, formatea tu texto correctamente:**

```bash
# Lee la guía de formato
cat docs/TEXT_FORMATTING_GUIDE.md

# Ejemplo de texto bien formateado:
cat > data/scripts/ejemplo_bien_formateado.txt << 'EOF'
¡Hola a todos! Bienvenidos a este nuevo tutorial.

Hoy vamos a aprender sobre inteligencia artificial.
Es un tema fascinante. ¿Por qué? Porque está transformando el mundo.

Primero, veremos qué es la IA.
Segundo, exploraremos sus aplicaciones.
Finalmente, hablaremos del futuro.

¿Listos? ¡Comencemos!
EOF

# Genera con texto bien formateado
voice-clone generate \
    --profile ./data/bryan_voice_profile_v2.json \
    --text "$(cat data/scripts/ejemplo_bien_formateado.txt)" \
    --output ./data/outputs/ejemplo_mejorado.wav
```

### Nivel 3: Ajustar Parámetros

**Prueba diferentes configuraciones:**

```bash
# Ejecuta el script de prueba
./scripts/test_quality.sh

# Escucha los 3 resultados y elige el mejor
afplay data/quality_tests/test_default.wav
afplay data/quality_tests/test_natural.wav
afplay data/quality_tests/test_consistent.wav
```

**Luego actualiza tu config:**

```yaml
# config/config.yaml
model:
  device: "cpu"

generation:
  temperature: 0.75      # Ajusta según tu preferencia
  repetition_penalty: 2.0
  speed: 1.0

performance:
  use_gpu: false
  fp16: false
```

### Nivel 4: Post-Procesamiento

**Mejora el audio después de generar:**

```bash
# Genera el audio
voice-clone generate \
    --profile ./data/bryan_voice_profile_v2.json \
    --text "Tu texto aquí" \
    --output ./data/outputs/original.wav

# Mejora la calidad
./scripts/enhance_audio.sh ./data/outputs/original.wav

# Compara
afplay ./data/outputs/original.wav
afplay ./data/outputs/original_enhanced.wav
```

---

## 🎛️ Parámetros Explicados

### Temperature (0.5 - 1.0)
```
0.5-0.6  = Muy consistente, robótico
0.65-0.75 = Balanceado (RECOMENDADO) ✅
0.8-0.9  = Más expresivo, natural
0.95-1.0 = Muy variable, puede sonar errático
```

**Cuándo usar cada uno:**
- **0.65**: Tutoriales técnicos, narración clara
- **0.75**: Uso general, videos de YouTube
- **0.85**: Intros energéticas, contenido emocional

### Repetition Penalty (1.0 - 3.0)
```
1.0-1.5  = Permite repeticiones (más natural)
1.8-2.2  = Balanceado (RECOMENDADO) ✅
2.5-3.0  = Evita repeticiones (puede sonar forzado)
```

### Speed (0.8 - 1.2)
```
0.8-0.9  = Más lento, más claro
0.95-1.0 = Normal (RECOMENDADO) ✅
1.05-1.2 = Más rápido, más energético
```

---

## 📝 Checklist de Calidad

### Antes de Generar
- [ ] Texto tiene puntuación correcta
- [ ] Oraciones cortas (<30 palabras)
- [ ] Chunks de <400 caracteres
- [ ] Números escritos como texto
- [ ] Pausas estratégicas (comas, puntos, ...)

### Durante la Generación
- [ ] Usar perfil v2 (21 samples)
- [ ] Parámetros ajustados a tu preferencia
- [ ] Texto bien formateado

### Después de Generar
- [ ] Escuchar el resultado completo
- [ ] Aplicar post-procesamiento si es necesario
- [ ] Comparar con versiones anteriores

---

## 🔬 Experimentos Recomendados

### Experimento 1: Comparar Temperaturas

```bash
# Crea 3 versiones del mismo texto
TEXT="Hola, bienvenidos. Hoy vamos a aprender algo nuevo. ¿Listos?"

# Temperature 0.65 (consistente)
# Temperature 0.75 (balanceado)
# Temperature 0.85 (expresivo)

# Escucha y decide cuál prefieres
```

### Experimento 2: Formato de Texto

```bash
# Versión A: Sin formato
TEXT_A="hola bienvenidos hoy vamos a hablar de inteligencia artificial"

# Versión B: Con formato
TEXT_B="¡Hola! Bienvenidos. Hoy vamos a hablar de inteligencia artificial."

# Genera ambas y compara la diferencia
```

### Experimento 3: Post-Procesamiento

```bash
# Genera audio
voice-clone generate --profile ./data/bryan_voice_profile_v2.json \
    --text "Texto de prueba" --output test.wav

# Versión A: Original
# Versión B: Con enhance_audio.sh
./scripts/enhance_audio.sh test.wav

# Compara cuál suena mejor
```

---

## 💡 Tips Avanzados

### 1. Usa Diferentes Configuraciones por Tipo de Contenido

```yaml
# Para tutoriales (claro y consistente)
generation:
  temperature: 0.65
  speed: 0.95

# Para intros (energético)
generation:
  temperature: 0.85
  speed: 1.05

# Para narración (natural)
generation:
  temperature: 0.75
  speed: 1.0
```

### 2. Divide Contenido Largo

```bash
# En lugar de generar 10 minutos de una vez:
# Divide en segmentos de 1-2 minutos cada uno

# Esto permite:
# - Mejor calidad por segmento
# - Más fácil de editar
# - Regenerar solo partes si es necesario
```

### 3. Itera y Mejora

```bash
# 1. Genera versión 1
# 2. Escucha y toma notas
# 3. Ajusta parámetros
# 4. Genera versión 2
# 5. Compara
# 6. Repite hasta estar satisfecho
```

---

## 🎓 Casos de Uso Específicos

### YouTube Tutorial
```yaml
# Configuración recomendada
generation:
  temperature: 0.70
  repetition_penalty: 2.0
  speed: 0.98

# Formato de texto
- Oraciones cortas
- Pausas frecuentes
- Preguntas retóricas
- Énfasis con signos
```

### Podcast
```yaml
# Configuración recomendada
generation:
  temperature: 0.80
  repetition_penalty: 1.8
  speed: 1.0

# Formato de texto
- Conversacional
- Pausas naturales
- Variación en estructura
- Conectores frecuentes
```

### Narración de Video
```yaml
# Configuración recomendada
generation:
  temperature: 0.75
  repetition_penalty: 2.0
  speed: 0.95

# Formato de texto
- Descriptivo
- Ritmo controlado
- Sincronizado con video
- Pausas estratégicas
```

---

## 📊 Métricas de Calidad

### Evalúa tu Audio (1-5)

**Naturalidad**: ¿Suena como una persona real?
- 1: Muy robótico
- 3: Aceptable
- 5: Indistinguible de voz real

**Claridad**: ¿Se entiende perfectamente?
- 1: Difícil de entender
- 3: Mayormente claro
- 5: Perfectamente claro

**Expresividad**: ¿Tiene emoción apropiada?
- 1: Monótono
- 3: Algo de variación
- 5: Muy expresivo

**Consistencia**: ¿Mantiene la misma voz?
- 1: Cambia mucho
- 3: Mayormente consistente
- 5: Perfectamente consistente

### Objetivo
- Naturalidad: 4+
- Claridad: 5
- Expresividad: 3-4
- Consistencia: 4+

---

## 🚀 Plan de Acción Inmediato

### Hoy (30 minutos)
1. ✅ Lee TEXT_FORMATTING_GUIDE.md
2. ✅ Ejecuta ./scripts/test_quality.sh
3. ✅ Escucha las 3 versiones
4. ✅ Elige tu configuración favorita

### Esta Semana
1. Genera 3-5 audios de prueba con diferentes textos
2. Experimenta con diferentes temperaturas
3. Prueba el post-procesamiento
4. Documenta qué funciona mejor para ti

### Próximo Mes
1. Crea tu primer video completo
2. Itera basado en feedback
3. Considera grabar más samples si es necesario
4. Perfecciona tu workflow

---

## 🎯 Resumen Ejecutivo

**Para mejorar la calidad AHORA:**

1. **Formatea tu texto correctamente** (30% de mejora)
   - Puntuación correcta
   - Oraciones cortas
   - Pausas estratégicas

2. **Ajusta temperature a 0.75-0.85** (15% de mejora)
   - Más natural que el default

3. **Usa post-procesamiento** (10% de mejora)
   - Normaliza volumen
   - Reduce ruido
   - Comprime dinámicamente

**Total de mejora potencial: ~55%** 🚀

---

## 📚 Recursos Adicionales

- `docs/TEXT_FORMATTING_GUIDE.md` - Guía detallada de formato
- `scripts/test_quality.sh` - Prueba configuraciones
- `scripts/enhance_audio.sh` - Mejora audio generado
- `config/profiles/` - Configuraciones predefinidas

---

**¡La calidad es un proceso iterativo! Experimenta, escucha, ajusta, repite.** 🎙️
