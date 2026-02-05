import pytest
from datetime import datetime, timezone
from src.application.dto import UpdateUserDTO, UserResponseDTO
from src.application.use_cases.users import UpdateUserUseCase
from src.domain.entities import UserEntity
from src.domain.exceptions import NotFoundException, InvalidDataException

TEST_DATA = [
  (
    UpdateUserDTO(
      first_name="Alice",
    ),
    UserResponseDTO(
      id="user_id_123",
      first_name="Alice",
      last_name="Doe",
      username="johndoe",
      avatar=None,
      created_at=datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
      updated_at=datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    )
  ),
  (
    UpdateUserDTO(
      last_name="Smith",
    ),
    UserResponseDTO(
      id="user_id_123",
      first_name="John",
      last_name="Smith",
      username="johndoe",
      avatar=None,
      created_at=datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
      updated_at=datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    )
  ), 
  (
    UpdateUserDTO(
      username="johnsmith",
    ),
    UserResponseDTO(
      id="user_id_123",
      first_name="John",
      last_name="Doe",
      username="johnsmith",
      avatar=None,
      created_at=datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
      updated_at=datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    )
  ),
]

class TestUpdateUserUseCase:
  @pytest.fixture
  def uow(self, mocker):
    uow = mocker.MagicMock()
    uow.users = mocker.Mock()
    return uow
  
  @pytest.fixture
  def use_case(self, uow):
    return UpdateUserUseCase(
      unit_of_work=uow,
    )
    
  @pytest.fixture
  def valid_update_data(self):
    return UpdateUserDTO(
      first_name="John",
      last_name="Smith",
      username="johnsmith",
      avatar=None
    )
  
  @pytest.fixture
  def existing_user(self):
    return UserEntity(
      id="user_id_123",
      first_name="John",
      last_name="Doe",
      username="johndoe",
      password="hashed_password",
      avatar=None,
      created_at=datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
      updated_at=datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    )
    
  @pytest.mark.parametrize(
    "update_data, expected_result",
    TEST_DATA
  )
  def test_execute_success(
    self, 
    use_case, 
    uow,
    existing_user,
    update_data,
    expected_result
  ):
    # Arrange
    uow.users.get_user_by_id.return_value = existing_user
    uow.users.get_user_by_username.return_value = None
    
    uow.users.update_user.side_effect = lambda user_id, user: existing_user
    
    # Act
    result = use_case.execute(
      user_id="user_id_123",
      data=update_data
    )
    
    # Assert
    uow.users.get_user_by_id.assert_called_once_with("user_id_123")
    
    uow.users.update_user.assert_called_once()
    
    assert result.id == expected_result.id
    assert result.first_name == expected_result.first_name
    assert result.last_name == expected_result.last_name
    assert result.username == expected_result.username
    assert result.avatar == expected_result.avatar
    assert result.created_at == expected_result.created_at
    assert result.updated_at != expected_result.updated_at  # updated_at should be updated
  
  def test_execute_user_not_found(
    self, 
    use_case, 
    uow,
    valid_update_data
  ):
    # Arrange
    uow.users.get_user_by_id.return_value = None
    uow.users.get_user_by_username.return_value = None
    
    # Act & Assert
    with pytest.raises(NotFoundException) as exc_info:
      use_case.execute(
        user_id="non_existent_user_id",
        data=valid_update_data
      )
    
    assert str(exc_info.value) == "User with identifier 'user_id: non_existent_user_id' was not found."
    uow.users.get_user_by_id.assert_called_once_with("non_existent_user_id")
  
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
  def test_execute_invalid_names(
    self,
    use_case,
    uow,
    existing_user,
    field,
    invalid_value,
    error_regex
  ):
    # Arrange
    uow.users.get_user_by_id.return_value = existing_user
    uow.users.get_user_by_username.return_value = None
    update_data = UpdateUserDTO(**{field: invalid_value})
    
    # Act & Assert
    with pytest.raises(Exception, match=error_regex) as exc_info:
      use_case.execute(
        user_id="user_id_123",
        data=update_data
      )
    
    uow.users.get_user_by_id.assert_called_once_with("user_id_123")
  
  def test_execute_no_fields_to_update(
    self,
    use_case,
    uow,
    existing_user
  ):
    # Arrange
    uow.users.get_user_by_id.return_value = existing_user
    uow.users.get_user_by_username.return_value = None
    update_data = UpdateUserDTO()  # No fields set
    
    uow.users.update_user.side_effect = lambda user_id, user: existing_user
    
    # Act
    result = use_case.execute(
      user_id="user_id_123",
      data=update_data
    )
    
    # Assert
    uow.users.get_user_by_id.assert_called_once_with("user_id_123")
    uow.users.update_user.assert_called_once()
    
    assert result.id == existing_user.id
    assert result.first_name == existing_user.first_name
    assert result.last_name == existing_user.last_name
    assert result.username == existing_user.username
    assert result.avatar == existing_user.avatar
    assert result.created_at == existing_user.created_at
    assert result.updated_at == existing_user.updated_at  # updated_at should remain unchanged 
  
  def test_execute_duplicate_username(
    self,
    use_case,
    uow,
    existing_user
  ):
    # Arrange
    uow.users.get_user_by_id.return_value = existing_user
    uow.users.get_user_by_username.return_value = UserEntity(
      id="another_user_id",
      first_name="Jane",
      last_name="Doe",
      username="existingusername",
      password="hashed_password",
      avatar=None,
      created_at=datetime(2024, 1, 2, 0, 0, 0, tzinfo=timezone.utc),
      updated_at=datetime(2024, 1, 2, 0, 0, 0, tzinfo=timezone.utc)
    )
    
    update_data = UpdateUserDTO(username="existingusername")
    
    # Act & Assert
    with pytest.raises(InvalidDataException) as exc_info:
      use_case.execute(
        user_id="user_id_123",
        data=update_data
      )
    
    assert str(exc_info.value) == "The username 'existingusername' is already taken."
    uow.users.get_user_by_id.assert_called_once_with("user_id_123")
    uow.users.get_user_by_username.assert_called_once_with("existingusername")