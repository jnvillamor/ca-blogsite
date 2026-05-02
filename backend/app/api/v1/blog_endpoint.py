import logging
from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_current_user
from app.database.db import get_db
from app.database.unit_of_work import get_uow
from app.repositories import BlogRepository, UserRepository
from app.services import UuidGenerator
from src.application.dto import (
  CreateBlogDTO,
  UpdateBlogDTO,
  BlogResponseDTO,
  PublicBlogResponseDTO,
  PaginationDTO,
  PaginationResponseDTO
)
from src.application.use_cases.blogs import (
  CreateBlogUseCase,
  GetBlogUseCase,
  UpdateBlogUseCase,
  DeleteBlogUseCase,
  PublishBlogUseCase
)
from src.domain.entities import UserEntity

logger = logging.getLogger(__name__)

router = APIRouter(
  prefix="/blogs",
  tags=["blogs"]
)

@router.post(
  "/",
  status_code=status.HTTP_201_CREATED,
  response_model=BlogResponseDTO,
  response_model_exclude_none=True,
  responses={
    201: {"description": "Blog successfully created."},
    400: {"description": "Bad Request."},
    500: {"description": "Internal Server Error."}
  }
)
async def create_blog(
  request: Request,
  blog_data: CreateBlogDTO,
  session: AsyncSession = Depends(get_db)
):
  logger.info(f"Creating blog with title: {blog_data.title} for author_id: {blog_data.author_id}")
  uuid_generator = UuidGenerator()
  unit_of_work = get_uow(session)
  use_case = CreateBlogUseCase(
    unit_of_work=unit_of_work,
    id_generator=uuid_generator
  )
  blog = await use_case.execute(blog_data)
  logger.info(f"Blog created with id: {blog.id}")
  return blog

@router.get(
  "/",
  status_code=status.HTTP_200_OK,
  response_model=PaginationResponseDTO[PublicBlogResponseDTO],
  response_model_exclude_none=True,
  responses={
    200: {"description": "Public blogs retrieved successfully."},
    400: {"description": "Bad Request."},
    500: {"description": "Internal Server Error."}
  }
)
async def list_blogs(
  request: Request,
  pagination: PaginationDTO = Depends(),
  session: AsyncSession = Depends(get_db)
):
  logger.info(f"Listing public blogs with pagination: skip: {pagination.skip}, limit: {pagination.limit}")
  blog_repository = BlogRepository(session)
  use_case = GetBlogUseCase(blog_repository)
  result = await use_case.get_all_public_blogs(pagination)
  logger.info(f"Number of public blogs retrieved: {len(result.items)}")
  return result

@router.get(
  "/author/{author_id}",
  status_code=status.HTTP_200_OK,
  response_model=PaginationResponseDTO[PublicBlogResponseDTO],
  response_model_exclude_none=True,
  responses={
    200: {"description": "Public blogs by author retrieved successfully."},
    400: {"description": "Bad Request."},
    500: {"description": "Internal Server Error."}
  }
)
@router.get(
  "/author/{author_id}/",
  include_in_schema=False
)
async def get_public_blogs_by_author(
  request: Request,
  author_id: str,
  pagination: PaginationDTO = Depends(),
  session: AsyncSession = Depends(get_db)
):
  logger.info(f"Fetching public blogs for author_id: {author_id} with pagination: skip: {pagination.skip}, limit: {pagination.limit}")
  blog_repository = BlogRepository(session)
  use_case = GetBlogUseCase(blog_repository)
  result = await use_case.get_all_public_blogs_by_author(author_id, pagination)
  logger.info(f"Number of public blogs fetched for author_id '{author_id}': {len(result.items)}")
  return result

@router.post(
  "/{blog_id}/publish",
  status_code=status.HTTP_200_OK,
  response_model=BlogResponseDTO,
  response_model_exclude_none=True,
  responses={
    200: {"description": "Blog published successfully."},
    404: {"description": "Blog not found."},
    403: {"description": "Not authorized to publish this blog."},
    500: {"description": "Internal Server Error."}
  }
)
@router.post(
  "/{blog_id}/publish/",
  include_in_schema=False
)
async def publish_blog(
  request: Request,
  blog_id: str,
  session: AsyncSession = Depends(get_db),
  current_user: UserEntity = Depends(get_current_user)
):
  logger.info(f"Publishing blog with id: {blog_id}")
  unit_of_work = get_uow(session)
  use_case = PublishBlogUseCase(unit_of_work)
  published_blog = await use_case.execute(current_user, blog_id)
  logger.info(f"Blog published: {published_blog.title} (id: {published_blog.id})")
  return published_blog

@router.get(
  "/{blog_id}",
  status_code=status.HTTP_200_OK,
  response_model=PublicBlogResponseDTO,
  response_model_exclude_none=True,
  responses={
    200: {"description": "Public blog retrieved successfully."},
    404: {"description": "Blog not found or not published."},
    500: {"description": "Internal Server Error."}
  }
)
@router.get(
  "/{blog_id}/",
  include_in_schema=False
)
async def get_public_blog(
  request: Request,
  blog_id: str,
  session: AsyncSession = Depends(get_db)
):
  logger.info(f"Fetching public view of blog with id: {blog_id}")
  blog_repository = BlogRepository(session)
  user_repository = UserRepository(session)
  use_case = GetBlogUseCase(blog_repository, user_repository)
  blog = await use_case.get_public_by_id(blog_id)
  if blog is None:
    logger.warning(f"Public blog with id: {blog_id} not found or not published.")
    return JSONResponse(
      status_code=status.HTTP_404_NOT_FOUND,
      content={"detail": f"Blog with id '{blog_id}' not found."}
    )
  logger.info(f"Public blog fetched: {blog.title} (id: {blog.id})")
  return blog

@router.put(
  "/{blog_id}",
  status_code=status.HTTP_200_OK,
  response_model=BlogResponseDTO,
  response_model_exclude_none=True,
  responses={
    200: {"description": "Blog updated successfully."},
    400: {"description": "Bad Request."},
    404: {"description": "Blog not found."},
    500: {"description": "Internal Server Error."}
  }
)
@router.put(
  "/{blog_id}/",
  include_in_schema=False
)
async def update_blog(
  request: Request,
  blog_id: str,
  blog_data: UpdateBlogDTO,
  session: AsyncSession = Depends(get_db),
  current_user: UserEntity = Depends(get_current_user)
):
  logger.info(f"Updating blog with id: {blog_id}")
  unit_of_work = get_uow(session)
  use_case = UpdateBlogUseCase(unit_of_work)
  updated_blog = await use_case.execute(
    current_user,
    blog_id,
    blog_data
  )
  logger.info(f"Blog updated: {updated_blog.title} (id: {updated_blog.id})")
  return updated_blog

@router.delete(
  "/{blog_id}",
  status_code=status.HTTP_204_NO_CONTENT,
  responses={
    204: {"description": "Blog deleted successfully."},
    404: {"description": "Blog not found."},
    500: {"description": "Internal Server Error."}
  }
)
@router.delete(
  "/{blog_id}/",
  include_in_schema=False
)
async def delete_blog(
  request: Request,
  blog_id: str,
  session: AsyncSession = Depends(get_db),
  current_user: UserEntity = Depends(get_current_user)
):
  logger.info(f"Deleting blog with id: {blog_id}")
  unit_of_work = get_uow(session)
  use_case = DeleteBlogUseCase(unit_of_work)
  await use_case.execute(current_user, blog_id)
  logger.info(f"Blog with id: {blog_id} deleted successfully.")
  return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=f"Blog with id '{blog_id}' deleted successfully.")
