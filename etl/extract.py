import logging
import urllib.request

from config import RAW_DATA_DIR, RAW_FILE, URLHAUS_URL
from logger import setup_logger


logger = logging.getLogger("threat_intelligence_pipeline")


def extract():
    """Download the latest URLHaus CSV into the raw data directory."""

    logger.info(
        "Extraction started | source=%s",
        URLHAUS_URL
    )

    try:
        RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

        logger.info(
            "Raw data directory verified | path=%s",
            RAW_DATA_DIR
        )

        urllib.request.urlretrieve(
            URLHAUS_URL,
            RAW_FILE
        )

        logger.info(
            "URLHaus data downloaded successfully | file=%s",
            RAW_FILE
        )

        return RAW_FILE

    except Exception:
        logger.exception("Extraction failed")
        raise


if __name__ == "__main__":
    setup_logger()
    extract()