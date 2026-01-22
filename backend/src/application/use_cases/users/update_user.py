from src.application.dto import UpdateUserDTO, UserResponseDTO
from src.application.services import IUnitOfWork, IPasswordHasher
from src.domain.exceptions import NotFoundException, InvalidDataException
from src.domain.value_objects import Password

class UpdateUserUseCase:
  def __init__(self, unit_of_work: IUnitOfWork, password_hasher: IPasswordHasher):
    self.uow = unit_of_work
    self.password_hasher = password_hasher
  
  def execute(self, user_id: str, data: UpdateUserDTO) -> UserResponseDTO:
    with self.uow:
      user = self.uow.users.get_user_by_id(user_id)

      if not user:
        raise NotFoundException("User", f"user_id: {user_id}")
      
      existing_username = self.uow.users.get_user_by_username(data.username) if data.username else None
      if existing_username and existing_username.id != user_id:
        raise InvalidDataException(f"The username '{data.username}' is already taken.")
    
    if data.password is not None:
      Password.is_valid(data.password)
      hashed_password = self.password_hasher.hash(data.password)
      user.password = hashed_password
    
    for field, value in data.model_dump(exclude_unset=True).items():
      if field != "password":
        setattr(user, field, value)
    
    updated_user = self.uow.users.update_user(user_id, user)
    return UserResponseDTO.model_validate(updated_user.to_dict())