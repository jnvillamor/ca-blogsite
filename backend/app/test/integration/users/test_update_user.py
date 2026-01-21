import pytest
from sqlalchemy.orm import Session
from app.database.models import UserModel
from app.database.unit_of_work import UnitOfWork
from app.services import PasswordHasher
from src.application.dto import UpdateUserDTO
from src.application.use_cases.users import UpdateUserUseCase
from src.domain.entities import UserEntity

@pytest.fixture
def update_user_use_case(db_session: Session) -> UpdateUserUseCase:
  unit_of_work = UnitOfWork(db_session)
  password_hasher = PasswordHasher()
  return UpdateUserUseCase(
    unit_of_work=unit_of_work,
    password_hasher=password_hasher
  )

class TestUpdateUserUseCase:
  def test_update_user_success(
    self,
    update_user_use_case: UpdateUserUseCase,
    create_test_user: callable
  ):
    test_user: UserEntity = create_test_user()
    
    update_dto = UpdateUserDTO(
      first_name="Updated",
      last_name="Name",
      username="updatedusername"
    )
    
    updated_user = update_user_use_case.execute(
      user_id = test_user.id,
      data=update_dto
    )
    
    assert updated_user.first_name == "Updated"
    assert updated_user.last_name == "Name"
    assert updated_user.username == "updatedusername"
  
  def test_update_user_non_existing(self, update_user_use_case):
    update_dto = UpdateUserDTO(
      first_name="Non",
      last_name="Existent",
      username="nonexistentuser"
    )
    
    with pytest.raises(Exception) as exc_info:
      update_user_use_case.execute(
        user_id = "non-existing-id",
        data=update_dto
      )
    
    assert "User with identifier 'user_id: non-existing-id' was not found." in str(exc_info.value)
  
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
  def test_update_user_invalid_names(
    self,
    update_user_use_case: UpdateUserUseCase,
    create_test_user: callable,
    field: str,
    invalid_value: str,
    error_regex: str
  ):
    test_user: UserEntity = create_test_user()
    update_data = UpdateUserDTO(**{field: invalid_value})
    
    with pytest.raises(Exception, match=error_regex) as exc_info:
      update_user_use_case.execute(
        user_id = test_user.id,
        data=update_data
      )

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
  def test_update_user_invalid_password(
    self,
    update_user_use_case: UpdateUserUseCase,
    create_test_user: callable,
    password: str,
    error_regex: str
  ):
    test_user: UserEntity = create_test_user()
    update_data = UpdateUserDTO(password=password)
    
    with pytest.raises(Exception, match=error_regex) as exc_info:
      update_user_use_case.execute(
        user_id = test_user.id,
        data=update_data
      )
      
  def test_update_user_password_success(
    self,
    update_user_use_case: UpdateUserUseCase,
    create_test_user: callable,
    db_session: Session
  ):
    test_user: UserEntity = create_test_user()
    
    new_password = "NewValid1!"
    update_dto = UpdateUserDTO(password=new_password)
    
    updated_user = update_user_use_case.execute(
      user_id = test_user.id,
      data=update_dto
    )
    
    user_model = db_session.query(UserModel).filter_by(id=test_user.id).first()
    
    assert updated_user is not None
    assert user_model.password != test_user.password  # Password should be hashed and different
    assert PasswordHasher().verify(new_password, user_model.password)  # Verify new password
