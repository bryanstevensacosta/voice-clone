"""Helper functions and utilities for voice cloning."""
from pathlib import Path


def validate_path(path: str | Path, must_exist: bool = False) -> Path:
    """Validate and convert path to Path object.

    Args:
        path: Path string or Path object
        must_exist: If True, raise error if path doesn't exist

    Returns:
        Validated Path object

    Raises:
        ValueError: If path is invalid
        FileNotFoundError: If must_exist=True and path doesn't exist
    """
    try:
        path_obj = Path(path)
    except Exception as e:
        raise ValueError(f"Invalid path: {path}") from e

    if must_exist and not path_obj.exists():
        raise FileNotFoundError(f"Path does not exist: {path_obj}")

    return path_obj


def ensure_directory(path: str | Path) -> Path:
    """Ensure directory exists, create if it doesn't.

    Args:
        path: Directory path

    Returns:
        Path object to directory

    Raises:
        PermissionError: If cannot create directory
    """
    path_obj = Path(path)

    if not path_obj.exists():
        try:
            path_obj.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise PermissionError(f"Cannot create directory: {path_obj}") from e

    if not path_obj.is_dir():
        raise ValueError(f"Path exists but is not a directory: {path_obj}")

    return path_obj


def file_exists(path: str | Path) -> bool:
    """Check if file exists.

    Args:
        path: File path

    Returns:
        True if file exists, False otherwise
    """
    try:
        path_obj = Path(path)
        return path_obj.exists() and path_obj.is_file()
    except Exception:
        return False


def safe_read_file(path: str | Path, encoding: str = "utf-8") -> str | None:
    """Safely read file content.

    Args:
        path: File path
        encoding: File encoding

    Returns:
        File content or None if error
    """
    try:
        path_obj = Path(path)
        with open(path_obj, encoding=encoding) as f:
            return f.read()
    except Exception:
        return None


def safe_write_file(path: str | Path, content: str, encoding: str = "utf-8") -> bool:
    """Safely write content to file.

    Args:
        path: File path
        content: Content to write
        encoding: File encoding

    Returns:
        True if successful, False otherwise
    """
    try:
        path_obj = Path(path)
        # Ensure parent directory exists
        path_obj.parent.mkdir(parents=True, exist_ok=True)

        with open(path_obj, "w", encoding=encoding) as f:
            f.write(content)
        return True
    except Exception:
        return False


def get_file_size(path: str | Path) -> int:
    """Get file size in bytes.

    Args:
        path: File path

    Returns:
        File size in bytes, or 0 if error
    """
    try:
        path_obj = Path(path)
        return path_obj.stat().st_size
    except Exception:
        return 0


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format.

    Args:
        size_bytes: Size in bytes

    Returns:
        Formatted size string (e.g., "1.5 MB")
    """
    size: float = float(size_bytes)
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} PB"
