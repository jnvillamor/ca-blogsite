import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock

from src.application.dto import ChangePasswordDTO, UserResponseDTO
from src.application.use_cases.users import ChangePasswordUseCase
from src.domain.entities import UserEntity
from src.domain.exceptions import NotFoundException, InvalidDataException, UnauthorizedException


@pytest.fixture
def create_existing_user():
  return UserEntity(
    id="user1",
    first_name="John",
    last_name="Doe",
    username="johndoe",
    avatar=None,
    password="oldpass",
    created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
    updated_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
  )


@pytest.fixture
def unit_of_work(mocker):
  uow = mocker.MagicMock()

  uow.__aenter__ = AsyncMock(return_value=uow)
  uow.__aexit__ = AsyncMock(return_value=None)

  uow.users = mocker.Mock()
  uow.users.get_user_by_id = AsyncMock()
  uow.users.update_user = AsyncMock()

  return uow


@pytest.fixture
def password_hasher(mocker):
  return mocker.MagicMock()


@pytest.fixture
def use_case(unit_of_work, password_hasher):
  return ChangePasswordUseCase(
    unit_of_work=unit_of_work,
    password_hasher=password_hasher
  )


class TestChangePasswordUseCase:

  @pytest.mark.asyncio
  async def test_execute_success(
    self,
    use_case,
    unit_of_work,
    password_hasher,
    create_existing_user
  ):
    user = create_existing_user

    unit_of_work.users.get_user_by_id.return_value = user
    password_hasher.verify.return_value = True
    password_hasher.hash.return_value = "hashed_new_password"

    original_password = user.password

    payload = ChangePasswordDTO(
      old_password=original_password,
      new_password="SecurePass.123",
      confirm_new_password="SecurePass.123"
    )

    unit_of_work.users.update_user.side_effect = lambda user_id, user: user

    result = await use_case.execute(
      active_user=user,
      user_id="user1",
      data=payload
    )

    unit_of_work.users.get_user_by_id.assert_awaited_once_with("user1")
    password_hasher.verify.assert_called_once_with(payload.old_password, original_password)
    password_hasher.hash.assert_called_once_with(payload.new_password)
    unit_of_work.users.update_user.assert_awaited_once()

    assert isinstance(result, UserResponseDTO)

    for field in user.to_dict():
      if field not in ["password", "access_token_id", "refresh_token_id"]:
        assert getattr(result, field) == getattr(user, field)

    assert user.password == "hashed_new_password"


  @pytest.mark.asyncio
  async def test_execute_user_not_found(
    self,
    use_case,
    create_existing_user,
    unit_of_work
  ):
    user = create_existing_user
    unit_of_work.users.get_user_by_id.return_value = None

    payload = ChangePasswordDTO(
      old_password="any_old_pass",
      new_password="SecurePass.123",
      confirm_new_password="SecurePass.123"
    )

    user_id = "non_existent_user"

    with pytest.raises(NotFoundException) as exc_info:
      await use_case.execute(
        active_user=user,
        user_id=user_id,
        data=payload
      )

    assert f"User with identifier 'user_id: {user_id}' was not found" in str(exc_info.value)


  @pytest.mark.asyncio
  async def test_execute_incorrect_old_password(
    self,
    use_case,
    unit_of_work,
    password_hasher,
    create_existing_user
  ):
    user = create_existing_user

    unit_of_work.users.get_user_by_id.return_value = user
    password_hasher.verify.return_value = False

    payload = ChangePasswordDTO(
      old_password="wrong_old_pass",
      new_password="SecurePass.123",
      confirm_new_password="SecurePass.123"
    )

    with pytest.raises(InvalidDataException) as exc_info:
      await use_case.execute(
        active_user=user,
        user_id="user1",
        data=payload
      )

    assert "Old password is incorrect." in str(exc_info.value)

    password_hasher.verify.assert_called_once_with(
      payload.old_password,
      user.password
    )


  @pytest.mark.asyncio
  async def test_execute_mismatched_new_passwords(
    self,
    use_case,
    unit_of_work,
    create_existing_user
  ):
    user = create_existing_user
    unit_of_work.users.get_user_by_id.return_value = user

    payload = ChangePasswordDTO(
      old_password="oldpass",
      new_password="SecurePass.123",
      confirm_new_password="DifferentPass.456"
    )

    with pytest.raises(InvalidDataException) as exc_info:
      await use_case.execute(
        active_user=user,
        user_id="user1",
        data=payload
      )

    assert "New password and confirmation do not match." in str(exc_info.value)


  @pytest.mark.asyncio
  @pytest.mark.parametrize(
    "password, error_regex",
    [
      ("", r"Password cannot be empty"),
      ("short", r"at least 8 characters"),
      ("NoDigits!", r"at least one digit"),
      ("nouppercase1!", r"at least one uppercase"),
      ("NOLOWERCASE1!", r"at least one lowercase"),
      ("NoSpecial1", r"at least one special character"),
    ]
  )
  async def test_invalid_new_password(
    self,
    use_case,
    unit_of_work,
    password_hasher,
    create_existing_user,
    password,
    error_regex
  ):
    user = create_existing_user

    unit_of_work.users.get_user_by_id.return_value = user
    password_hasher.verify.return_value = True

    payload = ChangePasswordDTO(
      old_password="oldpass",
      new_password=password,
      confirm_new_password=password
    )

    with pytest.raises(InvalidDataException, match=error_regex):
      await use_case.execute(
        active_user=user,
        user_id="user1",
        data=payload
      )

    password_hasher.verify.assert_called_once_with(
      payload.old_password,
      user.password
    )


  @pytest.mark.asyncio
  async def test_execute_unauthorized_user(
    self,
    use_case,
    unit_of_work,
    create_existing_user
  ):
    user = create_existing_user
    unit_of_work.users.get_user_by_id.return_value = user

    payload = ChangePasswordDTO(
      old_password="oldpass",
      new_password="SecurePass.123",
      confirm_new_password="SecurePass.123"
    )

    with pytest.raises(UnauthorizedException) as exc_info:
      await use_case.execute(
        active_user=UserEntity(
          id="other_user",
          first_name="Jane",
          last_name="Smith",
          username="janesmith",
          avatar=None,
          password="otherpass",
          created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
          updated_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
        ),
        user_id="user1",
        data=payload
      )

    assert "You are not authorized to change the password for this user." in str(exc_info.value)