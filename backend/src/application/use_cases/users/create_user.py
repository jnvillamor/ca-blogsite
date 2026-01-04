from src.application.services import IUnitOfWork, IPasswordHasher, IIdGenerator
from src.application.dto import CreateUserDTO, UserResponseDTO
from src.domain.entities import UserEntity
from src.domain.exceptions import UsernameExistsException
from src.domain.value_objects import Password

class CreateUserUseCase:
  def __init__(
    self,
    unit_of_work: IUnitOfWork,
    password_hasher: IPasswordHasher,
    id_generator: IIdGenerator
  ):
    self.uow = unit_of_work
    self.password_hasher = password_hasher
    self.id_generator = id_generator
  
  def execute(self, user_data: CreateUserDTO) -> UserResponseDTO: 
    with self.uow:
      # Validate if username is already taken
      existing_user = self.uow.users.get_user_by_username(user_data.username)
      
      if existing_user:
        raise UsernameExistsException(user_data.username)
      
      # Validate password
      Password.is_valid(user_data.password)
      
      # Hash password
      hashed_password = self.password_hasher.hash(user_data.password)
      
      # Generate user ID
      user_id = self.id_generator.generate()

      # Create user entity
      new_user = UserEntity(
        id=user_id,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        username=user_data.username,
        password=hashed_password,
        avatar=user_data.avatar
      )

      # Persist user entity
      self.uow.users.create_user(new_user)
      return UserResponseDTO.model_validate(new_user)

