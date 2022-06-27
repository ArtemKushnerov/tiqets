from tiqets import load
from tiqets.models import Barcode, Customer, Order


def test_loads_customers_orders(session):
    load.load_customers_orders("tests/data/test_orders.csv", session)
    assert session.query(Customer).count() == 10
    assert session.query(Order).count() == 10


def test_loads_customers_multiple_orders(session):
    load.load_customers_orders("tests/data/test_orders_multiple.csv", session)
    assert session.query(Customer).count() == 10
    assert session.query(Order).count() == 12


def test_loads_barcodes(session):
    load.load_customers_orders("tests/data/test_orders.csv", session)
    load.load_barcodes("tests/data/test_barcodes.csv", session)
    assert session.query(Barcode).count() == 10


def test_loads_duplicate_barcodes(session):
    load.load_customers_orders("tests/data/test_orders.csv", session)
    load.load_barcodes("tests/data/test_barcodes_duplicate.csv", session)
    assert session.query(Barcode).count() == 9


def test_doesnt_load_orders_without_barcodes(session, CustomerFactory, OrderFactory):
    customer = CustomerFactory()
    for i in range(1, 14):
        OrderFactory(customer_id=customer.id, id=i)

    load.load_barcodes("tests/data/test_no_barcodes_orders.csv", session)
    assert session.query(Barcode).count() == 10
    assert session.query(Order).count() == 10
