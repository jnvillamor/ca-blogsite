from src.application.services import IUnitOfWork
from src.domain.exceptions import NotFoundException

class DeleteUserUseCase:
  def __init__(self, unit_of_work: IUnitOfWork):
    self.unit_of_work = unit_of_work
    
  def execute(self, user_id: str) -> None: 
    with self.unit_of_work:
      user = self.unit_of_work.users.get_user_by_id(user_id)
      
      if not user:
        raise NotFoundException("User", f"user_id: {user_id}")
      
      self.unit_of_work.users.delete_user(user_id)