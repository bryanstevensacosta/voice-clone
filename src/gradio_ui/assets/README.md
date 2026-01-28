# Assets Directory

This directory contains static assets for the Gradio UI, including:

## Files

### styles.css
Custom CSS styles for the Gradio interface. Use this file to:
- Customize colors and theming
- Adjust layout and spacing
- Add branding elements
- Override default Gradio styles

## Usage

To use custom CSS in the Gradio app:

```python
import gradio as gr

with gr.Blocks(css="src/gradio_ui/assets/styles.css") as app:
    # Your UI components here
    pass
```

## Future Assets

This directory can also contain:
- Images (logos, icons)
- Example audio files
- Documentation resources
- Other static files needed by the UI

## Notes

- Keep assets organized and well-documented
- Optimize images for web use
- Use relative paths when referencing assets
- Consider file size for deployment
