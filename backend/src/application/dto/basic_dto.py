from pydantic import BaseModel
from typing import Optional

class BasicUserDTO(BaseModel):
  id: str
  first_name: str
  last_name: str
  username: str
  avatar: Optional[str] = None