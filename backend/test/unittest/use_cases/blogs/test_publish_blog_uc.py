import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock

from src.application.dto import BlogResponseDTO
from src.application.use_cases.blogs import PublishBlogUseCase
from src.domain.entities import BlogEntity, UserEntity
from src.domain.exceptions import NotFoundException, UnauthorizedException


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
def publish_blog_use_case(unit_of_work):
  return PublishBlogUseCase(unit_of_work=unit_of_work)


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
def draft_blog():
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


class TestPublishBlogUseCase:

  @pytest.mark.asyncio
  async def test_execute_success(
    self,
    publish_blog_use_case,
    unit_of_work,
    existing_user,
    draft_blog
  ):
    unit_of_work.blogs.get_blog_by_id.return_value = draft_blog
    unit_of_work.blogs.update_blog.side_effect = lambda blog_id, blog: blog

    result = await publish_blog_use_case.execute(
      current_user=existing_user,
      blog_id="blog-123"
    )

    assert isinstance(result, BlogResponseDTO)
    assert result.id == "blog-123"
    assert result.status == "published"
    assert result.published_title == "My Draft Blog"
    assert result.published_content == draft_blog.content
    assert result.published_at is not None
    assert result.title == "My Draft Blog"
    assert result.content == draft_blog.content

    unit_of_work.blogs.get_blog_by_id.assert_awaited_once_with("blog-123")
    unit_of_work.blogs.update_blog.assert_awaited_once()


  @pytest.mark.asyncio
  async def test_execute_blog_not_found(
    self,
    publish_blog_use_case,
    unit_of_work,
    existing_user
  ):
    unit_of_work.blogs.get_blog_by_id.return_value = None

    with pytest.raises(NotFoundException) as exc_info:
      await publish_blog_use_case.execute(
        current_user=existing_user,
        blog_id="nonexistent-blog"
      )

    assert str(exc_info.value) == "Blog with identifier 'blog_id: nonexistent-blog' was not found."

    unit_of_work.blogs.get_blog_by_id.assert_awaited_once_with("nonexistent-blog")
    unit_of_work.blogs.update_blog.assert_not_called()


  @pytest.mark.asyncio
  async def test_execute_unauthorized(
    self,
    publish_blog_use_case,
    unit_of_work,
    draft_blog
  ):
    unit_of_work.blogs.get_blog_by_id.return_value = draft_blog

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
      await publish_blog_use_case.execute(
        current_user=different_user,
        blog_id="blog-123"
      )

    assert str(exc_info.value) == "You are not authorized to publish this blog."

    unit_of_work.blogs.get_blog_by_id.assert_awaited_once_with("blog-123")
    unit_of_work.blogs.update_blog.assert_not_called()
