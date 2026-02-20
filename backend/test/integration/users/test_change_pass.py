import pytest
from sqlalchemy.orm import Session
from app.database.models import UserModel
from app.database.unit_of_work import UnitOfWork
from app.services import PasswordHasher
from src.application.dto import ChangePasswordDTO
from src.application.use_cases.users import ChangePasswordUseCase
from src.domain.entities import UserEntity
from src.domain.exceptions import NotFoundException, InvalidDataException, UnauthorizedException

@pytest.fixture
def change_password_use_case(db_session: Session) -> ChangePasswordUseCase:
  unit_of_work = UnitOfWork(db_session)
  password_hasher = PasswordHasher()
  return ChangePasswordUseCase(
    unit_of_work=unit_of_work,
    password_hasher=password_hasher
  )

class TestChangePasswordUseCase:
  def test_update_pass_success(
    self,
    db_session: Session,
    change_password_use_case: ChangePasswordUseCase,
    create_test_user,
  ):
    test_user = create_test_user()

    change_pass_dto = ChangePasswordDTO(
      old_password="Password123!",
      new_password="NewPassword123!",
      confirm_new_password="NewPassword123!"
    )

    result = change_password_use_case.execute(
      active_user=test_user,
      user_id = test_user.id,
      data = change_pass_dto
    )

    assert result.id == test_user.id
    user_in_db: UserModel = db_session.query(UserModel).filter_by(id=test_user.id).first()
    assert user_in_db is not None
  
  def test_update_pass_user_not_found(
    self,
    change_password_use_case: ChangePasswordUseCase,
    create_test_user,
  ):
    test_user = create_test_user()

    change_pass_dto = ChangePasswordDTO(
      old_password="Password123!",
      new_password="NewPassword123!",
      confirm_new_password="NewPassword123!"
    )

    with pytest.raises(NotFoundException) as exc_info:
      change_password_use_case.execute(
        active_user=test_user,
        user_id = "non_existent_user",
        data = change_pass_dto
      )
    
    assert "User with identifier 'user_id: non_existent_user' was not found" in str(exc_info.value)
  
  def test_update_pass_incorrect_old_password(
    self,
    change_password_use_case: ChangePasswordUseCase,
    create_test_user,
  ):
    test_user = create_test_user()

    change_pass_dto = ChangePasswordDTO(
      old_password="WrongOldPassword!",
      new_password="NewPassword123!",
      confirm_new_password="NewPassword123!"
    )

    with pytest.raises(InvalidDataException) as exc_info:
      change_password_use_case.execute(
        active_user=test_user,
        user_id = test_user.id,
        data = change_pass_dto
      )
    
    assert "Old password is incorrect." in str(exc_info.value)

  def test_update_pass_new_password_mismatch(
    self,
    change_password_use_case: ChangePasswordUseCase,
    create_test_user,
  ):
    test_user = create_test_user()

    change_pass_dto = ChangePasswordDTO(
      old_password="Password123!",
      new_password="NewPassword123!",
      confirm_new_password="MismatchPassword123!"
    )

    with pytest.raises(InvalidDataException) as exc_info:
      change_password_use_case.execute(
        active_user=test_user,
        user_id = test_user.id,
        data = change_pass_dto
      )
    
    assert "New password and confirmation do not match." in str(exc_info.value)

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
  def test_invalid_new_password(
    self,
    change_password_use_case: ChangePasswordUseCase,
    create_test_user,
    password,
    error_regex
  ):
    test_user = create_test_user()

    payload = ChangePasswordDTO(
      old_password="Password123!",
      new_password=password,
      confirm_new_password=password
    )

    with pytest.raises(InvalidDataException, match=error_regex) as exc_info:
      change_password_use_case.execute(
        active_user=test_user,
        user_id = test_user.id,
        data = payload
      )
    
    assert error_regex in str(exc_info.value)

  def test_execute_unauthorized_user(
    self,
    change_password_use_case: ChangePasswordUseCase,
    create_test_user,
  ):
    test_user = create_test_user()

    payload = ChangePasswordDTO(
      old_password="Password123!",
      new_password="NewPassword123!",
      confirm_new_password="NewPassword123!"
    )

    with pytest.raises(UnauthorizedException) as exc_info:
      change_password_use_case.execute(
        active_user=UserEntity(
          id="different_user_id",
          first_name="Jane",
          last_name="Smith",
          username="janesmith",
          password="SomePassword123!",
          avatar=None,
          created_at=test_user.created_at,
          updated_at=test_user.updated_at
        ),
        user_id = test_user.id,
        data = payload
      )