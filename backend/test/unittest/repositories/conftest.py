import pytest
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from src.domain.entities import UserEntity

@pytest.fixture
def create_user_entity(
  id: str,
  first_name: str = "John",
  last_name: str = "Doe",
  username: str = "johndoe",
  password: str = "securepassword",
  avatar=None,
  created_at=datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
  updated_at=datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
):
  return UserEntity(
    id=id,
    first_name=first_name,
    last_name=last_name,
    username=username,
    password=password,
    avatar=avatar,
    created_at=created_at,
    updated_at=updated_at
  )
