import pytest
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from .utils import _normalize_datetime
from app.repositories import BlogRepository
from src.domain.entities import BlogEntity
from src.domain.exceptions import NotFoundException

class TestBlogRepository:
  def test_create_and_get_blog(self, db_session: Session):
    repo = BlogRepository(db_session)
    blog = BlogEntity(
      id="blog123",
      title="Test Blog",
      content="This is a test blog.",
      author_id="user123",
      created_at=datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
      updated_at=datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    )
    repo.create_blog(blog)

    # get by id
    retrieved = repo.get_blog_by_id("blog123")
    assert retrieved is not None
    assert retrieved.id == blog.id
    assert retrieved.title == blog.title
    assert retrieved.content == blog.content
    assert retrieved.author_id == blog.author_id
    assert _normalize_datetime(retrieved.created_at) == _normalize_datetime(blog.created_at)
    assert _normalize_datetime(retrieved.updated_at) == _normalize_datetime(blog.updated_at)
  
  def test_get_all_blogs(self, db_session: Session):
    repo = BlogRepository(db_session)
    # create multiple blogs
    for i in range(15):
      blog = BlogEntity(
        id=f"blog{i}",
        title=f"Blog {i}",
        content="Content",
        author_id="user123",
        created_at=datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        updated_at=datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
      )
      repo.create_blog(blog)

    blogs, total = repo.get_all_blogs(skip=0, limit=10)
    assert total == 15
    assert len(blogs) == 10
    assert blogs[0].id == "blog0"
    assert blogs[9].id == "blog9"
    blogs_page_2, _ = repo.get_all_blogs(skip=10, limit=10)
    assert len(blogs_page_2) == 5
    assert blogs_page_2[0].id == "blog10"
    assert blogs_page_2[4].id == "blog14"
    blogs_search, total_search = repo.get_all_blogs(search="Blog 1")
    assert total_search == 6  # Blog 1, Blog 10, Blog 11, Blog 12, Blog 13, Blog 14
    assert len(blogs_search) == 6
    assert blogs_search[0].id == "blog1"
    assert blogs_search[1].id == "blog10"
    assert blogs_search[2].id == "blog11"
    assert blogs_search[3].id == "blog12"
    assert blogs_search[4].id == "blog13"
    assert blogs_search[5].id == "blog14"
    blogs_page, total = repo.get_all_blogs(skip=0, limit=20)
    assert total == 15
    assert len(blogs_page) == 15
    assert blogs_page[0].id == "blog0"
    assert blogs_page[14].id == "blog14"
    
  def test_get_nonexistent_blog(self, db_session: Session):
    repo = BlogRepository(db_session)
    retrieved = repo.get_blog_by_id("nonexistent_blog")
    assert retrieved is None
  
  def test_get_all_blogs_by_author(self, db_session: Session):
    repo = BlogRepository(db_session)
    # create blogs for multiple authors
    for i in range(10):
      blog = BlogEntity(
        id=f"blog{i}",
        title=f"Blog {i}",
        content="Content",
        author_id="user123" if i < 5 else "user456",
        created_at=datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        updated_at=datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
      )
      repo.create_blog(blog)

    blogs_user123, total_user123 = repo.get_all_blogs_by_author("user123")
    assert total_user123 == 5
    assert len(blogs_user123) == 5
    assert blogs_user123[0].id == "blog0"
    assert blogs_user123[4].id == "blog4"
    blogs_user456, total_user456 = repo.get_all_blogs_by_author("user456")
    assert total_user456 == 5
    assert len(blogs_user456) == 5
    assert blogs_user456[0].id == "blog5"
    assert blogs_user456[4].id == "blog9"
    blogs_user123_search, total_user123_search = repo.get_all_blogs_by_author("user123", search="Blog 1")
    assert total_user123_search == 1
    assert len(blogs_user123_search) == 1
    assert blogs_user123_search[0].id == "blog1"
    blogs_user456_search, total_user456_search = repo.get_all_blogs_by_author("user456", search="Blog 1")
    assert total_user456_search == 0
    assert len(blogs_user456_search) == 0

  def test_update_blog(self, db_session: Session):
    repo = BlogRepository(db_session)
    blog = BlogEntity(
      id="blog123",
      title="Test Blog",
      content="This is a test blog.",
      author_id="user123",
      created_at=datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
      updated_at=datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    )
    repo.create_blog(blog)
    # update blog
    updated_blog = BlogEntity(
      id="blog123",
      title="Updated Blog",
      content="This is an updated test blog.",
      author_id="user123",
      created_at=blog.created_at,
      updated_at=datetime(2024, 1, 2, 0, 0, 0, tzinfo=timezone.utc)
    )
    repo.update_blog("blog123", updated_blog)
    retrieved = repo.get_blog_by_id("blog123")
    assert retrieved is not None
    assert retrieved.id == updated_blog.id
    assert retrieved.title == updated_blog.title
    assert retrieved.content == updated_blog.content
    assert retrieved.author_id == updated_blog.author_id
    assert _normalize_datetime(retrieved.created_at) == _normalize_datetime(updated_blog.created_at)
    assert _normalize_datetime(retrieved.updated_at) == _normalize_datetime(updated_blog.updated_at)
  
  def test_update_nonexistent_blog(self, db_session: Session):
    repo = BlogRepository(db_session)
    blog = BlogEntity(
      id="blog123",
      title="Test Blog",
      content="This is a test blog.",
      author_id="user123",
      created_at=datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
      updated_at=datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    )
    with pytest.raises(NotFoundException):
      repo.update_blog("nonexistent_blog", blog)

  def test_delete_blog(self, db_session: Session):
    repo = BlogRepository(db_session)
    blog = BlogEntity(
      id="blog123",
      title="Test Blog",
      content="This is a test blog.",
      author_id="user123",
      created_at=datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
      updated_at=datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    )
    repo.create_blog(blog)
    # Check blog exists
    retrieved = repo.get_blog_by_id("blog123")
    assert retrieved is not None

    # delete blog
    repo.delete_blog("blog123")
    retrieved = repo.get_blog_by_id("blog123")
    assert retrieved is None