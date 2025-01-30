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

def test_get_existing_item(test_client):
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
    print("Create Response JSON:", create_response.json())

    item_id = create_response.json().get("_id")
    assert item_id is not None

    # Fetch the created item
    get_response = test_client.get(f"/items/{item_id}")
    
    assert get_response.status_code == 200
    item = get_response.json()
    assert item["name"] == "TestItem"
    assert item["postcode"] == "12345"

def test_get_item_invalid_id(test_client):
    response = test_client.get("/items/invalid-id")
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid item ID format."

def test_get_nonexistent_item(test_client):
    non_existent_id = str(ObjectId()) 
    response = test_client.get(f"/items/{non_existent_id}")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"
