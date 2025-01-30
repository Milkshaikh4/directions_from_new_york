import pytest
from fastapi.testclient import TestClient
from app.main import app
from mongoengine import connect, disconnect
import mongomock
from tests.utils.utils import getFutureDate

@pytest.fixture(scope="function", autouse=True)
def test_db():
    """
    This fixture sets up an in-memory MongoDB using mongomock.
    It ensures each test runs with a clean database.
    """
    disconnect() 
    connect(
        "mongoenginetest",
        mongo_client_class=mongomock.MongoClient, 
    )
    yield  
    disconnect()  

@pytest.fixture(scope="function")
def test_client():
    """
    Creates a test client for FastAPI.
    """
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
