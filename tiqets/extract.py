import csv
import logging

from tiqets import config

logger = logging.getLogger(__name__)


def extract_output_dataset(dataset, output_file=config.OUTPUT_FILE_NAME):
    with open(output_file, "w", newline="") as csvfile:
        fieldnames = ["customer_id", "order_id", "barcodes"]
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)
        writer.writerows(dataset)
    logger.info(f"Output is successfully saved to {config.OUTPUT_FILE_NAME}")
