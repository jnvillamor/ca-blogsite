import pytest
from src.application.use_cases.users import GetUserUseCase
from src.application.dto import PaginationDTO
from src.domain.entities import UserEntity
from app.repositories import UserRepository
from app.database.mappers import user_entity_to_model

@pytest.fixture
def get_user_use_case(db_session):
  user_repository = UserRepository(db_session)
  return GetUserUseCase(user_repository)
  
@pytest.fixture
def create_test_user(db_session):
  from app.database.models import UserModel
  
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

class TestGetUserUseCase:
  def test_get_by_id_existing_user(self, get_user_use_case, create_test_user):
    test_user = create_test_user()
    
    result = get_user_use_case.get_by_id(test_user.id)
    
    assert result is not None
    assert result.id == test_user.id
    assert result.username == test_user.username

  def test_get_by_id_non_existing_user(self, get_user_use_case):
    result = get_user_use_case.get_by_id("non-existing-id")
    
    assert result is None

  def test_get_by_username_existing_user(self, get_user_use_case, create_test_user):
    test_user = create_test_user()
    
    result = get_user_use_case.get_by_username(test_user.username)
    
    assert result is not None
    assert result.id == test_user.id
    assert result.username == test_user.username

  def test_get_by_username_non_existing_user(self, get_user_use_case):
    result = get_user_use_case.get_by_username("nonexistingusername")
    
    assert result is None

  def test_get_all_users(self, get_user_use_case, create_test_user):
    test_user1 = create_test_user()
    test_user2 = create_test_user(
      id="test-user-id-2", 
      first_name="Another", 
      last_name="User", 
      username="anotheruser"
    )
    
    pagination = PaginationDTO(skip=0, limit=10, search="")
    users, count = get_user_use_case.get_all_users(pagination)
    
    assert count >= 2
    assert any(user.id == test_user1.id for user in users)
    assert any(user.id == test_user2.id for user in users)
