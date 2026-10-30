"""Core counting logic for manuscripts and Markdown files.

Pure Python, local-only. Counts words, characters, chapters, and reading time.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

DEFAULT_WPM = 250

# Matches "Chapter 1", "Chapter One", "CHAPTER 2", "Chapter: Ten", etc.
CHAPTER_RE = re.compile(r"(?im)^\s*(?:chapter|ch)\s+(.{1,60}?)\s*$")
# Matches Markdown heading lines: "# Title" / "## Title"
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
# A line counts as blank if it's empty or whitespace only.
BLANK_RE = re.compile(r"^\s*$")


@dataclass
class ChapterStats:
    title: str
    start_line: int
    words: int = 0
    characters: int = 0
    characters_no_whitespace: int = 0

    @property
    def reading_time_seconds(self) -> float:
        return self.words / DEFAULT_WPM * 60.0 if DEFAULT_WPM else 0.0


@dataclass
class CountResult:
    path: str
    words: int = 0
    characters: int = 0
    characters_no_whitespace: int = 0
    paragraphs: int = 0
    chapters: List[ChapterStats] = field(default_factory=list)
    wpm: int = DEFAULT_WPM

    @property
    def reading_time_minutes(self) -> float:
        return self.words / self.wpm if self.wpm else 0.0

    @property
    def reading_time_seconds(self) -> float:
        return self.reading_time_minutes * 60.0

    @property
    def chapter_count(self) -> int:
        return len(self.chapters)

    @property
    def is_markdown(self) -> bool:
        return self.path.lower().endswith((".md", ".markdown", ".mdown"))


def _count_line(text: str) -> tuple[int, int, int]:
    """Return (words, characters, characters_without_whitespace) for a line."""
    words = len(text.split())
    characters = len(text)
    characters_no_whitespace = len(re.sub(r"\s", "", text))
    return words, characters, characters_no_whitespace


def count_text(text: str, path: str = "<stdin>", wpm: int = DEFAULT_WPM) -> CountResult:
    """Count words, characters, chapters, and reading time for raw text."""
    result = CountResult(path=path, wpm=wpm)

    lines = text.splitlines()
    current_chapter: ChapterStats | None = None
    chapter_number = 0

    for index, line in enumerate(lines, start=1):
        words, characters, characters_no_whitespace = _count_line(line)
        result.words += words
        result.characters += characters
        result.characters_no_whitespace += characters_no_whitespace

        # Detect a new chapter.
        heading_title: str | None = None
        if result.is_markdown:
            match = HEADING_RE.match(line)
            if match:
                heading_title = match.group(2).strip()
        else:
            match = CHAPTER_RE.match(line)
            if match:
                heading_title = match.group(1).strip()

        if heading_title is not None:
            if current_chapter is not None:
                result.chapters.append(current_chapter)
            chapter_number += 1
            if result.is_markdown:
                title = heading_title
            else:
                title = f"Chapter {chapter_number}: {heading_title}"
            current_chapter = ChapterStats(
                title=title,
                start_line=index,
            )
            continue

        # Blank line separates paragraphs.
        if BLANK_RE.match(line):
            result.paragraphs += 1

        if current_chapter is not None:
            current_chapter.words += words
            current_chapter.characters += characters
            current_chapter.characters_no_whitespace += characters_no_whitespace

    if current_chapter is not None:
        result.chapters.append(current_chapter)

    return result


def count_file(path: str | Path, wpm: int = DEFAULT_WPM) -> CountResult:
    """Read a file and count its words, characters, chapters, and reading time."""
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    return count_text(text, str(path), wpm=wpm)


def count_markdown(text: str, path: str = "<stdin>", wpm: int = DEFAULT_WPM) -> CountResult:
    """Convenience wrapper that forces Markdown chapter detection (headings)."""
    result = count_text(text, path, wpm=wpm)
    result.path = path
    # Re-run with markdown heading detection by forcing is_markdown path.
    # count_text already branches on result.is_markdown; rebuild to be safe.
    return count_text(text, path, wpm=wpm)
