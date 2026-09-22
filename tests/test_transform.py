from etl.transform import (
    extract_domain,
    is_valid_domain,
    transform,
)


def test_extract_domain():
    """Test extraction of a domain from a URL."""

    assert extract_domain(
        "https://example.com/test"
    ) == "example.com"

    assert extract_domain(
        "http://example.com/path"
    ) == "example.com"


def test_extract_domain_without_protocol():
    """Test domain extraction without HTTP or HTTPS."""

    assert extract_domain(
        "example.com/path"
    ) == "example.com"


def test_extract_domain_empty_value():
    """Test empty URL handling."""

    assert extract_domain("") is None
    assert extract_domain(None) is None


def test_valid_domain():
    """Test valid domain validation."""

    assert is_valid_domain("example.com") is True
    assert is_valid_domain("sub.example.com") is True


def test_invalid_domain():
    """Test invalid domain validation."""

    assert is_valid_domain("localhost") is False
    assert is_valid_domain("127.0.0.1") is False
    assert is_valid_domain("") is False


def test_transform(tmp_path):
    """Test URLHaus transformation and deduplication."""

    input_file = tmp_path / "urlhaus.csv"

    input_file.write_text(
        "# comment\n"
        "# id,dateadded,url,url_status\n"
        "1,2026-01-01,https://example.com/test,online\n"
        "2,2026-01-01,http://example.com/path,online\n"
        "3,2026-01-01,https://localhost/test,online\n"
        "4,2026-01-01,https://127.0.0.1/test,online\n"
        "5,2026-01-01,https://example.org/test,online\n",
        encoding="utf-8",
    )

    result = transform(input_file)

    assert result == [
        "example.com",
        "example.org",
    ]