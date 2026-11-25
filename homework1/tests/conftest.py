from collections.abc import Generator, Mapping
from typing import Any

import pytest
from dependencies import item_service
from fastapi.testclient import TestClient
from main import app
from repositories.moderation import _COLLECTION


@pytest.fixture
def app_client() -> Generator[TestClient, None, None]:
    return TestClient(app)


@pytest.fixture(autouse=True)
def clean_storage() -> Generator[None, None, None]:
    _COLLECTION.clear()
    yield
    _COLLECTION.clear()


@pytest.fixture(scope='function')
def valid_item_payload() -> Mapping[str, Any]:
    return {
        'seller_id': 1,
        'is_verified_seller': True,
        'item_id': 101,
        'name': 'Велосипед горный',
        'description': 'В отличном состоянии, почти новый',
        'category': 12,
        'images_qty': 3,
    }


@pytest.fixture
def broken_item_service() -> Generator[None, None, None]:
    class BrokenItemService:
        async def predict(self, **kwargs: Any) -> bool:
            raise RuntimeError('Database error')

    app.dependency_overrides[item_service] = lambda: BrokenItemService()
    yield
    app.dependency_overrides.clear()
