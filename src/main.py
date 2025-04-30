from config.libraries import LIBRARIES
from services.fetcher import PageFetcher
from services.parser import BookParser
from services.files import FileStorage, sanitize_filename
from services.index import IndexDatabase
from services.utils import extract_lexile
from utils.logger import setup_logger

def main():
    logger = setup_logger()
    fetcher = PageFetcher()
    parser = BookParser()

    storage = FileStorage("output")
    index = IndexDatabase("index.db")

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
                author = book.get("firstCreatorName")
                title = book.get("title")
                lexile = extract_lexile(book)

                if not (author and title and lexile):
                    logger.warning(f"Skipping book with missing author/title/lexile: {title} by {author}")
                    continue

                filename = sanitize_filename(author, title, lexile)
                storage.save_book_json(book, filename)
                index.insert_record(author, title, lexile, filename)

            logger.info(f"Processed page {page}/{total_pages} for {library_url}")

            if page >= total_pages:
                break
            page += 1

if __name__ == "__main__":
    main()