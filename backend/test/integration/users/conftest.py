import pytest
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.database.mappers import user_entity_to_model
from app.services import PasswordHasher
from src.domain.entities import UserEntity

@pytest.fixture
def create_test_user(db_session: Session):
  def _create_test_user(
    id: str = "test-user-id", 
    first_name: str = "Test", 
    last_name: str = "User", 
    username: str = "testuser") -> UserEntity:
    
    hashed_password = PasswordHasher().hash("Password123!")

    test_user = UserEntity(
      id=id,
      first_name=first_name,
      last_name=last_name,
      username=username,
      avatar="https://example.com/avatar.png",
      password=hashed_password,
      created_at=datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
      updated_at=datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    )
    user_model = user_entity_to_model(test_user)
    db_session.add(user_model)
    db_session.commit()
    return test_user
  
  return _create_test_user