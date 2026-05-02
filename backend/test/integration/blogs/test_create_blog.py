from app.database.unit_of_work import UnitOfWork
from app.services import UuidGenerator

from src.application.dto import CreateBlogDTO
from src.application.use_cases.blogs import CreateBlogUseCase
from src.domain.exceptions import InvalidDataException

import pytest
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
    "title",
    [
      "",
      " " * 10,
      "Shrt",
      "T" * 101,
    ],
    ids=["empty", "whitespace_only", "too_short", "too_long"]
  )
  async def test_create_blog_persists_draft_with_publish_invalid_title(
    self,
    db_session: AsyncSession,
    create_test_user,
    create_blog_use_case: CreateBlogUseCase,
    title
  ):
    """Drafts may carry titles that would be rejected at publish time.
    Create must accept and persist them. Publish-time invariants are tested
    in test_blog_entity.py / test_publish_blog_uc.py."""
    test_user = await create_test_user()
    author_id = test_user.id

    blog_data = CreateBlogDTO(
      title=title,
      content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Valid content for draft.", "styles": {}}], "children": []}],
      author_id=author_id
    )

    created_blog = await create_blog_use_case.execute(blog_data)

    # Title is normalized via `(value or "").strip()` inside Title.__init__.
    assert created_blog.title == title.strip()
    assert created_blog.status == "draft"
    assert created_blog.published_at is None


  @pytest.mark.asyncio
  async def test_create_blog_persists_draft_with_empty_content(
    self,
    db_session: AsyncSession,
    create_test_user,
    create_blog_use_case: CreateBlogUseCase,
  ):
    """Drafts may have an empty content list. Create must accept and persist."""
    test_user = await create_test_user()
    author_id = test_user.id

    blog_data = CreateBlogDTO(
      title="Valid Title for Empty Content Draft",
      content=[],
      author_id=author_id
    )

    created_blog = await create_blog_use_case.execute(blog_data)

    assert created_blog.content == []
    assert created_blog.status == "draft"
    assert created_blog.published_at is None


  @pytest.mark.asyncio
  async def test_create_blog_persists_empty_draft(
    self,
    db_session: AsyncSession,
    create_test_user,
    create_blog_use_case: CreateBlogUseCase,
  ):
    """Positive-path case the frontend's 'Write New Blog' relies on:
    a brand-new draft can be created with both empty title and empty content,
    and it is persisted as a draft."""
    test_user = await create_test_user()
    author_id = test_user.id

    blog_data = CreateBlogDTO(
      title="",
      content=[],
      author_id=author_id
    )

    created_blog = await create_blog_use_case.execute(blog_data)

    assert created_blog.id is not None
    assert created_blog.title == ""
    assert created_blog.content == []
    assert created_blog.author_id == author_id
    assert created_blog.status == "draft"
    assert created_blog.published_title is None
    assert created_blog.published_content is None
    assert created_blog.published_at is None