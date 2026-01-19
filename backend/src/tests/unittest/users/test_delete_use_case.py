import pytest
from pytest_mock import mocker
from src.application.use_cases.users import DeleteUserUseCase
from src.domain.entities import UserEntity
from src.domain.exceptions import NotFoundException

class TestDeleteUserUseCase:
  @pytest.fixture
  def uow(self, mocker):
    uow = mocker.MagicMock()
    uow.users = mocker.Mock()
    return uow
  
  @pytest.fixture
  def use_case(self, uow):
    return DeleteUserUseCase(unit_of_work=uow)
  
  @pytest.fixture
  def existing_user(self):
    return UserEntity(
      id="user123",
      first_name="Alice",
      last_name="Smith",
      username="alicesmith",
      password="hashedpassword",
      avatar=None,
      created_at="2024-01-01T00:00:00Z",
      updated_at="2024-01-01T00:00:00Z"
    )
  
  def test_execute_success(self, use_case, uow, existing_user):
    # Arrange
    user_id = "user123"
    uow.users.get_user_by_id.return_value = existing_user
    
    # Act
    use_case.execute(user_id)
    
    # Assert
    uow.users.delete_user.assert_called_once_with(user_id)
  
  def test_execute_user_not_found(self, use_case, uow):
    # Arrange
    user_id = "nonexistent_user"
    uow.users.get_user_by_id.return_value = None
    
    # Act & Assert
    with pytest.raises(NotFoundException) as exc_info:
      use_case.execute(user_id)
    
    assert str(exc_info.value) == "User with identifier 'user_id: nonexistent_user' was not found."