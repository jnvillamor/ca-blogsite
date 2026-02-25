from enum import Enum
from pydantic import BaseModel

from src.application.dto import BasicUserDTO

class TokenType(Enum):
  ACCESS = "access"
  REFRESH = "refresh"

class TokenData(BaseModel):
  user_id: str 

class Token(BaseModel):
  token: str
  ttl: int

class AuthResponse(BaseModel):
  access_token: str
  access_token_ttl: int
  refresh_token: str
  refresh_token_ttl: int
  user: BasicUserDTO