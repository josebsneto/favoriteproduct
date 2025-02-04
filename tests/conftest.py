import uuid
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient

from app import settings
from app.entrypoints.fastapi.endpoints.auth.v1.auth import (
    verify_http_bearer_access_token,
)
from app.entrypoints.fastapi.main import app


@pytest_asyncio.fixture
async def motor_db_name() -> str:
    suffix = str(uuid.uuid4()).replace("-", "")
    return f"app_test_db_{suffix}"


@pytest_asyncio.fixture
async def motor_db(
    motor_db_name: str,
) -> AsyncGenerator:
    motor_client = AsyncIOMotorClient(settings.DB_URL_TEST)  # type: ignore
    yield motor_client[motor_db_name]
    await motor_client.drop_database(motor_db_name)


@pytest.fixture(scope="session")
def test_client() -> TestClient:
    app.dependency_overrides[verify_http_bearer_access_token] = lambda: None
    return TestClient(app=app, base_url="https://test")
