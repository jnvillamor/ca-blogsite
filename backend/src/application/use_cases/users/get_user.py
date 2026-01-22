from src.application.dto import UserResponseDTO, PaginationDTO, PaginationResponseDTO
from src.application.repositories import IUserRepository
from typing import Tuple, List

class GetUserUseCase:
  def __init__(self, user_repository: IUserRepository):
    self.user_repository = user_repository
    
  def get_by_id(self, user_id: str) -> UserResponseDTO | None:
    user = self.user_repository.get_user_by_id(user_id)
    if not user:
      return None

    return UserResponseDTO.model_validate(user.to_dict())
  
  def get_by_username(self, username: str) -> UserResponseDTO | None:
    user = self.user_repository.get_user_by_username(username)
    if not user:
      return None
    
    return UserResponseDTO.model_validate(user.to_dict())
  
  def get_all_users(self, pagination: PaginationDTO) -> PaginationResponseDTO:
    users, count = self.user_repository.get_all_users(
      skip=pagination.skip,
      limit=pagination.limit,
      search=pagination.search
    )

    user_dtos = [UserResponseDTO.model_validate(user.to_dict()) for user in users]
    return PaginationResponseDTO(
      total=count,
      skip=pagination.skip,
      limit=pagination.limit,
      items=user_dtos
    )