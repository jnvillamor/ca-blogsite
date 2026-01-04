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
    self.first_name = first_name
    self.last_name = last_name
    self.username = username
    self.password = password
    self.avatar = avatar
    self.created_at = created_at
    self.updated_at = updated_at