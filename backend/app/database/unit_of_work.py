from src.application.services import IUnitOfWork
from app.repositories import UserRepository, BlogRepository
from sqlalchemy.orm import Session

class UnitOfWork(IUnitOfWork):
  def __init__(self, session: Session):
    self.session = session
    self.users = UserRepository(session)
    self.blogs = BlogRepository(session)
  
  def __enter__(self) -> 'IUnitOfWork':
    return self
  
  def __exit__(self, *args):
    exc_type, exc_val, exc_tb = args
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
