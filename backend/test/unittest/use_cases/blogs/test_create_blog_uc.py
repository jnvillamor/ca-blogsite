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
    "title, error_regex",
    [
      ("", r"Title cannot be empty."),
      (" " * 10, r"Title cannot be empty."),
      ("Shrt", r"Title must be at least 5 characters long."),
      ("T" * 101, r"Title cannot exceed 100 characters.")
    ]
  )
  async def test_execute_invalid_title(
    self,
    create_blog_use_case,
    blog_data,
    unit_of_work,
    existing_user,
    title,
    error_regex
  ):
    blog_data.title = title

    unit_of_work.users.get_user_by_id.return_value = existing_user

    with pytest.raises(InvalidDataException, match=error_regex):
      await create_blog_use_case.execute(blog_data)

    unit_of_work.users.get_user_by_id.assert_awaited_once_with(blog_data.author_id)


  @pytest.mark.asyncio
  @pytest.mark.parametrize(
    "content, error_regex",
    [
      ("", r"Content cannot be empty."),
      (" " * 10, r"Content cannot be empty.")
    ]
  )
  async def test_execute_invalid_content(
    self,
    create_blog_use_case,
    blog_data,
    unit_of_work,
    existing_user,
    content,
    error_regex
  ):
    blog_data.content = content

    unit_of_work.users.get_user_by_id.return_value = existing_user

    with pytest.raises(InvalidDataException, match=error_regex):
      await create_blog_use_case.execute(blog_data)

    unit_of_work.users.get_user_by_id.assert_awaited_once_with(blog_data.author_id)