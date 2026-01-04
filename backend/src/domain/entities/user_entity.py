from src.domain.value_objects import (
  FirstName,
  LastName,
  Username,
  Password
)
from datetime import datetime, timezone
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
    self.password = Password(password) 
    self.avatar = avatar
    self.created_at = created_at or datetime.now(timezone.utc).isoformat()
    self.updated_at = updated_at or datetime.now(timezone.utc).isoformat()