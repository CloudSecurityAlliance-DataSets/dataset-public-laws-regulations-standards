"""
Utility functions for CWE AI Analysis.

This module contains shared utility functions used across the library.
These are helper functions that don't fit cleanly into other modules.

Design principle:
    Keep utilities focused and well-documented. If a function grows complex
    or is only used in one place, consider moving it to a more specific module.
"""

import logging
import re
from typing import Any, Optional

logger = logging.getLogger(__name__)


def normalize_text(text: str) -> str:
    """
    Normalize text for consistent processing.

    Why normalization:
        CWE data can have inconsistent whitespace, special characters, and
        encoding. Normalizing ensures consistent matching and display.

    Operations:
        - Replace multiple whitespace with single space
        - Strip leading/trailing whitespace
        - Replace common special characters

    Args:
        text: The text to normalize.

    Returns:
        Normalized text string.
    """
    if not text:
        return ""

    # Replace multiple whitespace (including newlines) with single space
    text = re.sub(r"\s+", " ", text)

    # Strip leading/trailing whitespace
    text = text.strip()

    return text


def truncate_text(text: str, max_length: int = 200, suffix: str = "...") -> str:
    """
    Truncate text to a maximum length, adding suffix if truncated.

    Why truncation:
        For display purposes (CLI, reports), long descriptions need to be
        shortened while still being readable.

    Args:
        text: The text to truncate.
        max_length: Maximum length including suffix.
        suffix: String to append when truncated.

    Returns:
        Truncated text, or original if already short enough.
    """
    if not text or len(text) <= max_length:
        return text

    # Truncate and add suffix
    truncate_at = max_length - len(suffix)
    return text[:truncate_at] + suffix


def safe_int(value: Any, default: int = 0) -> int:
    """
    Safely convert a value to integer.

    Why this function:
        CWE data can have various representations of IDs (strings with spaces,
        None values, etc.). This handles conversion gracefully.

    Args:
        value: The value to convert.
        default: Default value if conversion fails.

    Returns:
        Integer value, or default if conversion fails.
    """
    if value is None:
        return default

    if isinstance(value, int):
        return value

    try:
        # Handle string representations
        if isinstance(value, str):
            # Remove any non-numeric characters except minus sign
            cleaned = re.sub(r"[^\d-]", "", value.strip())
            if cleaned:
                return int(cleaned)
        return int(value)
    except (ValueError, TypeError):
        return default


def format_cwe_id(cwe_id: int) -> str:
    """
    Format a CWE ID for display.

    Why formatting:
        Consistent display format (CWE-123) improves readability and
        matches MITRE's convention.

    Args:
        cwe_id: The numeric CWE identifier.

    Returns:
        Formatted string like "CWE-123".
    """
    return f"CWE-{cwe_id}"


def parse_cwe_id(text: str) -> Optional[int]:
    """
    Parse a CWE ID from various text formats.

    Why this function:
        CWE IDs appear in various formats: "CWE-79", "79", "CWE 79", etc.
        This handles them all.

    Args:
        text: Text containing a CWE ID.

    Returns:
        The numeric CWE ID, or None if not found.

    Examples:
        >>> parse_cwe_id("CWE-79")
        79
        >>> parse_cwe_id("79")
        79
        >>> parse_cwe_id("See CWE-1427 for details")
        1427
    """
    if not text:
        return None

    # Try to find CWE-NNN pattern first
    match = re.search(r"CWE[- ]?(\d+)", text, re.IGNORECASE)
    if match:
        return int(match.group(1))

    # Try plain number
    match = re.search(r"\b(\d+)\b", text)
    if match:
        return int(match.group(1))

    return None


def chunk_list(lst: list, chunk_size: int) -> list[list]:
    """
    Split a list into chunks of specified size.

    Why chunking:
        For batch processing (e.g., checkpointing, API calls), we need to
        split large lists into manageable pieces.

    Args:
        lst: The list to chunk.
        chunk_size: Maximum size of each chunk.

    Returns:
        List of chunks (each chunk is a list).

    Example:
        >>> chunk_list([1, 2, 3, 4, 5], 2)
        [[1, 2], [3, 4], [5]]
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def score_to_label(score: int) -> str:
    """
    Convert a numeric score to a human-readable label.

    Why labels:
        Numbers alone aren't meaningful to users. Labels like "Highly Applicable"
        are more informative than "3".

    Args:
        score: Numeric score (0-4).

    Returns:
        Human-readable label.
    """
    labels = {
        0: "Not Applicable",
        1: "Weakly Applicable",
        2: "Moderately Applicable",
        3: "Highly Applicable",
        4: "Primary Example",
    }
    return labels.get(score, f"Unknown ({score})")


def create_progress_bar(
    total: int,
    description: str = "Processing",
    disable: bool = False,
):
    """
    Create a progress bar for iteration.

    Why this wrapper:
        Centralizes progress bar creation with consistent styling.
        Can be disabled for non-interactive use or testing.

    Args:
        total: Total number of items.
        description: Label shown on the progress bar.
        disable: If True, progress bar is hidden (for non-TTY or testing).

    Returns:
        tqdm progress bar instance.
    """
    from tqdm import tqdm

    return tqdm(
        total=total,
        desc=description,
        disable=disable,
        unit="cwe",
        ncols=80,
    )


def validate_file_path(path: str, must_exist: bool = False) -> bool:
    """
    Validate a file path.

    Why validation:
        Catch invalid paths early with clear error messages rather than
        cryptic errors later during file operations.

    Args:
        path: The file path to validate.
        must_exist: If True, the file must already exist.

    Returns:
        True if valid, raises ValueError if not.
    """
    from pathlib import Path

    p = Path(path)

    if must_exist and not p.exists():
        raise ValueError(f"File not found: {path}")

    # Check for invalid characters (basic check)
    invalid_chars = '<>"|?*'
    if any(c in str(p) for c in invalid_chars):
        raise ValueError(f"Invalid characters in path: {path}")

    return True
