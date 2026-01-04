from src.domain.value_objects import FirstName, LastName, Username
from typing import Optional

class UserEntity:
  def __init__(
    self,
    id: str,
    first_name: str,
    last_name: str,
    username: str,
    password: str,
    avatar: Optional[str] = None,
    created_at: Optional[str] = None,
    updated_at: Optional[str] = None
  ):
    self.id = id
    self.first_name = FirstName(first_name) 
    self.last_name = LastName(last_name) 
    self.username = Username(username)
    self.password = password
    self.avatar = avatar
    self.created_at = created_at
    self.updated_at = updated_at