import pytest
from datetime import datetime, timedelta
from app.auth import TokenService, TokenData, TokenType, Token
from app.config import config

@pytest.fixture
def id_generator(mocker):
  generator = mocker.Mock()
  generator.generate.side_effect = lambda: f"token-{datetime.now().timestamp()}"
  return generator

class TestTokenService:
  def test_create_token(self, id_generator):
    id = id_generator.generate()
    data = TokenData(user_id="test_user_id", token_id=id)
    token = TokenService.create_token(data, TokenType.ACCESS)
    assert isinstance(token, Token)
    assert token.token is not None

  def test_verify_token(self, id_generator):
    id = id_generator.generate()
    data = TokenData(user_id="test_user_id", token_id=id)
    token = TokenService.create_token(data, TokenType.ACCESS)
    verified_data = TokenService.verify_token(token.token)
    assert verified_data.user_id == data.user_id
    
  def test_verify_token_invalid(self):
    with pytest.raises(Exception):
      TokenService.verify_token("invalid_token")
  
  def test_create_token_with_custom_expiry(self, id_generator):
    id = id_generator.generate()
    data = TokenData(user_id="test_user_id", token_id=id)
    expires_delta = timedelta(minutes=10)
    token = TokenService.create_token(data, TokenType.ACCESS, expires_delta)
    assert isinstance(token, Token)
    assert token.token is not None
