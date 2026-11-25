from collections.abc import Mapping
from http import HTTPStatus
from typing import Any

import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    ('is_verified_seller', 'images_qty'),
    [
        (True, 0),
        (True, 3),
        (False, 1),
        (False, 5),
    ],
)
def test_predict_positive_results(
    app_client: TestClient,
    valid_item_payload: Mapping[str, Any],
    is_verified_seller: bool,
    images_qty: int,
):
    payload = dict(
        valid_item_payload,
        is_verified_seller=is_verified_seller,
        images_qty=images_qty,
    )

    response = app_client.post('/predict', json=payload)

    assert response.status_code == HTTPStatus.OK
    assert response.json() is True


@pytest.mark.parametrize(
    ('is_verified_seller', 'images_qty'),
    [
        (False, 0),
    ],
)
def test_predict_negative_results(
    app_client: TestClient,
    valid_item_payload: Mapping[str, Any],
    is_verified_seller: bool,
    images_qty: int,
):
    payload = dict(
        valid_item_payload,
        is_verified_seller=is_verified_seller,
        images_qty=images_qty,
    )

    response = app_client.post('/predict', json=payload)

    assert response.status_code == HTTPStatus.OK
    assert response.json() is False


@pytest.mark.parametrize(
    'missing_field',
    [
        'seller_id',
        'is_verified_seller',
        'item_id',
        'name',
        'description',
        'category',
        'images_qty',
    ],
)
def test_predict_validation_missing_required_fields(
    app_client: TestClient,
    valid_item_payload: Mapping[str, Any],
    missing_field: str,
):
    payload = dict(valid_item_payload)
    del payload[missing_field]

    response = app_client.post('/predict', json=payload)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    ('field', 'invalid_value'),
    [
        ('seller_id', 'not_an_int'),
        ('item_id', 'not_a_number'),
        ('is_verified_seller', 'neither_true_nor_false'),
        ('category', 'electronic'),
        ('images_qty', 'five_photos'),
        ('seller_id', 12.34),
        ('images_qty', 2.5),
        ('name', ['invalid', 'list']),
        ('description', {'key': 'value'}),
        ('is_verified_seller', [True, False]),
        ('item_id', [101, 102]),
        ('images_qty', -1),
    ],
)
def test_predict_validation_invalid_types(
    app_client: TestClient,
    valid_item_payload: Mapping[str, Any],
    field: str,
    invalid_value: Any,
):
    payload = dict(valid_item_payload, **{field: invalid_value})

    response = app_client.post('/predict', json=payload)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_predict_duplicate_item_id_business_logic_error(
    app_client: TestClient,
    valid_item_payload: Mapping[str, Any],
):
    first_response = app_client.post('/predict', json=valid_item_payload)
    assert first_response.status_code == HTTPStatus.OK
    assert first_response.json() is True

    second_response = app_client.post('/predict', json=valid_item_payload)
    assert second_response.status_code == HTTPStatus.BAD_REQUEST
    assert second_response.json() == {'detail': 'Объявление с таким ID уже существует'}


def test_predict_internal_server_error_500(
    app_client: TestClient,
    valid_item_payload: Mapping[str, Any],
    broken_item_service: None,
):
    response = app_client.post('/predict', json=valid_item_payload)

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.json() == {'detail': 'Внутренняя ошибка сервера'}
