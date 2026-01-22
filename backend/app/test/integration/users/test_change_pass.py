import pytest
from sqlalchemy.orm import Session
from app.database.models import UserModel
from app.database.unit_of_work import UnitOfWork
from app.services import PasswordHasher
from src.application.dto import ChangePasswordDTO
from src.application.use_cases.users import ChangePasswordUseCase

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
    create_test_user: callable,
  ):
    test_user = create_test_user()

    change_pass_dto = ChangePasswordDTO(
      old_password="Password123!",
      new_password="NewPassword123!",
      confirm_new_password="NewPassword123!"
    )

    result = change_password_use_case.execute(
      user_id = test_user.id,
      data = change_pass_dto
    )

    assert result.id == test_user.id
    user_in_db: UserModel = db_session.query(UserModel).filter_by(id=test_user.id).first()
    assert user_in_db is not None
