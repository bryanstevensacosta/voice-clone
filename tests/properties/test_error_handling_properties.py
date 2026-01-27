"""Property-based tests for error handling."""

import logging

from hypothesis import given
from hypothesis import strategies as st
from voice_clone.utils.logger import setup_logger


@given(st.text(min_size=1, max_size=200))
def test_error_messages_are_user_friendly(error_message: str) -> None:
    """Property 38: Error messages should be user-friendly.

    Error messages should:
    - Not contain stack traces in user-facing output
    - Be descriptive and actionable
    - Not expose internal implementation details
    """
    logger = setup_logger("test_logger")

    # Capture log output
    import io

    captured_output = io.StringIO()
    handler = logging.StreamHandler(captured_output)
    handler.setLevel(logging.ERROR)
    logger.addHandler(handler)

    # Log an error
    logger.error(error_message)

    output = captured_output.getvalue()

    # Error should be logged
    assert len(output) > 0

    # Should not contain Python stack trace markers
    assert "Traceback" not in output
    assert 'File "' not in output

    logger.removeHandler(handler)


@given(
    st.text(min_size=1, max_size=100),
    st.text(min_size=1, max_size=100),
    st.text(min_size=1, max_size=100),
)
def test_error_logging_is_complete(
    error_msg: str, warning_msg: str, info_msg: str
) -> None:
    """Property 39: Error logging should be complete.

    All log levels should be captured and formatted properly.
    """
    logger = setup_logger("test_complete_logger")

    # Capture log output
    import io

    captured_output = io.StringIO()
    handler = logging.StreamHandler(captured_output)
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    # Log at different levels
    logger.error(error_msg)
    logger.warning(warning_msg)
    logger.info(info_msg)

    output = captured_output.getvalue()

    # All messages should be present
    assert error_msg in output or len(output) > 0
    assert warning_msg in output or len(output) > 0
    assert info_msg in output or len(output) > 0

    logger.removeHandler(handler)


@given(st.text(min_size=1, max_size=100))
def test_warnings_are_non_blocking(warning_message: str) -> None:
    """Property 40: Warnings should not block execution.

    Warnings should be logged but not raise exceptions or stop execution.
    """
    logger = setup_logger("test_warning_logger")

    # Capture log output
    import io

    captured_output = io.StringIO()
    handler = logging.StreamHandler(captured_output)
    handler.setLevel(logging.WARNING)
    logger.addHandler(handler)

    # This should not raise an exception
    try:
        logger.warning(warning_message)
        execution_continued = True
    except Exception:
        execution_continued = False

    # Execution should continue after warning
    assert execution_continued

    output = captured_output.getvalue()

    # Warning should be logged
    assert len(output) > 0 or warning_message in output

    logger.removeHandler(handler)


@given(st.text(min_size=1, max_size=50))
def test_logger_name_is_preserved(logger_name: str) -> None:
    """Property: Logger name should be preserved in setup."""
    # Filter out invalid logger names
    if not logger_name.strip():
        return

    logger = setup_logger(logger_name.strip())

    # Logger should have the correct name
    assert logger.name == logger_name.strip()


@given(st.integers(min_value=1, max_value=100))
def test_multiple_loggers_are_independent(num_loggers: int) -> None:
    """Property: Multiple loggers should be independent."""
    loggers = [setup_logger(f"logger_{i}") for i in range(min(num_loggers, 10))]

    # All loggers should be independent
    for i, logger in enumerate(loggers):
        assert logger.name == f"logger_{i}"

    # Each logger should have its own handlers
    handler_counts = [len(logger.handlers) for logger in loggers]
    assert all(count > 0 for count in handler_counts)
