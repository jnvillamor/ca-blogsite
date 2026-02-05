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
    self.__id = id
    self.__first_name = FirstName(first_name) 
    self.__last_name = LastName(last_name) 
    self.__username = Username(username)
    self.__password = Password(password) 
    self.__avatar = avatar
    self.__created_at = created_at or datetime.now(timezone.utc).isoformat()
    self.__updated_at = updated_at or datetime.now(timezone.utc).isoformat()
  
  @property
  def id(self) -> str:
    return self.__id
  
  @property
  def first_name(self) -> str:
    return self.__first_name.value
  
  @first_name.setter
  def first_name(self, value: str):
    self.__first_name = FirstName(value)
    self.__updated_at = datetime.now(timezone.utc).isoformat()

  @property
  def last_name(self) -> str:
    return self.__last_name.value
  
  @last_name.setter
  def last_name(self, value: str):
    self.__last_name = LastName(value)
    self.__updated_at = datetime.now(timezone.utc).isoformat()

  @property
  def username(self) -> str:
    return self.__username.value
  
  @username.setter
  def username(self, value: str):
    self.__username = Username(value)
    self.__updated_at = datetime.now(timezone.utc).isoformat()

  @property
  def password(self) -> str:
    return self.__password.value
  
  @password.setter
  def password(self, hashed_password: str):
    self.__password = Password(hashed_password)
    self.__updated_at = datetime.now(timezone.utc).isoformat()
  
  @property
  def avatar(self) -> Optional[str]:
    return self.__avatar
  
  @avatar.setter
  def avatar(self, avatar_url: Optional[str]):
    self.__avatar = avatar_url
    self.__updated_at = datetime.now(timezone.utc).isoformat()
  
  @property
  def created_at(self) -> str:
    return self.__created_at
  
  @property
  def updated_at(self) -> str:
    return self.__updated_at
    
  def to_dict(self) -> dict:
    return {
      "id": self.id,
      "first_name": self.first_name,
      "last_name": self.last_name,
      "username": self.username,
      "password": self.password,
      "avatar": self.avatar,
      "created_at": self.created_at,
      "updated_at": self.updated_at
    }