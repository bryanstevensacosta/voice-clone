"""Domain exceptions for TTS Studio.

Domain-specific exceptions that represent business rule violations.
These exceptions are part of the domain layer and have no infrastructure dependencies.
"""


class DomainException(Exception):
    """Base exception for all domain-level errors.

    All domain exceptions should inherit from this base class.
    This allows catching all domain errors with a single except clause.
    """

    pass


class InvalidProfileException(DomainException):
    """Raised when a voice profile does not meet business requirements.

    Examples:
    - Profile has too few samples
    - Total duration is too short or too long
    - Profile name is empty
    - Samples have invalid format
    """

    def __init__(self, message: str, validation_errors: list[str] | None = None):
        """Initialize the exception.

        Args:
            message: Error message
            validation_errors: List of specific validation errors
        """
        super().__init__(message)
        self.validation_errors = validation_errors or []


class InvalidSampleException(DomainException):
    """Raised when an audio sample does not meet requirements.

    Examples:
    - Sample duration is too short or too long
    - Sample rate is incorrect
    - Sample is not mono
    - Bit depth is incorrect
    - File format is unsupported
    """

    def __init__(self, message: str, sample_path: str | None = None):
        """Initialize the exception.

        Args:
            message: Error message
            sample_path: Path to the invalid sample
        """
        super().__init__(message)
        self.sample_path = sample_path


class GenerationException(DomainException):
    """Raised when audio generation fails.

    Examples:
    - TTS engine fails to generate audio
    - Profile is incompatible with engine
    - Text is too long
    - Output path is invalid
    """

    def __init__(
        self,
        message: str,
        profile_id: str | None = None,
        text_length: int | None = None,
    ):
        """Initialize the exception.

        Args:
            message: Error message
            profile_id: ID of the profile used
            text_length: Length of text that failed to generate
        """
        super().__init__(message)
        self.profile_id = profile_id
        self.text_length = text_length
