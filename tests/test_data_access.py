from tiqets import data_access


def test_get_output_dataset(session, CustomerFactory, OrderFactory, BarcodeFactory):
    customers = CustomerFactory.create_batch(2)
    orders12 = OrderFactory.create_batch(2, customer_id=customers[0].id)
    BarcodeFactory.create_batch(2, order_id=orders12[0].id)
    BarcodeFactory.create_batch(3, order_id=orders12[1].id)
    order3 = OrderFactory(customer_id=customers[1].id)
    BarcodeFactory.create_batch(2, order_id=order3.id)

    dataset = data_access.get_output_dataset(session)
    assert dataset == [(1, 1, "2,1"), (1, 2, "5,4,3"), (2, 3, "7,6")]


def test_get_top_customers(session, CustomerFactory, OrderFactory, BarcodeFactory):
    customers = CustomerFactory.create_batch(10)

    # highest rated customer orders
    orders012 = OrderFactory.create_batch(3, customer_id=customers[4].id)
    BarcodeFactory.create_batch(2, order_id=orders012[0].id)
    BarcodeFactory.create_batch(3, order_id=orders012[1].id)
    BarcodeFactory.create_batch(2, order_id=orders012[2].id)

    # second customer orders and so on
    orders34 = OrderFactory.create_batch(2, customer_id=customers[1].id)
    BarcodeFactory.create_batch(2, order_id=orders34[0].id)
    BarcodeFactory.create_batch(2, order_id=orders34[1].id)

    orders78 = OrderFactory.create_batch(2, customer_id=customers[2].id)
    BarcodeFactory.create_batch(1, order_id=orders78[0].id)
    BarcodeFactory.create_batch(1, order_id=orders78[1].id)

    orders89 = OrderFactory.create_batch(2, customer_id=customers[3].id)
    BarcodeFactory.create_batch(1, order_id=orders89[0].id)
    BarcodeFactory.create_batch(1, order_id=orders89[1].id)

    orders1011 = OrderFactory.create_batch(2, customer_id=customers[0].id)
    BarcodeFactory.create_batch(1, order_id=orders1011[0].id)
    BarcodeFactory.create_batch(1, order_id=orders1011[1].id)

    # should be ignored
    orders1213 = OrderFactory.create_batch(2, customer_id=customers[5].id)
    BarcodeFactory.create_batch(1, order_id=orders1213[0].id)
    BarcodeFactory.create_batch(1, order_id=orders1213[1].id)

    dataset = data_access.get_top_customers(session)
    assert dataset == [
        (customers[4].id, 7),
        (customers[1].id, 4),
        (customers[0].id, 2),
        (customers[2].id, 2),
        (customers[3].id, 2),
    ]


def test_get_amount_unused_barcodes(
    session, CustomerFactory, OrderFactory, BarcodeFactory
):
    customer = CustomerFactory()
    order = OrderFactory(customer_id=customer.id)
    BarcodeFactory.create_batch(10, order_id=None)
    BarcodeFactory.create_batch(20, order_id=order.id)
    assert data_access.get_amount_of_unused_barcodes(session) == 10
