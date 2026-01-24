from pydantic import BaseModel
from  typing import Optional

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
  created_at: str
  updated_at: str
  
  model_config = {
    'from_attributes': True
  }