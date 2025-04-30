import re
import json
from typing import List, Dict
from bs4 import BeautifulSoup


class BookParser:
    def parse_books(self, html: str) -> List[Dict]:
        """Extract full OverDrive mediaItems JSON blocks from the page."""
        books = []

        # Extract window.OverDrive.mediaItems JSON
        match = re.search(
            r"window\.OverDrive\.mediaItems\s*=\s*(\{.*?\});",
            html,
            re.DOTALL
        )
        if not match:
            return books

        try:
            media_items = json.loads(match.group(1))
        except json.JSONDecodeError:
            return books

        # Each value is a full book metadata object
        for _, book_data in media_items.items():
            books.append(book_data)

        return books

    def find_total_pages(self, html: str) -> int:
        """Finds the max page number from the pagination controls."""
        soup = BeautifulSoup(html, "html.parser")
        page_links = soup.select(".Pagination-item")

        max_page = 1
        for link in page_links:
            try:
                page_num = int(link.text.strip())
                if page_num > max_page:
                    max_page = page_num
            except ValueError:
                continue  # Skip if it's not a number (like Next/Prev)

        return max_page
