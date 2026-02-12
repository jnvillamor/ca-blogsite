import logging
from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.database.unit_of_work import get_uow
from app.repositories import BlogRepository
from app.services import UuidGenerator
from src.application.dto import (
  CreateBlogDTO, 
  UpdateBlogDTO,
  BlogResponseDTO,
  PaginationDTO,
  PaginationResponseDTO
)
from src.application.use_cases.blogs import (
  CreateBlogUseCase,
  GetBlogUseCase,
  UpdateBlogUseCase,
  DeleteBlogUseCase
)

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
def create_blog(
  request: Request,
  blog_data: CreateBlogDTO,
  session: Session = Depends(get_db)
):
  logger.info(f"Creating blog with title: {blog_data.title} for author_id: {blog_data.author_id}")
  uuid_generator = UuidGenerator()
  unit_of_work = get_uow(session)
  use_case = CreateBlogUseCase(
    unit_of_work=unit_of_work,
    id_generator=uuid_generator
  )
  blog = use_case.execute(blog_data)
  logger.info(f"Blog created with id: {blog.id}")
  return blog

@router.get(
  "/",
  status_code=status.HTTP_200_OK,
  response_model=PaginationResponseDTO[BlogResponseDTO],
  response_model_exclude_none=True,
  responses={
    200: {"description": "Blogs retrieved successfully."},
    400: {"description": "Bad Request."},
    500: {"description": "Internal Server Error."}
  }
)
def list_blogs(
  request: Request,
  pagination: PaginationDTO = Depends(),
  session: Session = Depends(get_db)
):
  logger.info(f"Listing blogs with pagination: skip: {pagination.skip}, limit: {pagination.limit}")
  blog_repository = BlogRepository(session)
  use_case = GetBlogUseCase(blog_repository)
  result = use_case.get_all_blogs(pagination)
  logger.info(f"Number of blogs retrieved: {len(result.items)}")
  return result

@router.get(
  "/{blog_id}",
  status_code=status.HTTP_200_OK,
  response_model=BlogResponseDTO,
  response_model_exclude_none=True,
  responses={
    200: {"description": "Blog retrieved successfully."},
    404: {"description": "Blog not found."},
    500: {"description": "Internal Server Error."}
  }
)
@router.get(
  "/{blog_id}/",
  include_in_schema=False
)
def get_blog(
  request: Request,
  blog_id: str,
  session: Session = Depends(get_db)
):
  logger.info(f"Fetching blog with id: {blog_id}")
  blog_repository = BlogRepository(session)
  use_case = GetBlogUseCase(blog_repository)
  blog = use_case.get_by_id(blog_id)
  if blog is None:
    logger.warning(f"Blog with id: {blog_id} not found.")
    return JSONResponse(
      status_code=status.HTTP_404_NOT_FOUND,
      content={"detail": f"Blog with id '{blog_id}' not found."}
    )
  logger.info(f"Blog fetched: {blog.title} (id: {blog.id})")
  return blog

@router.get(
  "/author/{author_id}",
  status_code=status.HTTP_200_OK,
  response_model=PaginationResponseDTO[BlogResponseDTO],
  response_model_exclude_none=True,
  responses={
    200: {"description": "Blogs by author retrieved successfully."},
    400: {"description": "Bad Request."},
    500: {"description": "Internal Server Error."}
  }
)
@router.get(
  "/author/{author_id}/",
  include_in_schema=False
)
def get_blogs_by_author(
  request: Request,
  author_id: str,
  pagination: PaginationDTO = Depends(),
  session: Session = Depends(get_db)
):
  logger.info(f"Fetching blogs for author_id: {author_id} with pagination: skip: {pagination.skip}, limit: {pagination.limit}")
  blog_repository = BlogRepository(session)
  use_case = GetBlogUseCase(blog_repository)
  result = use_case.get_all_blogs_by_author(author_id, pagination)
  logger.info(f"Number of blogs fetched for author_id '{author_id}': {len(result.items)}")
  return result

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
def update_blog(
  request: Request,
  blog_id: str,
  blog_data: UpdateBlogDTO,
  session: Session = Depends(get_db)
):
  logger.info(f"Updating blog with id: {blog_id}")
  unit_of_work = get_uow(session)
  use_case = UpdateBlogUseCase(unit_of_work)
  updated_blog = use_case.execute(blog_id, blog_data)
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
def delete_blog(
  request: Request,
  blog_id: str,
  session: Session = Depends(get_db)
):
  logger.info(f"Deleting blog with id: {blog_id}")
  unit_of_work = get_uow(session)
  use_case = DeleteBlogUseCase(unit_of_work)
  use_case.execute(blog_id)
  logger.info(f"Blog with id: {blog_id} deleted successfully.")
  return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=f"Blog with id '{blog_id}' deleted successfully.")