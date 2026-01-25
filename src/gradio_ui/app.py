"""
Gradio UI for Voice Clone Tool

This module provides a web-based user interface for the voice cloning tool
using Gradio. It offers three main workflows:
1. Prepare Voice Profile - Upload and validate audio samples
2. Generate Audio - Convert text to speech using cloned voice
3. Batch Processing - Process multiple text segments at once
"""


import gradio as gr

from gradio_ui.handlers.profile_handler import (
    create_profile_handler,
    list_available_profiles,
)

# Import handlers
from gradio_ui.handlers.sample_handler import validate_samples_handler


def create_app() -> gr.Blocks:
    """
    Create and configure the Gradio application.

    Returns:
        gr.Blocks: Configured Gradio application instance
    """

    with gr.Blocks(title="Voice Clone - AI Voice Cloning") as app:
        # Header
        gr.Markdown(
            """
        # 🎤 Voice Clone - AI Voice Cloning Tool

        Clone any voice with just a few audio samples and generate natural-sounding speech using **Qwen3-TTS**.

        ---
        """
        )

        # Main tabs for different workflows
        with gr.Tabs():
            # Tab 1: Prepare Voice Profile
            with gr.Tab("1️⃣ Prepare Voice Profile"):
                gr.Markdown(
                    """
                ### Step 1: Upload Voice Samples

                Upload 1-3 audio samples (10-20 seconds each) of the voice you want to clone.
                Samples should be clear, without background noise, and include different emotions/tones.
                """
                )

                with gr.Row():
                    with gr.Column(scale=1):
                        gr.Markdown("### 📁 Upload Samples")

                        # Placeholder components - will be implemented in Phase 2
                        samples_upload = gr.File(
                            file_count="multiple",
                            file_types=[".wav", ".mp3", ".m4a", ".flac"],
                            label="Audio Samples (1-3 files)",
                            type="filepath",
                        )

                        profile_name_input = gr.Textbox(
                            label="Profile Name",
                            placeholder="my_voice_profile",
                            max_lines=1,
                        )

                        reference_text_input = gr.Textbox(
                            lines=2,
                            label="Reference Text (Optional)",
                            placeholder="Hola, esta es una muestra de mi voz para clonación.",
                            info="Describe the content of your samples",
                        )

                        with gr.Row():
                            validate_btn = gr.Button(
                                "🔍 Validate Samples", variant="secondary", size="sm"
                            )
                            create_profile_btn = gr.Button(
                                "✨ Create Voice Profile", variant="primary", size="sm"
                            )

                    with gr.Column(scale=1):
                        gr.Markdown("### 📊 Results")
                        validation_output = gr.Markdown(
                            value="Upload samples and click **Validate** to check quality."
                        )
                        profile_output = gr.JSON(label="Voice Profile Info")

            # Tab 2: Generate Audio
            with gr.Tab("2️⃣ Generate Audio"):
                gr.Markdown(
                    """
                ### Step 2: Generate Speech from Text

                Select a voice profile and enter the text you want to convert to speech.
                """
                )

                with gr.Row():
                    with gr.Column(scale=1):
                        gr.Markdown("### 🎭 Input")

                        # Placeholder components - will be implemented in Phase 3
                        profile_selector = gr.Dropdown(
                            choices=list_available_profiles(),
                            label="Select Voice Profile",
                            info="Choose a previously created profile",
                        )

                        text_input = gr.Textbox(
                            lines=8,
                            max_lines=20,
                            label="Text to Generate",
                            placeholder="Escribe el texto que quieres convertir a voz...\n\nPuedes escribir hasta 2048 tokens (~500 caracteres recomendado para mejor calidad).",
                            max_length=2048,
                        )

                        with gr.Accordion("⚙️ Advanced Settings", open=False):
                            _temperature_slider = gr.Slider(
                                minimum=0.5,
                                maximum=1.0,
                                value=0.75,
                                step=0.05,
                                label="Temperature",
                                info="Control variability (lower = more consistent, higher = more varied)",
                            )

                            _speed_slider = gr.Slider(
                                minimum=0.8,
                                maximum=1.2,
                                value=1.0,
                                step=0.05,
                                label="Speed",
                                info="Speaking speed multiplier",
                            )

                        _generate_btn = gr.Button(
                            "🎙️ Generate Audio", variant="primary", size="lg"
                        )

                    with gr.Column(scale=1):
                        gr.Markdown("### 🔊 Output")
                        _output_audio = gr.Audio(
                            label="Generated Audio", type="filepath", interactive=False
                        )
                        _generation_info = gr.Markdown()

                # Example texts
                gr.Examples(
                    examples=[
                        [
                            "Hola, bienvenidos a este tutorial sobre inteligencia artificial."
                        ],
                        [
                            "La tecnología está transformando el mundo de maneras increíbles."
                        ],
                        [
                            "Gracias por ver este video. No olvides suscribirte al canal."
                        ],
                    ],
                    inputs=[text_input],
                    label="💡 Example Texts",
                )

            # Tab 3: Batch Processing
            with gr.Tab("3️⃣ Batch Processing"):
                gr.Markdown(
                    """
                ### Step 3: Process Multiple Segments

                Upload a script file with multiple text segments to generate audio for each one.

                **Script Format**:
                ```
                [INTRO]
                Hola, bienvenidos a este video.

                [SECTION_1]
                Hoy vamos a hablar sobre...

                [OUTRO]
                Gracias por ver.
                ```
                """
                )

                with gr.Row():
                    with gr.Column(scale=1):
                        gr.Markdown("### 📄 Input")

                        # Placeholder components - will be implemented in Phase 4
                        profile_selector_batch = gr.Dropdown(
                            choices=list_available_profiles(),
                            label="Select Voice Profile",
                        )

                        _script_file_input = gr.File(
                            label="Upload Script File (.txt)",
                            file_types=[".txt", ".md"],
                            type="filepath",
                        )

                        _batch_btn = gr.Button(
                            "⚡ Process Batch", variant="primary", size="lg"
                        )

                    with gr.Column(scale=1):
                        gr.Markdown("### 📦 Output")
                        _batch_output = gr.File(
                            label="Generated Files", file_count="multiple"
                        )
                        _batch_info = gr.Markdown()

        # Footer
        gr.Markdown(
            """
        ---

        ### 📚 Tips for Best Results:

        - **Samples**: Use clear audio without background noise
        - **Duration**: 10-20 seconds per sample is optimal
        - **Variety**: Include different emotions and tones
        - **Text Length**: Keep under 500 characters for best quality
        - **Format**: WAV files at 12000 Hz work best

        ### 🔗 Resources:

        - [Documentation](https://github.com/yourusername/voice-clone)
        - [Report Issues](https://github.com/yourusername/voice-clone/issues)
        - Powered by [Qwen3-TTS](https://github.com/QwenLM/Qwen-Audio)
        """
        )

        # Event Handlers
        # Tab 1: Validation
        validate_btn.click(
            fn=validate_samples_handler,
            inputs=[samples_upload],
            outputs=[validation_output],
            show_progress="minimal",
        )

        # Tab 1: Profile Creation
        create_profile_btn.click(
            fn=create_profile_handler,
            inputs=[samples_upload, profile_name_input, reference_text_input],
            outputs=[profile_output, profile_selector, profile_selector_batch],
            show_progress="full",
        )

    return app


def main(server_port: int = 7860, share: bool = False) -> None:
    """
    Launch the Gradio application.

    This is the entry point for the CLI command `voice-clone ui`.

    Args:
        server_port: Port to run the server on (default: 7860)
        share: Whether to create a public shareable link (default: False)
    """
    app = create_app()
    app.launch(
        server_name="0.0.0.0",
        server_port=server_port,
        share=share,
        show_error=True,
        quiet=False,
    )


if __name__ == "__main__":
    main()
