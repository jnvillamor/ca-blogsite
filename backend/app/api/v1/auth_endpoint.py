import logging
from fastapi import (
  APIRouter,
  Response,
  Request,
  status,
  Depends
)
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import get_current_user
from app.auth import AuthService, AuthResponse
from app.database.db import get_db
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
  user_repo = UserRepository(session)
  password_hasher = PasswordHasher()
  auth_response = AuthService.authenticate_user(
    user_repo=user_repo,
    password_hasher=password_hasher,
    username=form_data.username,
    password=form_data.password,
  )
  return auth_response


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

@router.post(
  "/refresh",
  status_code=status.HTTP_200_OK,
  response_model=AuthResponse,
  response_model_exclude_none=True,
  responses={
    status.HTTP_200_OK: {
      "description": "Successful token refresh",
    },
    status.HTTP_401_UNAUTHORIZED: {
      "description": "Invalid token",
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
      "description": "Internal server error",
    },
  }
)
@router.post(
  "/refresh/",
  include_in_schema=False
)
def refresh_token(
  request: Request,
  session=Depends(get_db), 
  current_user: UserEntity = Depends(get_current_user)
):
  user_repo = UserRepository(session)
  token = request.headers.get("Authorization")
  if token and token.startswith("Bearer "):
    token = token.split(" ")[1]
  else:
    token = None

  if not token:
    logger.error("Missing token in refresh request")
    return Response(content="Missing token", status_code=status.HTTP_401_UNAUTHORIZED)
  
  auth_response = AuthService.refresh_access_token(
    user_repo=user_repo,
    token=token,
  )
  return auth_response