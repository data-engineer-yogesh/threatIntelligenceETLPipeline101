import logging
import sqlite3

from config import DATABASE_PATH
from logger import setup_logger


logger = logging.getLogger("threat_intelligence_pipeline")


CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS domain_intelligence (
    domain TEXT PRIMARY KEY,
    resolved_ip TEXT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""


UPSERT_SQL = """
INSERT INTO domain_intelligence (
    domain,
    resolved_ip,
    last_updated
)
VALUES (?, ?, CURRENT_TIMESTAMP)
ON CONFLICT(domain)
DO UPDATE SET
    resolved_ip = excluded.resolved_ip,
    last_updated = CURRENT_TIMESTAMP
"""


def create_database_directory():
    """Create the database directory if it does not exist."""

    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )


def create_table(connection):
    """Create the domain intelligence table if required."""

    connection.execute(CREATE_TABLE_SQL)
    connection.commit()


def load(enriched_data):
    """
    Load enriched domain data into SQLite.

    Existing domains are updated using an UPSERT,
    making the load operation idempotent.
    """

    logger.info(
        "Load stage started | records=%d | database=%s",
        len(enriched_data),
        DATABASE_PATH
    )

    if not enriched_data:
        logger.warning(
            "Load stage skipped | no enriched records available"
        )
        return

    connection = None

    try:
        create_database_directory()

        connection = sqlite3.connect(DATABASE_PATH)

        create_table(connection)

        records = [
            (
                record["domain"],
                record["resolved_ip"]
            )
            for record in enriched_data
        ]

        connection.executemany(
            UPSERT_SQL,
            records
        )

        connection.commit()

        logger.info(
            "Load stage completed | records=%d",
            len(records)
        )

    except sqlite3.Error:
        if connection:
            connection.rollback()

        logger.exception(
            "Load stage failed | database=%s",
            DATABASE_PATH
        )

        raise

    except Exception:
        if connection:
            connection.rollback()

        logger.exception(
            "Unexpected error during load stage"
        )

        raise

    finally:
        if connection:
            connection.close()

            logger.debug(
                "Database connection closed"
            )


if __name__ == "__main__":
    setup_logger()

    test_data = [
        {
            "domain": "example.com",
            "resolved_ip": "93.184.216.34"
        },
        {
            "domain": "google.com",
            "resolved_ip": "142.250.72.14"
        }
    ]

    load(test_data)