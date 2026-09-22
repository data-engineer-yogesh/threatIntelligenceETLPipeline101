import logging
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

from config import DNS_MAX_WORKERS
from logger import setup_logger


logger = logging.getLogger("threat_intelligence_pipeline")


def resolve_ipv4(domain):
    """Resolve a domain to an IPv4 address."""

    try:
        results = socket.getaddrinfo(
            domain,
            None,
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        if results:
            return results[0][4][0]

    except (socket.gaierror, socket.timeout, OSError) as error:
        logger.debug(
            "DNS resolution failed | domain=%s | error=%s",
            domain,
            error
        )

    return None


def enrich(domains):
    """
    Resolve IPv4 addresses concurrently for all domains.

    DNS failures return None and do not stop the pipeline.
    """

    logger.info(
        "Enrich stage started | domains=%d | workers=%d",
        len(domains),
        DNS_MAX_WORKERS
    )

    enriched_data = []
    successful = 0
    failed = 0

    try:
        with ThreadPoolExecutor(
            max_workers=DNS_MAX_WORKERS
        ) as executor:

            future_to_domain = {
                executor.submit(resolve_ipv4, domain): domain
                for domain in domains
            }

            for future in as_completed(future_to_domain):
                domain = future_to_domain[future]

                try:
                    ipv4 = future.result()

                except Exception as error:
                    logger.warning(
                        "DNS lookup failed | domain=%s | error=%s",
                        domain,
                        error
                    )
                    ipv4 = None

                if ipv4:
                    successful += 1
                else:
                    failed += 1

                enriched_data.append(
                    {
                        "domain": domain,
                        "resolved_ip": ipv4
                    }
                )

        logger.info(
            "Enrich stage completed | total=%d | successful=%d | failed=%d",
            len(enriched_data),
            successful,
            failed
        )

        return enriched_data

    except Exception:
        logger.exception(
            "Enrich stage failed"
        )
        raise


if __name__ == "__main__":
    setup_logger()

    test_domains = [
        "google.com",
        "example.com",
        "this-domain-does-not-exist-12345.com"
    ]

    results = enrich(test_domains)

    for result in results:
        print(result)