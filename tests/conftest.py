
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import base, get_db as core_get_db
from app.routers import users as users_router


# Create an in-memory SQLite database for tests
test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


# Replace the database dependency with the test database
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[core_get_db] = override_get_db
app.dependency_overrides[users_router.get_db] = override_get_db


# Create a fresh database for each test
@pytest.fixture
def client():
    base.metadata.create_all(bind=test_engine)

    with TestClient(app) as test_client:
        yield test_client

    base.metadata.drop_all(bind=test_engine)
