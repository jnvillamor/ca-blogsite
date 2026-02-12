import pytest
from src.application.use_cases.blogs import DeleteBlogUseCase
from src.domain.exceptions import NotFoundException

@pytest.fixture
def unit_of_work(mocker):
  unit_of_work = mocker.MagicMock()
  unit_of_work.blogs = mocker.Mock()
  return unit_of_work

@pytest.fixture
def delete_blog_use_case(unit_of_work):
  return DeleteBlogUseCase(unit_of_work=unit_of_work)

class TestDeleteBlogUseCase:
  def test_execute_success(self, mocker, delete_blog_use_case, unit_of_work):
    blog_id = "blog-123"
    unit_of_work.blogs.get_blog_by_id.return_value = mocker.MagicMock()

    delete_blog_use_case.execute(blog_id)

    unit_of_work.blogs.delete_blog.assert_called_once_with(blog_id)

  def test_execute_blog_not_found(self, delete_blog_use_case, unit_of_work):
    blog_id = "nonexistent-blog"
    unit_of_work.blogs.get_blog_by_id.return_value = None

    with pytest.raises(NotFoundException) as exc_info:
      delete_blog_use_case.execute(blog_id)

    assert str(exc_info.value) == "Blog with identifier 'blog_id: nonexistent-blog' was not found."
    unit_of_work.blogs.delete_blog.assert_not_called()