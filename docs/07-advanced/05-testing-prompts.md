---
inclusion: always
---

# Prompt Examples - Voice Quality Testing

## Purpose
Este documento contiene textos de prueba diseñados para validar diferentes aspectos de la calidad de la voz clonada. Usar estos prompts de forma consistente permite comparar mejoras entre versiones del voice profile.

---

## Quick Test Suite

### Minimal Test (30 segundos)
```bash
# Test básico para verificar que todo funciona
voice-clone test --text "Hola, esta es una prueba rápida de mi voz clonada. ¿Suena natural?"
```

### Standard Test (2 minutos)
```bash
# Test completo de calidad
voice-clone batch --input tests/standard_test.txt
```

### Full Test Suite (5 minutos)
```bash
# Todos los tests de este documento
voice-clone batch --input tests/full_test_suite.txt
```

---

## Test Categories

## 1. Basic Pronunciation Tests

### 1.1 Simple Sentences (Neutral Tone)
```
Hola, mi nombre es [tu nombre] y este es un test de voz.

La inteligencia artificial está transformando el mundo.

Hoy vamos a aprender sobre tecnología y programación.

Este es un ejemplo de narración para videos de YouTube.

Bienvenidos a este nuevo episodio del podcast.
```

**Evaluar**:
- ✓ Pronunciación clara
- ✓ Velocidad natural
- ✓ Pausas apropiadas
- ✓ Tono neutro y profesional

### 1.2 Short Phrases (Different Lengths)
```
Hola.

Bienvenidos.

Gracias por ver este video.

Hoy vamos a hablar de un tema muy interesante.

La tecnología avanza rápidamente y debemos adaptarnos a estos cambios constantes.
```

**Evaluar**:
- ✓ Frases cortas no suenan cortadas
- ✓ Frases largas mantienen coherencia
- ✓ Transiciones suaves

---

## 2. Emotional Range Tests

### 2.1 Neutral/Informative
```
En este tutorial aprenderemos los conceptos básicos de programación.
Comenzaremos con variables, luego funciones, y finalmente estructuras de datos.
Es importante practicar cada concepto antes de avanzar al siguiente.
```

### 2.2 Enthusiastic/Excited
```
¡Hola a todos! ¡Bienvenidos a este increíble video!
Hoy tengo algo muy especial para compartir con ustedes.
¡No van a creer lo que descubrí! ¡Esto es genial!
```

### 2.3 Serious/Professional
```
Los datos muestran un incremento significativo en los últimos trimestres.
Es fundamental analizar estas tendencias con detenimiento.
Las decisiones estratégicas deben basarse en evidencia sólida.
```

### 2.4 Calm/Relaxed
```
Tómate un momento para respirar profundamente.
Relájate y escucha con atención.
Todo va a estar bien, solo necesitas concentrarte en el presente.
```

### 2.5 Curious/Questioning
```
¿Alguna vez te has preguntado cómo funciona esto?
¿Qué pasaría si intentamos algo diferente?
¿No es fascinante cómo la tecnología puede resolver estos problemas?
```

**Evaluar**:
- ✓ Cambios de emoción son perceptibles
- ✓ Entonación apropiada para cada emoción
- ✓ No suena forzado o artificial

---

## 3. Punctuation & Intonation Tests

### 3.1 Questions
```
¿Cómo estás?

¿Qué es la inteligencia artificial?

¿Por qué es importante aprender programación en el siglo veintiuno?

¿Alguna vez te has preguntado cómo funcionan las redes neuronales y por qué son tan efectivas?
```

**Evaluar**:
- ✓ Entonación ascendente al final
- ✓ Suena como pregunta real
- ✓ Pausas antes del signo de interrogación

### 3.2 Exclamations
```
¡Hola!

¡Esto es increíble!

¡No puedo creer que esto funcione tan bien!

¡Bienvenidos a todos! ¡Hoy tenemos un contenido espectacular!
```

**Evaluar**:
- ✓ Énfasis apropiado
- ✓ Energía en la voz
- ✓ No suena gritado

