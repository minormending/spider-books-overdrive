import sqlite3
import re
from typing import Optional

DB_PATH = "index.db"


def normalize_string(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s]+", " ", s)
    return s


def get_lexile(author: str, title: str, db_path: str = DB_PATH) -> Optional[int]:
    author_norm = normalize_string(author)
    title_norm = normalize_string(title)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT lexile FROM books
        WHERE lower(author) = ? AND lower(title) = ?
    """, (author_norm, title_norm))

    row = cursor.fetchone()
    conn.close()

    if row and row[0] is not None:
        return int(row[0])
    return None
