import pytest
import re
from sqlalchemy.orm import Session
from app.database.unit_of_work import UnitOfWork
from app.services import UuidGenerator
from src.application.dto import CreateBlogDTO
from src.application.use_cases.blog import CreateBlogUseCase
from src.domain.exceptions import NotFoundException

@pytest.fixture
def create_blog_use_case(db_session: Session) -> CreateBlogUseCase:
  unit_of_work = UnitOfWork(db_session)
  id_generator = UuidGenerator()
  return CreateBlogUseCase(
    unit_of_work=unit_of_work,
    id_generator=id_generator
  )

class TestCreateBlogUseCase:
  def test_create_blog_success(
    self, 
    db_session: Session,
    create_test_user,
    create_blog_use_case: CreateBlogUseCase
  ):
    # First, create a test user to be the author of the blog
    test_user = create_test_user()
    author_id = test_user.id

    blog_data = CreateBlogDTO(
      title="My First Blog",
      content="This is the content of my first blog.",
      author_id=author_id
    )

    created_blog = create_blog_use_case.execute(blog_data)
    
    assert created_blog.id is not None
    assert created_blog.title == "My First Blog"
    assert created_blog.content == "This is the content of my first blog."
    assert created_blog.author_id == author_id
    assert created_blog.created_at is not None
    assert created_blog.updated_at is not None
  
  def test_create_blog_invalid_author(
    self, 
    db_session: Session,
    create_blog_use_case: CreateBlogUseCase
  ):
    blog_data = CreateBlogDTO(
      title="Invalid Author Blog",
      content="This blog has an invalid author.",
      author_id="non-existent-author-id"
    )

    with pytest.raises(Exception) as exc_info:
      create_blog_use_case.execute(blog_data)
    
    assert isinstance(exc_info.value, NotFoundException)
    assert "User with identifier 'user_id: non-existent-author-id' was not found." in str(exc_info.value)

  @pytest.mark.parametrize(
    "title, error_regex",
    [
      ("", r"Title cannot be empty."),
      (" " * 10, r"Title cannot be empty."),
      ("Shrt", r"Title must be at least 5 characters long."),
      ("T" * 101, r"Title cannot exceed 100 characters.")
    ]
  )
  def test_create_blog_invalid_title(
    self,
    db_session: Session,
    create_test_user,
    create_blog_use_case: CreateBlogUseCase,
    title,
    error_regex
  ):
    test_user = create_test_user()
    author_id = test_user.id

    blog_data = CreateBlogDTO(
      title=title,
      content="Valid content for testing invalid title.",
      author_id=author_id
    )

    with pytest.raises(Exception, match=error_regex) as exc_info:
      create_blog_use_case.execute(blog_data)
    
    assert isinstance(exc_info.value, Exception)
    assert re.search(error_regex, str(exc_info.value)) is not None

  @pytest.mark.parametrize(
    "content, error_regex",
    [
      ("", r"Content cannot be empty."),
      (" " * 10, r"Content cannot be empty.")
    ]
  )
  def test_create_blog_invalid_content(
    self,
    db_session: Session,
    create_test_user,
    create_blog_use_case: CreateBlogUseCase,
    content,
    error_regex
  ):
    test_user = create_test_user()
    author_id = test_user.id

    blog_data = CreateBlogDTO(
      title="Valid Title for Testing Invalid Content",
      content=content,
      author_id=author_id
    )

    with pytest.raises(Exception, match=error_regex) as exc_info:
      create_blog_use_case.execute(blog_data)
    
    assert isinstance(exc_info.value, Exception)
    assert re.search(error_regex, str(exc_info.value)) is not None