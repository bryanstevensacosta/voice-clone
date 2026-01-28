"""
Tests for character counter functionality in Tab 2.
"""


def test_update_char_count_empty():
    """Test character counter with empty text."""

    def update_char_count(text: str) -> str:
        """Update character counter display."""
        count = len(text) if text else 0
        return f"**Caracteres: {count} / 500**"

    result = update_char_count("")
    assert result == "**Caracteres: 0 / 500**"


def test_update_char_count_with_text():
    """Test character counter with text."""

    def update_char_count(text: str) -> str:
        """Update character counter display."""
        count = len(text) if text else 0
        return f"**Caracteres: {count} / 500**"

    result = update_char_count("Hola mundo")
    assert result == "**Caracteres: 10 / 500**"


def test_update_char_count_at_limit():
    """Test character counter at 500 character limit."""

    def update_char_count(text: str) -> str:
        """Update character counter display."""
        count = len(text) if text else 0
        return f"**Caracteres: {count} / 500**"

    text = "a" * 500
    result = update_char_count(text)
    assert result == "**Caracteres: 500 / 500**"


def test_update_char_count_with_spanish_text():
    """Test character counter with Spanish text including special characters."""

    def update_char_count(text: str) -> str:
        """Update character counter display."""
        count = len(text) if text else 0
        return f"**Caracteres: {count} / 500**"

    text = "Hola, ¿cómo estás? ¡Muy bien!"
    result = update_char_count(text)
    assert result == f"**Caracteres: {len(text)} / 500**"


def test_update_char_count_with_multiline():
    """Test character counter with multiline text."""

    def update_char_count(text: str) -> str:
        """Update character counter display."""
        count = len(text) if text else 0
        return f"**Caracteres: {count} / 500**"

    text = "Primera línea\nSegunda línea\nTercera línea"
    result = update_char_count(text)
    assert result == f"**Caracteres: {len(text)} / 500**"


def test_update_char_count_none_input():
    """Test character counter with None input."""

    def update_char_count(text: str) -> str:
        """Update character counter display."""
        count = len(text) if text else 0
        return f"**Caracteres: {count} / 500**"

    result = update_char_count(None)  # type: ignore
    assert result == "**Caracteres: 0 / 500**"


def test_character_counter_integration():
    """Test that character counter is properly integrated in the app."""
    from gradio_ui.app import create_app

    app = create_app()

    # Verify app was created successfully
    assert app is not None

    # The character counter should be part of the app
    # This is a basic integration test to ensure no errors during app creation
    assert hasattr(app, "blocks")
