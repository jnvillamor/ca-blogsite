import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock

from src.application.dto import UpdateUserDTO, UserResponseDTO
from src.application.use_cases.users import UpdateUserUseCase
from src.domain.entities import UserEntity
from src.domain.exceptions import (
  NotFoundException,
  InvalidDataException,
  UnauthorizedException
)

TEST_DATA = [
  (
    UpdateUserDTO(first_name="Alice"),
    UserResponseDTO(
      id="user_id_123",
      first_name="Alice",
      last_name="Doe",
      username="johndoe",
      avatar=None,
      created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
      updated_at=datetime(2024, 1, 1, tzinfo=timezone.utc)
    )
  ),
  (
    UpdateUserDTO(last_name="Smith"),
    UserResponseDTO(
      id="user_id_123",
      first_name="John",
      last_name="Smith",
      username="johndoe",
      avatar=None,
      created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
      updated_at=datetime(2024, 1, 1, tzinfo=timezone.utc)
    )
  ),
  (
    UpdateUserDTO(username="johnsmith"),
    UserResponseDTO(
      id="user_id_123",
      first_name="John",
      last_name="Doe",
      username="johnsmith",
      avatar=None,
      created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
      updated_at=datetime(2024, 1, 1, tzinfo=timezone.utc)
    )
  )
]


class TestUpdateUserUseCase:

  @pytest.fixture
  def uow(self, mocker):
    uow = mocker.MagicMock()

    uow.__aenter__ = AsyncMock(return_value=uow)
    uow.__aexit__ = AsyncMock(return_value=None)

    uow.users = mocker.Mock()

    uow.users.get_user_by_id = AsyncMock()
    uow.users.get_user_by_username = AsyncMock()
    uow.users.update_user = AsyncMock()

    return uow

  @pytest.fixture
  def use_case(self, uow):
    return UpdateUserUseCase(unit_of_work=uow)

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
      created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
      updated_at=datetime(2024, 1, 1, tzinfo=timezone.utc)
    )

  @pytest.mark.asyncio
  @pytest.mark.parametrize("update_data, expected_result", TEST_DATA)
  async def test_execute_success(
    self,
    use_case,
    uow,
    existing_user,
    update_data,
    expected_result
  ):
    uow.users.get_user_by_id.return_value = existing_user
    uow.users.get_user_by_username.return_value = None
    uow.users.update_user.return_value = existing_user

    result = await use_case.execute(
      active_user=existing_user,
      user_id="user_id_123",
      data=update_data
    )

    uow.users.get_user_by_id.assert_awaited_once_with("user_id_123")
    uow.users.update_user.assert_awaited_once()

    assert result.id == expected_result.id
    assert result.first_name == expected_result.first_name
    assert result.last_name == expected_result.last_name
    assert result.username == expected_result.username
    assert result.avatar == expected_result.avatar
    assert result.created_at == expected_result.created_at
    assert result.updated_at != expected_result.updated_at

  @pytest.mark.asyncio
  async def test_execute_user_not_found(
    self,
    use_case,
    uow,
    existing_user,
    valid_update_data
  ):
    uow.users.get_user_by_id.return_value = None

    with pytest.raises(NotFoundException):
      await use_case.execute(
        active_user=existing_user,
        user_id="non_existent_user_id",
        data=valid_update_data
      )

    uow.users.get_user_by_id.assert_awaited_once_with("non_existent_user_id")

  @pytest.mark.asyncio
  async def test_execute_duplicate_username(
    self,
    use_case,
    uow,
    existing_user
  ):
    uow.users.get_user_by_id.return_value = existing_user

    uow.users.get_user_by_username.return_value = UserEntity(
      id="another_user_id",
      first_name="Jane",
      last_name="Doe",
      username="existingusername",
      password="hashed_password",
      avatar=None,
      created_at=datetime(2024, 1, 2, tzinfo=timezone.utc),
      updated_at=datetime(2024, 1, 2, tzinfo=timezone.utc)
    )

    update_data = UpdateUserDTO(username="existingusername")

    with pytest.raises(InvalidDataException):
      await use_case.execute(
        active_user=existing_user,
        user_id="user_id_123",
        data=update_data
      )

    uow.users.get_user_by_id.assert_awaited_once_with("user_id_123")
    uow.users.get_user_by_username.assert_awaited_once_with("existingusername")

  @pytest.mark.asyncio
  async def test_execute_unauthorized(
    self,
    use_case,
    existing_user,
    uow,
    valid_update_data
  ):
    uow.users.get_user_by_id.return_value = existing_user
    uow.users.get_user_by_username.return_value = None

    with pytest.raises(UnauthorizedException):
      await use_case.execute(
        active_user=UserEntity(
          id="different_user_id",
          first_name="Jane",
          last_name="Doe",
          username="janedoe",
          password="hashed_password",
          avatar=None,
          created_at=datetime(2024, 1, 2, tzinfo=timezone.utc),
          updated_at=datetime(2024, 1, 2, tzinfo=timezone.utc)
        ),
        user_id="user_id_123",
        data=valid_update_data
      )