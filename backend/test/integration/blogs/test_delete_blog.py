from app.database.models import BlogModel
from app.database.unit_of_work import UnitOfWork

from src.application.use_cases.blogs import DeleteBlogUseCase
from src.domain.exceptions import NotFoundException, UnauthorizedException

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

@pytest.fixture
def delete_blog_use_case(db_session: AsyncSession) -> DeleteBlogUseCase:
  unit_of_work = UnitOfWork(session=db_session)
  use_case = DeleteBlogUseCase(unit_of_work=unit_of_work)
  return use_case


class TestDeleteBlogUseCase:

  @pytest.mark.asyncio
  async def test_delete_blog_success(
    self,
    db_session: AsyncSession,
    create_test_blog,
    create_test_user,
    delete_blog_use_case: DeleteBlogUseCase,
  ):
    test_user = await create_test_user()
    test_blog = await create_test_blog(author_id=test_user.id)

    # Test if blog exists before deletion
    result = await db_session.execute(
      select(BlogModel).where(BlogModel.id == test_blog.id)
    )
    blog_in_db: BlogModel | None = result.scalar_one_or_none()

    assert blog_in_db is not None
    assert blog_in_db.title == test_blog.title
    assert blog_in_db.id == test_blog.id

    await delete_blog_use_case.execute(
      current_user=test_user,
      blog_id=test_blog.id
    )

    # Test if blog is deleted
    result = await db_session.execute(
      select(BlogModel).where(BlogModel.id == test_blog.id)
    )
    blog_after_delete = result.scalar_one_or_none()

    assert blog_after_delete is None


  @pytest.mark.asyncio
  async def test_delete_blog_non_existing(
    self,
    create_test_user,
    delete_blog_use_case: DeleteBlogUseCase,
  ):
    test_user = await create_test_user()
    non_existing_blog_id = "non-existing-id"

    with pytest.raises(NotFoundException) as exc_info:
      await delete_blog_use_case.execute(
        current_user=test_user,
        blog_id=non_existing_blog_id
      )

    assert "Blog with identifier 'blog_id: non-existing-id' was not found." in str(exc_info.value)


  @pytest.mark.asyncio
  async def test_delete_blog_unauthorized(
    self,
    create_test_blog,
    create_test_user,
    delete_blog_use_case: DeleteBlogUseCase,
  ):
    test_blog = await create_test_blog()
    unauthorized_user = await create_test_user(
      id="unauthorized-user-id",
      username="unauthorizeduser"
    )

    with pytest.raises(UnauthorizedException) as exc_info:
      await delete_blog_use_case.execute(
        current_user=unauthorized_user,
        blog_id=test_blog.id
      )

    assert "You are not authorized to delete this blog." in str(exc_info.value)