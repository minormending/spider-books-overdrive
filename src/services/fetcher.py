import httpx
import time
from typing import Optional

class PageFetcher:
    def __init__(self, timeout: int = 10, retries: int = 3):
        self.timeout = timeout
        self.retries = retries

    def fetch_search_page(self, base_url: str, page: int, params: dict) -> Optional[str]:
        """Fetches the search results HTML page."""
        search_url = f"{base_url}/search/title"
        params["page"] = page

        for attempt in range(self.retries):
            try:
                response = httpx.get(search_url, params=params, timeout=self.timeout)
                response.raise_for_status()
                return response.text
            except httpx.RequestError as e:
                print(f"Attempt {attempt + 1}: Failed to fetch {search_url} — {e}")
                time.sleep(2 * (attempt + 1))
        
        return None
