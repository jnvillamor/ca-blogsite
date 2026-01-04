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
  
  def set_first_name(self, value: str):
    self.first_name = FirstName(value)
    self.updated_at = datetime.now(timezone.utc).isoformat()
  
  def get_first_name(self) -> str:
    return self.first_name.value
  
  def set_last_name(self, value: str):
    self.last_name = LastName(value)
    self.updated_at = datetime.now(timezone.utc).isoformat()
    
  def get_last_name(self) -> str:
    return self.last_name.value
  
  def set_username(self, value: str):
    self.username = Username(value)
    self.updated_at = datetime.now(timezone.utc).isoformat()
    
  def get_username(self) -> str:
    return self.username.value
  
  def set_password(self, hashed_password: str):
    self.password = Password(hashed_password)
    self.updated_at = datetime.now(timezone.utc).isoformat()
    
  def get_password(self) -> str:
    return self.password.value
  
  def set_avatar(self, avatar_url: Optional[str]):
    self.avatar = avatar_url
    self.updated_at = datetime.now(timezone.utc).isoformat()
    
  def to_dict(self) -> dict:
    return {
      "id": self.id,
      "first_name": self.first_name.value,
      "last_name": self.last_name.value,
      "username": self.username.value,
      "password": self.password.value,
      "avatar": self.avatar,
      "created_at": self.created_at,
      "updated_at": self.updated_at
    }