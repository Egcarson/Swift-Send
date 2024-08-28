# configuration settings for testing purposes
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)



@pytest.mark.parametrize("first_name, last_name, email, phone_number, city, password", [("test", "app", "test@gmail.com", "09034793278", "Lagos", "password123")])
@pytest.fixture(scope="module")
def auth_headers(client, first_name, last_name, email, phone_number, city, password):

    # Signup the user
    response = client.post("/signup", json={"first_name": first_name, "last_name": last_name, "email": email, "phone_number": phone_number, "city": city, "password": password})
    assert response.status_code == 201

    data = response.json()
    assert data["email"] == email
    assert data["first_name"] == first_name

    # Authenticate client
    login_data = {"email": email, "password": password}
    response = client.post(
        "/login",
        data=login_data,
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "Bearer"

    access_token = data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    return headers