import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock

from src.application.dto import CreateUserDTO, UserResponseDTO
from src.application.use_cases.users import CreateUserUseCase
from src.domain.exceptions import UsernameExistsException, InvalidDataException


class TestCreateUserUseCase:

  @pytest.fixture
  def uow(self, mocker):
    uow = mocker.MagicMock()

    uow.__aenter__ = AsyncMock(return_value=uow)
    uow.__aexit__ = AsyncMock(return_value=None)

    uow.users = mocker.Mock()
    uow.users.get_user_by_username = AsyncMock()
    uow.users.create_user = AsyncMock()

    return uow

  @pytest.fixture
  def password_hasher(self, mocker):
    return mocker.Mock()

  @pytest.fixture
  def id_generator(self, mocker):
    return mocker.Mock()

  @pytest.fixture
  def use_case(self, uow, password_hasher, id_generator):
    return CreateUserUseCase(
      unit_of_work=uow,
      password_hasher=password_hasher,
      id_generator=id_generator
    )

  @pytest.fixture
  def valid_user_data(self):
    return CreateUserDTO(
      first_name="John",
      last_name="Doe",
      username="johndoe",
      password="SecurePass123!",
      avatar=None
    )

  @pytest.fixture
  def existing_user_data(self):
    return UserResponseDTO(
      id="existing_id",
      first_name="Jane",
      last_name="Doe",
      username="johndoe",
      avatar=None,
      created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
      updated_at=datetime(2024, 1, 1, tzinfo=timezone.utc)
    )

  @pytest.mark.asyncio
  async def test_execute_success(
    self,
    use_case,
    uow,
    password_hasher,
    id_generator,
    valid_user_data
  ):
    uow.users.get_user_by_username.return_value = None
    password_hasher.hash.return_value = "hashed_password"
    id_generator.generate.return_value = "id123"

    uow.users.create_user.side_effect = lambda user: user

    result = await use_case.execute(valid_user_data)

    uow.users.get_user_by_username.assert_awaited_once_with("johndoe")
    uow.users.create_user.assert_awaited_once()
    password_hasher.hash.assert_called_once_with("SecurePass123!")
    id_generator.generate.assert_called_once()

    assert result.first_name == "John"
    assert result.last_name == "Doe"
    assert result.username == "johndoe"
    assert result.id == "id123"

  @pytest.mark.asyncio
  async def test_execute_username_exists(
    self,
    use_case,
    uow,
    valid_user_data,
    existing_user_data
  ):
    uow.users.get_user_by_username.return_value = existing_user_data

    with pytest.raises(
      UsernameExistsException,
      match=f"The username '{valid_user_data.username}' is already taken."
    ):
      await use_case.execute(valid_user_data)

    uow.users.get_user_by_username.assert_awaited_once_with("johndoe")

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
  async def test_execute_invalid_password(
    self,
    use_case,
    uow,
    valid_user_data,
    password,
    error_regex
  ):
    uow.users.get_user_by_username.return_value = None
    valid_user_data.password = password

    with pytest.raises(InvalidDataException, match=error_regex):
      await use_case.execute(valid_user_data)

    uow.users.get_user_by_username.assert_awaited_once_with("johndoe")

  @pytest.mark.asyncio
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
  async def test_execute_invalid_names(
    self,
    use_case,
    uow,
    valid_user_data,
    field,
    invalid_value,
    error_regex
  ):
    uow.users.get_user_by_username.return_value = None
    setattr(valid_user_data, field, invalid_value)

    with pytest.raises(InvalidDataException, match=error_regex):
      await use_case.execute(valid_user_data)

    if field == "username":
      uow.users.get_user_by_username.assert_awaited_once_with(invalid_value)
    else:
      uow.users.get_user_by_username.assert_awaited_once_with(valid_user_data.username)