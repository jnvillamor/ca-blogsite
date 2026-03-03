from enum import Enum
from pydantic import BaseModel

from src.application.dto import BasicUserDTO

class TokenType(Enum):
  ACCESS = "access"
  REFRESH = "refresh"

class TokenData(BaseModel):
  user_id: str 
  token_id: str

class Token(BaseModel):
  token: str

class AuthResponse(BaseModel):
  access_token: str
  refresh_token: str
  user: BasicUserDTO