from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"

LOG_DIR = BASE_DIR / "logs"

RAW_FILE = RAW_DATA_DIR / "urlhaus.csv"

DATABASE_PATH = DATA_DIR / "threat_intelligence.db"

URLHAUS_URL = "https://urlhaus.abuse.ch/downloads/csv_recent/"

DNS_MAX_WORKERS = 50