# Overdrive Spider

Scrape book metadata from multiple OverDrive library websites and store it in a local TinyDB database.

---

## Features

- Scrape any number of OverDrive library websites with consistent backend
- Extract book metadata (title, author, ISBN, etc.)
- Automatically prevent duplicate entries by ISBN
- Track which libraries each book was found in
- Flexible and lightweight project structure
- Easy to extend and maintain

---

## Installation

**Requirements:**
- Python 3.10+
- [Poetry](https://python-poetry.org/) for dependency management

**Steps:**

1. Clone the repository:
    ```bash
    git clone https://your-repo-url.git
    cd overdrive-scraper
    ```

2. Install dependencies:
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

- Loop through all library URLs defined in `src/config/libraries.py`
- Fetch and parse book listings
- Save results into `books.json` using TinyDB
- Deduplicate books based on ISBN
- Track all libraries where each book appears

---

## Project Structure

```
overdrive_scraper/
├── src/
│   ├── config/
│   │   └── libraries.py    # List of library base URLs
│   ├── services/
│   │   ├── fetcher.py      # Fetches HTML pages
│   │   ├── parser.py       # Parses book metadata
│   │   ├── db.py           # TinyDB database manager
│   ├── utils/
│   │   └── logger.py       # Logging setup
│   └── main.py             # Scraper orchestration
├── books.json              # Output TinyDB file (created after first run)
├── pyproject.toml          # Poetry configuration
└── README.md
```

---

## Configuration

- Add or update library URLs in `src/config/libraries.py`
- Adjust query parameters if needed in `src/main.py`

Example of query parameters:
```python
query_params = {
    "lexileScoresMin": "200-400",
    "lexileScoresMax": "1800-",
    "sortBy": "newlyadded",
}
```

---

## Database

Books are stored in a TinyDB database (`books.json`), each entry like:

```json
{
  "isbn": "9780261103344",
  "title": "The Hobbit",
  "author": "J.R.R. Tolkien",
  "libraries": ["https://nmmi.overdrive.com", "https://anotherlibrary.overdrive.com"],
  "scraped_at": "2025-04-27T12:00:00Z"
}
```

---

## TODO

- [ ] Improve error recovery for bad pages
- [ ] Handle books with missing ISBNs more gracefully
- [ ] Export results to `.jsonl` or CSV
- [ ] Add CLI options to scrape single libraries
- [ ] Add resume capability if scraping interrupted

---

## License

This project is licensed under the MIT License.
