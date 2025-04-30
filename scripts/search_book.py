import argparse
import sqlite3
import json
import re
from pathlib import Path

DB_PATH = "index.db"
OUTPUT_DIR = Path("output")


def normalize_string(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s]+", " ", s)
    return s


def find_book(author: str, title: str):
    author_norm = normalize_string(author)
    title_norm = normalize_string(title)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT filename FROM books
        WHERE lower(author) = ? AND lower(title) = ?
    """, (author_norm, title_norm))

    row = cursor.fetchone()
    if not row:
        print("No book found with that author and title.")
        return

    filename = row[0]
    book_path = OUTPUT_DIR / filename

    if not book_path.exists():
        print(f"Metadata file not found: {book_path}")
        return

    with open(book_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    print(json.dumps(metadata, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search for a book by author and title")
    parser.add_argument("--author", required=True, help="Book author")
    parser.add_argument("--title", required=True, help="Book title")
    args = parser.parse_args()

    find_book(args.author, args.title)
