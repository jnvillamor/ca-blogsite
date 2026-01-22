import logging
from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.database.unit_of_work import get_uow
from app.repositories import UserRepository
from app.services import PasswordHasher, UuidGenerator
from src.application.dto import (
  CreateUserDTO, 
  UpdateUserDTO,
  UserResponseDTO,
  PaginationDTO,
  PaginationResponseDTO
)
from src.application.use_cases.users import (
  CreateUserUseCase, 
  GetUserUseCase,
  UpdateUserUseCase,
  DeleteUserUseCase
)

logger = logging.getLogger(__name__)

router = APIRouter(
  prefix="/users",
  tags=["users"]
)

@router.post(
  "/register", 
  status_code=status.HTTP_201_CREATED,
  response_model=UserResponseDTO,
  response_model_exclude_none=True,
  responses={
    201: {"description": "User successfully registered."},
    400: {"description": "Bad Request."},
    409: {"description": "Conflict. User already exists."},
    500: {"description": "Internal Server Error."}
  }
)
def register_user(
  request: Request,
  user_data: CreateUserDTO,
  session: Session = Depends(get_db)
):
  logger.info(f"Registering user with username: {user_data.username}")
  password_hasher = PasswordHasher()
  uuid_generator = UuidGenerator()
  unit_of_work = get_uow(session)
  use_case = CreateUserUseCase(
    unit_of_work=unit_of_work,
    password_hasher=password_hasher,
    id_generator=uuid_generator
  )
  result = use_case.execute(user_data)
  logger.info(f"User registered with ID: {result.id}")
  return result

@router.get(
  "/",
  status_code=status.HTTP_200_OK,
  response_model=PaginationResponseDTO,
  response_model_exclude_none=True,
  responses={
    200: {"description": "List of users retrieved successfully."},
    500: {"description": "Internal Server Error."}
  }
)
def get_users(
  request: Request,
  pagination: PaginationDTO = Depends(),
  session: Session = Depends(get_db),
):
  logger.info(f"Fetching users with pagination: skip={pagination.skip}, limit={pagination.limit}, search='{pagination.search}'")
  user_repo = UserRepository(session)
  use_case = GetUserUseCase(user_repo)
  result = use_case.get_all_users(pagination)
  logger.info(f"Number of users fetched: {len(result.items)}")
  return result

@router.get(
  "/{user_id}",
  status_code=status.HTTP_200_OK,
  response_model=UserResponseDTO,
  response_model_exclude_none=True,
  responses={
    200: {"description": "User found."},
    404: {"description": "User not found."},
    500: {"description": "Internal Server Error."}
  }
)
def get_user(
  request: Request,
  user_id: str,
  session: Session = Depends(get_db),
):
  logger.info(f"Fetching user with ID: {user_id}")
  user_repo = UserRepository(session)
  use_case = GetUserUseCase(user_repo)
  result = use_case.get_by_id(user_id)

  if result is None:
    logger.warning(f"User with ID '{user_id}' not found.")
    return JSONResponse(
      status_code=status.HTTP_404_NOT_FOUND,
      content={"detail": f"User with ID '{user_id}' not found."}
    )

  logger.info(f"User fetched: {result.username}")
  return result

@router.get(
  "/by-username/{username}",
  status_code=status.HTTP_200_OK,
  response_model=UserResponseDTO,
  response_model_exclude_none=True,
  responses={
    200: {"description": "User found."},
    404: {"description": "User not found."},
    500: {"description": "Internal Server Error."}
  }
)
def get_user_by_username(
  request: Request,
  username: str,
  session: Session = Depends(get_db),
):
  logger.info(f"Fetching user with username: {username}")
  user_repo = UserRepository(session)
  use_case = GetUserUseCase(user_repo)
  result = use_case.get_by_username(username)
  if result is None:
    logger.warning(f"User with username '{username}' not found.")
    return JSONResponse(
      status_code=status.HTTP_404_NOT_FOUND,
      content={"detail": f"User with username '{username}' not found."}
    )
  logger.info(f"User fetched: {result.id}")
  return result

@router.put(
  "/{user_id}",
  status_code=status.HTTP_200_OK,
  response_model=UserResponseDTO,
  response_model_exclude_none=True,
  responses={
    200: {"description": "User updated successfully."},
    400: {"description": "Bad Request."},
    404: {"description": "User not found."},
    500: {"description": "Internal Server Error."}
  }
)
def update_user(
  request: Request,
  user_id: str,
  user_data: UpdateUserDTO,
  session: Session = Depends(get_db)
):
  logger.info(f"Updating user with ID: {user_id}")
  unit_of_work = get_uow(session)
  use_case = UpdateUserUseCase(unit_of_work)
  result = use_case.execute(user_id, user_data)
  logger.info(f"User updated: {result.username}")
  return result

@router.delete(
  "/{user_id}",
  status_code=status.HTTP_204_NO_CONTENT,
  responses={
    204: {"description": "User deleted successfully."},
    404: {"description": "User not found."},
    500: {"description": "Internal Server Error."}
  }
)
def delete_user(
  request: Request,
  user_id: str,
  session: Session = Depends(get_db)
):
  logger.info(f"Deleting user with ID: {user_id}")
  unit_of_work = get_uow(session)
  use_case = DeleteUserUseCase(unit_of_work)
  use_case.execute(user_id)
  logger.info(f"User deleted with ID: {user_id}")