### 3.3 Complex Punctuation
```
La inteligencia artificial, como sabemos, está transformando el mundo.

Hay tres conceptos clave: variables, funciones y objetos.

Primero, debemos entender lo básico; segundo, practicar constantemente; tercero, nunca dejar de aprender.

"La práctica hace al maestro", dice el refrán... y es completamente cierto.

¿Sabías que el 80% de los datos del mundo se generaron en los últimos dos años? ¡Es impresionante!
```

**Evaluar**:
- ✓ Pausas en comas y punto y coma
- ✓ Cambio de tono en comillas
- ✓ Manejo de puntos suspensivos
- ✓ Transiciones entre signos

### 3.4 Lists & Enumerations
```
Los pasos son: uno, preparar el entorno; dos, instalar las dependencias; tres, ejecutar el código.

Necesitarás Python, Node.js, y Git instalados en tu sistema.

Primero lo primero. Segundo, no te apresures. Tercero, revisa tu trabajo. Y finalmente, publica tu proyecto.
```

**Evaluar**:
- ✓ Pausas entre elementos
- ✓ Ritmo consistente
- ✓ Énfasis en números/orden

---

## 4. Difficult Words & Pronunciation

### 4.1 Technical Terms (Spanish)
```
Vamos a hablar sobre algoritmos, arquitectura, y optimización.

La implementación requiere conocimientos de programación orientada a objetos.

Utilizaremos metodologías ágiles como Scrum y Kanban.

El framework utiliza TypeScript con React y Next.js.

La infraestructura está desplegada en Kubernetes con contenedores Docker.
```

### 4.2 Common Difficult Words
```
Específicamente, necesitamos desarrollar una funcionalidad extraordinaria.

La configuración predeterminada es suficientemente eficiente.

Desafortunadamente, la implementación anterior era incorrecta.

Simultáneamente, procesaremos múltiples solicitudes asíncronas.

Consecuentemente, debemos reestructurar la arquitectura completamente.
```

### 4.3 Foreign Terms (Common in Tech)
```
Vamos a hacer un deploy del código a producción.

El debugging reveló un bug crítico en el backend.

Necesitamos hacer un refactor del código legacy.

El workflow incluye testing, staging, y deployment.

Usaremos machine learning para el feature engineering.
```

**Evaluar**:
- ✓ Pronunciación correcta de términos técnicos
- ✓ Palabras largas no se cortan
- ✓ Términos en inglés suenan naturales
- ✓ Acentuación correcta

---

## 5. Numbers, Dates & Special Formats

### 5.1 Numbers
```
El número es 42.

Tenemos 1,234 usuarios activos.

El precio es de $99.99 dólares.

La velocidad alcanzó los 150 kilómetros por hora.

El resultado fue 3.14159, aproximadamente pi.
```

### 5.2 Dates
```
Hoy es 15 de enero de 2024.

El evento será el próximo 23 de marzo.

Nació el 5 de mayo de 1990.

Entre el 2020 y el 2023 hubo cambios significativos.

El plazo vence el día 31 de diciembre a las 23:59 horas.
```

### 5.3 Percentages & Statistics
```
El 80% de los usuarios prefiere esta opción.

Creció un 25.5% en comparación con el año anterior.

La tasa de conversión es del 3.2 por ciento.

Aproximadamente el 50% está de acuerdo, mientras que el otro 50% no.
```

### 5.4 Acronyms & Abbreviations
```
La API REST utiliza JSON para transferir datos.

El CEO de la empresa anunció el nuevo MVP.

Necesitas instalar el SDK y el IDE antes de comenzar.

La URL es HTTPS, no HTTP.

El DNS resuelve las direcciones IP automáticamente.
```

### 5.5 Time & Duration
```
Son las 3:30 de la tarde.

El video dura 10 minutos y 45 segundos.

Llegaremos en aproximadamente 2 horas.

El proceso toma entre 5 y 10 minutos.

A las 9 AM comenzamos, y terminamos a las 5 PM.
```

**Evaluar**:
- ✓ Números se pronuncian correctamente
- ✓ Fechas suenan naturales
- ✓ Siglas se leen apropiadamente
- ✓ Formatos especiales son claros

---

## 6. Long-Form Content Tests

