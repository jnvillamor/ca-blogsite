import jwt
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional

from .auth_model import Token, TokenData, TokenType
from app.config import config

logger = logging.getLogger(__name__)

class TokenService:
  @staticmethod
  def create_token(
    data: TokenData,
    token_type: TokenType,
    expires_delta: Optional[timedelta] = None,
  ) -> Token:
    to_encode = data.__dict__.copy()
    if expires_delta:
      expire = datetime.now(timezone.utc) + expires_delta
    elif token_type == TokenType.REFRESH:
      expire = datetime.now(timezone.utc) + timedelta(days=config.DEFAULT_REFRESH_TOKEN_EXPIRE_DAYS)
    else:
      expire = datetime.now(timezone.utc) + timedelta(minutes=config.DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return Token(token=encoded_jwt, ttl=int((expire - datetime.now(timezone.utc)).total_seconds()))

  @staticmethod
  def verify_token(token: str ) -> TokenData:
    try:
      payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
      user_id = payload.get("user_id")
      if user_id is None:
        raise jwt.InvalidTokenError("Token payload does not contain user_id")
      return TokenData(user_id=user_id)
    except jwt.PyJWTError as e:
      logger.error(f"Token verification failed: {str(e)}")
      raise e