from config.libraries import LIBRARIES
from services.fetcher import PageFetcher
from services.parser import BookParser
from services.db import BookDatabase
from utils.logger import setup_logger

def main():
    logger = setup_logger()
    fetcher = PageFetcher()
    parser = BookParser()
    db = BookDatabase()

    query_params = {
        "lexileScoresMin": "200-400",
        "lexileScoresMax": "1800-",
        "sortBy": "newlyadded",
    }

    for library_url in LIBRARIES:
        logger.info(f"Scraping library: {library_url}")
        page = 1
        total_pages = None

        while True:
            html = fetcher.fetch_search_page(library_url, page, query_params)
            if not html:
                logger.error(f"Failed to fetch page {page} for {library_url}. Skipping...")
                break

            if total_pages is None:
                total_pages = parser.find_total_pages(html)
                logger.info(f"Found {total_pages} pages for {library_url}")

            books = parser.parse_books(html)
            if not books:
                logger.warning(f"No books found on {library_url} page {page}")
                break

            for book in books:
                db.insert_or_update_book(book, library_url, logger=logger)

            logger.info(f"Processed page {page}/{total_pages} for {library_url}")

            if page >= total_pages:
                break
            page += 1

if __name__ == "__main__":
    main()