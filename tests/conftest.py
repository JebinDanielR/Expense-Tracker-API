import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from fastapi.testclient import TestClient

from app.main import app
from app.database import Base, get_db


SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={
        "check_same_thread": False
    },
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base.metadata.create_all(
    bind=engine
)

def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture
def category():

    response = client.post(
        "/categories",
        json={
            "name":"Transport"
        }
    )

    # print("STATUS:", response.status_code)
    # print("BODY:", response.json())

    return response.json()

@pytest.fixture(autouse=True)
def clean_database():

    yield

    db = TestingSessionLocal()

    for table in reversed(Base.metadata.sorted_tables):
        db.execute(table.delete())

    db.commit()
    db.close()