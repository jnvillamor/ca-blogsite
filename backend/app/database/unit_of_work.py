from src.application.services import IUnitOfWork
from app.repositories.user_repository import UserRepository
from sqlalchemy.orm import Session

class UnitOfWork(IUnitOfWork):
  def __init__(self, session: Session):
    self.session = session
    self.users = None
  
  def __enter__(self):
    self.users = UserRepository(self.session)
    return self
  
  def __exit__(self, exc_type, exc_value, traceback):
    if exc_type is not None:
      self.session.rollback()
    else:
      self.session.commit()
    self.session.close()
    
  def commit(self):
    self.session.commit()
  
  def rollback(self):
    self.session.rollback()
    
# Get unit of work instance
def get_uow(session: Session) -> UnitOfWork:
  return UnitOfWork(session)
