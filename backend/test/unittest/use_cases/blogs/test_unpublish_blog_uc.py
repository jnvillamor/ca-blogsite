import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock

from src.application.dto import BlogResponseDTO
from src.application.use_cases.blogs import UnpublishBlogUseCase
from src.domain.entities import BlogEntity, UserEntity
from src.domain.exceptions import (
  InvalidDataException,
  NotFoundException,
  UnauthorizedException
)


@pytest.fixture
def unit_of_work(mocker):
  uow = mocker.MagicMock()

  uow.__aenter__ = AsyncMock(return_value=uow)
  uow.__aexit__ = AsyncMock(return_value=None)

  uow.blogs = mocker.Mock()
  uow.blogs.get_blog_by_id = AsyncMock()
  uow.blogs.update_blog = AsyncMock()

  return uow


@pytest.fixture
def unpublish_blog_use_case(unit_of_work):
  return UnpublishBlogUseCase(unit_of_work=unit_of_work)


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


@pytest.fixture
def published_blog():
  """A blog that has already been published — the precondition for unpublish().

  Built by constructing a draft and then calling .publish() on it so that
  status, published_title, published_content, and published_at are populated
  exactly the way the production code would have left them.
  """
  blog = BlogEntity(
    id="blog-123",
    title="My Published Blog",
    content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Published content here.", "styles": {}}], "children": []}],
    author_id="author-123",
    status="draft",
    hero_image="http://example.com/hero.jpg",
    created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
    updated_at=datetime(2024, 1, 1, tzinfo=timezone.utc)
  )
  blog.publish()
  return blog


@pytest.fixture
def draft_blog():
  """A blog that has never been published — used for the InvalidDataException case."""
  return BlogEntity(
    id="blog-123",
    title="My Draft Blog",
    content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Draft content here.", "styles": {}}], "children": []}],
    author_id="author-123",
    status="draft",
    hero_image="http://example.com/hero.jpg",
    created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
    updated_at=datetime(2024, 1, 1, tzinfo=timezone.utc)
  )


class TestUnpublishBlogUseCase:

  @pytest.mark.asyncio
  async def test_execute_success(
    self,
    unpublish_blog_use_case,
    unit_of_work,
    existing_user,
    published_blog
  ):
    # Sanity check the fixture is in the expected published state.
    assert published_blog.status == "published"
    assert published_blog.published_at is not None

    unit_of_work.blogs.get_blog_by_id.return_value = published_blog
    unit_of_work.blogs.update_blog.side_effect = lambda blog_id, blog: blog

    result = await unpublish_blog_use_case.execute(
      current_user=existing_user,
      blog_id="blog-123"
    )

    # Returned DTO reflects the unpublished state.
    assert isinstance(result, BlogResponseDTO)
    assert result.id == "blog-123"
    assert result.status == "draft"
    assert result.published_at is None
    # Published snapshot is intentionally retained on unpublish.
    assert result.published_title == "My Published Blog"
    assert result.published_content == published_blog.content
    assert result.title == "My Published Blog"
    assert result.content == published_blog.content

    unit_of_work.blogs.get_blog_by_id.assert_awaited_once_with("blog-123")
    unit_of_work.blogs.update_blog.assert_awaited_once_with("blog-123", published_blog)


  @pytest.mark.asyncio
  async def test_execute_blog_not_found(
    self,
    unpublish_blog_use_case,
    unit_of_work,
    existing_user
  ):
    unit_of_work.blogs.get_blog_by_id.return_value = None

    with pytest.raises(NotFoundException) as exc_info:
      await unpublish_blog_use_case.execute(
        current_user=existing_user,
        blog_id="nonexistent-blog"
      )

    assert str(exc_info.value) == "Blog with identifier 'blog_id: nonexistent-blog' was not found."

    unit_of_work.blogs.get_blog_by_id.assert_awaited_once_with("nonexistent-blog")
    unit_of_work.blogs.update_blog.assert_not_called()


  @pytest.mark.asyncio
  async def test_execute_unauthorized(
    self,
    unpublish_blog_use_case,
    unit_of_work,
    published_blog
  ):
    unit_of_work.blogs.get_blog_by_id.return_value = published_blog

    different_user = UserEntity(
      id="different-user",
      first_name="Bob",
      last_name="Johnson",
      username="bobjohnson",
      password="hashedpassword",
      avatar=None,
      created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
      updated_at=datetime(2024, 1, 1, tzinfo=timezone.utc)
    )

    with pytest.raises(UnauthorizedException) as exc_info:
      await unpublish_blog_use_case.execute(
        current_user=different_user,
        blog_id="blog-123"
      )

    assert str(exc_info.value) == "You are not authorized to unpublish this blog."

    unit_of_work.blogs.get_blog_by_id.assert_awaited_once_with("blog-123")
    unit_of_work.blogs.update_blog.assert_not_called()


  @pytest.mark.asyncio
  async def test_execute_rejects_already_draft_blog(
    self,
    unpublish_blog_use_case,
    unit_of_work,
    existing_user,
    draft_blog
  ):
    """A blog that was never published cannot be unpublished — the entity
    raises InvalidDataException and the use case must not persist anything."""
    unit_of_work.blogs.get_blog_by_id.return_value = draft_blog

    with pytest.raises(InvalidDataException, match=r"Only published blogs can be unpublished\."):
      await unpublish_blog_use_case.execute(
        current_user=existing_user,
        blog_id="blog-123"
      )

    unit_of_work.blogs.get_blog_by_id.assert_awaited_once_with("blog-123")
    unit_of_work.blogs.update_blog.assert_not_called()
