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
        client.headers.update({"Authorization": "Bearer test_token"})
        yield client

def test_delete_existing_item(test_client):

    item_data = {
        "name": "TestItem",
        "postcode": "12345",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "users": ["TestItem"],
        "startDate": getFutureDate()
    }
    create_response = test_client.post("/items", json=item_data)
    assert create_response.status_code == 200

    # Extract the item ID from the response
    item_id = create_response.json().get("_id")
    assert item_id is not None

    # Delete the created item
    delete_response = test_client.delete(f"/items/{item_id}")
    
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == f"Item with ID {item_id} has been successfully deleted."

    # Verify item no longer exists
    get_response = test_client.get(f"/items/{item_id}")
    assert get_response.status_code == 404  # Item should be deleted

def test_delete_nonexistent_item(test_client):
    non_existent_id = str(ObjectId())  # Generate a valid but non-existing ObjectId
    response = test_client.delete(f"/items/{non_existent_id}")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found."

def test_delete_invalid_id(test_client):
    response = test_client.delete("/items/invalid-id")
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid item ID format."
