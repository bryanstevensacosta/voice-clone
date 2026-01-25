# Quick Start - Gradio Implementation

## 🚀 Comenzar Implementación Ahora

Este documento contiene los comandos exactos para comenzar la implementación de la UI con Gradio.

## Paso 1: Setup Inicial (5 minutos)

```bash
# 1. Crear estructura de directorios
mkdir -p src/gradio_ui/{components,handlers,utils,assets}

# 2. Crear archivos __init__.py
touch src/gradio_ui/__init__.py
touch src/gradio_ui/components/__init__.py
touch src/gradio_ui/handlers/__init__.py
touch src/gradio_ui/utils/__init__.py

# 3. Instalar Gradio
pip install gradio>=4.0.0

# 4. Actualizar requirements.txt
echo "gradio>=4.0.0" >> requirements.txt

# 5. Crear directorio para profiles
mkdir -p data/profiles
```

## Paso 2: Copiar Código Base (10 minutos)

### 2.1 Crear `src/gradio_ui/app.py`

Copiar el código completo de `.kiro/steering/gradio_integration.md` sección "Ejemplo Completo de Implementación" al archivo `src/gradio_ui/app.py`.

O usar este comando:

```bash
cat > src/gradio_ui/app.py << 'EOF'
"""
Gradio UI for Voice Clone Tool
"""
import gradio as gr
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any

# TODO: Importar desde voice_clone cuando esté listo
# from voice_clone.audio.processor import AudioProcessor
# from voice_clone.model.profile import VoiceProfile
# from voice_clone.model.generator import VoiceGenerator
# from voice_clone.batch.processor import BatchProcessor


def validate_samples(files: List[str]) -> str:
    """Validate uploaded audio samples."""
    if not files:
        return "⚠️ **No files uploaded**"

    return f"✅ Uploaded {len(files)} files (validation pending implementation)"


def create_voice_profile(
    files: List[str],
    name: str,
    ref_text: str
) -> Tuple[Dict[str, Any], gr.Dropdown, gr.Dropdown]:
    """Create a voice profile from uploaded samples."""
    if not files or not name:
        return {"error": "Missing files or name"}, gr.Dropdown(), gr.Dropdown()

    info = {
        "name": name,
        "samples": len(files),
        "status": "Profile creation pending implementation"
    }

    return info, gr.Dropdown(), gr.Dropdown()


def generate_audio(
    profile_name: str,
    text: str,
    temperature: float,
    speed: float
) -> Tuple[Optional[str], str]:
    """Generate audio from text."""
    if not profile_name or not text:
        return None, "⚠️ **Please select profile and enter text**"

    return None, "⚠️ **Audio generation pending implementation**"


def batch_process(
    profile_name: str,
    script_file: str
) -> Tuple[List[str], str]:
    """Process a script file in batch mode."""
    if not profile_name or not script_file:
        return [], "⚠️ **Please select profile and upload script**"

    return [], "⚠️ **Batch processing pending implementation**"


def get_available_profiles() -> List[str]:
    """Get list of available voice profiles."""
    profiles_dir = Path("data/profiles")
    if not profiles_dir.exists():
        return []
    return [p.stem for p in profiles_dir.glob("*.json")]


def create_app() -> gr.Blocks:
    """Create the Gradio application."""

    with gr.Blocks(
        title="Voice Clone - AI Voice Cloning",
        theme=gr.themes.Soft(primary_hue="blue", secondary_hue="cyan")
    ) as app:

        gr.Markdown("""
        # 🎤 Voice Clone - AI Voice Cloning Tool

        Clone any voice with Qwen3-TTS and generate natural-sounding speech.

        ---
        """)

        with gr.Tabs():

            # Tab 1: Prepare Voice Profile
            with gr.Tab("1️⃣ Prepare Voice Profile"):
                gr.Markdown("### Upload Voice Samples")

                with gr.Row():
                    with gr.Column(scale=1):
                        samples_upload = gr.File(
                            file_count="multiple",
                            file_types=[".wav", ".mp3", ".m4a"],
                            label="Audio Samples (1-3 files)"
                        )

                        profile_name_input = gr.Textbox(
                            label="Profile Name",
                            placeholder="my_voice_profile"
                        )

                        reference_text_input = gr.Textbox(
                            lines=2,
                            label="Reference Text (Optional)",
                            placeholder="Hola, esta es mi voz..."
                        )

                        with gr.Row():
                            validate_btn = gr.Button("🔍 Validate", variant="secondary")
                            create_profile_btn = gr.Button("✨ Create Profile", variant="primary")

                    with gr.Column(scale=1):
                        gr.Markdown("### Results")
                        validation_output = gr.Markdown()
                        profile_output = gr.JSON(label="Profile Info")

            # Tab 2: Generate Audio
            with gr.Tab("2️⃣ Generate Audio"):
                with gr.Row():
                    with gr.Column(scale=1):
                        profile_selector = gr.Dropdown(
                            choices=get_available_profiles(),
                            label="Voice Profile"
                        )

                        text_input = gr.Textbox(
                            lines=5,
                            label="Text to Generate",
                            placeholder="Escribe el texto aquí..."
                        )

                        with gr.Accordion("⚙️ Advanced Settings", open=False):
                            temperature_slider = gr.Slider(0.5, 1.0, 0.75, label="Temperature")
                            speed_slider = gr.Slider(0.8, 1.2, 1.0, label="Speed")

                        generate_btn = gr.Button("🎙️ Generate Audio", variant="primary", size="lg")

                    with gr.Column(scale=1):
                        gr.Markdown("### Output")
                        output_audio = gr.Audio(label="Generated Audio", type="filepath")
                        generation_info = gr.Markdown()

            # Tab 3: Batch Processing
            with gr.Tab("3️⃣ Batch Processing"):
                with gr.Row():
                    with gr.Column(scale=1):
                        profile_selector_batch = gr.Dropdown(
                            choices=get_available_profiles(),
                            label="Voice Profile"
                        )

                        script_file_input = gr.File(
                            label="Script File (.txt)",
                            file_types=[".txt"]
                        )

                        batch_btn = gr.Button("⚡ Process Batch", variant="primary", size="lg")

                    with gr.Column(scale=1):
                        batch_output = gr.File(label="Generated Files", file_count="multiple")
                        batch_info = gr.Markdown()

        # Event Handlers
        validate_btn.click(
            fn=validate_samples,
            inputs=[samples_upload],
            outputs=[validation_output]
        )

        create_profile_btn.click(
            fn=create_voice_profile,
            inputs=[samples_upload, profile_name_input, reference_text_input],
            outputs=[profile_output, profile_selector, profile_selector_batch]
        )

        generate_btn.click(
            fn=generate_audio,
            inputs=[profile_selector, text_input, temperature_slider, speed_slider],
            outputs=[output_audio, generation_info],
            show_progress="full"
        )

        batch_btn.click(
            fn=batch_process,
            inputs=[profile_selector_batch, script_file_input],
            outputs=[batch_output, batch_info],
            show_progress="full"
        )

    return app


def main():
    """Launch the Gradio application."""
    app = create_app()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )


if __name__ == "__main__":
    main()
EOF
```

