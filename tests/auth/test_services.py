from datetime import datetime

import jwt
import pytest

from app import settings
from app.auth.exceptions import (
    AuthExpiredTokenError,
    AuthInvalidTokenError,
    AuthTokenExpNotFoundError,
)
from app.auth.schemas import Token
from app.auth.services import create_access_token, verify_access_token


def test_create_access_token() -> None:
    username_mock = "jhon@doe.com"
    token = create_access_token(username_mock)

    payload = jwt.decode(
        token.access_token,
        str(settings.SECRET_KEY),
        [settings.SECRET_ALGORITHM],
    )

    assert payload["sub"] == username_mock
    assert token.token_type == settings.ACCESS_TOKEN_TYPE


def test_verify_access_token() -> None:
    username_mock = "jhon@doe.com"
    token_mock = jwt.encode(
        {
            "sub": username_mock,
            "exp": datetime.now(settings.TIMEZONE).timestamp() + 9999,
        },
        str(settings.SECRET_KEY),
        settings.SECRET_ALGORITHM,
    )

    token_schema_mock = Token(
        access_token=token_mock, token_type=settings.ACCESS_TOKEN_TYPE
    )
    verify_access_token(token_schema_mock)


def test_verify_expired_access_token() -> None:
    username_mock = "jhon@doe.com"
    token_mock = jwt.encode(
        {
            "sub": username_mock,
            "exp": datetime.now(settings.TIMEZONE).timestamp(),
        },
        str(settings.SECRET_KEY),
        settings.SECRET_ALGORITHM,
    )

    token_schema_mock = Token(
        access_token=token_mock, token_type=settings.ACCESS_TOKEN_TYPE
    )

    with pytest.raises(AuthExpiredTokenError):
        verify_access_token(token_schema_mock)


def test_verify_malformated_payload_access_token() -> None:
    username_mock = "jhon@doe.com"
    token_mock = jwt.encode(
        {"sub": username_mock},
        str(settings.SECRET_KEY),
        settings.SECRET_ALGORITHM,
    )

    token_schema_mock = Token(
        access_token=token_mock, token_type=settings.ACCESS_TOKEN_TYPE
    )

    with pytest.raises(AuthTokenExpNotFoundError):
        verify_access_token(token_schema_mock)


def test_verify_invalid_access_token() -> None:
    username_mock = "jhon@doe.com"
    token_mock = jwt.encode(
        {
            "sub": username_mock,
            "exp": datetime.now(settings.TIMEZONE).timestamp() + 9999,
        },
        "a_invalid_secrect",
        settings.SECRET_ALGORITHM,
    )

    token_schema_mock = Token(
        access_token=token_mock, token_type=settings.ACCESS_TOKEN_TYPE
    )

    with pytest.raises(AuthInvalidTokenError):
        verify_access_token(token_schema_mock)
