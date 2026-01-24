#!/bin/bash

# Script para mejorar la calidad del audio generado

if [ $# -eq 0 ]; then
    echo "Uso: ./enhance_audio.sh <archivo_entrada.wav> [archivo_salida.wav]"
    exit 1
fi

INPUT=$1
OUTPUT=${2:-"${INPUT%.wav}_enhanced.wav"}

echo "🎵 Mejorando calidad de audio..."
echo "Input: $INPUT"
echo "Output: $OUTPUT"
echo ""

# Crear archivo temporal
TEMP1="${INPUT%.wav}_temp1.wav"
TEMP2="${INPUT%.wav}_temp2.wav"

# Paso 1: Normalizar volumen (EBU R128)
echo "1️⃣ Normalizando volumen..."
ffmpeg -i "$INPUT" \
    -af "loudnorm=I=-16:TP=-1.5:LRA=11" \
    "$TEMP1" \
    -y -loglevel error

# Paso 2: Reducir ruido de fondo (high-pass filter)
echo "2️⃣ Reduciendo ruido de fondo..."
ffmpeg -i "$TEMP1" \
    -af "highpass=f=80" \
    "$TEMP2" \
    -y -loglevel error

# Paso 3: Comprimir dinámicamente (hace la voz más consistente)
echo "3️⃣ Comprimiendo dinámicamente..."
ffmpeg -i "$TEMP2" \
    -af "acompressor=threshold=-20dB:ratio=3:attack=100:release=500" \
    "$OUTPUT" \
    -y -loglevel error

# Limpiar archivos temporales
rm -f "$TEMP1" "$TEMP2"

echo ""
echo "✅ Audio mejorado guardado en: $OUTPUT"
echo ""
echo "Comparar:"
echo "  Original: afplay $INPUT"
echo "  Mejorado: afplay $OUTPUT"
