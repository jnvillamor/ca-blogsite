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
    create_test_user
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
    create_test_user
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
    create_test_user
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

  @pytest.mark.parametrize(
    "pagination, expected_count, item_count",
    [
      (PaginationDTO(skip=0, limit=10), 5, 5),
      (PaginationDTO(skip=0, limit=3), 5, 3),
      (PaginationDTO(skip=3, limit=3), 5, 2),
      (PaginationDTO(skip=0, limit=10, search="Test"), 4, 4),
      (PaginationDTO(skip=0, limit=10, search="Another"), 1, 1),
      (PaginationDTO(skip=0, limit=10, search="Non-existing"), 0, 0)
    ]
  )
  def test_get_all_users_with_pagination_and_search(
    self,
    get_user_use_case: GetUserUseCase,
    create_test_user,
    pagination: PaginationDTO,
    expected_count: int,
    item_count: int
  ):
    create_test_user()
    create_test_user(
      id="test-user-id-2", 
      first_name="Another", 
      last_name="User", 
      username="anotheruser"
    )
    create_test_user(
      id="test-user-id-3", 
      first_name="Test3", 
      last_name="User", 
      username="testuser3"
    )
    create_test_user(
      id="test-user-id-4", 
      first_name="Test4", 
      last_name="User", 
      username="testuser4"
    )
    create_test_user(
      id="test-user-id-5", 
      first_name="Test5", 
      last_name="User", 
      username="testuser5"
    )

    result: PaginationResponseDTO = get_user_use_case.get_all_users(pagination)
    
    assert result.total == expected_count
    assert len(result.items) == item_count