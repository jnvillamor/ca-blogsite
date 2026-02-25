from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from app.auth import AuthService
from app.database.db import get_db
from app.repositories import UserRepository
from src.application.repositories import IUserRepository
from src.domain.entities import UserEntity

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")

def get_user_repository(
  session = Depends(get_db),
) -> IUserRepository:
  return UserRepository(session)

def get_current_user(
  user_repo: IUserRepository = Depends(get_user_repository),
  token: str = Depends(oauth2_scheme),
) -> UserEntity:
  return AuthService.get_current_user(user_repo, token)