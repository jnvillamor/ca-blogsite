from abc import ABC, abstractmethod
from typing import Optional, Tuple, List
from src.domain.entities import UserEntity

class IUserRepository(ABC):
  @abstractmethod
  def create_user(self, user: UserEntity) -> UserEntity:
    """Create a new user.

    Args:
      user (UserEntity): The user entity to create.

    Returns:
      UserEntity: The created user entity
    """
    pass
  
  @abstractmethod
  def get_user_by_id(self, user_id: str) -> Optional[UserEntity]:
    """Retrieve a user by their ID.

    Args:
      user_id (str): The ID of the user to retrieve.

    Returns:
      Optional[UserEntity]: The user entity if found, otherwise None.
    """
    pass

  @abstractmethod
  def get_user_by_username(self, username: str) -> Optional[UserEntity]:
    """Retrieve a user by their username.

    Args:
      username (str): The username of the user to retrieve.

    Returns:
      Optional[UserEntity]: The user entity if found, otherwise None.
    """
    pass
  
  @abstractmethod
  def get_all_users(
    self,
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None
  ) -> Tuple[List[UserEntity], int]:
    """Retrieve all users with pagination and optional search.

    Args:
      skip (int, optional): Number of records to skip. Defaults to 0.
      limit (int, optional): Maximum number of records to return. Defaults to 10.
      search (Optional[str], optional): Search term for filtering users. Defaults to None.

    Returns:
      Tuple[List[UserEntity], int]: A tuple containing the list of user entities and the total count.
    """
    pass
  
  @abstractmethod
  def update_user(self, user_id: str, user: UserEntity) -> Optional[UserEntity]:
    """Update an existing user.

    Args:
      user (UserEntity): The user entity with updated data.

    Returns:
      UserEntity: The updated user entity.
    """
    pass
  
  @abstractmethod
  def delete_user(self, user_id: str) -> bool:
    """Delete a user by their ID.

    Args:
      user_id (str): The ID of the user to delete.
    """
    pass