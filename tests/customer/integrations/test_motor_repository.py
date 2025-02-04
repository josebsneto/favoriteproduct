import json
from collections.abc import Callable
from unittest.mock import AsyncMock

import pytest
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import ServerSelectionTimeoutError

from app.customer.adapters.repository import (
    CustomerDatabaseError,
    CustomerMotorRepository,
    Paginator,
)
from app.customer.exceptions import (
    CustomerAlreadyExistError,
    CustomerNotFoundError,
    CustomerNotUpdatedError,
)

pytestmark = [
    pytest.mark.asyncio,
]


async def test_create_and_get_customer(
    get_customer: Callable,
    motor_db: AsyncIOMotorDatabase,
) -> None:
    repo = CustomerMotorRepository(motor_db)
    customer = get_customer()
    await repo.create(customer)

    result, _ = await repo.get(customer.email, Paginator(1))

    assert result.email == customer.email
    assert result.name == customer.name


async def test_create_customer_already_exists(
    get_customer: Callable,
    motor_db: AsyncIOMotorDatabase,
) -> None:
    repo = CustomerMotorRepository(motor_db)
    await repo.create(get_customer())

    with pytest.raises(CustomerAlreadyExistError):
        await repo.create(get_customer())


async def test_get_customer_not_found(
    get_customer: Callable,
    motor_db: AsyncIOMotorDatabase,
) -> None:
    repo = CustomerMotorRepository(motor_db)

    paginator = Paginator(page=2, limit=1)
    with pytest.raises(CustomerNotFoundError):
        await repo.get("a_not_found_email", paginator)


async def test_update_customer(
    get_customer: Callable,
    motor_db: AsyncIOMotorDatabase,
) -> None:
    repo = CustomerMotorRepository(motor_db)
    customer = get_customer()
    await repo.create(customer)

    updated_name = "a_updated_name"
    await repo.update(customer.email, updated_name)
    result, _ = await repo.get(customer.email)

    assert result.name == updated_name


async def test_delete_customer(
    get_customer: Callable,
    motor_db: AsyncIOMotorDatabase,
) -> None:
    repo = CustomerMotorRepository(motor_db)
    customer = get_customer()
    await repo.create(customer)

    await repo.delete(customer.email)

    with pytest.raises(CustomerNotFoundError):
        await repo.get(customer.email)


async def test_get_paginate_customer_product(
    get_customer: Callable,
    motor_db: AsyncIOMotorDatabase,
) -> None:
    repo = CustomerMotorRepository(motor_db)
    customer = get_customer()
    await repo.create(customer)

    js_customer = json.loads(customer.model_dump_json())
    paginator = Paginator(page=2, limit=1)
    result, _ = await repo.get(customer.email, paginator)

    second_product_client_list = js_customer["product_ids"][paginator.page - 1]
    assert len(result.product_ids) == 1
    assert result.product_ids[0] == second_product_client_list


async def test_get_lifo_customer_product(
    get_customer: Callable,
    motor_db: AsyncIOMotorDatabase,
) -> None:
    repo = CustomerMotorRepository(motor_db)
    customer = get_customer()
    await repo.create(customer)
    await repo.add_product(customer.email, "firts_product")

    paginator = Paginator(page=1, limit=1)
    result, _ = await repo.get(customer.email, paginator)

    assert result.product_ids[0] == "firts_product"


async def test_customer_add_product(
    get_customer: Callable,
    get_customer_product_id: Callable,
    motor_db: AsyncIOMotorDatabase,
) -> None:
    repo = CustomerMotorRepository(motor_db)
    customer = get_customer()
    await repo.create(customer)

    result, _ = await repo.get(customer.email, Paginator(1))
    assert len(result.product_ids) == 2

    product = get_customer_product_id()
    await repo.add_product(customer.email, product)

    result, _ = await repo.get(customer.email, Paginator(1))
    assert len(result.product_ids) == 3


async def test_customer_add_same_product(
    get_customer: Callable,
    motor_db: AsyncIOMotorDatabase,
) -> None:
    repo = CustomerMotorRepository(motor_db)
    customer = get_customer()
    await repo.create(customer)

    result, _ = await repo.get(customer.email, Paginator(1))
    assert len(result.product_ids) == 2

    same_product = customer.product_ids[0]

    with pytest.raises(CustomerNotUpdatedError):
        await repo.add_product(customer.email, same_product)


async def test_customer_not_add_product(
    get_customer: Callable,
    get_customer_product_id: Callable,
    motor_db: AsyncIOMotorDatabase,
) -> None:
    repo = CustomerMotorRepository(motor_db)

    product = get_customer_product_id()
    with pytest.raises(CustomerNotUpdatedError):
        await repo.add_product("inexistent_email", product)


async def test_create_database_timeout(
    get_customer: Callable,
) -> None:
    motor_db = AsyncMock()

    repo = CustomerMotorRepository(motor_db)
    repo.collection = AsyncMock()
    repo.collection.insert_one = AsyncMock(
        side_effect=ServerSelectionTimeoutError()
    )

    customer = get_customer()
    with pytest.raises(CustomerDatabaseError):
        await repo.create(customer)


async def test_update_database_timeout(
    get_customer: Callable,
) -> None:
    motor_db = AsyncMock()

    repo = CustomerMotorRepository(motor_db)
    repo.collection = AsyncMock()
    repo.collection.update_one = AsyncMock(
        side_effect=ServerSelectionTimeoutError()
    )

    customer = get_customer()
    with pytest.raises(CustomerDatabaseError):
        await repo.update(customer.email, "updated_name")


async def test_delete_database_timeout(
    get_customer: Callable,
) -> None:
    motor_db = AsyncMock()

    repo = CustomerMotorRepository(motor_db)
    repo.collection = AsyncMock()
    repo.collection.delete_one = AsyncMock(
        side_effect=ServerSelectionTimeoutError()
    )

    customer = get_customer()
    with pytest.raises(CustomerDatabaseError):
        await repo.delete(customer)
