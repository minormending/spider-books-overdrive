import sqlite3

class IndexDatabase:
    def __init__(self, db_path: str = "index.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            author TEXT NOT NULL,
            title TEXT NOT NULL,
            lexile INTEGER,
            filename TEXT NOT NULL UNIQUE
        )
        """)
        self.conn.commit()

    def insert_record(self, author: str, title: str, lexile: int, filename: str):
        self.conn.execute("""
        INSERT OR IGNORE INTO books (author, title, lexile, filename)
        VALUES (?, ?, ?, ?)
        """, (author, title, lexile, filename))
        self.conn.commit()
