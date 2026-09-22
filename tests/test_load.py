import sqlite3
from unittest.mock import patch

from etl.load import load


def test_load(tmp_path):
    """Test loading enriched data into SQLite."""

    database_path = tmp_path / "test.db"

    data = [
        {
            "domain": "example.com",
            "resolved_ip": "93.184.216.34",
        },
        {
            "domain": "example.org",
            "resolved_ip": "93.184.216.35",
        },
    ]

    with patch(
        "etl.load.DATABASE_PATH",
        database_path,
    ):
        load(data)

    connection = sqlite3.connect(database_path)

    rows = connection.execute(
        """
        SELECT domain, resolved_ip
        FROM domain_intelligence
        ORDER BY domain
        """
    ).fetchall()

    connection.close()

    assert rows == [
        ("example.com", "93.184.216.34"),
        ("example.org", "93.184.216.35"),
    ]


def test_load_upsert(tmp_path):
    """Test that loading the same domain updates the existing record."""

    database_path = tmp_path / "test.db"

    first_data = [
        {
            "domain": "example.com",
            "resolved_ip": "1.1.1.1",
        }
    ]

    second_data = [
        {
            "domain": "example.com",
            "resolved_ip": "2.2.2.2",
        }
    ]

    with patch(
        "etl.load.DATABASE_PATH",
        database_path,
    ):
        load(first_data)
        load(second_data)

    connection = sqlite3.connect(database_path)

    rows = connection.execute(
        """
        SELECT domain, resolved_ip
        FROM domain_intelligence
        """
    ).fetchall()

    connection.close()

    assert rows == [
        ("example.com", "2.2.2.2"),
    ]