import pytest
from datetime import datetime, timezone
from src.application.dto import CreateBlogDTO, BlogResponseDTO
from src.application.use_cases.blogs import CreateBlogUseCase
from src.domain.entities import UserEntity
from src.domain.exceptions import NotFoundException, InvalidDataException

@pytest.fixture
def unit_of_work(mocker):
  unit_of_work = mocker.MagicMock()
  unit_of_work.users = mocker.Mock()
  unit_of_work.blogs = mocker.Mock()
  return unit_of_work

@pytest.fixture
def id_generator(mocker):
  id_gen = mocker.Mock()
  return id_gen

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
    content="This is a test blog content.",
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
    created_at=datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
    updated_at=datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
  )

class TestCreateBlogUseCase:
  def test_execute_success(
    self,
    create_blog_use_case,
    blog_data,
    unit_of_work,
    id_generator
  ):
    unit_of_work.users.get_user_by_id.return_value = existing_user
    id_generator.generate.return_value = "blog-123"

    unit_of_work.blogs.create_blog.side_effect = lambda blog: blog

    result = create_blog_use_case.execute(blog_data)

    assert type(result) == BlogResponseDTO
    assert result.id == "blog-123"
    assert result.title == blog_data.title
    assert result.content == blog_data.content
    assert result.author_id == blog_data.author_id
    assert result.hero_image == blog_data.hero_image
    assert result.created_at is not None
    assert result.updated_at is not None

    unit_of_work.users.get_user_by_id.assert_called_once_with(blog_data.author_id)
    id_generator.generate.assert_called_once()
    unit_of_work.blogs.create_blog.assert_called_once()
  
  def test_execute_user_not_found(
    self,
    create_blog_use_case,
    blog_data,
    unit_of_work
  ):
    unit_of_work.users.get_user_by_id.return_value = None

    with pytest.raises(NotFoundException) as exc_info:
      create_blog_use_case.execute(blog_data)

    assert str(exc_info.value) == f"User with identifier 'user_id: {blog_data.author_id}' was not found."
    unit_of_work.users.get_user_by_id.assert_called_once_with(blog_data.author_id)
  
  @pytest.mark.parametrize(
    "title, error_regex",
    [
      ("", r"Title cannot be empty."),
      (" " * 10, r"Title cannot be empty."),
      ("Shrt", r"Title must be at least 5 characters long."),
      ("T" * 101, r"Title cannot exceed 100 characters.")
    ]
  )
  def test_execute_invalid_title(
    self,
    create_blog_use_case,
    blog_data,
    unit_of_work,
    title,
    error_regex
  ):
    blog_data.title = title
    unit_of_work.users.get_user_by_id.return_value = existing_user

    with pytest.raises(InvalidDataException, match=error_regex):
      create_blog_use_case.execute(blog_data)

    unit_of_work.users.get_user_by_id.assert_called_once_with(blog_data.author_id)
  
  @pytest.mark.parametrize(
    "content, error_regex",
    [
      ("", r"Content cannot be empty."),
      (" " * 10, r"Content cannot be empty.")
    ]
  )
  def test_execute_invalid_content(
    self,
    create_blog_use_case,
    blog_data,
    unit_of_work,
    content,
    error_regex
  ):
    blog_data.content = content
    unit_of_work.users.get_user_by_id.return_value = existing_user

    with pytest.raises(InvalidDataException, match=error_regex):
      create_blog_use_case.execute(blog_data)

    unit_of_work.users.get_user_by_id.assert_called_once_with(blog_data.author_id)