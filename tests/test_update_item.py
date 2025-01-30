import pytest
from fastapi.testclient import TestClient
from app.main import app
from mongoengine import connect, disconnect
import mongomock
from tests.utils.utils import getFutureDate
from bson import ObjectId

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
        yield client

def test_update_existing_item(test_client):
    item_data = {
        "name": "OldItem",
        "postcode": "12345",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "users": ["OldItem"],
        "startDate": getFutureDate()
    }
    create_response = test_client.post("/items", json=item_data)
    assert create_response.status_code == 200

    # Extract the item ID from the response
    item_id = create_response.json().get("_id")
    assert item_id is not None

    # Update the created item
    update_data = {
        "name": "UpdatedItem",
        "title": "Updated Title"
    }
    update_response = test_client.put(f"/items/{item_id}", json=update_data)

    assert update_response.status_code == 200
    assert update_response.json()["message"] == f"Item with ID {item_id} has been successfully updated."

    # Fetch the updated item
    get_response = test_client.get(f"/items/{item_id}")
    assert get_response.status_code == 200
    item = get_response.json()
    assert item["name"] == "UpdatedItem"
    assert item["title"] == "Updated Title"

def test_update_nonexistent_item(test_client):
    non_existent_id = str(ObjectId())  # Generate a valid but non-existing ObjectId
    update_data = {"name": "NonExistentItem"}

    response = test_client.put(f"/items/{non_existent_id}", json=update_data)
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found."

def test_update_invalid_id(test_client):
    update_data = {"name": "InvalidIDItem"}

    response = test_client.put("/items/invalid-id", json=update_data)
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid item ID format."

def test_update_item_invalid_fields(test_client):
    item_data = {
        "name": "ItemWithInvalidFields",
        "postcode": "12345",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "users": ["ItemWithInvalidFields"],
        "startDate": getFutureDate()
    }
    create_response = test_client.post("/items", json=item_data)
    assert create_response.status_code == 200

    # Extract the item ID from the response
    item_id = create_response.json().get("_id")
    assert item_id is not None

    # Attempt to update using invalid fields
    update_data = {
        "invalid_field": "InvalidValue",
        "another_invalid_field": "Should not be updated"
    }
    update_response = test_client.put(f"/items/{item_id}", json=update_data)

    assert update_response.status_code == 200
    assert update_response.json()["message"] == f"Item with ID {item_id} has been successfully updated."

    # Fetch the updated item
    get_response = test_client.get(f"/items/{item_id}")
    assert get_response.status_code == 200
    item = get_response.json()

    # Ensure invalid fields were ignored and not added
    assert "invalid_field" not in item
    assert "another_invalid_field" not in item

def test_update_item_missing_required_fields(test_client):
    item_data = {
        "name": "ItemWithMissingFields",
        "postcode": "12345",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "users": ["ItemWithMissingFields"],
        "startDate": getFutureDate()
    }
    create_response = test_client.post("/items", json=item_data)
    assert create_response.status_code == 200

    # Extract the item ID from the response
    item_id = create_response.json().get("_id")
    assert item_id is not None

    # Attempt to update without required fields
    update_data = {}  # Empty payload
    update_response = test_client.put(f"/items/{item_id}", json=update_data)

    assert update_response.status_code == 200
    assert update_response.json()["message"] == f"Item with ID {item_id} has been successfully updated."

    # Fetch the updated item
    get_response = test_client.get(f"/items/{item_id}")
    assert get_response.status_code == 200
    item = get_response.json()

    # Ensure the item remains unchanged
    assert item["name"] == "ItemWithMissingFields"
