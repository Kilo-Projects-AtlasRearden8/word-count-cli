# wordcount

A local-only Python CLI that counts words, characters, chapters, and reading
time for manuscripts and Markdown files. Built by **Asdale Dynamics, LLC**.

Plain English, step by step, never condescending — built for beginner authors,
self-publishers, and anyone who wants to know how long their writing will take
to read. No network calls, no secrets, no personal data. Everything happens on
your machine.

## Who this is for

Dylan Asdale is a registered nurse turned AI author and founder of
**Asdale Dynamics, LLC** (Indiana, formed October 2026). His book *The Massive
AI Manual* and hub site dylanasdale.github.io explain AI "like a friend would":
plain English, step by step, never condescending.

This tool is part of the LLC's small-business and author-tools line: practical,
beginner-friendly software for KDP/book publishing, writing, and editing.

## Features

* Counts **words**, **characters** (with and without whitespace), and
  **paragraphs**
* Detects **chapters** — Markdown headings (`#`, `##`, …) or manuscript
  chapter lines (`Chapter 1`, `CHAPTER TWO`, etc.)
* Estimates **reading time** at a configurable words-per-minute rate
* Prints a per-**chapter breakdown**
* Exports the breakdown to **CSV** (per chapter + totals)
* Runs entirely **locally** — nothing leaves your computer

## Install

```bash
git clone <this-repo>
cd word-count-cli
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Or install with `pip install -e .` from the repo root.

## Usage

```bash
wordcount my-book.md
wordcount manuscript.txt --wpm 200
wordcount my-book.md --csv breakdown.csv --no-chapters
```

### Example

```bash
$ wordcount sample.md
File: sample.md
Words: 1,234
Characters: 6,789
Characters (no whitespace): 5,432
Paragraphs: 42
Chapters: 5
Reading time (@250 wpm): 4m 56s

Chapter breakdown:
#    Title                                      Words    Chars     Read
------------------------------------------------------------------------
1    Chapter 1: The Beginning                    300    1,600     1m 12s
...
```

```bash
$ wordcount sample.md --csv report.csv
File: sample.md
...
CSV export written to: report.csv
```

The CSV has one row per chapter plus a `TOTAL` row:

```
chapter,title,words,characters,characters_no_whitespace,reading_time_seconds,reading_time_minutes
1,Chapter 1: The Beginning,300,1600,1280,72.0,1.2
...
TOTAL,,1234,6789,5432,296.2,4.94
```

## Options

| Option | Meaning |
|--------|---------|
| `file` | Path to the manuscript or Markdown file (required) |
| `--wpm N` | Words per minute for reading time (default 250) |
| `--csv PATH` | Write per-chapter breakdown to this CSV file |
| `--no-chapters` | Skip printing the chapter breakdown |

## Testing

```bash
source .venv/bin/activate
pip install pytest
pytest
```

## License

MIT License

Copyright (c) 2026 Asdale Dynamics, LLC

See [LICENSE](LICENSE) for the full text.

## Credit

Built and maintained by **Asdale Dynamics, LLC** — beginner-friendly AI
education, books and guides, and practical tools for authors and small
businesses. Learn more at dylanasdale.github.io.
