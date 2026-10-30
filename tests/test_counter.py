"""Tests for the counting logic."""

from wordcount.counter import count_text, count_file, DEFAULT_WPM
from pathlib import Path
import tempfile
import os


def test_empty_text():
    result = count_text("", path="empty.txt")
    assert result.words == 0
    assert result.characters == 0
    assert result.characters_no_whitespace == 0
    assert result.chapter_count == 0
    assert result.reading_time_minutes == 0.0


def test_basic_counting():
    text = "Hello world. This is a test."
    result = count_text(text, path="test.txt")
    assert result.words == 6
    assert result.characters == len(text)
    assert result.characters_no_whitespace == len(text.replace(" ", ""))


def test_reading_time():
    text = "word " * 250
    result = count_text(text, path="test.txt", wpm=250)
    assert result.reading_time_minutes == 1.0


def test_wpm_custom():
    text = "word " * 500
    result = count_text(text, path="test.txt", wpm=500)
    assert result.reading_time_minutes == 1.0


def test_paragraph_counting():
    text = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."
    result = count_text(text, path="test.txt")
    assert result.paragraphs == 2


def test_manuscript_chapter_detection():
    text = """Prologue text here.

Chapter 1
The adventure begins in a small village.

Chapter 2
The hero travels to the big city.
"""
    result = count_text(text, path="book.txt")
    assert result.chapter_count == 2
    assert result.chapters[0].title.startswith("Chapter 1:")
    assert result.chapters[1].title.startswith("Chapter 2:")
    assert result.chapters[0].words > 0
    assert result.chapters[1].words > 0


def test_manuscript_chapter_case_insensitive():
    text = "CHAPTER ONE\nSome words here.\nchapter two\nMore words."
    result = count_text(text, path="book.txt")
    assert result.chapter_count == 2


def test_markdown_chapter_detection():
    text = """# Introduction

Welcome to the book.

## Chapter One

The story starts here.

# Conclusion

The end.
"""
    result = count_text(text, path="book.md")
    assert result.chapter_count == 3
    assert result.is_markdown is True
    assert result.chapters[0].title == "Introduction"
    assert result.chapters[1].title == "Chapter One"
    assert result.chapters[2].title == "Conclusion"


def test_front_matter_not_in_chapter():
    text = """Some intro text before any chapter.

Chapter 1
Actual chapter content.
"""
    result = count_text(text, path="book.txt")
    # Front matter words counted in total but not assigned to a chapter.
    chapter_words = sum(c.words for c in result.chapters)
    assert chapter_words < result.words
    assert "Chapter 1" in result.chapters[0].title


def test_count_file(tmp_path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("Hello world\n\nChapter 1\nMore words here.", encoding="utf-8")
    result = count_file(file_path)
    assert result.path == str(file_path)
    # "Hello world Chapter 1 More words here." -> 7 tokens.
    assert result.words == 7
    assert result.chapter_count == 1


def test_default_wpm_constant():
    assert DEFAULT_WPM == 250
