from pydantic import BaseModel
from  typing import Optional

class BasicUserDTO(BaseModel):
  id: str
  first_name: str
  last_name: str
  username: str
  avatar: Optional[str] = None
  
class CreateUserDTO(BaseModel):
  first_name: str
  last_name: str
  username: str
  password: str
  avatar: Optional[str] = None

class UserResponseDTO(BasicUserDTO):
  created_at: str
  updated_at: str
  
  model_config = {
    'from_attributes': True
  }