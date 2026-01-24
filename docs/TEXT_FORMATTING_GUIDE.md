# Guía de Formato de Texto para Mejor Calidad

## 🎯 Reglas de Oro

### 1. **Usa Puntuación Correcta**

```
❌ MAL:
hola como estas hoy vamos a hablar de inteligencia artificial

✅ BIEN:
Hola, ¿cómo estás? Hoy vamos a hablar de inteligencia artificial.
```

### 2. **Divide Oraciones Largas**

```
❌ MAL (muy largo):
La inteligencia artificial es una tecnología que permite a las máquinas aprender de datos y tomar decisiones de manera autónoma sin intervención humana directa lo cual ha revolucionado múltiples industrias.

✅ BIEN (dividido):
La inteligencia artificial es una tecnología fascinante. Permite a las máquinas aprender de datos. También pueden tomar decisiones de manera autónoma. Esto ha revolucionado múltiples industrias.
```

### 3. **Usa Pausas Estratégicas**

```
✅ Pausa corta (coma):
Primero, vamos a ver esto. Segundo, esto otro.

✅ Pausa media (punto):
Este es el primer tema. Ahora el segundo.

✅ Pausa larga (puntos suspensivos):
Y el ganador es... ¡tú!

✅ Pausa muy larga (doble salto de línea):
Este es el primer párrafo.

Este es el segundo párrafo.
```

### 4. **Énfasis con Signos**

```
✅ Preguntas:
¿Sabías que la IA puede hacer esto? ¿No es increíble?

✅ Exclamaciones:
¡Hola a todos! ¡Bienvenidos!

✅ Comillas para citas:
Como dijo Einstein: "La imaginación es más importante que el conocimiento".
```

### 5. **Números y Fechas**

```
✅ Escribe números como texto (mejor entonación):
- "veinticinco por ciento" en lugar de "25%"
- "dos mil veinticuatro" en lugar de "2024"
- "tres punto catorce" en lugar de "3.14"

⚠️ O usa el número si quieres que suene técnico:
- "El modelo GPT-4 tiene 1.7 billones de parámetros"
```

### 6. **Longitud Óptima por Chunk**

```
✅ ÓPTIMO: 200-400 caracteres
⚠️ ACEPTABLE: 100-500 caracteres
❌ EVITAR: >500 caracteres (divide en chunks)
```

## 📝 Ejemplos Prácticos

### Ejemplo 1: Intro de Video

```
❌ MAL:
hola bienvenidos a este video hoy vamos a hablar de programacion

✅ BIEN:
¡Hola a todos! Bienvenidos a este nuevo video.
Hoy vamos a hablar sobre programación.
¿Listos? ¡Comencemos!
```

### Ejemplo 2: Explicación Técnica

```
❌ MAL:
las redes neuronales son modelos que aprenden de datos

✅ BIEN:
Las redes neuronales son modelos computacionales fascinantes.
Aprenden patrones directamente de los datos.
Es como enseñarle a una máquina a pensar.
```

### Ejemplo 3: Narración con Emoción

```
❌ MAL:
esto es increible no puedo creerlo funciona muy bien

✅ BIEN:
¡Esto es increíble! No puedo creerlo...
¡Funciona perfectamente! ¿Pueden ver los resultados?
```

## 🎬 Plantillas por Tipo de Contenido

### Tutorial/Educativo
```
Hola, bienvenidos. Hoy vamos a aprender sobre [tema].

Primero, veamos [concepto 1]. Es importante porque [razón].

Segundo, exploremos [concepto 2]. Esto nos permite [beneficio].

Finalmente, [conclusión]. ¿Tiene sentido?

Gracias por ver este tutorial. ¡Nos vemos en el próximo!
```

### Review/Análisis
```
Hoy vamos a revisar [producto/tema].
Después de usarlo durante [tiempo], puedo decir que [opinión general].

Lo bueno: [punto positivo 1]. También [punto positivo 2].

Lo malo: [punto negativo 1]. Además [punto negativo 2].

En conclusión, [veredicto final]. ¿Lo recomiendo? [Sí/No y por qué].
```

### Storytelling/Narrativa
```
Había una vez [introducción].
Todo comenzó cuando [evento inicial].

Entonces, [desarrollo]. Pero luego... [giro].

Al final, [conclusión]. Y así fue como [lección aprendida].
```

## 💡 Tips Avanzados

### 1. Controla el Ritmo
```
Rápido (sin pausas):
"Vamos vamos vamos no hay tiempo que perder"

Normal (con comas):
"Vamos, vamos, vamos. No hay tiempo que perder."

Lento (con puntos y pausas):
"Vamos. Vamos. Vamos... No hay tiempo que perder."
```

### 2. Varía la Estructura
```
❌ Monótono:
"Esto es bueno. Esto es útil. Esto es importante."

✅ Variado:
"Esto es bueno. ¿Por qué? Porque es útil. Y lo más importante... funciona."
```

### 3. Usa Conectores
```
✅ Buenos conectores:
- "Primero... Segundo... Finalmente..."
- "Por un lado... Por otro lado..."
- "Sin embargo... No obstante... Además..."
- "En otras palabras... Es decir... Dicho de otra forma..."
```

## 🔧 Herramientas de Ayuda

### Script de Validación de Texto

Puedes crear un archivo de texto y validarlo antes de generar:

```bash
# Cuenta caracteres
wc -m mi_texto.txt

# Verifica que tenga puntuación
grep -E '[.,;:!?]' mi_texto.txt

# Divide en chunks de 400 caracteres
fold -w 400 -s mi_texto.txt
```

### Checklist Pre-Generación

Antes de generar audio, verifica:
- [ ] ¿Tiene puntuación correcta?
- [ ] ¿Las oraciones son cortas (<30 palabras)?
- [ ] ¿Hay pausas donde deben estar?
- [ ] ¿Los números están escritos como texto?
- [ ] ¿Cada chunk tiene <400 caracteres?
- [ ] ¿Suena natural al leerlo en voz alta?

## 📊 Comparación de Calidad

### Texto Mal Formateado (Calidad: 2/5)
```
hola hoy vamos a hablar de inteligencia artificial que es muy importante en el mundo moderno y tiene muchas aplicaciones practicas en diferentes industrias como la medicina el transporte y la educacion
```

### Texto Bien Formateado (Calidad: 5/5)
```
¡Hola! Hoy vamos a hablar de inteligencia artificial.

Es muy importante en el mundo moderno. ¿Por qué?
Porque tiene aplicaciones prácticas en múltiples industrias.

Por ejemplo: medicina, transporte y educación.
Cada una con casos de uso fascinantes.
```

## 🎓 Ejercicio Práctico

Toma este texto mal formateado y mejóralo:

```
❌ ANTES:
la programacion es importante todos deberian aprender a programar porque es util y te ayuda a pensar mejor ademas hay muchos trabajos bien pagados

✅ DESPUÉS:
La programación es una habilidad fundamental.
¿Por qué todos deberían aprenderla?

Primero, te ayuda a pensar de manera lógica.
Segundo, desarrolla tu capacidad de resolver problemas.

Y además... hay muchos trabajos bien pagados.
¿No es una gran razón para empezar?
```

---

**Recuerda**: El 50% de la calidad viene de los samples, el otro 50% viene del formato del texto. ¡Invierte tiempo en formatear bien!
