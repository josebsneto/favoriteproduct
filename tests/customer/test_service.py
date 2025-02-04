from collections.abc import Callable

import pytest
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.customer.adapters.repository import CustomerMotorRepository, Paginator
from app.customer.service import CustomerService
from app.product.adapters.repository import ProductCachedMotorRepository
from app.product.adapters.requester import ProductAiohttpRequester

pytestmark = [
    pytest.mark.asyncio,
]


async def test_add_customer_product_by_cache(
    mocker,
    motor_db: AsyncIOMotorDatabase,
    get_product_dict: Callable,
    get_customer: Callable,
):
    customer = get_customer()
    js_product = get_product_dict()
    customer.product_ids = [js_product["id"]]
    js_product = get_product_dict()
    mocker.patch.object(
        ProductAiohttpRequester,
        "get",
        new_callable=mocker.AsyncMock,
        return_value=js_product.copy(),
    )
    customer_repo = CustomerMotorRepository(motor_db)
    product_cached_repo = ProductCachedMotorRepository(motor_db)
    product_requester = ProductAiohttpRequester(mocker.AsyncMock())
    await customer_repo.create(customer)

    service = CustomerService(
        customer_repo=customer_repo,
        product_cached_repo=product_cached_repo,
        product_requester=product_requester,
    )

    result, _ = await service.get_products_by_customer(
        customer.email, Paginator(page=1)
    )

    result_cache = await product_cached_repo.get(js_product["id"])

    assert len(result) == len(customer.product_ids)
    assert result[0] == js_product
    assert result_cache == js_product
