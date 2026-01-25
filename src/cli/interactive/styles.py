"""Custom styles for questionary prompts."""

from questionary import Style


def get_custom_style() -> Style:
    """Get custom style for CLI prompts."""
    return Style(
        [
            ("qmark", "fg:#673ab7 bold"),  # Question mark
            ("question", "bold"),  # Question text
            ("answer", "fg:#f44336 bold"),  # Selected answer
            ("pointer", "fg:#673ab7 bold"),  # Pointer (>)
            ("highlighted", "fg:#673ab7 bold"),  # Highlighted option
            ("selected", "fg:#cc5454"),  # Selected option
            ("separator", "fg:#cc5454"),  # Separator
            ("instruction", ""),  # Instruction text
            ("text", ""),  # Normal text
            ("disabled", "fg:#858585 italic"),  # Disabled option
        ]
    )
