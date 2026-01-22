import pytest
from sqlalchemy.orm import Session
from app.repositories import UserRepository
from src.application.use_cases.users import GetUserUseCase
from src.application.dto import PaginationDTO, PaginationResponseDTO
from src.domain.entities import UserEntity

@pytest.fixture
def get_user_use_case(db_session: Session) -> GetUserUseCase:
  user_repository = UserRepository(db_session)
  return GetUserUseCase(user_repository)
  
class TestGetUserUseCase:
  def test_get_by_id_existing_user(
    self, 
    get_user_use_case: GetUserUseCase, 
    create_test_user: callable
  ):
    test_user: UserEntity = create_test_user()
    
    result = get_user_use_case.get_by_id(test_user.id)
    
    assert result is not None
    assert result.id == test_user.id
    assert result.username == test_user.username

  def test_get_by_id_non_existing_user(
    self, 
    get_user_use_case: GetUserUseCase
  ):
    result = get_user_use_case.get_by_id("non-existing-id")
    
    assert result is None

  def test_get_by_username_existing_user(
    self,
    get_user_use_case: GetUserUseCase,
    create_test_user: callable
  ):
    test_user: UserEntity = create_test_user()
    
    result = get_user_use_case.get_by_username(test_user.username)
    
    assert result is not None
    assert result.id == test_user.id
    assert result.username == test_user.username

  def test_get_by_username_non_existing_user(
    self,
    get_user_use_case: GetUserUseCase
  ):
    result = get_user_use_case.get_by_username("nonexistingusername")
    
    assert result is None

  def test_get_all_users(
    self, 
    get_user_use_case: GetUserUseCase, 
    create_test_user: callable
  ):
    test_user1: UserEntity = create_test_user()
    test_user2: UserEntity = create_test_user(
      id="test-user-id-2", 
      first_name="Another", 
      last_name="User", 
      username="anotheruser"
    )
    
    pagination = PaginationDTO(skip=0, limit=10, search="")
    result = get_user_use_case.get_all_users(pagination)
    
    assert result.total >= 2
    assert any(user.id == test_user1.id for user in result.items)
    assert any(user.id == test_user2.id for user in result.items)
