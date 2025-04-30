from typing import Optional

def extract_lexile(book: dict) -> Optional[int]:
    for level in book.get("levels", []):
        if level.get("id") == "lexile":
            try:
                return int(level.get("value"))
            except (TypeError, ValueError):
                return None
    return None
