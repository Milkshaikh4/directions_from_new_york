import pytest
from fastapi.testclient import TestClient
from app.main import app
from mongomock import MongoClient
from app.main import app 
from unittest.mock import patch
from datetime import datetime, timedelta
from pytz import UTC

def getFutureDate(weeks=2):
    current_date = datetime.now(UTC)
    future_date = current_date + timedelta(weeks=2)

    return future_date.isoformat()

@pytest.fixture(scope="function")
def test_client():
    mock_client = MongoClient()
    mock_db = mock_client["test_db"]
    
    with patch("app.database.MongoClient") as MockMongoClient:
        MockMongoClient.return_value = mock_client
        with TestClient(app) as client:
            yield client

def test_app_is_defined():
    assert app is not None

def test_create_item_success(test_client):
    data = {
        "name": "Item1",
        "postcode": "12345",
        "latitude": 12.3456,
        "longitude": -78.9012,
        "users": ["Item1"],
        "startDate": getFutureDate(),
    }
    response = test_client.post("/items", json=data)
    # assert response.json()["detail"] == "Invalid latitude. Must be between -90 and 90."
    assert response.status_code == 200

    print(response.json())


def test_create_item_success_postcode_with_hyphen(test_client):
    data = {
        "name": "Item2",
        "postcode": "12345-6789",
        "latitude": 12.3456,
        "longitude": -78.9012,
        "users": ["Item2"],
        "startDate": getFutureDate(),
    }
    response = test_client.post("/items", json=data)
    assert response.status_code == 200

def test_create_item_invalid_postcode(test_client):
    data = {
        "name": "Item3",
        "postcode": "invalid",
        "latitude": 12.3456,
        "longitude": -78.9012,
        "users": ["Item3"],
        "startDate": getFutureDate(),
    }
    response = test_client.post("/items", json=data)
    assert response.status_code == 400

def test_create_item_missing_name(test_client):
    data = {
        "postcode": "12345",
        "latitude": 12.3456,
        "longitude": -78.9012,
        "users": ["Item1"],
        "startDate": getFutureDate(),
    }
    response = test_client.post("/items", json=data)
    assert response.status_code == 400

def test_create_item_missing_postcode(test_client):
    data = {
        "name": "Item1",
        "latitude": 12.3456,
        "longitude": -78.9012,
        "users": ["Item1"],
        "startDate": getFutureDate(),
    }
    response = test_client.post("/items", json=data)
    assert response.status_code == 400

def test_create_item_missing_latitude(test_client):
    data = {
        "name": "Item1",
        "postcode": "12345",
        "longitude": -78.9012,
        "users": ["Item1"],
        "startDate": getFutureDate(),
    }
    response = test_client.post("/items", json=data)
    assert response.status_code == 400

def test_create_item_missing_longitude(test_client):
    data = {
        "name": "Item1",
        "postcode": "12345",
        "latitude": 12.3456,
        "users": ["Item1"],
        "startDate": getFutureDate(),
    }
    response = test_client.post("/items", json=data)
    assert response.status_code == 400

def test_create_item_invalid_latitude_type(test_client):
    data = {
            "name": "Item1",
            "postcode": "12345",
            "latitude": "invalid", 
            "longitude": -78.9012,
            "users": ["Item1"],
            "startDate": getFutureDate(),
        }
    response = test_client.post("/items", json=data)
    assert response.status_code == 400

def test_create_item_invalid_longitude_type(test_client):
    data = {
            "name": "Item1",
            "postcode": "12345",
            "latitude": 12.3456,
            "longitude": "invalid", 
            "users": ["Item1"],
            "startDate": getFutureDate(),
        }
    response = test_client.post("/items", json=data)
    assert response.status_code == 400

def test_create_item_invalid_start_date_format(test_client):
    data = {
        "name": "Item1",
        "postcode": "12345",
        "latitude": 12.3456,
        "longitude": -78.9012,
        "users": ["Item1"],
        "startDate": "invalid_date",
    }
    response = test_client.post("/items", json=data)
    assert response.status_code == 400

def test_create_item_name_not_in_users_list(test_client):
    data = {
        "name": "Item3",
        "postcode": "12345",
        "latitude": 12.3456,
        "longitude": -78.9012,
        "users": ["Item1"],
        "startDate": getFutureDate(),
    }
    response = test_client.post("/items", json=data)
    assert response.status_code == 400
