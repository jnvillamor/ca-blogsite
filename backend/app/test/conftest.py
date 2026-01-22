import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from app.database.db import Base

TEST_DB_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
  engine = create_engine(
    TEST_DB_URL,
    connect_args={"check_same_thread": False},
  )

  TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
  )

  Base.metadata.create_all(bind=engine)

  session = TestingSessionLocal()
  try:
    yield session
  finally:
    session.close()
    Base.metadata.drop_all(bind=engine)