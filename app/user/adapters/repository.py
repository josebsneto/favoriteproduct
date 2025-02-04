import abc
import json

from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import DuplicateKeyError, PyMongoError

from app.user.exceptions import (
    UserAlreadyExistError,
    UserDatabaseError,
    UserNotFoundError,
)
from app.user.models import User, UserCreate


class UserRepository(abc.ABC):
    @abc.abstractmethod
    async def create(self, user: UserCreate) -> None: ...  # pragma: nocoverage

    @abc.abstractmethod
    async def get(self, username: str) -> User: ...  # pragma: nocoverage


class UserMotorRepository(UserRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["users"]

    async def create(self, user: UserCreate) -> None:
        try:
            js_user = json.loads(user.model_dump_json())
            js_user["_id"] = js_user.pop("username")
            await self.collection.insert_one(js_user)
        except DuplicateKeyError as err:
            raise UserAlreadyExistError(str(err))
        except PyMongoError as err:
            raise UserDatabaseError(str(err))

    async def get(self, username: str) -> User:
        try:
            if js_user := await self.collection.find_one({"_id": username}):
                js_user["username"] = js_user.pop("_id")
                return User(**js_user)
            raise UserNotFoundError(f"No docuemnt matches _id {username}.")
        except PyMongoError as err:
            raise UserDatabaseError(str(err))
