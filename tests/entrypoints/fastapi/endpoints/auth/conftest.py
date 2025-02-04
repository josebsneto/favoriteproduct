from collections.abc import Callable

import pytest


@pytest.fixture()
def get_user_dict() -> Callable:
    return lambda: {
        "username": "jhon",
        "password": "doe",
    }
