from pydantic import BaseModel, field_serializer
from typing import Optional
from datetime import datetime, timezone

class CreateUserDTO(BaseModel):
  first_name: str
  last_name: str
  username: str
  password: str
  avatar: Optional[str] = None

class UpdateUserDTO(BaseModel):
  first_name: Optional[str] = None
  last_name: Optional[str] = None
  username: Optional[str] = None
  avatar: Optional[str] = None

class ChangePasswordDTO(BaseModel):
  old_password: str
  new_password: str
  confirm_new_password: str

class UserResponseDTO(BaseModel):
  id: str
  first_name: str
  last_name: str
  username: str
  avatar: Optional[str] = None
  created_at: datetime
  updated_at: datetime
  
  model_config = {
    'from_attributes': True
  }

  @field_serializer("created_at", "updated_at")
  def serialize_dt(self, value: datetime) -> str:
    # SQLite gives naive datetime → force UTC
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.isoformat()