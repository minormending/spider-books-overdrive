import re
import json
from pathlib import Path

def sanitize_filename(author: str, title: str, lexile: int) -> str:
    base = f"{author}_{title}_{lexile}"
    base = re.sub(r"[^\w\s-]", "", base.lower())
    base = re.sub(r"[\s]+", "-", base)
    return base + ".json"

class FileStorage:
    def __init__(self, output_dir: str = "output"):
        self.output_path = Path(output_dir)
        self.output_path.mkdir(parents=True, exist_ok=True)

    def save_book_json(self, data: dict, filename: str):
        file_path = self.output_path / filename
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
