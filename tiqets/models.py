from sqlalchemy import BigInteger, Column, ForeignKey, Integer, create_engine
from sqlalchemy.orm import declarative_base

from tiqets import config

Base = declarative_base()
engine = create_engine(
    f"mysql://root@{config.DB_HOST}:3306/{config.DB_NAME}",
    echo=config.ECHO_QUERIES,
    future=True,
)


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)

    def __repr__(self):
        return f"Customer({self.id=})"

    def __hash__(self):
        # NOTE good enough for the purpose of the task
        return self.id

    def __eq__(self, other):
        if not isinstance(other, Customer):
            return False
        return self.id == other.id


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)

    def __repr__(self):
        return f"Order({self.id=}, {self.customer_id=})"

    def __hash__(self):
        return self.id

    def __eq__(self, other):
        if not isinstance(other, Order):
            return False
        return self.id == other.id



class Barcode(Base):
    __tablename__ = "barcodes"

    value = Column(BigInteger, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True)

    def __repr__(self):
        return f"Barcode({self.value=}, {self.order_id=})"

    def __hash__(self):
        return self.value

    def __eq__(self, other):
        if not isinstance(other, Barcode):
            return False
        return self.value == other.value


# NOTE it's better to use tools like alembic here, but to not overcomplicate lets not to
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
