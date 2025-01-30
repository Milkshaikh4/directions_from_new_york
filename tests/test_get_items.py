import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import Item
from mongoengine import connect, disconnect
from unittest.mock import patch
import mongomock

@pytest.fixture(scope="function", autouse=True)
def test_db():
    """
    This fixture sets up an in-memory MongoDB using mongomock.
    It ensures each test runs with a clean database.
    """
    disconnect() 

    connect(
        "mongoenginetest",
        host="mongodb://localhost", 
        mongo_client_class=mongomock.MongoClient,  
    )

    yield 

    disconnect()  

@pytest.fixture(scope="function")
def test_client():
    """
    Creates a test client for FastAPI.
    Ensures the test database is used.
    """
    with TestClient(app) as client:
        client.headers.update({"Authorization": "Bearer test_token"})
        yield client

def test_app_is_defined():
    assert app is not None

def test_get_items_empty(test_client):
    response = test_client.get("/items")
    assert response.status_code == 200
    assert response.json() == []  # Expecting an empty list if no items exist

def test_get_items_with_data(test_client):
    Item(name="Alice", postcode="10001", latitude=40.7128, longitude=-74.0060, users=["Alice"]).save()
    Item(name="Bob", postcode="94105", latitude=37.7749, longitude=-122.4194, users=["Bob"]).save()

    response = test_client.get("/items")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2 

    assert "name" in data[0]
    assert "postcode" in data[0]
    assert "latitude" in data[0]
    assert "longitude" in data[0]

def test_get_items_serialization(test_client):
    item = Item(
        name="Charlie",
        postcode="30301",
        latitude=33.7490,
        longitude=-84.3880,
        users=["Charlie"]
    ).save()

    response = test_client.get("/items")
    assert response.status_code == 200

    data = response.json()
    assert any(item["name"] == "Charlie" for item in data)
    assert isinstance(data[0]["latitude"], float)
    assert isinstance(data[0]["longitude"], float)

def test_get_items_unexpected_error(test_client):
    """
    Simulate a database failure to check if the endpoint handles errors.
    """
    with patch.object(Item.objects, "all", side_effect=Exception("Simulated database error")):
        response = test_client.get("/items")
    
    assert response.status_code == 500
    assert "Unexpected error" in response.json()["detail"]

# TODO: If I had more time I would test for database failures