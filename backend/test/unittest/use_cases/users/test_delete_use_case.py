import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock

from src.application.use_cases.users import DeleteUserUseCase
from src.domain.entities import UserEntity
from src.domain.exceptions import NotFoundException


class TestDeleteUserUseCase:

  @pytest.fixture
  def uow(self, mocker):
    uow = mocker.MagicMock()

    uow.__aenter__ = AsyncMock(return_value=uow)
    uow.__aexit__ = AsyncMock(return_value=None)

    uow.users = mocker.Mock()
    uow.users.get_user_by_id = AsyncMock()
    uow.users.delete_user = AsyncMock()

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
      created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
      updated_at=datetime(2024, 1, 1, tzinfo=timezone.utc)
    )

  @pytest.mark.asyncio
  async def test_execute_success(self, use_case, uow, existing_user):
    user_id = "user123"

    uow.users.get_user_by_id.return_value = existing_user

    await use_case.execute(
      active_user=existing_user,
      user_id=user_id
    )

    uow.users.delete_user.assert_awaited_once_with(user_id)

  @pytest.mark.asyncio
  async def test_execute_user_not_found(self, use_case, uow):
    user_id = "nonexistent_user"

    uow.users.get_user_by_id.return_value = None

    with pytest.raises(NotFoundException) as exc_info:
      await use_case.execute(
        active_user=UserEntity(
          id="user123",
          first_name="Alice",
          last_name="Smith",
          username="alicesmith",
          password="hashedpassword",
          avatar=None,
          created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
          updated_at=datetime(2024, 1, 1, tzinfo=timezone.utc)
        ),
        user_id=user_id
      )

    assert str(exc_info.value) == "User with identifier 'user_id: nonexistent_user' was not found."

  @pytest.mark.asyncio
  async def test_execute_unauthorized(self, use_case, uow, existing_user):
    user_id = "user123"

    uow.users.get_user_by_id.return_value = existing_user

    with pytest.raises(Exception) as exc_info:
      await use_case.execute(
        active_user=UserEntity(
          id="user456",
          first_name="Bob",
          last_name="Johnson",
          username="bobjohnson",
          password="hashedpassword",
          avatar=None,
          created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
          updated_at=datetime(2024, 1, 1, tzinfo=timezone.utc)
        ),
        user_id=user_id
      )

    assert str(exc_info.value) == "You are not authorized to delete this user."