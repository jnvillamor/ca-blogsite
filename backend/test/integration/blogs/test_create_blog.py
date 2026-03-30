from app.database.unit_of_work import UnitOfWork
from app.services import UuidGenerator

from src.application.dto import CreateBlogDTO
from src.application.use_cases.blogs import CreateBlogUseCase
from src.domain.exceptions import InvalidDataException

import pytest
import re
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture
def create_blog_use_case(db_session: AsyncSession) -> CreateBlogUseCase:
  unit_of_work = UnitOfWork(db_session)
  id_generator = UuidGenerator()

  return CreateBlogUseCase(
    unit_of_work=unit_of_work,
    id_generator=id_generator
  )


class TestCreateBlogUseCase:

  @pytest.mark.asyncio
  async def test_create_blog_success(
    self,
    db_session: AsyncSession,
    create_test_user,
    create_blog_use_case: CreateBlogUseCase
  ):
    test_user = await create_test_user()
    author_id = test_user.id

    content_blocks = [{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "This is the content of my first blog.", "styles": {}}], "children": []}]
    blog_data = CreateBlogDTO(
      title="My First Blog",
      content=content_blocks,
      author_id=author_id
    )

    created_blog = await create_blog_use_case.execute(blog_data)

    assert created_blog.id is not None
    assert created_blog.title == "My First Blog"
    assert created_blog.content == content_blocks
    assert created_blog.author_id == author_id
    assert created_blog.created_at is not None
    assert created_blog.updated_at is not None


  @pytest.mark.asyncio
  async def test_create_blog_invalid_author(
    self,
    db_session: AsyncSession,
    create_blog_use_case: CreateBlogUseCase
  ):
    blog_data = CreateBlogDTO(
      title="Invalid Author Blog",
      content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "This blog has an invalid author.", "styles": {}}], "children": []}],
      author_id="non-existent-author-id"
    )

    with pytest.raises(Exception) as exc_info:
      await create_blog_use_case.execute(blog_data)

    assert isinstance(exc_info.value, InvalidDataException)
    assert "Author not found." in str(exc_info.value)


  @pytest.mark.asyncio
  @pytest.mark.parametrize(
    "title, error_regex",
    [
      ("", r"Title cannot be empty."),
      (" " * 10, r"Title cannot be empty."),
      ("Shrt", r"Title must be at least 5 characters long."),
      ("T" * 101, r"Title cannot exceed 100 characters.")
    ]
  )
  async def test_create_blog_invalid_title(
    self,
    db_session: AsyncSession,
    create_test_user,
    create_blog_use_case: CreateBlogUseCase,
    title,
    error_regex
  ):
    test_user = await create_test_user()
    author_id = test_user.id

    blog_data = CreateBlogDTO(
      title=title,
      content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Valid content for testing invalid title.", "styles": {}}], "children": []}],
      author_id=author_id
    )

    with pytest.raises(Exception, match=error_regex) as exc_info:
      await create_blog_use_case.execute(blog_data)

    assert isinstance(exc_info.value, Exception)
    assert re.search(error_regex, str(exc_info.value)) is not None


  @pytest.mark.asyncio
  async def test_create_blog_invalid_content_empty_list(
    self,
    db_session: AsyncSession,
    create_test_user,
    create_blog_use_case: CreateBlogUseCase,
  ):
    test_user = await create_test_user()
    author_id = test_user.id

    blog_data = CreateBlogDTO(
      title="Valid Title for Testing Invalid Content",
      content=[],
      author_id=author_id
    )

    with pytest.raises(Exception, match=r"Content cannot be empty.") as exc_info:
      await create_blog_use_case.execute(blog_data)

    assert isinstance(exc_info.value, Exception)
    assert re.search(r"Content cannot be empty.", str(exc_info.value)) is not None