### 6.1 Short Paragraph (100-150 words)
```
La inteligencia artificial ha revolucionado la forma en que interactuamos con la tecnología.
Desde asistentes virtuales hasta sistemas de recomendación, la IA está presente en nuestra vida diaria.
Los modelos de lenguaje como GPT han demostrado capacidades impresionantes en la generación de texto,
mientras que los sistemas de visión por computadora pueden identificar objetos con precisión sorprendente.
Sin embargo, es importante recordar que estas tecnologías son herramientas creadas por humanos,
y debemos usarlas de manera responsable y ética. El futuro de la IA depende de cómo decidamos
desarrollarla e implementarla en nuestra sociedad.
```

**Evaluar**:
- ✓ Consistencia de voz durante todo el párrafo
- ✓ Pausas naturales entre oraciones
- ✓ No hay cambios abruptos de tono
- ✓ Mantiene energía hasta el final

### 6.2 Medium Paragraph (200-300 words)
```
Bienvenidos a este tutorial sobre desarrollo web moderno. Hoy vamos a explorar las tecnologías
más importantes que todo desarrollador debe conocer en 2024. Comenzaremos con los fundamentos:
HTML, CSS y JavaScript siguen siendo la base de cualquier aplicación web. Sin embargo, el ecosistema
ha evolucionado significativamente en los últimos años.

Los frameworks modernos como React, Vue y Angular han transformado la manera en que construimos
interfaces de usuario. Estos frameworks nos permiten crear aplicaciones interactivas y dinámicas
con mayor facilidad y eficiencia. Por el lado del backend, Node.js ha democratizado el desarrollo
con JavaScript, permitiendo usar el mismo lenguaje en frontend y backend.

Pero eso no es todo. Las herramientas de desarrollo también han mejorado enormemente.
TypeScript añade tipado estático a JavaScript, reduciendo errores y mejorando la mantenibilidad del código.
Los bundlers como Webpack y Vite optimizan nuestro código para producción. Y las plataformas de deployment
como Vercel y Netlify hacen que publicar aplicaciones sea más fácil que nunca.

En este tutorial, aprenderás paso a paso cómo utilizar estas tecnologías para crear tu propia aplicación web.
No necesitas experiencia previa, solo ganas de aprender y dedicación. ¡Comencemos!
```

**Evaluar**:
- ✓ Voz consistente en texto largo
- ✓ Transiciones entre párrafos
- ✓ Mantiene interés del oyente
- ✓ Ritmo apropiado (no muy rápido ni lento)

### 6.3 Technical Explanation (250-350 words)
```
Las redes neuronales son modelos computacionales inspirados en el funcionamiento del cerebro humano.
Están compuestas por capas de neuronas artificiales que procesan información de manera similar a como
lo hacen las neuronas biológicas. Cada neurona recibe múltiples inputs, los procesa mediante una función
matemática, y genera un output que se transmite a las neuronas de la siguiente capa.

El proceso de entrenamiento de una red neuronal es fascinante. Primero, inicializamos los pesos de las
conexiones con valores aleatorios. Luego, alimentamos la red con datos de entrenamiento y comparamos
sus predicciones con los resultados esperados. La diferencia entre la predicción y el resultado real
se llama "error" o "loss". Mediante un algoritmo llamado backpropagation, ajustamos los pesos de la red
para minimizar este error.

Este proceso se repite miles o incluso millones de veces, en lo que llamamos "épocas" de entrenamiento.
Con cada iteración, la red aprende patrones más complejos en los datos. Es como si la red estuviera
"memorizando" las relaciones entre inputs y outputs, pero de una manera que le permite generalizar
a datos nuevos que nunca ha visto antes.

Las aplicaciones de las redes neuronales son prácticamente ilimitadas. Desde reconocimiento de imágenes
hasta procesamiento de lenguaje natural, desde predicción de series temporales hasta generación de contenido.
La tecnología que estás escuchando ahora mismo, esta voz clonada, es el resultado de redes neuronales
entrenadas con miles de horas de audio humano.

Es importante entender que, aunque son poderosas, las redes neuronales no son mágicas. Son herramientas
matemáticas sofisticadas que requieren datos de calidad, arquitecturas bien diseñadas, y mucho poder
computacional para funcionar correctamente.
```

