from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse

from app import logging, settings
from app.entrypoints.fastapi.exceptions.custom import (
    AppHttpException,
    AppRequestValidationHttpException,
)

logger = logging.get_logger(__name__)


async def custom_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    AppHttpException("An unexpected error has occurred")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error has occurred"},
    )


async def custom_http_exception_handler(
    request: Request, exc: HTTPException
) -> JSONResponse:
    AppHttpException(exc.detail)
    if headers := getattr(exc, "headers", None):
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.detail},
            headers=headers,
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


async def custom_validator_request_http_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    The fastapi use pydantic for scheme erros
    Custom exception error for pydantic validator
    -> RequestValidationError, WebSocketRequestValidationError, etc.
    """
    erros = jsonable_encoder(exc.errors())
    AppRequestValidationHttpException(erros)

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": erros},
    )


async def invalid_jwt(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content="Invalid authentication token",
        headers={"WWW-Authenticate": settings.ACCESS_TOKEN_TYPE},
    )
