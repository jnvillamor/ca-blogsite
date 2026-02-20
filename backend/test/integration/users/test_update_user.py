import pytest
from sqlalchemy.orm import Session
from typing import Callable
from app.database.unit_of_work import UnitOfWork
from src.application.dto import UpdateUserDTO
from src.application.use_cases.users import UpdateUserUseCase
from src.domain.entities import UserEntity

@pytest.fixture
def update_user_use_case(db_session: Session) -> UpdateUserUseCase:
  unit_of_work = UnitOfWork(db_session)
  return UpdateUserUseCase(
    unit_of_work=unit_of_work,
  )

class TestUpdateUserUseCase:
  def test_update_user_success(
    self,
    update_user_use_case: UpdateUserUseCase,
    create_test_user: Callable[..., UserEntity]
  ):
    test_user: UserEntity = create_test_user()
    
    update_dto = UpdateUserDTO(
      first_name="Updated",
      last_name="Name",
      username="updatedusername"
    )
    
    updated_user = update_user_use_case.execute(
      active_user=test_user,
      user_id = test_user.id,
      data=update_dto
    )
    
    assert updated_user.first_name == "Updated"
    assert updated_user.last_name == "Name"
    assert updated_user.username == "updatedusername"
  
  def test_update_user_non_existing(
      self, 
      update_user_use_case: UpdateUserUseCase,
      create_test_user: Callable[..., UserEntity]
    ):
    update_dto = UpdateUserDTO(
      first_name="Non",
      last_name="Existent",
      username="nonexistentuser"
    )

    test_user = create_test_user()
    
    with pytest.raises(Exception) as exc_info:
      update_user_use_case.execute(
        active_user=test_user,
        user_id = "non-existing-id",
        data=update_dto
      )
    
    assert "User with identifier 'user_id: non-existing-id' was not found." in str(exc_info.value)
  
  @pytest.mark.parametrize(
    "field, invalid_value, error_regex",
    [
      ("first_name", "", r"First Name cannot be empty"),
      ("first_name", "J", r"First Name must be at least \d+ characters long"),
      ("first_name", "J" * 31, r"First Name cannot exceed \d+ characters"),

      ("last_name", "", r"Last Name cannot be empty"),
      ("last_name", "D", r"Last Name must be at least \d+ characters long"),
      ("last_name", "D" * 31, r"Last Name cannot exceed \d+ characters"),

      ("username", "", r"Username cannot be empty"),
      ("username", "ab", r"Username must be at least \d+ characters long"),
      ("username", "a" * 21, r"Username cannot exceed \d+ characters"),
    ]
  )
  def test_update_user_invalid_names(
    self,
    update_user_use_case: UpdateUserUseCase,
    create_test_user: Callable[..., UserEntity],
    field: str,
    invalid_value: str,
    error_regex: str
  ):
    test_user: UserEntity = create_test_user()
    update_data = UpdateUserDTO(**{field: invalid_value})
    
    with pytest.raises(Exception, match=error_regex) as exc_info:
      update_user_use_case.execute(
        active_user=test_user,
        user_id = test_user.id,
        data=update_data
      )

  def test_update_user_duplicate_username(
    self,
    update_user_use_case: UpdateUserUseCase,
    create_test_user: Callable[..., UserEntity]
  ):
    user1: UserEntity = create_test_user(
      id="user1",
      username="uniqueusername1"
    )
    user2: UserEntity = create_test_user(
      id="user2",
      username="uniqueusername2"
    )
    
    update_dto = UpdateUserDTO(
      username="uniqueusername1"
    )
    
    with pytest.raises(Exception) as exc_info:
      update_user_use_case.execute(
        active_user=user2,
        user_id = user2.id,
        data=update_dto
      )
    
    assert "The username 'uniqueusername1' is already taken." in str(exc_info.value)
  
  def test_update_user_unauthorized(
    self,
    update_user_use_case: UpdateUserUseCase,
    create_test_user: Callable[..., UserEntity]
  ):
    existing_user: UserEntity = create_test_user()
    other_user = create_test_user(
      id="other_user_id",
      username="otheruser"
    )
    valid_update_data = UpdateUserDTO(
      first_name="Valid",
      last_name="Update",
      username="validupdateusername"
    )
    
     # Act & Assert for unauthorized user
    with pytest.raises(Exception) as exc_info:
      update_user_use_case.execute(
        active_user=other_user,
        user_id=existing_user.id,
        data=valid_update_data
      )
    
    assert str(exc_info.value) == "You are not authorized to update this user."
