from tinydb import TinyDB, Query
from datetime import datetime
from typing import Optional
import logging
import re


def normalize_string(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)  # Remove punctuation
    s = re.sub(r"[\s]+", "-", s)    # Replace whitespace with hyphens
    return s


def build_id(title: str, author: str) -> str:
    return f"{normalize_string(author)}_{normalize_string(title)}"

class BookDatabase:
    def __init__(self, db_path: str = "books.json"):
        self.db = TinyDB(db_path)
        self.book_table = self.db.table("books")

    def insert_or_update_book(self, book_json: dict, library_url: str, logger: Optional[logging.Logger] = None):
        title = book_json.get("title")
        author = book_json.get("firstCreatorName")

        if not title or not author:
            if logger:
                logger.warning(
                    f"Skipped book missing title or author (OverDrive ID: {book_json.get('id')}) from {library_url}"
                )
            return

        book_id = build_id(title, author)

        Book = Query()
        existing = self.book_table.get(Book.id == book_id)

        if existing:
            libraries = existing.get("libraries", [])
            if library_url not in libraries:
                libraries.append(library_url)
                self.book_table.update({"libraries": libraries}, Book.id == book_id)
        else:
            book_json["libraries"] = [library_url]
            book_json["scraped_at"] = datetime.utcnow().isoformat()
            book_json["id"] = book_id
            self.book_table.insert(book_json)
    
    def book_exists(self, library_url: str, title: str) -> bool:
        """Optional: Check if a book already exists (prevent duplicates)."""
        pass
