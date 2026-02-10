import pytest
from datetime import datetime, timezone
from src.application.dto import PaginationDTO, PaginationResponseDTO, UserResponseDTO
from src.application.use_cases.users import GetUserUseCase
from src.application.repositories import IUserRepository
from src.domain.entities import UserEntity

class TestGetUserUseCase:
  @pytest.fixture
  def user_repository(self, mocker):
    user_repository = mocker.Mock()
    return user_repository
  
  @pytest.fixture
  def use_case(self, user_repository) -> GetUserUseCase:
    return GetUserUseCase(user_repository=user_repository)
  
  @pytest.fixture
  def valid_user_data(self) -> UserEntity:
    return UserEntity(
      id='123',
      first_name='John',
      last_name='Doe',
      username='johndoe',
      password='hashedpassword',
      avatar='',
      created_at=datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
      updated_at=datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    )
  
  @pytest.fixture
  def valid_users_list(self) -> list[UserEntity]:
    return [
      UserEntity(
        id='123',
        first_name='John',
        last_name='Doe',
        username='johndoe',
        password='hashedpassword',
        avatar='',
        created_at=datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        updated_at=datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
      ),
      UserEntity(
        id='124',
        first_name='Jane',
        last_name='Smith',
        username='janesmith',
        password='hashedpassword2',
        avatar='',
        created_at=datetime(2024, 1, 2, 0, 0, 0, tzinfo=timezone.utc),
        updated_at=datetime(2024, 1, 2, 0, 0, 0, tzinfo=timezone.utc)
      )
    ]
    
  def test_get_by_id_success(
    self, 
    use_case, 
    user_repository, 
    valid_user_data
  ):
    # Arrange
    user_repository.get_user_by_id.return_value = valid_user_data
    
    # Act
    result = use_case.get_by_id('123')

    # Assert
    assert result == UserResponseDTO.model_validate(valid_user_data.to_dict())
    user_repository.get_user_by_id.assert_called_once_with('123')
    
  def test_get_by_id_not_found(
    self, 
    use_case, 
    user_repository
  ):
    # Arrange
    user_repository.get_user_by_id.return_value = None
    
    # Act
    result = use_case.get_by_id('999')

    # Assert
    assert result is None
    user_repository.get_user_by_id.assert_called_once_with('999')
    
  def test_get_by_username_success(
    self,
    use_case,
    user_repository,
    valid_user_data
  ):
    # Arrange
    user_repository.get_user_by_username.return_value = valid_user_data

    # Act
    result = use_case.get_by_username('johndoe')
    
    # Assert
    assert result == UserResponseDTO.model_validate(valid_user_data.to_dict())
    user_repository.get_user_by_username.assert_called_once_with('johndoe')
  
  def test_by_username_not_found(
    self,
    use_case,
    user_repository
  ):
    # Arrange
    user_repository.get_user_by_username.return_value = None

    # Act
    result = use_case.get_by_username('unknownuser')
    
    # Assert
    assert result is None
    user_repository.get_user_by_username.assert_called_once_with('unknownuser')
  
  def test_get_all_users(
    self,
    use_case,
    user_repository,
    valid_users_list
  ):
    # Arrange
    pagination = PaginationDTO(skip=0, limit=10, search=None)
    user_repository.get_all_users.return_value = (valid_users_list, len(valid_users_list))
    
    # Act
    result = use_case.get_all_users(pagination)
    
    # Assert
    expected_dtos = [UserResponseDTO.model_validate(user.to_dict()) for user in valid_users_list]
    assert result == PaginationResponseDTO(
      total=len(valid_users_list),
      skip=pagination.skip,
      limit=pagination.limit,
      items=expected_dtos
    )
    user_repository.get_all_users.assert_called_once_with(
      skip=pagination.skip,
      limit=pagination.limit,
      search=pagination.search
    )
  
  def test_get_all_users_with_search(
    self,
    use_case,
    user_repository,
    valid_users_list
  ):
    # Arrange
    pagination = PaginationDTO(skip=0, limit=10, search='john')
    filtered_users = [user for user in valid_users_list if 'john' in user.username]
    user_repository.get_all_users.return_value = (filtered_users, len(filtered_users))
    
    # Act
    result = use_case.get_all_users(pagination)
    
    # Assert
    expected_dtos = [UserResponseDTO.model_validate(user.to_dict()) for user in filtered_users]
    assert result == PaginationResponseDTO(
      total=len(filtered_users),
      skip=pagination.skip,
      limit=pagination.limit,
      items=expected_dtos
    )
    user_repository.get_all_users.assert_called_once_with(
      skip=pagination.skip,
      limit=pagination.limit,
      search=pagination.search
    )