import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from app.database.db import Base

TEST_DB_URL = "sqlite:///:memory:"

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
