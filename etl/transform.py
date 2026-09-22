import csv
import logging
import re

from logger import setup_logger


logger = logging.getLogger("threat_intelligence_pipeline")


DOMAIN_PATTERN = re.compile(
    r"^(?=.{1,253}$)"
    r"(?:[a-zA-Z0-9]"
    r"(?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+"
    r"[a-zA-Z]{2,63}$"
)


def extract_domain(url):
    """Extract the hostname/domain from a URL."""

    if not url:
        return None

    url = url.strip()

    url = re.sub(
        r"^https?://",
        "",
        url,
        flags=re.IGNORECASE
    )

    domain = re.split(r"[/:?#]", url)[0]

    return domain.lower()


def is_valid_domain(domain):
    """Return True when the domain has a valid format."""

    if not domain:
        return False

    if domain.lower() in {"localhost", "127.0.0.1"}:
        return False

    return bool(DOMAIN_PATTERN.match(domain))


def transform(input_file):
    """
    Clean URLHaus data and return unique valid domains.

    The transformation:
    - removes comment lines
    - extracts the URL column
    - extracts the domain/hostname
    - removes localhost values
    - validates domain format
    - removes duplicate domains
    """

    logger.info(
        "Transform stage started | input=%s",
        input_file
    )

    total_rows = 0
    valid_domains = 0
    domains = set()

    try:
        with open(
            input_file,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as file:

            header = None

            for line in file:
                line = line.strip()

                if not line:
                    continue

                # URLHaus stores the CSV header as a comment.
                if line.startswith("# id,"):
                    header = line[2:].split(",")
                    continue

                # Ignore all other comment lines.
                if line.startswith("#"):
                    continue

                # Do not process data until the header is found.
                if header is None:
                    continue

                try:
                    row = next(csv.reader([line]))
                except csv.Error:
                    logger.warning(
                        "Invalid CSV row skipped"
                    )
                    continue

                if len(row) != len(header):
                    logger.warning(
                        "CSV row does not match header length"
                    )
                    continue

                total_rows += 1

                record = dict(zip(header, row))

                url = record.get("url")

                domain = extract_domain(url)

                if is_valid_domain(domain):
                    valid_domains += 1
                    domains.add(domain)

        result = sorted(domains)

        logger.info(
            "Transform stage completed | "
            "rows=%d | valid=%d | unique=%d",
            total_rows,
            valid_domains,
            len(result)
        )

        return result

    except FileNotFoundError:
        logger.exception(
            "Transform failed | input file not found | file=%s",
            input_file
        )
        raise

    except Exception:
        logger.exception(
            "Transform stage failed"
        )
        raise


if __name__ == "__main__":
    setup_logger()

    input_file = "data/raw/urlhaus.csv"

    domains = transform(input_file)

    print(f"Total unique domains: {len(domains)}")
