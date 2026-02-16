import pytest
from datetime import timedelta
from app.auth import TokenService, TokenData, TokenType, Token
from app.config import config

class TestTokenService:
  def test_create_token(self):
    data = TokenData(user_id="test_user_id")
    token = TokenService.create_token(data, TokenType.ACESS)
    assert isinstance(token, Token)
    assert token.token is not None
    assert token.ttl > 0

  def test_verify_token(self):
    data = TokenData(user_id="test_user_id")
    token = TokenService.create_token(data, TokenType.ACESS)
    verified_data = TokenService.verify_token(token.token)
    assert verified_data.user_id == data.user_id
    
  def test_verify_token_invalid(self):
    with pytest.raises(Exception):
      TokenService.verify_token("invalid_token")
  
  def test_create_token_with_custom_expiry(self):
    data = TokenData(user_id="test_user_id")
    expires_delta = timedelta(minutes=10)
    token = TokenService.create_token(data, TokenType.ACESS, expires_delta)
    assert isinstance(token, Token)
    assert token.token is not None
    assert token.ttl <= 600  # Should be less than or equal to 10 minutes in seconds
