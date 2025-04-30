# Overdrive Book Scraper

Scrape book metadata from OverDrive-powered library websites, store structured data as individual JSON files, and index key attributes (author, title, lexile) in a fast SQLite database.

---

## Features

- Scrapes OverDrive search pages using a shared `window.OverDrive.mediaItems` JSON object
- Saves each book's full metadata as a standalone `.json` file in an output directory
- Creates a SQLite index mapping `author`, `title`, and `lexile` score to each saved file
- Automatically sanitizes filenames for filesystem compatibility
- Skips and logs entries that are missing key metadata (author, title, or lexile score)
- Prevents duplicate entries using a normalized `author+title` combination
- Provides a search script to retrieve full metadata by `author` and `title`
- Provides a reusable module to look up lexile scores by `author` and `title` for use in other projects

---

## Installation

**Requirements:**
- Python 3.10+
- [Poetry](https://python-poetry.org/) for dependency management

**Install dependencies:**
```bash
poetry install
```

---

## Usage

Run the scraper:

```bash
poetry run python src/main.py
```

This will:
- Loop through the library URLs in `src/config/libraries.py`
- Fetch all paginated book data
- Extract metadata using embedded JSON
- Save each book to `output/author-title-lexile.json`
- Add the book’s author, title, lexile, and filename to `index.db`

---

## Project Structure

```
overdrive_scraper/
├── output/                    # Full book metadata files (JSON)
├── index.db                  # SQLite DB with indexed attributes
├── scripts/
│   └── search_book.py        # CLI to fetch book metadata by author + title
├── src/
│   ├── config/
│   │   └── libraries.py      # List of library base URLs
│   ├── services/
│   │   ├── fetcher.py        # Fetches HTML pages
│   │   ├── parser.py         # Parses book metadata from script tag
│   │   ├── files.py          # Handles saving JSON files and filenames
│   │   ├── index.py          # Manages SQLite index
│   │   ├── utils.py          # Lexile extraction helper
│   │   └── lexile_lookup.py  # Reusable module to look up lexile by author/title
│   └── main.py               # Orchestrates the scraping process
├── README.md
├── pyproject.toml
```

---

## Example Output

Sample JSON filename:
```
output/gregory-maguire_wicked_890.json
```

Example SQLite row:
```
author: "gregory maguire"
title: "wicked"
lexile: 890
filename: "gregory-maguire_wicked_890.json"
```

---

## Metadata Access

To fetch metadata for a given book:
```bash
python scripts/search_book.py --author "Gregory Maguire" --title "Wicked"
```

---

## Lexile Score Lookup

Use the `lexile_lookup.py` module in other projects:

```python
from services.lexile_lookup import get_lexile

score = get_lexile("Gregory Maguire", "Wicked")
print(score)  # e.g. 890
```

---

## TODO

- [ ] Batch search or CSV import for lexile lookups
- [ ] CLI to export metadata or index as CSV
- [ ] Fuzzy/partial title and author search
- [ ] Subject and level index enhancements
- [ ] Remote sync or deduplication logic

---

## License

MIT License