## Paso 3: Probar UI Básica (2 minutos)

```bash
# Ejecutar la aplicación
python src/gradio_ui/app.py

# Abrir en navegador: http://localhost:7860
```

Deberías ver la interfaz con 3 tabs, aunque las funciones aún no están implementadas.

## Paso 4: Agregar Comando CLI (5 minutos)

### 4.1 Editar `src/voice_clone/cli.py`

Agregar al final del archivo (antes de `if __name__ == "__main__"`):

```python
@cli.command()
@click.option("--port", default=7860, help="Port to run the UI")
@click.option("--share", is_flag=True, help="Create public link")
def ui(port: int, share: bool):
    """Launch the Gradio web interface."""
    try:
        from gradio_ui.app import create_app

        app = create_app()
        app.launch(
            server_name="0.0.0.0",
            server_port=port,
            share=share,
            show_error=True
        )
    except ImportError:
        click.secho("❌ Gradio not installed. Run: pip install gradio>=4.0.0", fg="red")
        sys.exit(1)
```

### 4.2 Probar comando

```bash
# Reinstalar en modo editable
pip install -e .

# Probar comando
voice-clone ui

# Con opciones
voice-clone ui --port 8080
voice-clone ui --share  # Crear link público
```

## Paso 5: Implementar Handlers (30-60 minutos)

### 5.1 Sample Handler

```bash
cat > src/gradio_ui/handlers/sample_handler.py << 'EOF'
"""Handler for sample validation."""
from pathlib import Path
from typing import List
from voice_clone.audio.processor import AudioProcessor


def validate_samples_handler(files: List[str]) -> str:
    """Validate uploaded audio samples."""
    if not files:
        return "⚠️ **No files uploaded**"

    processor = AudioProcessor()
    results = ["## Validation Results\n"]

    for file_path in files:
        try:
            result = processor.validate_sample(Path(file_path))

            if result.is_valid:
                results.append(f"### ✅ {Path(file_path).name}")
                results.append(f"- Duration: {result.duration:.1f}s")
                results.append(f"- Sample Rate: {result.sample_rate} Hz")
                results.append(f"- Channels: {result.channels}\n")
            else:
                results.append(f"### ❌ {Path(file_path).name}")
                for error in result.errors:
                    results.append(f"- ⚠️ {error}")
                results.append("")
        except Exception as e:
            results.append(f"### ❌ {Path(file_path).name}")
            results.append(f"- ⚠️ Error: {str(e)}\n")

    return "\n".join(results)
EOF
```

