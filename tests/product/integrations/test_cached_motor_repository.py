from collections.abc import Callable
from unittest.mock import AsyncMock

import pytest
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import ServerSelectionTimeoutError

from app.product.adapters.repository import ProductCachedMotorRepository
from app.product.exceptions import ProductDatabaseError

pytestmark = [
    pytest.mark.asyncio,
]


async def test_create_and_get_cache_product(
    get_product_dict: Callable,
    motor_db: AsyncIOMotorDatabase,
) -> None:
    repo = ProductCachedMotorRepository(motor_db)
    product = get_product_dict()
    await repo.upsert(product.copy())

    result = await repo.get(product["id"])

    assert result == product


async def test_update_cache_product(
    get_product_dict: Callable,
    motor_db: AsyncIOMotorDatabase,
) -> None:
    repo = ProductCachedMotorRepository(motor_db)
    product = get_product_dict()
    await repo.upsert(product.copy())
    product["title"] = "title_updated"
    await repo.upsert(product.copy())

    result = await repo.get(product["id"])

    assert result is not None
    assert result.get("title") == "title_updated"


async def test_get_cache_product_not_found(
    motor_db: AsyncIOMotorDatabase,
) -> None:
    repo = ProductCachedMotorRepository(motor_db)
    result = await repo.get("not_found_id")
    assert result is None


async def test_update_database_timeout(
    get_product_dict: Callable,
) -> None:
    motor_db = AsyncMock()
    repo = ProductCachedMotorRepository(motor_db)
    repo.collection = AsyncMock()
    repo.collection.update_one = AsyncMock(
        side_effect=ServerSelectionTimeoutError()
    )

    with pytest.raises(ProductDatabaseError):
        await repo.upsert(get_product_dict())


async def test_get_database_timeout() -> None:
    motor_db = AsyncMock()
    repo = ProductCachedMotorRepository(motor_db)
    repo.collection = AsyncMock()
    repo.collection.find_one = AsyncMock(
        side_effect=ServerSelectionTimeoutError()
    )

    with pytest.raises(ProductDatabaseError):
        await repo.get("a_product_id")
