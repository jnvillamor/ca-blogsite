import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from app.database.db import Base
from app.database.mappers import user_entity_to_model
from src.domain.entities import UserEntity

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


@pytest.fixture
def create_test_user(db_session: Session) -> callable:
  def _create_test_user(
    id: str = "test-user-id", 
    first_name: str = "Test", 
    last_name: str = "User", 
    username: str = "testuser") -> UserEntity:
    
    test_user = UserEntity(
      id=id,
      first_name=first_name,
      last_name=last_name,
      username=username,
      avatar="https://example.com/avatar.png",
      password="hashedpassword",
      created_at="2024-01-01T00:00:00Z",
      updated_at="2024-01-01T00:00:00Z"
    )
    user_model = user_entity_to_model(test_user)
    db_session.add(user_model)
    db_session.commit()
    return test_user
  
  return _create_test_user