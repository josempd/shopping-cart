import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from domain.models import Base
from infrastructure.database import get_db

# Organized and grouped imports for readability

@pytest.fixture(scope="module")
def test_client():
    """
    Setup TestClient with a test database for the duration of the tests.
    """
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        try:
            db = TestSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    Base.metadata.drop_all(bind=engine)

class CustomTestClient(TestClient):
    """
    Extends TestClient to add a method for DELETE requests with a payload.
    """
    def delete_with_payload(self, url, json):
        return self.request(method="DELETE", url=url, json=json)

def test_create_item_product(test_client):
    response = test_client.post(
        "/item/",
        json={
            "name": "Test Item",
            "price": 10.99,
            "description": "A test item",
            "thumbnail": "http://example.com/test.jpg",
            "stock": 100,
            "type": "Product",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["type"] == "Product"

def test_create_item_event(test_client):
    response = test_client.post(
        "/item/",
        json={
            "name": "Test Event",
            "price": 1000,
            "description": "A test event",
            "thumbnail": "http://example.com/event.jpg",
            "stock": 100,
            "type": "Event",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Event"
    assert data["type"] == "Event"

def test_create_item_other(test_client):
    response = test_client.post(
        "/item/",
        json={
            "name": "Test other",
            "price": 3,
            "description": "A wrong item",
            "thumbnail": "http://example.com/wrong_item.jpg",
            "stock": 1,
            "type": "other",
        },
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Item type must be either 'Event' or 'Product'"

def test_create_item_and_update(test_client):
    response = test_client.post(
        "/item/",
        json={
            "name": "Test Item",
            "price": 50,
            "description": "A test item",
            "thumbnail": "http://example.com/test.jpg",
            "stock": 100,
            "type": "Product",
        },
    )
    assert response.status_code == 200
    data = response.json()
    item_id = data["id"]
    response_updated = test_client.put(
        f"/item/{item_id}",
        json={
            "name": "Test Item updated",
            "price": 5,
            "description": "A test item updated",
            "thumbnail": "http://example.com/test_updated.jpg",
            "stock": 50,
            "type": "Product",
        },
    )
    assert response_updated.status_code == 200
    data_updated = response_updated.json()
    assert data_updated["name"] == "Test Item updated"
    assert data_updated["price"] == 5
    assert data_updated["description"] == "A test item updated"
    assert data_updated["thumbnail"] == "http://example.com/test_updated.jpg"
    assert data_updated["stock"] == 50
    assert data_updated["type"] == "Product"

def test_get_single_item(test_client):
    """
    Verify fetching a single item by ID returns a 200 status code, indicating successful retrieval.
    """
    response = test_client.get("/item/1")
    assert response.status_code == 200

def test_create_cart(test_client):
    """
    Test if creating a new shopping cart successfully returns a 200 status code, indicating creation success.
    """
    response = test_client.post("/cart/")
    assert response.status_code == 200


def test_list_carts(test_client):
    """
    Ensure that listing all carts returns a 200 status code, indicating the successful retrieval of cart list.
    """
    response = test_client.get("/cart/all")
    assert response.status_code == 200

def test_read_cart(test_client):
    """
    Test reading a specific cart by ID to verify if it returns a 200 status code, indicating successful cart retrieval.
    """
    response = test_client.get("/cart/1")
    assert response.status_code == 200

def test_cart_total_calculation(test_client):
    """
    Test creating a cart, adding an item and verifying the total. The item is the item added previously
    """
    create_cart = test_client.post("/cart/")
    assert create_cart.status_code == 200
    cart = create_cart.json()
    cart_id = cart["id"]
    test_client.post(f"/cart/{cart_id}/add", json={"item_id": 1, "quantity": 1})
    response = test_client.get(f"/cart/{cart_id}")
    cart_details = response.json()
    expected_total =  10.99
    assert cart_details["total"] == expected_total


def test_cart_add_and_remove_item(test_client):
    """
    Test creating a cart, adding an item and then removing it. The item quantity should decrease by one.
    """
    create_cart = test_client.post("/cart/")
    assert create_cart.status_code == 200
    cart = create_cart.json()
    cart_id = cart["id"]
    test_client.post(f"/cart/{cart_id}/add", json={"item_id": 1, "quantity": 5})
    response = test_client.get(f"/cart/{cart_id}")
    item_to_remove = {
        "item_id": 1,
        "quantity": 1
    }
    custom_test_client = CustomTestClient(app)
    response = custom_test_client.delete_with_payload(url=f"/cart/{cart_id}/remove", json=item_to_remove)
    assert response.status_code == 200
    response_after_removal = test_client.get(f"/cart/{cart_id}")
    response_after_removal_json = response_after_removal.json()
    assert response_after_removal_json["items"][0]["quantity"] == 4