**Evaluar**:
- ✓ Claridad en explicaciones técnicas
- ✓ Pausas apropiadas para comprensión
- ✓ Énfasis en conceptos clave
- ✓ Mantiene tono profesional y educativo

---

## 7. Real-World Content Examples

### 7.1 YouTube Video Intro
```
¡Hola a todos! Bienvenidos a un nuevo video. Hoy vamos a hablar sobre un tema super interesante:
cómo crear tu propia herramienta de inteligencia artificial. Si eres nuevo en el canal, no olvides
suscribirte y activar la campanita para no perderte ningún video. Y si te gusta el contenido,
déjame un like, eso me ayuda muchísimo. ¡Vamos a comenzar!
```

### 7.2 Tutorial Narration
```
En este paso, vamos a instalar las dependencias necesarias. Abre tu terminal y escribe el siguiente comando:
npm install. Esto descargará todos los paquetes que necesitamos. El proceso puede tomar unos minutos,
así que ten paciencia. Una vez que termine, verás un mensaje de confirmación. Ahora estamos listos
para continuar con el siguiente paso.
```

### 7.3 Podcast Introduction
```
Bienvenidos a otro episodio de TechTalk, el podcast donde exploramos las últimas tendencias en tecnología.
Soy tu host, [nombre], y hoy tenemos un episodio muy especial. Vamos a hablar sobre el futuro de la
inteligencia artificial y cómo está transformando industrias enteras. Pero antes, un mensaje de nuestro
patrocinador.
```

### 7.4 Product Review
```
Hoy vamos a revisar el nuevo MacBook Pro con chip M1 Pro. Después de usarlo durante dos semanas,
puedo decir que es una máquina impresionante. El rendimiento es excepcional, la batería dura todo el día,
y la pantalla es simplemente hermosa. Sin embargo, hay algunos aspectos que podrían mejorar.
Hablemos primero de lo bueno.
```

### 7.5 News/Information
```
En noticias de tecnología, OpenAI ha anunciado el lanzamiento de su nuevo modelo de lenguaje.
Según la compañía, este modelo supera a sus predecesores en múltiples benchmarks. Los expertos
consideran que este avance podría tener implicaciones significativas para la industria.
Más detalles a continuación.
```

### 7.6 Educational Content
```
Hoy vamos a aprender sobre variables en programación. Una variable es como una caja donde guardamos
información. Por ejemplo, si queremos guardar tu edad, podemos crear una variable llamada "edad"
y asignarle el valor 25. Luego, podemos usar esa variable en nuestro código cada vez que necesitemos
ese valor. Es un concepto simple pero fundamental.
```

### 7.7 Call to Action
```
Si este video te fue útil, por favor dale like y compártelo con tus amigos. Suscríbete al canal
para más contenido como este. Déjame en los comentarios qué otros temas te gustaría que cubriera.
Y recuerda, la práctica hace al maestro. ¡Nos vemos en el próximo video!
```

**Evaluar**:
- ✓ Suena natural en contexto real
- ✓ Tono apropiado para cada tipo de contenido
- ✓ Mantiene engagement del oyente
- ✓ Transiciones suaves entre secciones

---

## 8. Edge Cases & Challenges

### 8.1 Tongue Twisters (Pronunciation Challenge)
```
Tres tristes tigres tragaban trigo en un trigal.

Parangaricutirimícuaro es un lugar en México.

El perro de San Roque no tiene rabo porque Ramón Ramírez se lo ha robado.
```

### 8.2 Repeated Words
```
El desarrollo de desarrollo de software requiere desarrollar habilidades de desarrollo constantemente.

La inteligencia artificial es inteligente, pero la inteligencia humana es irreemplazable.
```

### 8.3 Homonyms (Same Sound, Different Meaning)
```
Voy a ir a ver si hay algo que ver en la televisión.

Hola, me gustaría que me digas la hora actual.

El tuvo que guardar el tubo en el almacén.
```

### 8.4 Very Long Sentences
```
La inteligencia artificial, que ha sido objeto de investigación durante décadas y que ahora está
experimentando un renacimiento gracias a los avances en poder computacional y disponibilidad de datos,
está transformando industrias que van desde la medicina hasta el entretenimiento, pasando por la educación,
el transporte, las finanzas, y prácticamente cualquier sector que puedas imaginar.
```

