from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError

from app import logging, settings
from app.auth.exceptions import (
    AuthExpiredTokenError,
    AuthInvalidTokenError,
    AuthTokenExpNotFoundError,
)
from app.entrypoints import factories
from app.entrypoints.fastapi.endpoints.auth.v1 import auth
from app.entrypoints.fastapi.endpoints.customers.v1 import customers
from app.entrypoints.fastapi.exceptions.handlers import (
    custom_exception_handler,
    custom_http_exception_handler,
    custom_validator_request_http_exception_handler,
    invalid_jwt,
)

logger = logging.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    factories.get_motor_db()
    yield
    factories.clean_motor_client()


def create_app() -> FastAPI:
    # app conf init
    app = FastAPI(
        title=settings.APP_NAME,
    )

    uvicorn_logger = logging.get_logger("uvicorn.access")
    uvicorn_logger.handlers.clear()
    logging.setup_logger(uvicorn_logger)

    # exceptions
    app.add_exception_handler(Exception, custom_exception_handler)
    app.add_exception_handler(
        HTTPException, custom_http_exception_handler  # type: ignore
    )
    app.add_exception_handler(
        RequestValidationError,
        custom_validator_request_http_exception_handler,  # type: ignore
    )
    app.add_exception_handler(AuthInvalidTokenError, invalid_jwt)
    app.add_exception_handler(AuthExpiredTokenError, invalid_jwt)
    app.add_exception_handler(AuthTokenExpNotFoundError, invalid_jwt)

    # add urls of endpoints
    app.include_router(
        customers.router,
        prefix="/api/customer",
        dependencies=[Depends(auth.verify_http_bearer_access_token)],
    )
    app.include_router(auth.router, prefix="/api/auth")

    return app


app = create_app()
