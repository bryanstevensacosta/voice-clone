"""Logging setup with Rich handler for formatted output."""
import logging

from rich.console import Console
from rich.logging import RichHandler


def setup_logger(
    name: str = "voice_clone",
    level: str = "INFO",
    rich_tracebacks: bool = True,
) -> logging.Logger:
    """Setup logger with Rich handler for formatted output.

    Args:
        name: Logger name
        level: Log level (DEBUG, INFO, WARNING, ERROR)
        rich_tracebacks: Enable rich tracebacks for exceptions

    Returns:
        Configured logger instance
    """
    # Create console for rich output
    console = Console(stderr=True)

    # Configure rich handler
    rich_handler = RichHandler(
        console=console,
        rich_tracebacks=rich_tracebacks,
        tracebacks_show_locals=False,
        markup=True,
    )

    # Set format
    rich_handler.setFormatter(
        logging.Formatter(
            "%(message)s",
            datefmt="[%X]",
        )
    )

    # Get or create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))

    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()

    # Add rich handler
    logger.addHandler(rich_handler)

    # Prevent propagation to root logger
    logger.propagate = False

    return logger


def format_error(error: Exception, user_friendly: bool = True) -> str:
    """Format error message in a user-friendly way.

    Args:
        error: Exception to format
        user_friendly: If True, return simplified message. If False, include details.

    Returns:
        Formatted error message
    """
    if user_friendly:
        # User-friendly error messages
        error_type = type(error).__name__
        error_msg = str(error)

        if isinstance(error, FileNotFoundError):
            return f"❌ File not found: {error_msg}"
        elif isinstance(error, PermissionError):
            return f"❌ Permission denied: {error_msg}"
        elif isinstance(error, ValueError):
            return f"❌ Invalid value: {error_msg}"
        elif isinstance(error, RuntimeError):
            return f"❌ Runtime error: {error_msg}"
        else:
            return f"❌ {error_type}: {error_msg}"
    else:
        # Detailed error for debugging
        return f"{type(error).__name__}: {error}"


# Global logger instance
logger = setup_logger()
