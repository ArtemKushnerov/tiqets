import logging
import os

logging.basicConfig(level="INFO", format="%(asctime)s %(levelname)s %(message)s")


def to_bool(value):
    return value in ("True", "true", True)


DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "tiqets")
ECHO_QUERIES = False
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
OUTPUT_FILE_NAME = os.getenv("OUTPUT_FILE_NAME", "output.csv")
TOP_CUSTOMERS_TTL_SECONDS = 60
USE_CACHE = to_bool(os.getenv("USE_CACHE", False))
