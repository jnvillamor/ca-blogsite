from .auth_exceptions import AuthException
from .auth_model import AuthResponse, TokenData, TokenType
from .token_service import TokenService
from src.application.dto import BasicUserDTO, UserResponseDTO
from src.application.repositories import IUserRepository
from src.application.services import IPasswordHasher

class AuthService:
  @staticmethod
  def authenticate_user(
    user_repo: IUserRepository,
    password_hasher: IPasswordHasher,
    username: str,
    password: str,
  ) -> AuthResponse:
    user = user_repo.get_user_by_username(username)

    if (
      not user
      or not password_hasher.verify(password, user.password)
    ):
      raise AuthException("Invalid username or password")
    
    token_data = TokenData(user_id=user.id)
    access_token = TokenService.create_token(token_data, TokenType.ACESS)
    refresh_token = TokenService.create_token(token_data, TokenType.REFRESH)
    result = AuthResponse(
      access_token=access_token.token,
      access_token_ttl=access_token.ttl,
      refresh_token=refresh_token.token,
      refresh_token_ttl=refresh_token.ttl,
      user=BasicUserDTO.model_validate(user.to_dict())
    )
    return result
  
  @staticmethod
  def get_current_user(
    user_repo: IUserRepository,
    token: str,
  ) -> UserResponseDTO:
    token_data = TokenService.verify_token(token)
    user = user_repo.get_user_by_id(token_data.user_id)
    if not user:
      raise AuthException("User not found")
    
    return UserResponseDTO.model_validate(user)
  
  @staticmethod
  def refresh_access_token(
    user_repo: IUserRepository,
    token: str,
  ) -> AuthResponse:
    token_data = TokenService.verify_token(token)
    user = user_repo.get_user_by_id(token_data.user_id)
    if not user:
      raise AuthException("User not found")
    
    new_token_data = TokenData(user_id=user.id)
    new_access_token = TokenService.create_token(new_token_data, TokenType.ACESS)
    new_refresh_token = TokenService.create_token(new_token_data, TokenType.REFRESH)
    return AuthResponse(
      access_token=new_access_token.token,
      access_token_ttl=new_access_token.ttl,
      refresh_token=new_refresh_token.token,
      refresh_token_ttl=new_refresh_token.ttl,
      user=BasicUserDTO.model_validate(user.to_dict())
    )