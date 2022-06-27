import logging
import os

logging.basicConfig(level="INFO")

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_NAME = os.getenv("DB_NAME", "tiqets")
ECHO_QUERIES = False
OUTPUT_FILE_NAME = os.getenv("OUTPUT_FILE_NAME", "output.csv")
