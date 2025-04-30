import logging

def setup_logger():
    """Sets up and returns a configured logger."""
    logger = logging.getLogger("overdrive_scraper")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger