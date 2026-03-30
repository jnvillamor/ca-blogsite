import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Callable, Awaitable
from app.database.models import BlogModel, UserModel
from app.database.unit_of_work import UnitOfWork
from src.application.dto import UpdateBlogDTO
from src.application.use_cases.blogs import UpdateBlogUseCase
from src.domain.exceptions import NotFoundException


@pytest.fixture
def update_blog_use_case(db_session: AsyncSession) -> UpdateBlogUseCase:
  unit_of_work = UnitOfWork(db_session)
  return UpdateBlogUseCase(
    unit_of_work=unit_of_work,
  )


class TestUpdateBlogUseCase:

  @pytest.mark.asyncio
  async def test_update_blog_success(
    self,
    update_blog_use_case: UpdateBlogUseCase,
    create_test_user: Callable[..., Awaitable[UserModel]],
    create_test_blog: Callable[..., Awaitable[BlogModel]]
  ):
    test_user = await create_test_user()
    author_id = test_user.id

    test_blog = await create_test_blog(author_id=author_id)
    blog_id = test_blog.id

    updated_content = [{"id": "2", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "This is the updated content of the test blog.", "styles": {}}], "children": []}]
    update_dto = UpdateBlogDTO(
      title="Updated Blog Title",
      content=updated_content,
      hero_image="https://example.com/updated-hero-image.png"
    )

    updated_blog = await update_blog_use_case.execute(
      current_user=test_user,
      blog_id=blog_id,
      blog_data=update_dto
    )

    assert updated_blog.title == "Updated Blog Title"
    assert updated_blog.content == updated_content
    assert updated_blog.hero_image == "https://example.com/updated-hero-image.png"


  @pytest.mark.asyncio
  async def test_update_blog_non_existing(
    self,
    update_blog_use_case: UpdateBlogUseCase,
    create_test_user: Callable[..., Awaitable[UserModel]]
  ):
    update_dto = UpdateBlogDTO(
      title="Non-Existent Blog",
      content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "This blog does not exist.", "styles": {}}], "children": []}],
      hero_image="https://example.com/non-existent-hero-image.png"
    )

    test_user = await create_test_user()

    with pytest.raises(NotFoundException) as exc_info:
      await update_blog_use_case.execute(
        current_user=test_user,
        blog_id="non-existing-id",
        blog_data=update_dto
      )

    assert "Blog with identifier 'blog_id: non-existing-id' was not found." in str(exc_info.value)


  @pytest.mark.asyncio
  @pytest.mark.parametrize(
    "field, invalid_value, error_regex",
    [
      ("title", "", r"Title cannot be empty"),
      ("title", "A" * 101, r"Title cannot exceed \d+ characters"),
      ("content", [], r"Content cannot be empty"),
    ]
  )
  async def test_update_blog_validation_errors(
    self,
    update_blog_use_case: UpdateBlogUseCase,
    create_test_user: Callable[..., Awaitable[UserModel]],
    create_test_blog: Callable[..., Awaitable[BlogModel]],
    field: str,
    invalid_value,
    error_regex: str
  ):
    test_user = await create_test_user()
    author_id = test_user.id

    test_blog = await create_test_blog(author_id=author_id)
    blog_id = test_blog.id

    update_data = {
      "title": "Valid Title",
      "content": [{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Valid content for the blog.", "styles": {}}], "children": []}],
      "hero_image": "https://example.com/valid-hero-image.png"
    }

    update_data[field] = invalid_value
    update_dto = UpdateBlogDTO(**update_data)

    with pytest.raises(Exception, match=error_regex):
      await update_blog_use_case.execute(
        current_user=test_user,
        blog_id=blog_id,
        blog_data=update_dto
      )


  @pytest.mark.asyncio
  async def test_update_blog_unauthorized(
    self,
    update_blog_use_case: UpdateBlogUseCase,
    create_test_user: Callable[..., Awaitable[UserModel]],
    create_test_blog: Callable[..., Awaitable[BlogModel]]
  ):
    test_user = await create_test_user()
    author_id = test_user.id

    test_blog = await create_test_blog(author_id=author_id)
    blog_id = test_blog.id

    unauthorized_user = await create_test_user(
      username="unauthorizeduser",
      id="unauthorized-user-id"
    )

    update_dto = UpdateBlogDTO(
      title="Updated Title",
      content=[{"id": "2", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Updated content.", "styles": {}}], "children": []}],
      hero_image="https://example.com/updated-hero-image.png"
    )

    with pytest.raises(Exception, match=r"You are not authorized to update this blog."):
      await update_blog_use_case.execute(
        current_user=unauthorized_user,
        blog_id=blog_id,
        blog_data=update_dto
      )