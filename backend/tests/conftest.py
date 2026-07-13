import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import SessionLocal


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
async def db_session():
    """
    Fixture yielding an active, isolated database session.
    """
    async with SessionLocal() as session:
        yield session
