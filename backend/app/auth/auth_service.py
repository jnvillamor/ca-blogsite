import logging
from sqlalchemy.ext.asyncio import AsyncSession 

from .auth_model import AuthResponse, TokenData, TokenType
from .token_service import TokenService

from src.application.dto import BasicUserDTO
from src.application.repositories import IUserRepository
from src.application.services import IPasswordHasher, IIdGenerator
from src.domain.entities import UserEntity
from src.domain.exceptions import UnauthorizedException

logger = logging.getLogger(__name__)
class AuthService:
  @staticmethod
  async def authenticate_user(
    session: AsyncSession,
    id_generator: IIdGenerator,
    user_repo: IUserRepository,
    password_hasher: IPasswordHasher,
    username: str,
    password: str,
  ) -> AuthResponse:
    logger.info(f"Attempting authentication for username: {username}")
    user = await user_repo.get_user_by_username(username)

    if (
      not user
      or not password_hasher.verify(password, user.password)
    ):
      raise UnauthorizedException("Invalid username or password")
    
    access_token_id = id_generator.generate()
    access_token_data = TokenData(user_id=user.id, token_id=access_token_id)
    access_token = TokenService.create_token(access_token_data, TokenType.ACCESS)

    refresh_token_id = id_generator.generate()
    refresh_token_data = TokenData(user_id=user.id, token_id=refresh_token_id)
    refresh_token = TokenService.create_token(refresh_token_data, TokenType.REFRESH)

    result = AuthResponse(
      access_token=access_token.token,
      refresh_token=refresh_token.token,
      user=BasicUserDTO.model_validate(user.to_dict())
    )

    user.access_token_id = access_token_id
    user.refresh_token_id = refresh_token_id
    user = await user_repo.update_user(user_id=user.id, user=user)
    await session.commit()

    logger.info(f"Authentication successful for username: {username}, user_id: {user.id}")
    return result
  
  @staticmethod
  async def get_current_user(
    user_repo: IUserRepository,
    token: str,
  ) -> UserEntity:
    logger.info(f"Getting current user from token.")
    token_data = TokenService.verify_token(token)

    user = await user_repo.get_user_by_id(token_data.user_id)
    token_id = token_data.token_id

    if not user:
      raise UnauthorizedException("User not found")
    
    if user.access_token_id != token_id:
      logger.warning(f"Access token mismatch for user_id: {user.id}")
      raise UnauthorizedException("Invalid access token")

    logger.info(f"Current user retrieved successfully for username: {user.username}, user_id: {user.id}")
    return user
  
  @staticmethod
  async def refresh_access_token(
    session: AsyncSession,
    id_generator: IIdGenerator,
    user_repo: IUserRepository,
    token: str,
  ) -> AuthResponse:
    logger.info(f"Refreshing access token.")
    token_data = TokenService.verify_token(token)

    user = await user_repo.get_user_by_id(token_data.user_id)
    token_id = token_data.token_id

    if not user:
      logger.warning(f"Token refresh failed: User not found for user_id: {token_data.user_id}")
      raise UnauthorizedException("User not found")

    if user.refresh_token_id != token_id:
      logger.warning(f"Refresh token mismatch for user_id: {user.id}")
      raise UnauthorizedException("Invalid refresh token")

    logger.info(f"Refreshing access token for user_id: {user.id}")

    new_access_token_id = id_generator.generate()
    new_access_token_data = TokenData(user_id=user.id, token_id=new_access_token_id)
    new_access_token = TokenService.create_token(new_access_token_data, TokenType.ACCESS)

    new_refresh_token_id = id_generator.generate()
    new_refresh_token_data = TokenData(user_id=user.id, token_id=new_refresh_token_id)
    new_refresh_token = TokenService.create_token(new_refresh_token_data, TokenType.REFRESH)

    user.access_token_id = new_access_token_id
    user.refresh_token_id = new_refresh_token_id
    user = await user_repo.update_user(user_id=user.id, user=user)
    await session.commit()

    logger.info(f"Access token refreshed successfully for user_id: {user.id}")
    return AuthResponse(
      access_token=new_access_token.token,
      refresh_token=new_refresh_token.token,
      user=BasicUserDTO.model_validate(user.to_dict())
    )
  
  @staticmethod
  async def logout_user(
    session: AsyncSession,
    user_repo: IUserRepository,
    user_id: str,
  ) -> bool:
    logger.info(f"Logging out user with user_id: {user_id}")
    user = await user_repo.get_user_by_id(user_id)
    if not user:
      logger.warning(f"Logout failed: User not found for user_id: {user_id}")
      raise UnauthorizedException("User not found")
    
    user.access_token_id = None
    user.refresh_token_id = None

    user = await user_repo.update_user(user_id=user.id, user=user)
    await session.commit()

    logger.info(f"User logged out successfully for user_id: {user.id}")
    return True