import abc
from typing import Any

from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import PyMongoError

from app.product.exceptions import ProductDatabaseError


class ProductCachedRepository(abc.ABC):
    @abc.abstractmethod
    async def upsert(self, js_product: dict) -> None: ...  # pragma: nocoverage

    @abc.abstractmethod
    async def get(
        self,
        product_id: str,
    ) -> dict[str, Any] | None: ...  # pragma: nocoverage


class ProductCachedMotorRepository(ProductCachedRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["product_cached"]

    async def upsert(self, js_product: dict) -> None:
        try:
            js_db_product = js_product.copy()
            js_db_product["_id"] = js_db_product.pop("id")
            await self.collection.update_one(
                {"_id": js_db_product["_id"]}, {"$set": js_db_product}, True
            )
        except PyMongoError as err:
            raise ProductDatabaseError(str(err))

    async def get(self, product_id: str) -> dict[str, Any] | None:
        try:
            if js_product := await self.collection.find_one(
                {"_id": product_id},
            ):
                js_product["id"] = js_product.pop("_id")
                return dict(js_product)
            return None
        except PyMongoError as err:
            raise ProductDatabaseError(str(err))
