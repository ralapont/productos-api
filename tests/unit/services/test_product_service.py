from unittest.mock import Mock

from productos_api.models.product import Product
from productos_api.services.product_service import ProductService


def test_get_by_id_returns_product():

    expected_product = Product(
        id=1,
        name="Portátil",
        price=1000
    )

    session = Mock()
    session.get.return_value = expected_product

    result = ProductService.get_by_id(
        session=session,
        product_id=1
    )

    session.get.assert_called_once_with(
        Product,
        1
    )

    assert result == expected_product

def test_get_by_id_returns_none_when_product_not_exists():

    session = Mock()
    session.get.return_value = None

    result = ProductService.get_by_id(
        session=session,
        product_id=999
    )

    session.get.assert_called_once_with(
        Product,
        999
    )

    assert result is None

def test_create_product():

    product_create = Product(
        name="Portátil",
        description="Portátil de alta gama",
        price=1000,
        stock=10
    )

    product_expected = Product(
        name="Portátil",
        description="Portátil de alta gama",
        price=1000,
        stock=10
    )

    session = Mock()
    session.add.return_value = None
    session.commit.return_value = None
    session.refresh.return_value = None

    result = ProductService.create(
        session=session,
        product_create=product_create
    )

    session.add.assert_called_once_with(product_create)
    session.commit.assert_called_once()
    session.refresh.assert_called_once_with(product_create)

    assert result == product_expected

def test_get_all_products():

    expected_products = [
        Product(
            id=1,
            name="Portátil",
            description="Portátil de alta gama",
            price=1000,
            stock=10
        ),
        Product(
            id=2,
            name="Teléfono",
            description="Teléfono de última generación",
            price=500,
            stock=20
        )
    ]

    session = Mock()
    session.exec.return_value.all.return_value = expected_products

    result = ProductService.get_all(session=session)

    session.exec.assert_called_once()
    session.exec.return_value.all.assert_called_once()

    assert len(result) == 2
    assert result == expected_products    