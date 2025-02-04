from collections.abc import Callable

import pytest

from app.product.models import Product


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


@pytest.fixture
def get_product() -> Callable:
    return lambda: Product(
        id="1",
        title="Isolante Térmico Azteq Odin Dobrável",
        image_uri="https://a-static.mlcdn.com.br/800x560/isolante-"
        "termico-azteq-odin-dobravel-eva-aluminizado-camping/olistplus"
        "/opmc5yct93nmqyy2/b8cd8339069f2b0baea4195813733b97.jpeg",
        brand="azteq",
        price=189.86,
        reviewScore=4.8,
    )


@pytest.fixture
def get_other_product() -> Callable:
    return lambda: Product(
        id="1",
        title="Conjunto de Mesa e Cadeiras Dobráveis Domo - Nautika",
        image_uri="https://a-static.mlcdn.com.br/800x560/conjunto-de"
        "-mesa-e-cadeiras-dobraveis-domo-nautika/jade-shop"
        "/p3444/27fc20b4332239cf8ab3c8d11e1b0589.jpeg",
        brand="Nautika",
        price=359.99,
        reviewScore=4.9,
    )
