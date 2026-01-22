import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from app.database.db import Base, get_db
from app.database.models import UserModel
from app.main import app

TEST_DB_URL = "sqlite:///./test_e2e.db"

EXISTING_USERS = [
  {
    "id": "user1",
    "first_name": "Alice",
    "last_name": "Smith",
    "username": "alicesmith",
    "password": "Hashed_Password!",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  },
  {
    "id": "user2",
    "first_name": "Bob",
    "last_name": "Johnson",
    "username": "bobjohnson",
    "password": "hashed_Password2@",
    "created_at": "2024-01-02T00:00:00Z",
    "updated_at": "2024-01-02T00:00:00Z"
  },
  {
    "id": "user3",
    "first_name": "Charlie",
    "last_name": "Brown",
    "username": "charliebrown",
    "password": "Hashed_password3#",      
    "created_at": "2024-01-03T00:00:00Z",
    "updated_at": "2024-01-03T00:00:00Z"
  }
]

engine = create_engine(
  TEST_DB_URL,
  connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
  autocommit=False,
  autoflush=False,
  bind=engine,
)

@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
  session = TestingSessionLocal()
  try:
    yield session
  finally:
    session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function", autouse=True)
def setup_database():
  Base.metadata.create_all(bind=engine)
  yield
  Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(db_session) -> Generator[TestClient, None, None]:
  app.dependency_overrides[get_db] = lambda: db_session
  with TestClient(app) as client:
    yield client
  app.dependency_overrides.clear()

@pytest.fixture
def create_existing_users(db_session: Session):
  payloads = EXISTING_USERS

  for payload in payloads:
    user = UserModel(**payload)
    db_session.add(user)
  db_session.commit()
