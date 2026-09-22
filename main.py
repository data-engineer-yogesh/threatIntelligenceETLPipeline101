import argparse
import logging

from etl.extract import extract
from etl.transform import transform
from etl.enrich import enrich
from etl.load import load
from logger import setup_logger


logger = logging.getLogger("threat_intelligence_pipeline")

VERSION = "1.0.0"


def run_pipeline():
    """Run the complete threat intelligence ETL pipeline."""

    logger.info("ETL pipeline started")

    try:
        # Stage 1: Extract
        # Download the latest URLHaus CSV file.
        raw_file = extract()

        logger.info(
            "Extract stage completed | file=%s",
            raw_file
        )

        # Stage 2: Transform
        # Parse URLs, extract domains, validate domains,
        # remove noise, and remove duplicate domains.
        domains = transform(raw_file)

        logger.info(
            "Transform stage completed | domains=%d",
            len(domains)
        )

        # Stage 3: Enrich
        # Resolve valid domains to IPv4 addresses.
        # DNS failures are stored as None.
        enriched_data = enrich(domains)

        logger.info(
            "Enrich stage completed | records=%d",
            len(enriched_data)
        )

        # Stage 4: Load
        # Store the enriched domain information in SQLite.
        # Existing domains are updated using an idempotent UPSERT.
        load(enriched_data)

        logger.info("Load stage completed")
        logger.info("ETL pipeline completed successfully")

    except Exception:
        logger.exception("ETL pipeline failed")
        raise


def main():
    """Parse command-line arguments and start the ETL pipeline."""

    parser = argparse.ArgumentParser(
        description=(
            "Threat Intelligence ETL pipeline that downloads "
            "URLHaus data, transforms and validates domains, "
            "performs IPv4 DNS enrichment, and loads the "
            "results into SQLite."
        )
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"Threat Intelligence ETL Pipeline {VERSION}"
    )

    parser.parse_args()

    setup_logger()

    run_pipeline()


if __name__ == "__main__":
    main()
