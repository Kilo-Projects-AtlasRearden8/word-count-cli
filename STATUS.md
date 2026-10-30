# STATUS — wordcount CLI

## What was built

A local-only Python CLI (`wordcount`) that counts words, characters,
characters-without-whitespace, paragraphs, chapters, and reading time for
manuscripts and Markdown files. It prints a summary, an optional per-chapter
breakdown, and can export the breakdown to CSV.

Package: `wordcount` (console script: `wordcount`)
Version: 1.0.0
License: MIT — Copyright (c) 2026 Asdale Dynamics, LLC

Files:
- `pyproject.toml` — packaging + pytest config + `wordcount` entry point
- `wordcount/__init__.py` — public API
- `wordcount/counter.py` — counting logic (words, chars, chapters, reading time)
- `wordcount/cli.py` — argparse CLI (`--wpm`, `--csv`, `--no-chapters`)
- `wordcount/csv_export.py` — per-chapter CSV export with totals row
- `tests/test_counter.py` — 11 tests for counting logic
- `README.md` — usage, options, example, credits Asdale Dynamics, LLC
- `LICENSE` — MIT, exact copyright line: `Copyright (c) 2026 Asdale Dynamics, LLC`
- `.gitignore` — Python/build/test/IDE ignores
- `STATUS.md` — this file

## How to run

```bash
cd word-count-cli
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

wordcount my-book.md
wordcount manuscript.txt --wpm 200
wordcount my-book.md --csv breakdown.csv --no-chapters
```

Run tests:

```bash
source .venv/bin/activate
pip install pytest
pytest
```

Build a wheel:

```bash
source .venv/bin/activate
pip install build setuptools wheel
python -m build --wheel --no-isolation
```

## Verification results

- `pytest`: 11 passed (all counting-logic tests)
- Wheel build: `wordcount-1.0.0-py3-none-any.whl` builds successfully
- CLI smoke test: ran against a sample Markdown file; printed summary, chapter
  breakdown, and wrote a CSV file with per-chapter rows + TOTAL row

Chapter detection:
- Markdown: treats `#` / `##` / … heading lines as chapters (uses heading text
  as the title).
- Manuscript/plain text: treats lines matching `Chapter N` / `CHAPTER N` / `ch
  N` as chapters (case-insensitive), numbered sequentially.

Reading time: words / wpm (default 250 wpm), configurable with `--wpm`.

## Known gaps

- Chapter detection for plain-text manuscripts relies on the `Chapter N`
  pattern; books that use unnumbered or stylized chapter titles won't be split
  automatically.
- Reading-time estimate uses a single fixed wpm; it does not adjust for content
  density or reading level.
- Only a single input file per invocation (no batch directory mode yet).
- No JSON output mode (CSV only).
- No handling of non-UTF-8 encoded input files.

## Credits

Built and maintained by Asdale Dynamics, LLC — beginner-friendly AI education,
books and guides, and practical tools for authors and small businesses.
dylanasdale.github.io
