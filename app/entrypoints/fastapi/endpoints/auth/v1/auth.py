from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.auth.exceptions import (
    AuthExpiredTokenError,
    AuthInvalidTokenError,
    AuthTokenExpNotFoundError,
)
from app.auth.schemas import Token
from app.auth.services import create_access_token, verify_access_token
from app.entrypoints.factories import make_user_motor_repository
from app.user.adapters.repository import UserRepository
from app.user.exceptions import (
    UserAlreadyExistError,
    UserDatabaseError,
    UserNotAuthenticated,
    UserNotFoundError,
)
from app.user.models import UserCreate

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/singin")


async def verify_http_bearer_access_token(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> None:
    try:
        verify_access_token(Token(access_token=token))
    except (
        AuthExpiredTokenError,
        AuthTokenExpNotFoundError,
        AuthInvalidTokenError,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post(
    "/singin",
    summary="Generate authentication bearer token",
)
async def signin(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    repo: UserRepository = Depends(make_user_motor_repository),
) -> Token:
    try:
        user = await repo.get(username=form_data.username)
        user.authenticate(form_data.password)
        return create_access_token(user.username)
    except (UserNotFoundError, UserNotAuthenticated):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except UserDatabaseError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post(
    "/singup",
    status_code=status.HTTP_201_CREATED,
    summary="Create authentication user",
)
async def singup(
    user: UserCreate,
    repo: UserRepository = Depends(make_user_motor_repository),
) -> None:
    try:
        await repo.create(user)
    except UserAlreadyExistError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists.",
        )
    except UserDatabaseError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
