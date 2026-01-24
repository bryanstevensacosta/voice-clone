"""Audio validation for voice cloning."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ValidationResult:
    """Result of audio validation operation."""

    success: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def is_valid(self) -> bool:
        """Check if validation passed (no errors).

        Warnings are acceptable, only errors make validation fail.

        Returns:
            True if no errors, False otherwise
        """
        return len(self.errors) == 0

    def format_message(self) -> str:
        """Format validation result as user-friendly message.

        Returns:
            Formatted message string
        """
        lines = []

        if self.success and self.is_valid():
            lines.append("✓ Validation passed")
        else:
            lines.append("✗ Validation failed")

        # Add errors
        for error in self.errors:
            lines.append(f"  ✗ ERROR: {error}")

        # Add warnings
        for warning in self.warnings:
            lines.append(f"  ⚠ WARNING: {warning}")

        # Add metadata if present
        if self.metadata:
            lines.append("\nMetadata:")
            for key, value in self.metadata.items():
                lines.append(f"  {key}: {value}")

        return "\n".join(lines)
