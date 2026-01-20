import pytest
from app.database.db import Base
from app.database.unit_of_work import UnitOfWork
from app.services import PasswordHasher, UuidGenerator
from src.application.dto import CreateUserDTO
from src.application.use_cases.users import CreateUserUseCase

class TestCreateUserUseCase:
  def test_create_user_success(self, db_session):
    unit_of_work = UnitOfWork(db_session)
    use_case = CreateUserUseCase(
      unit_of_work=unit_of_work,
      password_hasher=PasswordHasher(),
      id_generator=UuidGenerator()
    )

    user_data = CreateUserDTO(
      first_name="Alice",
      last_name="Smith",
      username="alicesmith",
      password="Password123!",
      avatar=None
    )

    created_user = use_case.execute(user_data)
    
    assert created_user.id is not None
    assert created_user.first_name == "Alice"
    assert created_user.last_name == "Smith"
    assert created_user.username == "alicesmith"
    assert created_user.avatar is None
    assert created_user.created_at is not None
    assert created_user.updated_at is not None
  
  def test_create_user_duplicate_username(self, db_session):
    unit_of_work = UnitOfWork(db_session)
    use_case = CreateUserUseCase(
      unit_of_work=unit_of_work,
      password_hasher=PasswordHasher(),
      id_generator=UuidGenerator()
    )

    user_data = CreateUserDTO(
      first_name="Bob",
      last_name="Johnson",
      username="bobjohnson",
      password="Password123!",
      avatar=None
    )

    # Create the first user
    use_case.execute(user_data)

    # Attempt to create a second user with the same username
    with pytest.raises(Exception) as exc_info:
      use_case.execute(user_data)
    
    assert f"The username '{user_data.username}' is already taken" in str(exc_info.value)
  
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
  def test_create_user_invalid_password(self, db_session, password, error_regex):
    unit_of_work = UnitOfWork(db_session)
    use_case = CreateUserUseCase(
      unit_of_work=unit_of_work,
      password_hasher=PasswordHasher(),
      id_generator=UuidGenerator()
    )

    user_data = CreateUserDTO(
      first_name="Charlie",
      last_name="Brown",
      username="charliebrown",
      password=password,
      avatar=None
    )

    with pytest.raises(Exception, match=error_regex) as exc_info:
      use_case.execute(user_data)
    
  # ─────────────────────────────
  # Parameterized test for invalid names
  # ─────────────────────────────
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
  def test_create_user_invalid_names(
    self,
    db_session,
    field,
    invalid_value,
    error_regex
  ):
    unit_of_work = UnitOfWork(db_session)
    use_case = CreateUserUseCase(
      unit_of_work=unit_of_work,
      password_hasher=PasswordHasher(),
      id_generator=UuidGenerator()
    )

    user_data = CreateUserDTO(
      first_name="ValidFirstName",
      last_name="ValidLastName",
      username="validusername",
      password="Password123!",
      avatar=None
    )

    setattr(user_data, field, invalid_value)

    with pytest.raises(Exception, match=error_regex) as exc_info:
      use_case.execute(user_data)