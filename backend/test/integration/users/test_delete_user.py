import pytest
from sqlalchemy.orm import Session 
from app.database.models import UserModel
from app.database.unit_of_work import UnitOfWork
from src.application.use_cases.users import DeleteUserUseCase
from src.domain.entities import UserEntity

@pytest.fixture
def delete_user_use_case(db_session: Session) -> DeleteUserUseCase:
  unit_of_work = UnitOfWork(session=db_session)
  use_case = DeleteUserUseCase(unit_of_work=unit_of_work)
  return use_case

class TestDeleteUserUseCase:
  def test_delete_user_success(
    self,
    db_session: Session,
    create_test_user: callable,
    delete_user_use_case: DeleteUserUseCase,
  ):
    test_user: UserEntity = create_test_user()
    
    # Test if user exists before deletion
    user_in_db: UserModel = db_session.query(UserModel).filter_by(id=test_user.id).first()
    assert user_in_db is not None
    assert user_in_db.username == test_user.username
    assert user_in_db.id == test_user.id
    delete_user_use_case.execute(user_id=test_user.id)
    
    # Test if user is deleted
    user_after_delete = db_session.query(UserModel).filter_by(id=test_user.id).first()
    
    assert user_after_delete is None
  
  def test_delete_user_non_existing(
    self,
    delete_user_use_case: DeleteUserUseCase,
  ):
    non_existing_user_id = "non-existing-id"
    
    with pytest.raises(Exception) as exc_info:
      delete_user_use_case.execute(user_id=non_existing_user_id)
    
    assert "User with identifier 'user_id: non-existing-id' was not found." in str(exc_info.value)