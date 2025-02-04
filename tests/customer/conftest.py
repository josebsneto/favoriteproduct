from collections.abc import Callable

import pytest

from app.customer.models import Customer


@pytest.fixture
def get_customer() -> Callable:
    return lambda: Customer(
        email="josebernardinoneto@gmail.com",
        name="José Bernardino Neto",
        product_ids=["dh1be31595", "fh04bfe236"],
    )


@pytest.fixture
def get_other_customer() -> Callable:
    return lambda: Customer(
        email="jhon.doe@gmail.com",
        name="Jhon Doe",
        product_ids=["dh1be31595", "fh04bfe236"],
    )


@pytest.fixture
def get_customer_product_id() -> Callable:
    return lambda: "122801800"


@pytest.fixture
def get_same_customer_product_id() -> Callable:
    return lambda: "dh1be31595"


@pytest.fixture
def get_product_dict() -> Callable:
    return lambda: {
        "id": "1",
        "title": "Isolante Térmico Azteq Odin Dobrável",
        "image_uri": "https://a-static.mlcdn.com.br/800x560/isolante-"
        "termico-azteq-odin-dobravel-eva-aluminizado-camping/olistplus"
        "/opmc5yct93nmqyy2/b8cd8339069f2b0baea4195813733b97.jpeg",
        "brand": "azteq",
        "price": 189.86,
        "reviewScore": 4.8,
    }
