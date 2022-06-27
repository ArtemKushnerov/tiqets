import csv
import logging
from collections import defaultdict

from tiqets import data_access
from tiqets.models import Barcode, Customer, Order

logger = logging.getLogger(__name__)


def load_customers_orders(csv_path, session):
    with open(csv_path, newline="") as csvfile:
        csv_reader = csv.DictReader(csvfile)
        customers = set()
        orders = set()
        for row in csv_reader:
            customer_id = int(row["customer_id"])
            order_id = int(row["order_id"])
            customers.add(Customer(id=customer_id))
            orders.add(Order(id=order_id, customer_id=customer_id))
    session.add_all(customers)
    session.add_all(orders)
    session.commit()


def load_barcodes(csv_path, session):
    with open(csv_path, newline="") as csvfile:
        csv_reader = csv.DictReader(csvfile)
        barcodes = {}
        duplicates_barcodes = defaultdict(list)
        for row in csv_reader:
            order_id = None if row["order_id"] == "" else int(row["order_id"])
            barcode_value = None if row["barcode"] == "" else int(row["barcode"])
            if not barcode_value:
                logger.warning(f"Empty barcode value, order_id={order_id}")
                continue

            barcode = Barcode(value=barcode_value, order_id=order_id)
            if first_duplicate := barcodes.pop(barcode_value, None):
                duplicates_barcodes[barcode_value].extend([barcode, first_duplicate])
            elif barcode_value in duplicates_barcodes:
                duplicates_barcodes[barcode_value].append(barcode)
            else:
                barcodes[barcode_value] = barcode

        if duplicates_barcodes:
            logger.warning("Duplicate barcodes found:")
            for value, duplicates in duplicates_barcodes.items():
                logger.warning(f"{value=}: {duplicates=}")

    session.add_all(barcodes.values())
    session.commit()
    data_access.remove_empty_orders(session)
