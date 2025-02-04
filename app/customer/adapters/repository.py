import abc
import json

from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import DuplicateKeyError, PyMongoError

from app.customer.adapters.schemas import Paginator, PaginatorResponse
from app.customer.exceptions import (
    CustomerAlreadyExistError,
    CustomerDatabaseError,
    CustomerNotDeletedError,
    CustomerNotFoundError,
    CustomerNotUpdatedError,
)
from app.customer.models import Customer


class CustomerRepository(abc.ABC):
    @abc.abstractmethod
    async def create(
        self, customer: Customer
    ) -> Customer: ...  # pragma: nocoverage

    @abc.abstractmethod
    async def get(
        self,
        email: str,
        product_ids_pag: Paginator = Paginator(),
    ) -> tuple[Customer, PaginatorResponse]: ...  # pragma: nocoverage

    @abc.abstractmethod
    async def update(
        self, email: str, name: str
    ) -> None: ...  # pragma: nocoverage

    @abc.abstractmethod
    async def delete(self, email) -> None: ...  # pragma: nocoverage

    @abc.abstractmethod
    async def add_product(
        self,
        email: str,
        product_id: str,
    ) -> None: ...  # pragma: nocoverage


class CustomerMotorRepository(CustomerRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["customers"]

    async def create(self, customer: Customer):
        try:
            js_customer = json.loads(customer.model_dump_json())
            js_customer["_id"] = js_customer.pop("email")
            return await self.collection.insert_one(js_customer)
        except DuplicateKeyError as err:
            raise CustomerAlreadyExistError(str(err))
        except PyMongoError as err:
            raise CustomerDatabaseError(str(err))

    async def get(
        self, email: str, product_ids_pag: Paginator = Paginator()
    ) -> tuple[Customer, PaginatorResponse]:
        try:
            skip, limit = product_ids_pag.make_paginator()
            cursor = self.collection.aggregate(
                [
                    {"$match": {"_id": email}},
                    {
                        "$project": {
                            "email": "$_id",
                            "name": 1,
                            "product_ids": {
                                "$slice": ["$product_ids", skip, limit]
                            },
                            "total": {"$size": "$product_ids"},
                        }
                    },
                ]
            )

            if result := await cursor.to_list(length=1):
                js_result = dict(result[0])
                customer = Customer(**js_result)
                paginator = PaginatorResponse(
                    page=product_ids_pag.page, total=js_result["total"]
                )
                return customer, paginator
            raise CustomerNotFoundError(f"No docuemnt matches _id {email}.")
        except PyMongoError as err:
            raise CustomerDatabaseError(str(err))

    async def update(self, email: str, name: str) -> None:
        try:
            res = await self.collection.update_one(
                {
                    "_id": email,
                },
                {"$set": {"name": name}},
            )
            if res.modified_count == 0:
                raise CustomerNotUpdatedError()
        except PyMongoError as err:
            raise CustomerDatabaseError(str(err))

    async def delete(self, email: str) -> None:
        try:
            res = await self.collection.delete_one({"_id": email})
            if res.deleted_count == 0:
                raise CustomerNotDeletedError()
        except PyMongoError as err:
            raise CustomerDatabaseError(str(err))

    async def add_product(self, email: str, product_id: str) -> None:
        try:
            res = await self.collection.update_one(
                {"_id": email, "product_ids": {"$ne": product_id}},
                {
                    "$push": {
                        "product_ids": {"$each": [product_id], "$position": 0}
                    }
                },
            )
            if res.modified_count == 0:
                raise CustomerNotUpdatedError()
        except PyMongoError as err:
            raise CustomerDatabaseError(str(err))
