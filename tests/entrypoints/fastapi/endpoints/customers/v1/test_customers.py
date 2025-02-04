from collections.abc import Callable

from fastapi import status
from fastapi.testclient import TestClient

from app.customer.adapters.repository import CustomerMotorRepository
from app.customer.exceptions import (
    CustomerAlreadyExistError,
    CustomerDatabaseError,
    CustomerNotFoundError,
    CustomerNotUpdatedError,
)
from app.customer.service import CustomerService
from app.entrypoints.factories import (
    make_customer_motor_repository,
    make_customer_service,
)
from app.entrypoints.fastapi.endpoints.customers.v1.schema import (
    CustomerGetResponse,
)
from app.entrypoints.fastapi.main import app


def test_create_customer(
    mocker,
    test_client: TestClient,
    get_customer_dict: Callable,
) -> None:
    mocker.patch.object(
        CustomerMotorRepository,
        "create",
        new_callable=mocker.AsyncMock,
    )

    repo = CustomerMotorRepository(mocker.AsyncMock())
    app.dependency_overrides[make_customer_motor_repository] = lambda: repo

    response = test_client.post(
        "api/customer",
        json=get_customer_dict(),
    )

    assert response.status_code == status.HTTP_201_CREATED


def test_create_customer_already_exist(
    mocker,
    test_client: TestClient,
    get_customer_dict: Callable,
) -> None:
    mocker.patch.object(
        CustomerMotorRepository,
        "create",
        new_callable=mocker.AsyncMock,
        side_effect=CustomerAlreadyExistError(),
    )

    repo = CustomerMotorRepository(mocker.AsyncMock())
    app.dependency_overrides[make_customer_motor_repository] = lambda: repo

    response = test_client.post(
        "api/customer",
        json=get_customer_dict(),
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_customer_database_timeout(
    mocker,
    test_client: TestClient,
    get_customer_dict: Callable,
) -> None:
    mocker.patch.object(
        CustomerMotorRepository,
        "create",
        new_callable=mocker.AsyncMock,
        side_effect=CustomerDatabaseError(),
    )

    repo = CustomerMotorRepository(mocker.AsyncMock())
    app.dependency_overrides[make_customer_motor_repository] = lambda: repo

    response = test_client.post(
        "api/customer",
        json=get_customer_dict(),
    )

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


def test_get_customer(
    mocker,
    test_client: TestClient,
    get_customer: Callable,
    get_paginator_response: Callable,
) -> None:
    customer = get_customer()
    pag_response = get_paginator_response()
    mocker.patch.object(
        CustomerMotorRepository,
        "get",
        new_callable=mocker.AsyncMock,
        return_value=(customer, pag_response),
    )

    repo = CustomerMotorRepository(mocker.AsyncMock())
    app.dependency_overrides[make_customer_motor_repository] = lambda: repo

    response = test_client.get(
        "api/customer/jhon@doe.com",
    )
    result = CustomerGetResponse(**response.json())

    assert response.status_code == status.HTTP_200_OK
    assert result.item == customer
    assert result.paginator_product_ids == pag_response


def test_get_customer_not_found(
    mocker,
    test_client: TestClient,
    get_customer_dict: Callable,
) -> None:
    mocker.patch.object(
        CustomerMotorRepository,
        "get",
        new_callable=mocker.AsyncMock,
        side_effect=CustomerNotFoundError(),
    )

    repo = CustomerMotorRepository(mocker.AsyncMock())
    app.dependency_overrides[make_customer_motor_repository] = lambda: repo

    response = test_client.get(
        "api/customer/customer@notfound.com",
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_add_customer_product(mocker, test_client: TestClient) -> None:
    mocker.patch.object(
        CustomerService,
        "add_customer_product",
        new_callable=mocker.AsyncMock,
    )

    service = CustomerService(
        mocker.AsyncMock(), mocker.AsyncMock(), mocker.AsyncMock()
    )
    app.dependency_overrides[make_customer_service] = lambda: service

    response = test_client.put(
        "api/customer/jhon@doe.com/products",
        json={"product_id": "a_product_id"},
    )

    assert response.status_code == status.HTTP_202_ACCEPTED


def test_add_customer_product_email_not_found(
    mocker, test_client: TestClient
) -> None:
    mocker.patch.object(
        CustomerService,
        "add_customer_product",
        new_callable=mocker.AsyncMock,
        side_effect=CustomerNotUpdatedError(),
    )

    service = CustomerService(
        mocker.AsyncMock(), mocker.AsyncMock(), mocker.AsyncMock()
    )
    app.dependency_overrides[make_customer_service] = lambda: service

    response = test_client.put(
        "api/customer/customer@notfound.com/products",
        json={"product_id": "a_product_id"},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
