from collections.abc import Callable

import pytest

from app.user.models import User, UserCreate


@pytest.fixture
def get_user() -> Callable:
    return lambda: User(
        username="jhon@doe.com",
        password="a_password",
    )  # nosec


@pytest.fixture
def get_same_user() -> Callable:
    return lambda: User(
        username="jhon@doe.com",
        password="a_other_password",  # nosec
    )


@pytest.fixture
def get_user_create() -> Callable:
    return lambda: UserCreate(
        username="jhon@doe.com",
        password="a_password",  # nosec
    )


@pytest.fixture
def get_same_user_create() -> Callable:
    return lambda: UserCreate(
        username="jhon@doe.com", password="a_other_password"  # nosec
    )
