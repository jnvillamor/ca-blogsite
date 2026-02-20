import logging
from fastapi import (
  APIRouter,
  Response,
  Request,
  status,
  Depends
)
from fastapi.security import OAuth2PasswordRequestForm

from app.auth import AuthService, AuthResponse
from app.database.db import get_db
from app.dependencies import get_current_user
from app.repositories import UserRepository
from app.services import PasswordHasher
from src.application.dto import UserResponseDTO
from src.domain.entities import UserEntity

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["auth"])

@router.post(
  "/login",
  status_code=status.HTTP_200_OK,
  response_model=AuthResponse,
  response_model_exclude_none=True,
  responses={
    status.HTTP_200_OK: {
      "description": "Successful login",
    },
    status.HTTP_401_UNAUTHORIZED: {
      "description": "Invalid username or password",
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
      "description": "Internal server error",
    },
  }
)
@router.post(
  "/login/",
  include_in_schema=False
)
def login(
  response: Response,
  session=Depends(get_db), 
  form_data: OAuth2PasswordRequestForm = Depends(),
):
  try:
    user_repo = UserRepository(session)
    password_hasher = PasswordHasher()
    auth_response = AuthService.authenticate_user(
      user_repo=user_repo,
      password_hasher=password_hasher,
      username=form_data.username,
      password=form_data.password,
    )
    return auth_response
  except Exception as e:
    logger.error(f"Login failed: {str(e)}")
    response.status_code = status.HTTP_401_UNAUTHORIZED
    return {"detail": "Invalid username or password"}

@router.get(
  "/me",
  status_code=status.HTTP_200_OK,
  response_model=UserResponseDTO,
  response_model_exclude_none=True,
  responses={
    status.HTTP_200_OK: {
      "description": "Successful retrieval of current user",
    },
    status.HTTP_401_UNAUTHORIZED: {
      "description": "Invalid token",
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
      "description": "Internal server error",
    },
  }
)
@router.get(
  "/me/",
  include_in_schema=False
)
def get_authenticated_user(
  request: Request,
  current_user: UserEntity = Depends(get_current_user)
):
  return UserResponseDTO.model_validate(current_user.to_dict()) 