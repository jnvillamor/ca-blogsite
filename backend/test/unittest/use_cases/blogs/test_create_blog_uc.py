import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock

from src.application.dto import CreateBlogDTO, BlogResponseDTO
from src.application.use_cases.blogs import CreateBlogUseCase
from src.domain.entities import UserEntity
from src.domain.exceptions import InvalidDataException


@pytest.fixture
def unit_of_work(mocker):
  uow = mocker.MagicMock()

  uow.__aenter__ = AsyncMock(return_value=uow)
  uow.__aexit__ = AsyncMock(return_value=None)

  uow.users = mocker.Mock()
  uow.blogs = mocker.Mock()

  uow.users.get_user_by_id = AsyncMock()
  uow.blogs.create_blog = AsyncMock()

  return uow


@pytest.fixture
def id_generator(mocker):
  return mocker.Mock()


@pytest.fixture
def create_blog_use_case(unit_of_work, id_generator):
  return CreateBlogUseCase(
    unit_of_work=unit_of_work,
    id_generator=id_generator
  )


@pytest.fixture
def blog_data():
  return CreateBlogDTO(
    title="Test Blog",
    content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "This is a test blog content.", "styles": {}}], "children": []}],
    author_id="author-123",
    hero_image="http://example.com/hero.jpg"
  )


@pytest.fixture
def existing_user():
  return UserEntity(
    id="author-123",
    first_name="Alice",
    last_name="Smith",
    username="alicesmith",
    password="hashedpassword",
    avatar=None,
    created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
    updated_at=datetime(2024, 1, 1, tzinfo=timezone.utc)
  )


class TestCreateBlogUseCase:

  @pytest.mark.asyncio
  async def test_execute_success(
    self,
    create_blog_use_case,
    blog_data,
    unit_of_work,
    id_generator,
    existing_user
  ):
    unit_of_work.users.get_user_by_id.return_value = existing_user
    id_generator.generate.return_value = "blog-123"

    unit_of_work.blogs.create_blog.side_effect = lambda blog: blog

    result = await create_blog_use_case.execute(blog_data)

    assert isinstance(result, BlogResponseDTO)
    assert result.id == "blog-123"
    assert result.title == blog_data.title
    assert result.content == blog_data.content
    assert result.author_id == blog_data.author_id
    assert result.hero_image == blog_data.hero_image
    assert result.status == "draft"
    assert result.published_title is None
    assert result.published_content is None
    assert result.published_at is None
    assert result.created_at is not None
    assert result.updated_at is not None

    unit_of_work.users.get_user_by_id.assert_awaited_once_with(blog_data.author_id)
    id_generator.generate.assert_called_once()
    unit_of_work.blogs.create_blog.assert_awaited_once()


  @pytest.mark.asyncio
  async def test_execute_user_not_found(
    self,
    create_blog_use_case,
    blog_data,
    unit_of_work
  ):
    unit_of_work.users.get_user_by_id.return_value = None

    with pytest.raises(InvalidDataException) as exc_info:
      await create_blog_use_case.execute(blog_data)

    assert str(exc_info.value) == "Author not found."

    unit_of_work.users.get_user_by_id.assert_awaited_once_with(blog_data.author_id)


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
  async def test_execute_accepts_invalid_publish_title_at_draft_time(
    self,
    create_blog_use_case,
    blog_data,
    unit_of_work,
    id_generator,
    existing_user,
    title
  ):
    """Drafts may carry titles that would fail publish-time invariants
    (empty, whitespace-only, too short, or too long). Create must not reject them.
    The publish-time invariants are exercised in test_blog_entity.py and
    test_publish_blog_uc.py.
    """
    blog_data.title = title

    unit_of_work.users.get_user_by_id.return_value = existing_user
    id_generator.generate.return_value = "blog-draft-1"
    unit_of_work.blogs.create_blog.side_effect = lambda blog: blog

    result = await create_blog_use_case.execute(blog_data)

    assert isinstance(result, BlogResponseDTO)
    assert result.id == "blog-draft-1"
    # Title is stored as-is after the value object's `(value or "").strip()` normalization.
    assert result.title == title.strip()
    assert result.status == "draft"

    unit_of_work.users.get_user_by_id.assert_awaited_once_with(blog_data.author_id)
    unit_of_work.blogs.create_blog.assert_awaited_once()


  @pytest.mark.asyncio
  async def test_execute_accepts_empty_content_at_draft_time(
    self,
    create_blog_use_case,
    blog_data,
    unit_of_work,
    id_generator,
    existing_user,
  ):
    """Drafts may have an empty content list. The empty-content invariant only
    fires at publish time."""
    blog_data.content = []

    unit_of_work.users.get_user_by_id.return_value = existing_user
    id_generator.generate.return_value = "blog-draft-2"
    unit_of_work.blogs.create_blog.side_effect = lambda blog: blog

    result = await create_blog_use_case.execute(blog_data)

    assert isinstance(result, BlogResponseDTO)
    assert result.id == "blog-draft-2"
    assert result.content == []
    assert result.status == "draft"

    unit_of_work.users.get_user_by_id.assert_awaited_once_with(blog_data.author_id)
    unit_of_work.blogs.create_blog.assert_awaited_once()


  @pytest.mark.asyncio
  async def test_execute_creates_empty_draft(
    self,
    create_blog_use_case,
    blog_data,
    unit_of_work,
    id_generator,
    existing_user,
  ):
    """Positive-path case the frontend relies on: clicking 'Write New Blog'
    creates a brand-new draft with empty title and empty content."""
    blog_data.title = ""
    blog_data.content = []

    unit_of_work.users.get_user_by_id.return_value = existing_user
    id_generator.generate.return_value = "blog-empty-draft"
    unit_of_work.blogs.create_blog.side_effect = lambda blog: blog

    result = await create_blog_use_case.execute(blog_data)

    assert isinstance(result, BlogResponseDTO)
    assert result.id == "blog-empty-draft"
    assert result.title == ""
    assert result.content == []
    assert result.status == "draft"
    assert result.published_title is None
    assert result.published_content is None
    assert result.published_at is None

    unit_of_work.blogs.create_blog.assert_awaited_once()