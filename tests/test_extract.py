from unittest.mock import patch

from etl.extract import extract


@patch("etl.extract.urllib.request.urlretrieve")
def test_extract(mock_urlretrieve, tmp_path):
    """Test that URLHaus data is downloaded successfully."""

    output_file = tmp_path / "urlhaus.csv"

    with patch("etl.extract.RAW_FILE", output_file):
        with patch("etl.extract.RAW_DATA_DIR", tmp_path):
            result = extract()

    mock_urlretrieve.assert_called_once()

    assert result == output_file