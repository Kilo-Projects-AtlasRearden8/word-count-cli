"""Command-line interface for the word-count tool."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import List, Optional

from .counter import count_file, DEFAULT_WPM, ChapterStats


def _format_seconds(seconds: float) -> str:
    total = int(round(seconds))
    minutes, secs = divmod(total, 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours}h {minutes}m {secs}s"
    if minutes:
        return f"{minutes}m {secs}s"
    return f"{secs}s"


def _print_summary(result) -> None:
    print(f"File: {result.path}")
    print(f"Words: {result.words:,}")
    print(f"Characters: {result.characters:,}")
    print(f"Characters (no whitespace): {result.characters_no_whitespace:,}")
    print(f"Paragraphs: {result.paragraphs:,}")
    print(f"Chapters: {result.chapter_count}")
    print(f"Reading time (@{result.wpm} wpm): {_format_seconds(result.reading_time_seconds)}")


def _print_chapters(result) -> None:
    if not result.chapters:
        print("\nNo chapters detected.")
        return
    print("\nChapter breakdown:")
    print(f"{'#':<4} {'Title':<40} {'Words':>7} {'Chars':>8} {'Read':>8}")
    print("-" * 72)
    for idx, chapter in enumerate(result.chapters, start=1):
        read = _format_seconds(chapter.reading_time_seconds)
        title = chapter.title[:38]
        print(f"{idx:<4} {title:<40} {chapter.words:>7,} {chapter.characters:>8,} {read:>8}")


def _write_csv(path: str, result, chapters: List[ChapterStats]) -> None:
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
        for idx, chapter in enumerate(chapters, start=1):
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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="wordcount",
        description=(
            "Count words, characters, chapters, and reading time for "
            "manuscripts and Markdown files. Local-only processing."
        ),
    )
    parser.add_argument("file", help="Path to the manuscript or Markdown file.")
    parser.add_argument(
        "--wpm",
        type=int,
        default=DEFAULT_WPM,
        help=f"Words per minute for reading-time estimate (default {DEFAULT_WPM}).",
    )
    parser.add_argument(
        "--csv",
        metavar="PATH",
        help="Export per-chapter breakdown to a CSV file.",
    )
    parser.add_argument(
        "--no-chapters",
        action="store_true",
        help="Skip printing the per-chapter breakdown.",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    file_path = Path(args.file)
    if not file_path.is_file():
        print(f"Error: file not found: {file_path}", file=sys.stderr)
        return 1

    result = count_file(file_path, wpm=args.wpm)

    _print_summary(result)

    if not args.no_chapters:
        _print_chapters(result)

    if args.csv:
        _write_csv(args.csv, result, result.chapters)
        print(f"\nCSV export written to: {args.csv}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
