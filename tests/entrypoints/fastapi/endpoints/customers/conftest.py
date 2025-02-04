from collections.abc import Callable

import pytest

from app.customer.adapters.schemas import PaginatorResponse
from app.customer.models import Customer


@pytest.fixture
def get_customer_dict() -> Callable:
    return lambda: {
        "email": "jhon@doe.com",
        "name": "Jhon Doe",
        "product_ids": ["dh1be31595", "fh04bfe236"],
    }


@pytest.fixture
def get_customer() -> Callable:
    return lambda: Customer(
        email="josebernardinoneto@gmail.com",
        name="José Bernardino Neto",
        product_ids=["dh1be31595", "fh04bfe236"],
    )


@pytest.fixture
def get_paginator_response() -> Callable:
    return lambda: PaginatorResponse(page=1, total=2)
