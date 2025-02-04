from datetime import datetime, timedelta

import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from app import settings
from app.auth.exceptions import (
    AuthExpiredTokenError,
    AuthInvalidTokenError,
    AuthTokenExpNotFoundError,
)
from app.auth.schemas import Token


def create_access_token(username: str) -> Token:
    expire_seconds = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    ).total_seconds()
    to_encode = {
        "sub": username,
        "exp": datetime.now(settings.TIMEZONE).timestamp() + expire_seconds,
    }
    return Token(
        access_token=jwt.encode(
            to_encode,
            str(settings.SECRET_KEY),
            settings.SECRET_ALGORITHM,
        ),
        token_type=settings.ACCESS_TOKEN_TYPE,
    )


def verify_access_token(token: Token) -> None:
    try:
        payload = jwt.decode(
            token.access_token,
            str(settings.SECRET_KEY),
            [settings.SECRET_ALGORITHM],
        )
        if not payload.get("exp"):
            raise AuthTokenExpNotFoundError()
    except ExpiredSignatureError:
        raise AuthExpiredTokenError()
    except InvalidTokenError:
        raise AuthInvalidTokenError()
