import logging

from sqlalchemy import func

from tiqets.decorators import cache
from tiqets.models import Barcode, Customer, Order

logger = logging.getLogger(__name__)


CUSTOMERS_IN_THE_TOP = 5


def get_output_dataset(session):
    """
    Generates the following SQL:

    select c.id customer_id, o.id order_id, group_concat(b.value order by b.value desc) barcodes
    from customers c
    inner join orders o on c.id=o.customer_id
    inner join barcodes b on o.id=b.order_id
    group by c.id, o.id
    order by c.id asc , o.id asc

    Inner joins additionally ensure that we ignore orders without barcodes.
    """
    query = (
        session.query(
            Customer.id.label("customer_id"),
            Order.id.label("order_id"),
            func.group_concat(Barcode.value.op("order by")(Barcode.value.desc())).label(
                "barcodes"
            ),
        )
        .select_from(Customer)
        .join(Order)
        .join(Barcode)
        .group_by(Customer.id, Order.id)
        .order_by(Customer.id.asc(), Order.id.asc())
    )
    return query.all()


def get_top_customers(session):
    rows = _get_top_customers(session)
    logger.info(f"Top {CUSTOMERS_IN_THE_TOP} customers:")
    for row in rows:
        logger.info(row)
    return rows


# NOTE the query seem like a good fit for simple caching with TTL, since there's likely no need to refresh in real time
@cache(key="top_customers", ttl=60)
def _get_top_customers(session):
    """
    Generates the following SQL:

    select c.id customer_id, count(b.value) amount_of_barcodes
    from customers c
    join orders o on c.id=o.customer_id
    join barcodes b on o.id=b.order_id
    group by c.id
    order by amount_of_barcodes desc, c.id asc
    limit 5
    """
    amount_of_barcodes = func.count(Barcode.value).label("amount_of_barcodes")
    query = (
        session.query(Customer.id.label("customer_id"), amount_of_barcodes)
        .select_from(Customer)
        .join(Order)
        .join(Barcode)
        .group_by(Customer.id)
        .order_by(amount_of_barcodes.desc(), Customer.id.asc())
        .limit(CUSTOMERS_IN_THE_TOP)
    )
    rows = query.all()
    return rows


def get_amount_of_unused_barcodes(session):
    amount = session.query(Barcode).filter(Barcode.order_id.is_(None)).count()
    logger.info(f"Amount of unused barcodes: {amount}")
    return amount


def remove_empty_orders(session):
    query = (
        session.query(Order.id)
        .select_from(Order)
        .outerjoin(Barcode)
        .filter(Barcode.value.is_(None))
    )
    ids = [r.id for r in query]
    logger.warning(f"Empty orders detected: {ids}")
    session.query(Order).filter(Order.id.in_(ids)).delete()
    session.commit()
    logger.info("Successfully deleted empty orders")
