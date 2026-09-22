from unittest.mock import patch

from etl.enrich import enrich, resolve_ipv4


def test_resolve_ipv4():
    """Test successful IPv4 DNS resolution."""

    fake_result = [
        (
            None,
            None,
            None,
            None,
            ("93.184.216.34", 0),
        )
    ]

    with patch(
        "etl.enrich.socket.getaddrinfo",
        return_value=fake_result,
    ):
        result = resolve_ipv4("example.com")

    assert result == "93.184.216.34"


def test_resolve_ipv4_failure():
    """Test DNS failure returns None."""

    with patch(
        "etl.enrich.socket.getaddrinfo",
        side_effect=OSError("DNS failure"),
    ):
        result = resolve_ipv4("invalid.example")

    assert result is None


def test_enrich():
    """Test concurrent DNS enrichment."""

    fake_result = [
        (
            None,
            None,
            None,
            None,
            ("93.184.216.34", 0),
        )
    ]

    with patch(
        "etl.enrich.socket.getaddrinfo",
        return_value=fake_result,
    ):
        result = enrich(
            [
                "example.com",
                "example.org",
            ]
        )

    assert len(result) == 2

    domains = {
        record["domain"]
        for record in result
    }

    assert domains == {
        "example.com",
        "example.org",
    }

    assert all(
        record["resolved_ip"] == "93.184.216.34"
        for record in result
    )