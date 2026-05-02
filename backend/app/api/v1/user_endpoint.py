import logging
from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession 

from app.api.dependencies import get_current_user, get_user_include_options
from app.database.db import get_db
from app.database.unit_of_work import get_uow
from app.repositories import UserRepository, BlogRepository
from app.services import PasswordHasher, UuidGenerator
from src.application.dto import (
  CreateUserDTO,
  UpdateUserDTO,
  ChangePasswordDTO,
  UserResponseDTO,
  BlogResponseDTO,
  PaginationDTO,
  PaginationResponseDTO,
  UserIncludeOptions
)
from src.application.use_cases.users import (
  CreateUserUseCase,
  GetUserUseCase,
  UpdateUserUseCase,
  ChangePasswordUseCase,
  DeleteUserUseCase
)
from src.application.use_cases.blogs import GetBlogUseCase
from src.domain.entities import UserEntity

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
@router.post(
  "/register/",
  include_in_schema=False
)
async def register_user(
  request: Request,
  user_data: CreateUserDTO,
  session: AsyncSession = Depends(get_db)
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
  result = await use_case.execute(user_data)
  logger.info(f"User registered with ID: {result.id}")
  return result

@router.get(
  "/",
  status_code=status.HTTP_200_OK,
  response_model=PaginationResponseDTO[UserResponseDTO],
  response_model_exclude_none=True,
  responses={
    200: {"description": "List of users retrieved successfully."},
    500: {"description": "Internal Server Error."}
  }
)
async def get_users(
  request: Request,
  pagination: PaginationDTO = Depends(),
  include_options: UserIncludeOptions = Depends(get_user_include_options),
  session: AsyncSession = Depends(get_db),
):
  logger.info(f"Fetching users with pagination: skip={pagination.skip}, limit={pagination.limit}, search='{pagination.search}'")
  user_repo = UserRepository(session)
  blog_repo = BlogRepository(session)
  use_case = GetUserUseCase(user_repo, blog_repo)
  result = await use_case.get_all_users(pagination, include_options)
  logger.info(f"Number of users fetched: {len(result.items)}")
  return result

@router.get(
  "/me/blogs",
  status_code=status.HTTP_200_OK,
  response_model=PaginationResponseDTO[BlogResponseDTO],
  response_model_exclude_none=True,
  responses={
    200: {"description": "Owner blogs retrieved successfully."},
    401: {"description": "Not authenticated."},
    500: {"description": "Internal Server Error."}
  }
)
@router.get(
  "/me/blogs/",
  include_in_schema=False
)
async def list_my_blogs(
  request: Request,
  pagination: PaginationDTO = Depends(),
  session: AsyncSession = Depends(get_db),
  current_user: UserEntity = Depends(get_current_user)
):
  logger.info(f"Listing blogs for current_user_id: {current_user.id} with pagination: skip: {pagination.skip}, limit: {pagination.limit}")
  blog_repo = BlogRepository(session)
  use_case = GetBlogUseCase(blog_repo)
  result = await use_case.get_all_blogs_for_owner(current_user, pagination)
  logger.info(f"Number of blogs fetched for current_user_id '{current_user.id}': {len(result.items)}")
  return result

@router.get(
  "/me/blogs/{blog_id}",
  status_code=status.HTTP_200_OK,
  response_model=BlogResponseDTO,
  response_model_exclude_none=True,
  responses={
    200: {"description": "Owner blog retrieved successfully."},
    401: {"description": "Not authenticated."},
    404: {"description": "Blog not found."},
    500: {"description": "Internal Server Error."}
  }
)
@router.get(
  "/me/blogs/{blog_id}/",
  include_in_schema=False
)
async def get_my_blog(
  request: Request,
  blog_id: str,
  session: AsyncSession = Depends(get_db),
  current_user: UserEntity = Depends(get_current_user)
):
  logger.info(f"Fetching owner view of blog with id: {blog_id} for current_user_id: {current_user.id}")
  blog_repo = BlogRepository(session)
  use_case = GetBlogUseCase(blog_repo)
  blog = await use_case.get_owner_by_id(current_user, blog_id)
  if blog is None:
    logger.warning(f"Owner blog with id: {blog_id} not found for current_user_id: {current_user.id}.")
    return JSONResponse(
      status_code=status.HTTP_404_NOT_FOUND,
      content={"detail": f"Blog with id '{blog_id}' not found."}
    )
  logger.info(f"Owner blog fetched: {blog.title} (id: {blog.id})")
  return blog

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
@router.get(
  "/{user_id}/",
  include_in_schema=False
)
async def get_user(
  request: Request,
  user_id: str,
  include_options: UserIncludeOptions = Depends(get_user_include_options),
  session: AsyncSession = Depends(get_db),
):
  logger.info(f"Fetching user with ID: {user_id}")
  user_repo = UserRepository(session)
  blog_repo = BlogRepository(session)
  use_case = GetUserUseCase(user_repo, blog_repo)
  result = await use_case.get_by_id(user_id, include_options)

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
@router.get(
  "/by-username/{username}/",
  include_in_schema=False
)
async def get_user_by_username(
  request: Request,
  username: str,
  include_options: UserIncludeOptions = Depends(get_user_include_options),
  session: AsyncSession = Depends(get_db),
):
  logger.info(f"Fetching user with username: {username}")
  user_repo = UserRepository(session)
  blog_repo = BlogRepository(session)
  use_case = GetUserUseCase(user_repo, blog_repo)
  result = await use_case.get_by_username(username, include_options)
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
@router.put(
  "/{user_id}/",
  include_in_schema=False
) 
async def update_user(
  request: Request,
  user_id: str,
  user_data: UpdateUserDTO,
  session: AsyncSession = Depends(get_db),
  active_user: UserEntity = Depends(get_current_user)
):
  logger.info(f"Updating user with ID: {user_id}")
  unit_of_work = get_uow(session)
  use_case = UpdateUserUseCase(unit_of_work)
  result = await use_case.execute(
    active_user=active_user, 
    user_id=user_id, 
    data=user_data
  )
  logger.info(f"User updated: {result.username}")
  return result

@router.put(
  "/change-password/{user_id}",
  status_code=status.HTTP_200_OK,
  response_model=UserResponseDTO,
  response_model_exclude_none=True,
  responses={
    200: {"description": "User password changed successfully."},
    400: {"description": "Bad Request."},
    404: {"description": "User not found."},
    500: {"description": "Internal Server Error."}
  }
)
@router.put(
  "/change-password/{user_id}/",
  include_in_schema=False
)
async def change_user_password(
  request: Request,
  user_id: str,
  pass_data: ChangePasswordDTO,
  session: AsyncSession = Depends(get_db),
  active_user: UserEntity = Depends(get_current_user)
):
  logger.info(f"Changing password for user with ID: {user_id}")
  password_hasher = PasswordHasher()
  unit_of_work = get_uow(session)
  use_case = ChangePasswordUseCase(
    unit_of_work=unit_of_work,
    password_hasher=password_hasher
  )
  result = await use_case.execute(
    active_user=active_user, 
    user_id=user_id, 
    data=pass_data
  )
  logger.info(f"Password changed for user ID: {user_id}")
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
@router.delete(
  "/{user_id}/",
  include_in_schema=False
)
async def delete_user(
  request: Request,
  user_id: str,
  session: AsyncSession = Depends(get_db),
  active_user: UserEntity = Depends(get_current_user)
):
  logger.info(f"Deleting user with ID: {user_id}")
  unit_of_work = get_uow(session)
  use_case = DeleteUserUseCase(unit_of_work)
  await use_case.execute(
    active_user=active_user, 
    user_id=user_id
  )
  logger.info(f"User deleted with ID: {user_id}")