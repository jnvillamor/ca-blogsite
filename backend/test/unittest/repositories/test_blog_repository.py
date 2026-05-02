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
      content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "This is a test blog.", "styles": {}}], "children": []}],
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
  async def test_get_all_public_blogs(self, db_session: AsyncSession):
    repo = BlogRepository(db_session)

    for i in range(15):
      blog = BlogEntity(
        id=f"blog{i}",
        title=f"Blog {i}",
        content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Content", "styles": {}}], "children": []}],
        author_id="user123",
        status="published",
        published_title=f"Blog {i}",
        published_content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Content", "styles": {}}], "children": []}],
        published_at=datetime(2024, 6, 1, tzinfo=timezone.utc),
        created_at=datetime(2024,1,1,tzinfo=timezone.utc),
        updated_at=datetime(2024,1,1,tzinfo=timezone.utc)
      )
      await repo.create_blog(blog)

    blogs, total = await repo.get_all_public_blogs(skip=0, limit=10)

    assert total == 15
    assert len(blogs) == 10
    assert blogs[0].id == "blog0"
    assert blogs[9].id == "blog9"

    blogs_page_2, _ = await repo.get_all_public_blogs(skip=10, limit=10)

    assert len(blogs_page_2) == 5
    assert blogs_page_2[0].id == "blog10"
    assert blogs_page_2[4].id == "blog14"

    blogs_search, total_search = await repo.get_all_public_blogs(search="Blog 1")

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
        content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Content", "styles": {}}], "children": []}],
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
  async def test_get_all_public_blogs_with_search(self, db_session: AsyncSession):
    repo = BlogRepository(db_session)

    for i in range(10):
      blog = BlogEntity(
        id=f"blog{i}",
        title=f"Test Blog {i}",
        content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Content", "styles": {}}], "children": []}],
        author_id="user123",
        status="published",
        published_title=f"Test Blog {i}",
        published_content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Content", "styles": {}}], "children": []}],
        published_at=datetime(2024, 6, 1, tzinfo=timezone.utc),
        created_at=datetime(2024,1,1,tzinfo=timezone.utc),
        updated_at=datetime(2024,1,1,tzinfo=timezone.utc)
      )
      await repo.create_blog(blog)

    blogs_search, total_search = await repo.get_all_public_blogs(search="Test Blog 1")

    assert total_search == 1
    assert blogs_search[0].id == "blog1"

    blogs_search, total_search = await repo.get_all_public_blogs(search="Test Blog")

    assert total_search == 10


  @pytest.mark.asyncio
  async def test_update_blog(self, db_session: AsyncSession):
    repo = BlogRepository(db_session)

    blog = BlogEntity(
      id="blog123",
      title="Test Blog",
      content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "This is a test blog.", "styles": {}}], "children": []}],
      author_id="user123",
      created_at=datetime(2024,1,1,tzinfo=timezone.utc),
      updated_at=datetime(2024,1,1,tzinfo=timezone.utc)
    )

    await repo.create_blog(blog)

    updated_blog = BlogEntity(
      id="blog123",
      title="Updated Blog",
      content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Updated content", "styles": {}}], "children": []}],
      author_id="user123",
      created_at=blog.created_at,
      updated_at=datetime(2024,1,2,tzinfo=timezone.utc)
    )

    await repo.update_blog("blog123", updated_blog)

    retrieved = await repo.get_blog_by_id("blog123")

    assert retrieved is not None
    assert retrieved.title == "Updated Blog"
    assert retrieved.content == [{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Updated content", "styles": {}}], "children": []}]


  @pytest.mark.asyncio
  async def test_update_nonexistent_blog(self, db_session: AsyncSession):
    repo = BlogRepository(db_session)

    blog = BlogEntity(
      id="blog123",
      title="Test Blog",
      content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Content", "styles": {}}], "children": []}],
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
      content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Content", "styles": {}}], "children": []}],
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


  @pytest.mark.asyncio
  async def test_get_blog_counts_by_author_no_blogs(self, db_session: AsyncSession):
    repo = BlogRepository(db_session)

    total, published, draft = await repo.get_blog_counts_by_author("user-without-blogs")

    assert total == 0
    assert published == 0
    assert draft == 0


  @pytest.mark.asyncio
  async def test_get_blog_counts_by_author_mixed_statuses(self, db_session: AsyncSession):
    repo = BlogRepository(db_session)

    # 2 drafts, 3 published for user123
    for i in range(2):
      await repo.create_blog(BlogEntity(
        id=f"draft-{i}",
        title=f"Draft Blog {i}",
        content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Content", "styles": {}}], "children": []}],
        author_id="user123",
        status="draft",
        created_at=datetime(2024,1,1,tzinfo=timezone.utc),
        updated_at=datetime(2024,1,1,tzinfo=timezone.utc)
      ))
    for i in range(3):
      await repo.create_blog(BlogEntity(
        id=f"pub-{i}",
        title=f"Published Blog {i}",
        content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Content", "styles": {}}], "children": []}],
        author_id="user123",
        status="published",
        created_at=datetime(2024,1,1,tzinfo=timezone.utc),
        updated_at=datetime(2024,1,1,tzinfo=timezone.utc)
      ))

    total, published, draft = await repo.get_blog_counts_by_author("user123")

    assert total == 5
    assert published == 3
    assert draft == 2


  @pytest.mark.asyncio
  async def test_get_blog_counts_by_author_filters_by_author(self, db_session: AsyncSession):
    repo = BlogRepository(db_session)

    # user123: 1 draft, 1 published
    await repo.create_blog(BlogEntity(
      id="u123-draft",
      title="User123 Draft",
      content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Content", "styles": {}}], "children": []}],
      author_id="user123",
      status="draft",
      created_at=datetime(2024,1,1,tzinfo=timezone.utc),
      updated_at=datetime(2024,1,1,tzinfo=timezone.utc)
    ))
    await repo.create_blog(BlogEntity(
      id="u123-pub",
      title="User123 Published",
      content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Content", "styles": {}}], "children": []}],
      author_id="user123",
      status="published",
      created_at=datetime(2024,1,1,tzinfo=timezone.utc),
      updated_at=datetime(2024,1,1,tzinfo=timezone.utc)
    ))
    # user456: 2 published
    for i in range(2):
      await repo.create_blog(BlogEntity(
        id=f"u456-pub-{i}",
        title=f"User456 Pub {i}",
        content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Content", "styles": {}}], "children": []}],
        author_id="user456",
        status="published",
        created_at=datetime(2024,1,1,tzinfo=timezone.utc),
        updated_at=datetime(2024,1,1,tzinfo=timezone.utc)
      ))

    total_123, pub_123, draft_123 = await repo.get_blog_counts_by_author("user123")
    assert (total_123, pub_123, draft_123) == (2, 1, 1)

    total_456, pub_456, draft_456 = await repo.get_blog_counts_by_author("user456")
    assert (total_456, pub_456, draft_456) == (2, 2, 0)


  @pytest.mark.asyncio
  async def test_get_blog_counts_by_author_returns_ints(self, db_session: AsyncSession):
    repo = BlogRepository(db_session)

    total, published, draft = await repo.get_blog_counts_by_author("no-such-user")

    # Cover the coalesce(..., 0) / int cast path — empty result must still be plain ints.
    assert isinstance(total, int)
    assert isinstance(published, int)
    assert isinstance(draft, int)


class TestGetAllPublicBlogsByAuthor:

  def _make_blog(
    self,
    id: str,
    title: str = "Some Title",
    author_id: str = "user123",
    status: str = "draft",
    published_title=None,
    published_content=None,
    published_at=None
  ) -> BlogEntity:
    return BlogEntity(
      id=id,
      title=title,
      content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Content", "styles": {}}], "children": []}],
      author_id=author_id,
      status=status,
      published_title=published_title,
      published_content=published_content,
      published_at=published_at,
      created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
      updated_at=datetime(2024, 1, 1, tzinfo=timezone.utc)
    )


  @pytest.mark.asyncio
  async def test_returns_only_blogs_with_published_at_not_null(self, db_session: AsyncSession):
    repo = BlogRepository(db_session)

    # 2 with non-null published_at, 2 with NULL published_at.
    await repo.create_blog(self._make_blog(
      id="pub-a",
      author_id="user123",
      status="published",
      published_title="Snap A",
      published_content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Snap A content.", "styles": {}}], "children": []}],
      published_at=datetime(2024, 6, 1, tzinfo=timezone.utc)
    ))
    await repo.create_blog(self._make_blog(
      id="pub-b",
      author_id="user123",
      status="published",
      published_title="Snap B",
      published_content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Snap B content.", "styles": {}}], "children": []}],
      published_at=datetime(2024, 6, 2, tzinfo=timezone.utc)
    ))
    await repo.create_blog(self._make_blog(id="draft-a", author_id="user123", status="draft"))
    await repo.create_blog(self._make_blog(id="draft-b", author_id="user123", status="draft"))

    blogs, total = await repo.get_all_public_blogs_by_author("user123")

    assert total == 2
    ids = sorted(b.id for b in blogs)
    assert ids == ["pub-a", "pub-b"]


  @pytest.mark.asyncio
  async def test_includes_blog_with_draft_status_but_published_at_set(
    self, db_session: AsyncSession
  ):
    """Regression guard: a published-then-edited blog has status='draft' but a non-null published_at.

    Such a blog must still be returned in the public list.
    """
    repo = BlogRepository(db_session)

    await repo.create_blog(self._make_blog(
      id="edited-after-publish",
      author_id="user123",
      status="draft",
      published_title="Original Title",
      published_content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Original published content.", "styles": {}}], "children": []}],
      published_at=datetime(2024, 5, 1, tzinfo=timezone.utc)
    ))
    await repo.create_blog(self._make_blog(
      id="never-published",
      author_id="user123",
      status="draft"
    ))

    blogs, total = await repo.get_all_public_blogs_by_author("user123")

    assert total == 1
    assert blogs[0].id == "edited-after-publish"
    assert blogs[0].status == "draft"
    assert _normalize_datetime(blogs[0].published_at) == datetime(2024, 5, 1, tzinfo=timezone.utc)


  @pytest.mark.asyncio
  async def test_filters_by_author_id(self, db_session: AsyncSession):
    repo = BlogRepository(db_session)

    # 3 published for user123, 2 published for user456.
    for i in range(3):
      await repo.create_blog(self._make_blog(
        id=f"u123-pub-{i}",
        author_id="user123",
        status="published",
        published_title=f"Snap {i}",
        published_content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": f"Snap {i} content.", "styles": {}}], "children": []}],
        published_at=datetime(2024, 6, i + 1, tzinfo=timezone.utc)
      ))
    for i in range(2):
      await repo.create_blog(self._make_blog(
        id=f"u456-pub-{i}",
        author_id="user456",
        status="published",
        published_title=f"U456 Snap {i}",
        published_content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": f"U456 Snap {i} content.", "styles": {}}], "children": []}],
        published_at=datetime(2024, 7, i + 1, tzinfo=timezone.utc)
      ))

    blogs_123, total_123 = await repo.get_all_public_blogs_by_author("user123")
    assert total_123 == 3
    assert all(b.author_id == "user123" for b in blogs_123)

    blogs_456, total_456 = await repo.get_all_public_blogs_by_author("user456")
    assert total_456 == 2
    assert all(b.author_id == "user456" for b in blogs_456)


  @pytest.mark.asyncio
  async def test_search_filter_applies_on_top_of_published_filter(
    self, db_session: AsyncSession
  ):
    repo = BlogRepository(db_session)

    # 3 published, all matching "Foo" in title.
    for i in range(3):
      await repo.create_blog(self._make_blog(
        id=f"foo-pub-{i}",
        title=f"Foo Blog {i}",
        author_id="user123",
        status="published",
        published_title=f"Foo Snap {i}",
        published_content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": f"Foo {i}.", "styles": {}}], "children": []}],
        published_at=datetime(2024, 6, i + 1, tzinfo=timezone.utc)
      ))
    # 1 published with non-matching title.
    await repo.create_blog(self._make_blog(
      id="bar-pub-0",
      title="Bar Blog",
      author_id="user123",
      status="published",
      published_title="Bar Snap",
      published_content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Bar.", "styles": {}}], "children": []}],
      published_at=datetime(2024, 6, 9, tzinfo=timezone.utc)
    ))
    # 1 unpublished but title matches "Foo" — should NOT appear.
    await repo.create_blog(self._make_blog(
      id="foo-draft-0",
      title="Foo Draft Only",
      author_id="user123",
      status="draft"
    ))

    blogs, total = await repo.get_all_public_blogs_by_author("user123", search="Foo")

    assert total == 3
    ids = sorted(b.id for b in blogs)
    assert ids == ["foo-pub-0", "foo-pub-1", "foo-pub-2"]


  @pytest.mark.asyncio
  async def test_pagination_skip_limit_and_total(self, db_session: AsyncSession):
    repo = BlogRepository(db_session)

    for i in range(12):
      await repo.create_blog(self._make_blog(
        id=f"pub-{i:02d}",
        title=f"Pub Blog {i}",
        author_id="user123",
        status="published",
        published_title=f"Snap {i}",
        published_content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": f"Snap {i}.", "styles": {}}], "children": []}],
        published_at=datetime(2024, 6, i + 1, tzinfo=timezone.utc)
      ))

    page_1, total_1 = await repo.get_all_public_blogs_by_author("user123", skip=0, limit=5)
    assert total_1 == 12
    assert len(page_1) == 5

    page_2, total_2 = await repo.get_all_public_blogs_by_author("user123", skip=5, limit=5)
    assert total_2 == 12
    assert len(page_2) == 5

    page_3, total_3 = await repo.get_all_public_blogs_by_author("user123", skip=10, limit=5)
    assert total_3 == 12
    assert len(page_3) == 2

    page_past_end, total_past = await repo.get_all_public_blogs_by_author("user123", skip=20, limit=5)
    assert total_past == 12
    assert page_past_end == []


  @pytest.mark.asyncio
  async def test_no_blogs_returns_empty(self, db_session: AsyncSession):
    repo = BlogRepository(db_session)

    blogs, total = await repo.get_all_public_blogs_by_author("user-without-blogs")

    assert total == 0
    assert blogs == []