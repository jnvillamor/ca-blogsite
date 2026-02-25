import pytest
from datetime import datetime, timezone
from src.application.dto import UpdateBlogDTO
from src.application.use_cases.blogs import UpdateBlogUseCase
from src.domain.entities import BlogEntity, UserEntity
from src.domain.exceptions import NotFoundException, UnauthorizedException 

@pytest.fixture
def unit_of_work(mocker):
  unit_of_work = mocker.MagicMock()
  unit_of_work.blogs = mocker.Mock()
  return unit_of_work

@pytest.fixture
def update_blog_use_case(unit_of_work):
  return UpdateBlogUseCase(
    unit_of_work=unit_of_work
  )

@pytest.fixture
def blog_data():
  return BlogEntity(
    id="blog-123",
    title="Original Title",
    content="Original content.",
    author_id="author-123",
    hero_image="http://example.com/original_hero.jpg",
    created_at=datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
    updated_at=datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
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
    created_at=datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
    updated_at=datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
  )

class TestUpdateBlogUseCase:
  @pytest.mark.parametrize(
    "title, content, hero_image",
    [
      (None, None, None),
      ("Updated Title", None, None),
      (None, "Updated content.", None),
      (None, None, "http://example.com/updated_hero.jpg"),
      ("Updated Title", "Updated content.", "http://example.com/updated_hero.jpg"),
    ]
  )
  def test_update_blog_success(
    self,
    update_blog_use_case,
    unit_of_work,
    blog_data,
    existing_user,
    title,
    content,
    hero_image
  ):
    unit_of_work.blogs.get_blog_by_id.return_value = blog_data
    update_data = UpdateBlogDTO(
      title=title,
      content=content,
      hero_image=hero_image
    )
    unit_of_work.blogs.update_blog.side_effect = lambda blog_id, blog: blog

    result = update_blog_use_case.execute(
      current_user=existing_user,
      blog_id=blog_data.id,
      blog_data=update_data
    )

    unit_of_work.blogs.get_blog_by_id.assert_called_once_with(blog_data.id)
    unit_of_work.blogs.update_blog.assert_called_once()

    assert result.title == title if title is not None else blog_data.title
    assert result.content == content if content is not None else blog_data.content
    assert result.hero_image == hero_image if hero_image is not None else blog_data.hero_image
    assert result.id == blog_data.id
    assert result.author_id == blog_data.author_id 
    assert result.created_at == blog_data.created_at
    assert result.updated_at == blog_data.updated_at
    
  def test_update_blog_not_found(
    self,
    update_blog_use_case,
    unit_of_work,
    blog_data,
    existing_user
  ):
    unit_of_work.blogs.get_blog_by_id.return_value = None
    update_data = UpdateBlogDTO(
      title="Updated Title"
    )

    with pytest.raises(NotFoundException) as exc_info:
      update_blog_use_case.execute(
        current_user=existing_user,
        blog_id=blog_data.id,
        blog_data=update_data
      )
    
    unit_of_work.blogs.get_blog_by_id.assert_called_once_with(blog_data.id)
    unit_of_work.blogs.update_blog.assert_not_called()

    assert str(exc_info.value) == f"Blog with identifier 'blog_id: {blog_data.id}' was not found."
  
  def test_execute_unauthorized(
    self,
    update_blog_use_case,
    unit_of_work,
    blog_data,
    existing_user
  ):
    unit_of_work.blogs.get_blog_by_id.return_value = blog_data
    update_data = UpdateBlogDTO(
      title="Updated Title"
    )

    with pytest.raises(UnauthorizedException) as exc_info:
      update_blog_use_case.execute(
        current_user=UserEntity(
          id="different_user",
          first_name="Bob",
          last_name="Johnson",
          username="bobjohnson",
          password="hashedpassword",
          avatar=None,
          created_at=datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
          updated_at=datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        ),
        blog_id=blog_data.id,
        blog_data=update_data
      )
    
    unit_of_work.blogs.get_blog_by_id.assert_called_once_with(blog_data.id)
    unit_of_work.blogs.update_blog.assert_not_called()

    assert str(exc_info.value) == "You are not authorized to update this blog."