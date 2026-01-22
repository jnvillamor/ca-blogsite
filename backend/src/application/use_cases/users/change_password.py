from src.application.services import IPasswordHasher, IUnitOfWork
from src.application.dto import ChangePasswordDTO, UserResponseDTO
from src.domain.exceptions import InvalidDataException, NotFoundException
from src.domain.value_objects import Password

class ChangePasswordUseCase:
  def __init__(
    self,
    unit_of_work: IUnitOfWork,
    password_hasher: IPasswordHasher
  ):
    self.uow = unit_of_work
    self.password_hasher = password_hasher

  def execute(self, user_id: str, data: ChangePasswordDTO) -> UserResponseDTO:
    with self.uow:
      user = self.uow.users.get_user_by_id(user_id)

      if not user:
        raise NotFoundException("User", f"user_id: {user_id}")
      
      if data.confirm_new_password != data.new_password:
        raise InvalidDataException(f"New password and confirmation do not match.")
      
      if not self.password_hasher.verify(data.old_password, user.password):
        raise InvalidDataException("Old password is incorrect.")
      
      Password.is_valid(data.new_password)

      hashed_new_password = self.password_hasher.hash(data.new_password)

      user.password = hashed_new_password
      updated_user = self.uow.users.update_user(user_id, user)
      return UserResponseDTO.model_validate(updated_user.to_dict())