### 8.5 Rapid Topic Changes
```
Hablemos de Python. Es un lenguaje genial. ¿Te gusta el café? Yo prefiero el té.
La programación es divertida. Mañana será un buen día. Los gatos son animales fascinantes.
Volviendo a Python, es muy versátil.
```

### 8.6 Mixed Languages (Code-Switching)
```
Vamos a hacer un git commit con el mensaje "fix bug en el login form".

El framework que usamos es React, específicamente la versión 18 con hooks.

Necesitamos hacer un pull request para mergear los cambios al branch main.
```

**Evaluar**:
- ✓ Maneja casos difíciles sin errores graves
- ✓ Pronunciación clara incluso en trabalenguas
- ✓ Transiciones coherentes en cambios abruptos
- ✓ Code-switching suena natural

---

## 9. Silence & Pause Tests

### 9.1 Natural Pauses
```
Hola... ¿cómo estás?

Déjame pensar... creo que la respuesta es sí.

Primero, vamos a preparar el entorno. Segundo... espera, olvidé algo. Tercero, ejecutamos el código.
```

### 9.2 Dramatic Pauses
```
Y el ganador es... ¡tú!

La respuesta a la pregunta más importante del universo es... cuarenta y dos.

Después de mucho trabajo, finalmente... lo logramos.
```

### 9.3 Paragraph Breaks
```
Este es el primer párrafo. Contiene información importante.

Este es el segundo párrafo. Debe haber una pausa clara entre ambos.

Y este es el tercer párrafo. Las pausas deben ser consistentes.
```

**Evaluar**:
- ✓ Pausas naturales en puntos suspensivos
- ✓ Silencio apropiado entre párrafos
- ✓ Timing dramático funciona correctamente

---

## 10. Quality Comparison Tests

### 10.1 Before/After Optimization
```
# Usar este texto para comparar versiones del voice profile
La inteligencia artificial está transformando el mundo de maneras que apenas comenzamos a comprender.
Desde asistentes virtuales hasta vehículos autónomos, la IA está presente en cada vez más aspectos
de nuestra vida diaria. Es fundamental que entendamos tanto sus beneficios como sus limitaciones.
```

### 10.2 Different Parameter Settings
```
# Generar con diferentes temperatures (0.5, 0.7, 0.9) y comparar
Este es un texto de prueba para evaluar cómo diferentes configuraciones afectan la calidad de la voz.
Presta atención a la naturalidad, la entonación, y la consistencia del audio generado.
```

### 10.3 Sample Quality Impact
```
# Generar con diferentes conjuntos de samples y comparar
Hola, mi nombre es [nombre] y estoy probando cómo la calidad de las muestras de referencia
afecta el resultado final de la voz clonada. ¿Notas alguna diferencia?
```

---

## Testing Workflow

### Quick Daily Test (30 seconds)
```bash
# Test rápido para verificar que todo funciona
voice-clone test --text "Hola, esta es una prueba rápida. La inteligencia artificial es fascinante."
```

### Standard Quality Check (2 minutes)
```bash
# Test estándar antes de producción
cat > test_standard.txt << 'EOF'
Hola, bienvenidos a este test de calidad de voz.

La inteligencia artificial está transformando el mundo. ¿No es fascinante?

Hoy vamos a hablar sobre tecnología, programación, y desarrollo de software.

Los números importantes son: 42, 3.14, y el 100% de dedicación.

¡Gracias por escuchar! Nos vemos en el próximo video.
EOF

voice-clone generate --text "$(cat test_standard.txt)" --output test_output.wav
```

### Full Test Suite (5-10 minutes)
```bash
# Test completo con todos los casos
voice-clone batch --input tests/full_test_suite.txt --output-dir tests/results
```

### A/B Comparison Test
```bash
# Comparar dos versiones del voice profile
voice-clone generate --profile v1.json --text "Texto de prueba" --output test_v1.wav
voice-clone generate --profile v2.json --text "Texto de prueba" --output test_v2.wav

# Escuchar ambos y comparar
afplay test_v1.wav
afplay test_v2.wav
```

