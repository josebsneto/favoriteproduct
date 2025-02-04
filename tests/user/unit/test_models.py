import pytest

from app.user.exceptions import UserNotAuthenticated
from app.user.models import User, UserCreate


def test_create_user():
    password = "a_password"  # nosec
    user = UserCreate(username="jhon@doe.com", password=password)

    assert isinstance(user, UserCreate)
    assert user.password != password


def test_user_autenticated():
    plain_password = "a_password"  # nosec
    user = UserCreate(username="jhon@doe.com", password=plain_password)

    user_hashed = User(username=user.username, password=user.password)
    res = user_hashed.authenticate(plain_password)

    assert isinstance(res, User)
    assert res.password != plain_password
    assert res.password == user.password


def test_user_not_autenticated():
    plain_password = "a_password"  # nosec
    user = UserCreate(username="jhon@doe.com", password=plain_password)

    user_hashed = User(username=user.username, password=user.password)

    invalid_plain_password = "a_other_password"  # nosec
    with pytest.raises(UserNotAuthenticated):
        user_hashed.authenticate(invalid_plain_password)
