#!/bin/bash

# Script para convertir archivos M4A del iPhone al formato correcto para voice cloning
# Formato objetivo: WAV, 22050 Hz, Mono, 16-bit

echo "🎵 Convirtiendo archivos M4A a WAV..."
echo ""

# Crear directorio de salida si no existe
mkdir -p data/samples

# Contador
count=0
total=$(ls recordings-from-iphone/*.m4a 2>/dev/null | wc -l)

echo "📁 Encontrados: $total archivos M4A"
echo ""

# Convertir cada archivo
for file in recordings-from-iphone/*.m4a; do
    if [ -f "$file" ]; then
        # Obtener nombre base sin extensión
        basename=$(basename "$file" .m4a)
        
        # Crear nombre de salida más simple
        count=$((count + 1))
        output="data/samples/sample_$(printf "%02d" $count).wav"
        
        echo "[$count/$total] Convirtiendo: $basename"
        
        # Convertir con FFmpeg
        ffmpeg -i "$file" \
            -ar 22050 \
            -ac 1 \
            -sample_fmt s16 \
            -af "loudnorm=I=-16:TP=-1.5:LRA=11" \
            "$output" \
            -y \
            -loglevel error
        
        if [ $? -eq 0 ]; then
            # Obtener duración
            duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$output")
            duration_int=$(printf "%.0f" $duration)
            echo "   ✓ Guardado: $output (${duration_int}s)"
        else
            echo "   ✗ Error al convertir: $basename"
        fi
        echo ""
    fi
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Conversión completada!"
echo "📊 Total convertidos: $count archivos"
echo "📁 Ubicación: data/samples/"
echo ""
echo "🔍 Siguiente paso: Validar los samples"
echo "   voice-clone validate-samples --dir ./data/samples"
echo ""
