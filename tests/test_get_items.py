# Assuming this structure based on your description
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app, get_db  # Import get_db here if it's defined in main.py
from app.models import Base

# Setup test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestSessionLocal()
        yield db
    finally:
        db.close()


# Correctly override the dependency
app.dependency_overrides[get_db] = override_get_db  # Use get_db directly
client = TestClient(app)


def test_create_item():
    response = client.post(
        "/items/",
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


def test_get_single_item():
    response = client.get("/items/1")
    assert response.status_code == 200


def test_create_cart():
    response = client.post("/carts/")
    assert response.status_code == 200


def test_list_carts():
    response = client.get("/carts/")
    assert response.status_code == 200


def test_read_cart():
    response = client.get("/carts/1")
    assert response.status_code == 200