---

## Evaluation Checklist

### After Each Test, Evaluate:

#### Pronunciation (1-5)
- [ ] 5 - Perfecto, sin errores
- [ ] 4 - Muy bueno, errores mínimos
- [ ] 3 - Bueno, algunos errores notables
- [ ] 2 - Regular, varios errores
- [ ] 1 - Malo, muchos errores

#### Naturalness (1-5)
- [ ] 5 - Indistinguible de voz real
- [ ] 4 - Muy natural, mínimos artefactos
- [ ] 3 - Natural, algunos momentos robóticos
- [ ] 2 - Algo robótico, claramente sintético
- [ ] 1 - Muy robótico, poco natural

#### Intonation (1-5)
- [ ] 5 - Perfecta, muy expresiva
- [ ] 4 - Muy buena, apropiada
- [ ] 3 - Buena, algo monótona
- [ ] 2 - Regular, bastante plana
- [ ] 1 - Mala, completamente monótona

#### Consistency (1-5)
- [ ] 5 - Perfectamente consistente
- [ ] 4 - Muy consistente
- [ ] 3 - Mayormente consistente
- [ ] 2 - Inconsistente en partes
- [ ] 1 - Muy inconsistente

#### Overall Quality (1-5)
- [ ] 5 - Excelente, listo para producción
- [ ] 4 - Muy bueno, usable
- [ ] 3 - Bueno, necesita ajustes menores
- [ ] 2 - Regular, necesita mejoras
- [ ] 1 - Malo, no usable

---

## Troubleshooting Guide

### If Pronunciation is Poor:
- Agregar más samples de referencia
- Verificar calidad de samples existentes
- Ajustar puntuación en el texto
- Usar phonetic spelling para palabras difíciles

### If Voice Sounds Robotic:
- Aumentar temperature (0.8-0.9)
- Agregar samples con más variedad emocional
- Verificar que samples sean naturales
- Reducir repetition_penalty

### If Intonation is Flat:
- Usar más signos de puntuación
- Agregar samples con diferentes emociones
- Aumentar temperature
- Verificar que el texto tenga variedad

### If Consistency is Poor:
- Reducir temperature (0.6-0.7)
- Usar samples más homogéneos
- Aumentar repetition_penalty
- Dividir textos largos en chunks más pequeños

---

## Best Practices

### Do's
- ✅ Test después de cada cambio en voice profile
- ✅ Usar los mismos textos para comparar versiones
- ✅ Documentar qué configuraciones funcionan mejor
- ✅ Probar con contenido real antes de producción
- ✅ Escuchar tests en diferentes dispositivos

### Don'ts
- ❌ No confiar solo en un test
- ❌ No omitir tests de casos edge
- ❌ No asumir que funciona sin verificar
- ❌ No usar textos muy cortos para evaluar
- ❌ No ignorar problemas menores (se acumulan)

---

## Sample Test Results Template

```markdown
# Voice Test Results - [Date]

## Configuration
- Voice Profile: v2.json
- Temperature: 0.75
- Speed: 1.0
- Samples Used: 8 (neutral, happy, serious, calm)

## Test Results

### Basic Pronunciation: 4/5
- Clear pronunciation
- Minor issues with "específicamente"

### Emotional Range: 3/5
- Neutral tone works well
- Excited tone sounds forced

### Numbers & Dates: 5/5
- Perfect pronunciation
- Natural flow

### Long-Form Content: 4/5
- Consistent throughout
- Slight energy drop at end

### Overall: 4/5
- Ready for production
- Consider adding more excited samples

## Action Items
- [ ] Add 2 more enthusiastic samples
- [ ] Test with longer content (5+ min)
- [ ] Adjust temperature to 0.8 for variety
```

---

## Conclusion

Usar estos prompts de forma consistente te permitirá:
- Evaluar calidad objetivamente
- Comparar diferentes versiones del voice profile
- Identificar áreas de mejora específicas
- Asegurar calidad antes de producción
- Documentar progreso a lo largo del tiempo

Recuerda: la calidad de la voz clonada mejora iterativamente. No esperes perfección en el primer intento.
