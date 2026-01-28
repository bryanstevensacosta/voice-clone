"""
Gradio UI for Voice Clone Tool

This module provides a web-based user interface for the voice cloning tool
using Gradio. It offers three main workflows:
1. Prepare Voice Profile - Upload and validate audio samples
2. Generate Audio - Convert text to speech using cloned voice
3. Batch Processing - Process multiple text segments at once
"""

import gradio as gr

from gradio_ui.handlers.batch_handler import batch_process_handler

# Import handlers
from gradio_ui.handlers.generation_handler import generate_audio_handler
from gradio_ui.handlers.profile_handler import (
    create_profile_handler,
    list_available_profiles,
)
from gradio_ui.handlers.sample_handler import validate_samples_handler
from gradio_ui.handlers.visualization_handler import generate_sample_visualization


def create_app() -> gr.Blocks:
    """
    Create and configure the Gradio application.

    Returns:
        gr.Blocks: Configured Gradio application instance
    """

    app: gr.Blocks
    with gr.Blocks(title="Voice Clone - AI Voice Cloning") as app:
        # Header
        gr.Markdown("""
        # AI Voice Cloning Tool

        Clone any voice with just a few audio samples and generate natural-sounding speech using **Qwen3-TTS**.

        ---
        """)

        # Main tabs for different workflows
        with gr.Tabs():
            # Tab 1: Prepare Voice Profile
            with gr.Tab("1️⃣ Prepare Voice Profile"):
                gr.Markdown("""
                ### Step 1: Upload Voice Samples

                Upload 1-3 audio samples (10-20 seconds each) of the voice you want to clone.
                Samples should be clear, without background noise, and include different emotions/tones.
                """)

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

                        # Audio visualization
                        gr.Markdown("### 🎵 Audio Visualization")
                        spectrogram_plot = gr.Plot(
                            label="Spectrogram & Waveform", visible=True
                        )

            # Tab 2: Generate Audio
            with gr.Tab("2️⃣ Generate Audio"):
                gr.Markdown("""
                ### Step 2: Generate Speech from Text

                Select a voice profile and enter the text you want to convert to speech.
                """)

                with gr.Row():
                    with gr.Column(scale=1):
                        gr.Markdown("### 🎭 Input")

                        # Profile selection dropdown
                        available_profiles = list_available_profiles()
                        profile_selector = gr.Dropdown(
                            choices=available_profiles,
                            label="Select Voice Profile",
                            info=(
                                "Choose a previously created profile"
                                if available_profiles
                                else "⚠️ No profiles available. Create one in Tab 1 first."
                            ),
                        )

                        text_input = gr.Textbox(
                            lines=8,
                            max_lines=20,
                            label="Text to Generate",
                            placeholder="Escribe el texto que quieres convertir a voz...\n\nPuedes escribir hasta 500 caracteres para mejor calidad.",
                            max_length=500,
                        )

                        # Character counter
                        char_counter = gr.Markdown(
                            value="**Caracteres: 0 / 500**", visible=True
                        )

                        with gr.Accordion("⚙️ Advanced Settings", open=False):
                            temperature_slider = gr.Slider(
                                minimum=0.5,
                                maximum=1.0,
                                value=0.75,
                                step=0.05,
                                label="Temperature",
                                info="Control variability (lower = more consistent, higher = more varied)",
                            )

                            speed_slider = gr.Slider(
                                minimum=0.8,
                                maximum=1.2,
                                value=1.0,
                                step=0.05,
                                label="Speed",
                                info="Speaking speed multiplier",
                            )

                        generate_btn = gr.Button(
                            "🎙️ Generate Audio", variant="primary", size="lg"
                        )

                    with gr.Column(scale=1):
                        gr.Markdown("### 🔊 Output")
                        output_audio = gr.Audio(
                            label="Generated Audio",
                            type="filepath",
                            interactive=False,
                            buttons=["download"],
                        )
                        generation_info = gr.Markdown()

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
                gr.Markdown("""
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
                """)

                with gr.Row():
                    with gr.Column(scale=1):
                        gr.Markdown("### 📄 Input")

                        # Profile selection dropdown (synced with Tab 2)
                        available_profiles_batch = list_available_profiles()
                        profile_selector_batch = gr.Dropdown(
                            choices=available_profiles_batch,
                            label="Select Voice Profile",
                            info=(
                                "Choose a previously created profile"
                                if available_profiles_batch
                                else "⚠️ No profiles available. Create one in Tab 1 first."
                            ),
                        )

                        script_file_input = gr.File(
                            label="Upload Script File (.txt)",
                            file_types=[".txt", ".md"],
                            type="filepath",
                        )

                        batch_btn = gr.Button(
                            "⚡ Process Batch", variant="primary", size="lg"
                        )

                    with gr.Column(scale=1):
                        gr.Markdown("### 📦 Output")
                        batch_output = gr.File(
                            label="Generated Files", file_count="multiple"
                        )
                        batch_info = gr.Markdown()

        # Footer
        gr.Markdown("""
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
        """)

        # Event Handlers
        # Tab 1: Validation
        validate_btn.click(
            fn=validate_samples_handler,
            inputs=[samples_upload],
            outputs=[validation_output],
            show_progress="minimal",
        )

        # Tab 1: Update spectrogram when files are uploaded
        samples_upload.change(
            fn=generate_sample_visualization,
            inputs=[samples_upload],
            outputs=[spectrogram_plot],
        )

        # Tab 1: Profile Creation
        create_profile_btn.click(
            fn=create_profile_handler,
            inputs=[samples_upload, profile_name_input, reference_text_input],
            outputs=[profile_output, profile_selector, profile_selector_batch],
            show_progress="full",
        )

        # Tab 2: Character counter update
        def update_char_count(text: str) -> str:
            """Update character counter display."""
            count = len(text) if text else 0
            return f"**Caracteres: {count} / 500**"

        text_input.change(
            fn=update_char_count,
            inputs=[text_input],
            outputs=[char_counter],
        )

        # Tab 2: Audio Generation
        generate_btn.click(
            fn=generate_audio_handler,
            inputs=[profile_selector, text_input, temperature_slider, speed_slider],
            outputs=[output_audio, generation_info],
            show_progress="full",
        )

        # Tab 3: Batch Processing
        batch_btn.click(
            fn=batch_process_handler,
            inputs=[profile_selector_batch, script_file_input],
            outputs=[batch_output, batch_info],
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
