from sqlalchemy.orm import Session

from tiqets.data_access import (
    get_amount_of_unused_barcodes,
    get_output_dataset,
    get_top_customers,
)
from tiqets.extract import extract_output_dataset
from tiqets.load import load_barcodes, load_customers_orders
from tiqets.models import engine

with Session(engine) as session:
    load_customers_orders("data/orders.csv", session)
    load_barcodes("data/barcodes.csv", session)
    output_dataset = get_output_dataset(session)
    get_top_customers(session)
    get_amount_of_unused_barcodes(session)
    extract_output_dataset(output_dataset)
