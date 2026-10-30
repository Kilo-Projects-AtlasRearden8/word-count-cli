"""CSV export for chapter breakdowns."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import List

from .counter import CountResult


def write_csv(path: str | Path, result: CountResult) -> None:
    """Write a per-chapter breakdown plus totals row to a CSV file."""
    path = Path(path)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(
            [
                "chapter",
                "title",
                "words",
                "characters",
                "characters_no_whitespace",
                "reading_time_seconds",
                "reading_time_minutes",
            ]
        )
        for idx, chapter in enumerate(result.chapters, start=1):
            writer.writerow(
                [
                    idx,
                    chapter.title,
                    chapter.words,
                    chapter.characters,
                    chapter.characters_no_whitespace,
                    round(chapter.reading_time_seconds, 2),
                    round(chapter.reading_time_seconds / 60.0, 4),
                ]
            )
        writer.writerow([])
        writer.writerow(
            [
                "TOTAL",
                "",
                result.words,
                result.characters,
                result.characters_no_whitespace,
                round(result.reading_time_seconds, 2),
                round(result.reading_time_minutes, 4),
            ]
        )
