from collections.abc import Callable

from fastapi import status
from fastapi.testclient import TestClient

from app.auth.schemas import Token
from app.entrypoints.factories import make_user_motor_repository
from app.entrypoints.fastapi.main import app
from app.user.adapters.repository import UserMotorRepository
from app.user.exceptions import UserAlreadyExistError, UserNotFoundError
from app.user.models import User, UserCreate


def test_singin(
    mocker,
    test_client: TestClient,
    get_user_dict: Callable,
) -> None:
    user_create = UserCreate(**get_user_dict())

    mocker.patch.object(
        UserMotorRepository,
        "get",
        new_callable=mocker.AsyncMock,
        return_value=User(
            username=user_create.username, password=user_create.password
        ),
    )

    repo = UserMotorRepository(mocker.AsyncMock())
    app.dependency_overrides[make_user_motor_repository] = lambda: repo

    response = test_client.post(
        "api/auth/singin",
        data=get_user_dict(),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(Token(**response.json()), Token)


def test_singin_user_not_authenticated(
    mocker,
    test_client: TestClient,
    get_user_dict: Callable,
) -> None:
    user_create = UserCreate(**get_user_dict())

    mocker.patch.object(
        UserMotorRepository,
        "get",
        new_callable=mocker.AsyncMock,
        return_value=User(
            username=user_create.username, password=user_create.password
        ),
    )

    repo = UserMotorRepository(mocker.AsyncMock())
    app.dependency_overrides[make_user_motor_repository] = lambda: repo

    user_in = get_user_dict()
    user_in["password"] = "a_invalid_password"  # nosec
    response = test_client.post(
        "api/auth/singin",
        data=user_in,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"message": "Invalid username or password"}


def test_singin_user_not_found(
    mocker, test_client: TestClient, get_user_dict: Callable
) -> None:
    mocker.patch.object(
        UserMotorRepository,
        "get",
        new_callable=mocker.AsyncMock,
        side_effect=UserNotFoundError(),
    )

    repo = UserMotorRepository(mocker.AsyncMock())
    app.dependency_overrides[make_user_motor_repository] = lambda: repo

    response = test_client.post(
        "api/auth/singin",
        data=get_user_dict(),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"message": "Invalid username or password"}


def test_singup(
    mocker, test_client: TestClient, get_user_dict: Callable
) -> None:
    mocker.patch.object(
        UserMotorRepository, "create", new_callable=mocker.AsyncMock
    )

    repo = UserMotorRepository(mocker.AsyncMock())
    app.dependency_overrides[make_user_motor_repository] = lambda: repo

    response = test_client.post(
        "api/auth/singup",
        json=get_user_dict(),
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() is None


def test_singup_user_already_exist(
    mocker, test_client: TestClient, get_user_dict: Callable
) -> None:
    mocker.patch.object(
        UserMotorRepository,
        "create",
        new_callable=mocker.AsyncMock,
        side_effect=UserAlreadyExistError(),
    )

    repo = UserMotorRepository(mocker.AsyncMock())
    app.dependency_overrides[make_user_motor_repository] = lambda: repo

    response = test_client.post(
        "api/auth/singup",
        json=get_user_dict(),
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
