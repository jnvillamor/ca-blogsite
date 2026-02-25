import pytest
from datetime import datetime, timezone
from src.application.use_cases.blogs import DeleteBlogUseCase
from src.domain.entities import UserEntity
from src.domain.exceptions import NotFoundException, UnauthorizedException

@pytest.fixture
def unit_of_work(mocker):
  unit_of_work = mocker.MagicMock()
  unit_of_work.blogs = mocker.Mock()
  return unit_of_work

@pytest.fixture
def delete_blog_use_case(unit_of_work):
  return DeleteBlogUseCase(unit_of_work=unit_of_work)

@pytest.fixture
def existing_user():
  return UserEntity(
    id="user123",
    first_name="Alice",
    last_name="Smith",
    username="alicesmith",
    password="hashedpassword",
    avatar=None,
    created_at=datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
    updated_at=datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
  )
  
class TestDeleteBlogUseCase:
  def test_execute_success(
    self, 
    mocker, 
    delete_blog_use_case, 
    unit_of_work,
    existing_user
  ):
    blog_id = "blog-123"
    unit_of_work.blogs.get_blog_by_id.return_value = mocker.MagicMock(author_id=existing_user.id)

    delete_blog_use_case.execute(current_user=existing_user, blog_id=blog_id)

    unit_of_work.blogs.delete_blog.assert_called_once_with(blog_id)

  def test_execute_blog_not_found(self, delete_blog_use_case, unit_of_work, existing_user):
    blog_id = "nonexistent-blog"
    unit_of_work.blogs.get_blog_by_id.return_value = None

    with pytest.raises(NotFoundException) as exc_info:
      delete_blog_use_case.execute(current_user=existing_user, blog_id=blog_id)

    assert str(exc_info.value) == "Blog with identifier 'blog_id: nonexistent-blog' was not found."
    unit_of_work.blogs.delete_blog.assert_not_called()
  
  def test_execute_unauthorized(
    self, 
    mocker,
    delete_blog_use_case,
    unit_of_work,
    existing_user
  ):
    blog_id = "blog-123"
    unit_of_work.blogs.get_blog_by_id.return_value = mocker.MagicMock(author_id="different_user")

    with pytest.raises(UnauthorizedException) as exc_info:
      delete_blog_use_case.execute(current_user=existing_user, blog_id=blog_id)

    assert str(exc_info.value) == "You are not authorized to delete this blog."
    unit_of_work.blogs.delete_blog.assert_not_called()