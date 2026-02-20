from src.application.services import IUnitOfWork
from src.domain.entities import UserEntity
from src.domain.exceptions import NotFoundException, UnauthorizedException

class DeleteUserUseCase:
  def __init__(self, unit_of_work: IUnitOfWork):
    self.unit_of_work = unit_of_work
    
  def execute(self, active_user: UserEntity, user_id: str) -> None: 
    if not active_user:
      raise UnauthorizedException("You must be authenticated to delete a user.")

    with self.unit_of_work:
      user = self.unit_of_work.users.get_user_by_id(user_id)
      
      if not user:
        raise NotFoundException("User", f"user_id: {user_id}")
      
      if active_user.id != user_id:
        raise UnauthorizedException("You are not authorized to delete this user.")
      self.unit_of_work.users.delete_user(user_id)