### 5.2 Actualizar `app.py` para usar el handler

Reemplazar la función `validate_samples` en `app.py`:

```python
from gradio_ui.handlers.sample_handler import validate_samples_handler as validate_samples
```

### 5.3 Repetir para otros handlers

Crear archivos similares para:
- `profile_handler.py`
- `generation_handler.py`
- `batch_handler.py`

## Paso 6: Testing (15 minutos)

```bash
# Crear test básico
cat > tests/gradio_ui/test_app.py << 'EOF'
"""Tests for Gradio app."""
import pytest
from gradio_ui.app import create_app


def test_app_creation():
    """Test that app can be created."""
    app = create_app()
    assert app is not None


def test_app_has_tabs():
    """Test that app has expected tabs."""
    app = create_app()
    # TODO: Add more specific tests
    assert True
EOF

# Ejecutar tests
pytest tests/gradio_ui/
```

## Paso 7: Actualizar pyproject.toml (5 minutos)

```bash
# Editar pyproject.toml manualmente
# Cambiar:
# name = "voice-clone-cli" → name = "voice-clone"
# description = "..." → "AI voice cloning tool with web UI and CLI"

# Agregar en dependencies:
# gradio = ">=4.0.0"

# Agregar en [project.scripts]:
# voice-clone-ui = "gradio_ui.app:main"
```

## Checklist de Implementación

### Fase 1: Setup ✅
- [ ] Estructura de directorios creada
- [ ] Gradio instalado
- [ ] `app.py` básico creado
- [ ] UI se inicia correctamente
- [ ] Comando `voice-clone ui` funciona

### Fase 2: Handlers 🔄
- [ ] `sample_handler.py` implementado
- [ ] `profile_handler.py` implementado
- [ ] `generation_handler.py` implementado
- [ ] `batch_handler.py` implementado
- [ ] Todos los handlers integrados en `app.py`

### Fase 3: Testing 🔄
- [ ] Tests unitarios de handlers
- [ ] Tests de integración
- [ ] Manual testing completo

### Fase 4: Polish 🔄
- [ ] CSS personalizado
- [ ] Manejo de errores robusto
- [ ] Progress bars funcionando
- [ ] Ejemplos pre-cargados

### Fase 5: Documentation 🔄
- [ ] Screenshots capturados
- [ ] User guide creado
- [ ] README actualizado con screenshots
- [ ] Deployment guide

## Comandos Útiles Durante Desarrollo

```bash
# Reiniciar UI después de cambios
# Ctrl+C para detener
python src/gradio_ui/app.py

# O con comando CLI
voice-clone ui

# Ver logs en tiempo real
voice-clone ui --debug

# Ejecutar tests específicos
pytest tests/gradio_ui/test_handlers.py -v

# Ejecutar con coverage
pytest --cov=gradio_ui tests/gradio_ui/

# Formatear código
black src/gradio_ui/

# Linting
ruff check src/gradio_ui/
```

## Troubleshooting

### Error: "Module 'gradio_ui' not found"

```bash
# Reinstalar en modo editable
pip install -e .
```

### Error: "Cannot import AudioProcessor"

```bash
# Verificar que voice_clone está instalado
pip install -e .

# Verificar imports en app.py
python -c "from voice_clone.audio.processor import AudioProcessor"
```

### UI no se actualiza después de cambios

```bash
# Gradio tiene hot reload, pero a veces necesitas reiniciar
# Ctrl+C y volver a ejecutar
python src/gradio_ui/app.py
```

## Próximos Pasos

1. ✅ Completar Fase 1 (Setup)
2. 🔄 Implementar Fase 2 (Handlers)
3. ⏳ Implementar Fase 3 (Testing)
4. ⏳ Implementar Fase 4 (Polish)
5. ⏳ Implementar Fase 5 (Documentation)

## Recursos

- [Gradio Integration Guide](.kiro/steering/gradio_integration.md)
- [Migration Guide](GRADIO_MIGRATION.md)
- [Implementation Summary](IMPLEMENTATION_SUMMARY.md)
- [Gradio Docs](https://www.gradio.app/docs)

---

**¡Comienza ahora!** Ejecuta los comandos del Paso 1 y tendrás la UI básica funcionando en 5 minutos.
