"""Local-only word, character, chapter, and reading-time counter.

Pure-Python, no network, no secrets, no personal data. Counts words,
characters, chapters, and estimates reading time for plain-text manuscripts
and Markdown files, with optional chapter breakdown and CSV export.
"""

from .counter import count_file, count_text, DEFAULT_WPM, ChapterStats, CountResult
from .csv_export import write_csv
from .cli import main, build_parser

__all__ = [
    "count_file",
    "count_text",
    "count_markdown",
    "DEFAULT_WPM",
    "ChapterStats",
    "CountResult",
    "write_csv",
    "main",
    "build_parser",
]
__version__ = "1.0.0"


def count_markdown(text: str, path: str = "<stdin>", wpm: int = DEFAULT_WPM) -> CountResult:
    """Count text forcing Markdown heading-based chapter detection."""
    return count_text(text, path, wpm=wpm)
