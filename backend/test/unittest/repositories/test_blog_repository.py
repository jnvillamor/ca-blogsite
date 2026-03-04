import pytest
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from .utils import _normalize_datetime
from app.repositories import BlogRepository
from src.domain.entities import BlogEntity
from src.domain.exceptions import NotFoundException


class TestBlogRepository:

  @pytest.mark.asyncio
  async def test_create_and_get_blog(self, db_session: AsyncSession):
    repo = BlogRepository(db_session)

    blog = BlogEntity(
      id="blog123",
      title="Test Blog",
      content="This is a test blog.",
      author_id="user123",
      created_at=datetime(2024,1,1,tzinfo=timezone.utc),
      updated_at=datetime(2024,1,1,tzinfo=timezone.utc)
    )

    await repo.create_blog(blog)

    retrieved = await repo.get_blog_by_id("blog123")

    assert retrieved is not None
    assert retrieved.id == blog.id
    assert retrieved.title == blog.title
    assert retrieved.content == blog.content
    assert retrieved.author_id == blog.author_id
    assert _normalize_datetime(retrieved.created_at) == _normalize_datetime(blog.created_at)
    assert _normalize_datetime(retrieved.updated_at) == _normalize_datetime(blog.updated_at)


  @pytest.mark.asyncio
  async def test_get_all_blogs(self, db_session: AsyncSession):
    repo = BlogRepository(db_session)

    for i in range(15):
      blog = BlogEntity(
        id=f"blog{i}",
        title=f"Blog {i}",
        content="Content",
        author_id="user123",
        created_at=datetime(2024,1,1,tzinfo=timezone.utc),
        updated_at=datetime(2024,1,1,tzinfo=timezone.utc)
      )
      await repo.create_blog(blog)

    blogs, total = await repo.get_all_blogs(skip=0, limit=10)

    assert total == 15
    assert len(blogs) == 10
    assert blogs[0].id == "blog0"
    assert blogs[9].id == "blog9"

    blogs_page_2, _ = await repo.get_all_blogs(skip=10, limit=10)

    assert len(blogs_page_2) == 5
    assert blogs_page_2[0].id == "blog10"
    assert blogs_page_2[4].id == "blog14"

    blogs_search, total_search = await repo.get_all_blogs(search="Blog 1")

    assert total_search == 6
    assert len(blogs_search) == 6


  @pytest.mark.asyncio
  async def test_get_nonexistent_blog(self, db_session: AsyncSession):
    repo = BlogRepository(db_session)

    retrieved = await repo.get_blog_by_id("nonexistent_blog")

    assert retrieved is None


  @pytest.mark.asyncio
  async def test_get_all_blogs_by_author(self, db_session: AsyncSession):
    repo = BlogRepository(db_session)

    for i in range(10):
      blog = BlogEntity(
        id=f"blog{i}",
        title=f"Blog {i}",
        content="Content",
        author_id="user123" if i < 5 else "user456",
        created_at=datetime(2024,1,1,tzinfo=timezone.utc),
        updated_at=datetime(2024,1,1,tzinfo=timezone.utc)
      )
      await repo.create_blog(blog)

    blogs_user123, total_user123 = await repo.get_all_blogs_by_author("user123")

    assert total_user123 == 5
    assert len(blogs_user123) == 5

    blogs_user456, total_user456 = await repo.get_all_blogs_by_author("user456")

    assert total_user456 == 5
    assert len(blogs_user456) == 5


  @pytest.mark.asyncio
  async def test_get_all_blogs_with_search(self, db_session: AsyncSession):
    repo = BlogRepository(db_session)

    for i in range(10):
      blog = BlogEntity(
        id=f"blog{i}",
        title=f"Test Blog {i}",
        content="Content",
        author_id="user123",
        created_at=datetime(2024,1,1,tzinfo=timezone.utc),
        updated_at=datetime(2024,1,1,tzinfo=timezone.utc)
      )
      await repo.create_blog(blog)

    blogs_search, total_search = await repo.get_all_blogs(search="Test Blog 1")

    assert total_search == 1
    assert blogs_search[0].id == "blog1"

    blogs_search, total_search = await repo.get_all_blogs(search="Test Blog")

    assert total_search == 10


  @pytest.mark.asyncio
  async def test_update_blog(self, db_session: AsyncSession):
    repo = BlogRepository(db_session)

    blog = BlogEntity(
      id="blog123",
      title="Test Blog",
      content="This is a test blog.",
      author_id="user123",
      created_at=datetime(2024,1,1,tzinfo=timezone.utc),
      updated_at=datetime(2024,1,1,tzinfo=timezone.utc)
    )

    await repo.create_blog(blog)

    updated_blog = BlogEntity(
      id="blog123",
      title="Updated Blog",
      content="Updated content",
      author_id="user123",
      created_at=blog.created_at,
      updated_at=datetime(2024,1,2,tzinfo=timezone.utc)
    )

    await repo.update_blog("blog123", updated_blog)

    retrieved = await repo.get_blog_by_id("blog123")

    assert retrieved is not None
    assert retrieved.title == "Updated Blog"
    assert retrieved.content == "Updated content"


  @pytest.mark.asyncio
  async def test_update_nonexistent_blog(self, db_session: AsyncSession):
    repo = BlogRepository(db_session)

    blog = BlogEntity(
      id="blog123",
      title="Test Blog",
      content="Content",
      author_id="user123",
      created_at=datetime(2024,1,1,tzinfo=timezone.utc),
      updated_at=datetime(2024,1,1,tzinfo=timezone.utc)
    )

    with pytest.raises(NotFoundException):
      await repo.update_blog("nonexistent_blog", blog)


  @pytest.mark.asyncio
  async def test_delete_blog(self, db_session: AsyncSession):
    repo = BlogRepository(db_session)

    blog = BlogEntity(
      id="blog123",
      title="Test Blog",
      content="Content",
      author_id="user123",
      created_at=datetime(2024,1,1,tzinfo=timezone.utc),
      updated_at=datetime(2024,1,1,tzinfo=timezone.utc)
    )

    await repo.create_blog(blog)

    retrieved = await repo.get_blog_by_id("blog123")
    assert retrieved is not None

    await repo.delete_blog("blog123")

    retrieved = await repo.get_blog_by_id("blog123")
    assert retrieved is None