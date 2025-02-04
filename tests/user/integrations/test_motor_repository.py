from collections.abc import Callable

import pytest
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.user.adapters.repository import UserMotorRepository
from app.user.exceptions import UserAlreadyExistError

pytestmark = [
    pytest.mark.asyncio,
]


async def test_create_and_get_user(
    get_user_create: Callable,
    motor_db: AsyncIOMotorDatabase,
) -> None:
    repo = UserMotorRepository(motor_db)
    user = get_user_create()
    await repo.create(user)

    result = await repo.get(username=user.username)

    assert user.username == result.username
    assert user.password == result.password


async def test_create_user_already_exist(
    get_user_create: Callable,
    get_same_user_create: Callable,
    motor_db: AsyncIOMotorDatabase,
) -> None:
    repo = UserMotorRepository(motor_db)
    user = get_user_create()
    await repo.create(user)

    same_user = get_same_user_create()
    with pytest.raises(UserAlreadyExistError):
        await repo.create(same_user)
