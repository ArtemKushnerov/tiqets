import factory
import pytest
from sqlalchemy import delete
from sqlalchemy.orm import Session

from tiqets.models import Barcode, Customer, Order, engine


@pytest.fixture(scope="session", autouse=True)
def session():
    with Session(engine) as session:
        yield session


@pytest.fixture(scope="function", autouse=True)
def cleanup(session):
    session.execute(delete(Barcode))
    session.execute(delete(Order))
    session.execute(delete(Customer))
    yield


@pytest.fixture
def CustomerFactory(session):
    class Customer_Factory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = Customer
            sqlalchemy_session = session
            sqlalchemy_session_persistence = "flush"

    return Customer_Factory


@pytest.fixture
def OrderFactory(session):
    class Order_Factory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = Order
            sqlalchemy_session = session
            sqlalchemy_session_persistence = "flush"

    return Order_Factory


@pytest.fixture
def BarcodeFactory(session):
    class Barcode_Factory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = Barcode
            sqlalchemy_session = session
            sqlalchemy_session_persistence = "flush"

    return Barcode_Factory
