import pytest
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import BlogModel
from app.repositories import BlogRepository
from src.application.use_cases.blogs import GetBlogUseCase
from src.application.dto import PaginationDTO, PaginationResponseDTO, PublicBlogResponseDTO


@pytest.fixture
def get_blog_use_case(db_session: AsyncSession) -> GetBlogUseCase:
  blog_repository = BlogRepository(db_session)
  return GetBlogUseCase(blog_repository)


class TestGetBlogUseCase:

  @pytest.mark.asyncio
  async def test_get_by_id_existing_blog(
    self,
    get_blog_use_case: GetBlogUseCase,
    create_test_user,
    create_test_blog
  ):
    test_user = await create_test_user()
    test_blog = await create_test_blog(author_id=test_user.id)

    result = await get_blog_use_case.get_by_id(test_blog.id)

    assert result is not None
    assert result.id == test_blog.id
    assert result.title == test_blog.title
    assert result.content == test_blog.content
    assert result.author_id == test_blog.author_id
    assert result.hero_image == test_blog.hero_image


  @pytest.mark.asyncio
  async def test_get_by_id_non_existing_blog(
    self,
    get_blog_use_case: GetBlogUseCase
  ):
    result = await get_blog_use_case.get_by_id("non-existing-id")

    assert result is None


  @pytest.mark.asyncio
  @pytest.mark.parametrize(
    "pagination, expected_count, item_count",
    [
      (PaginationDTO(skip=0, limit=10), 15, 10),
      (PaginationDTO(skip=10, limit=10), 15, 5),
      (PaginationDTO(skip=0, limit=20), 15, 15),
      (PaginationDTO(skip=20, limit=10), 15, 0),
      (PaginationDTO(skip=0, limit=5, search="Test Blog Title 1"), 6, 5),
      (PaginationDTO(skip=0, limit=5, search="Non-existing"), 0, 0),
      (PaginationDTO(skip=0, limit=5, search="Test Blog Title"), 15, 5)
    ]
  )
  async def test_get_all_blogs(
    self,
    get_blog_use_case: GetBlogUseCase,
    create_test_user,
    create_test_blog,
    pagination: PaginationDTO,
    expected_count: int,
    item_count: int
  ):
    test_user = await create_test_user()

    for i in range(15):
      await create_test_blog(
        id=f"test-blog-id-{i}",
        title=f"Test Blog Title {i}",
        content=[{"id": str(i), "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": f"This is the content of test blog {i}.", "styles": {}}], "children": []}],
        author_id=test_user.id,
        hero_image=f"https://example.com/hero-image-{i}.png"
      )

    result: PaginationResponseDTO = await get_blog_use_case.get_all_blogs(pagination)

    assert result.total == expected_count
    assert len(result.items) == item_count


  @pytest.mark.asyncio
  async def test_get_all_blogs_by_author(
    self,
    get_blog_use_case: GetBlogUseCase,
    create_test_user,
    create_test_blog,
  ):
    for i in range(5):
      test_user = await create_test_user(
        id=f"test-user-id-{i}",
        first_name=f"Test{i}",
        last_name="User",
        username=f"testuser{i}"
      )

      for j in range(3):
        await create_test_blog(
          id=f"test-blog-id-{i}-{j}",
          title=f"Test Blog Title {i}-{j}",
          content=[{"id": f"{i}-{j}", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": f"This is the content of test blog {i}-{j}.", "styles": {}}], "children": []}],
          author_id=test_user.id,
          hero_image=f"https://example.com/hero-image-{i}-{j}.png"
        )

    pagination = PaginationDTO(skip=0, limit=10)
    result = await get_blog_use_case.get_all_blogs_by_author("test-user-id-2", pagination)

    assert result.total == 3
    assert len(result.items) == 3

    for blog in result.items:
      assert blog.author_id == "test-user-id-2"

    pagination_with_search = PaginationDTO(skip=0, limit=10, search="Test Blog Title 2-1")
    result_with_search = await get_blog_use_case.get_all_blogs_by_author(
      "test-user-id-2",
      pagination_with_search
    )

    assert result_with_search.total == 1
    assert len(result_with_search.items) == 1
    assert result_with_search.items[0].title == "Test Blog Title 2-1"
    assert result_with_search.items[0].author_id == "test-user-id-2"


  async def _create_blog_with_publish_fields(
    self,
    db_session: AsyncSession,
    *,
    id: str,
    title: str,
    author_id: str,
    status: str = "draft",
    published_title=None,
    published_content=None,
    published_at=None,
    content=None,
    hero_image="https://example.com/hero.png",
  ) -> BlogModel:
    """Direct BlogModel insert — needed because the create_test_blog fixture
    doesn't expose the published_* fields."""
    if content is None:
      content = [{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Default content.", "styles": {}}], "children": []}]

    blog = BlogModel(
      id=id,
      title=title,
      content=content,
      author_id=author_id,
      hero_image=hero_image,
      status=status,
      published_title=published_title,
      published_content=published_content,
      published_at=published_at,
    )
    db_session.add(blog)
    await db_session.commit()
    await db_session.refresh(blog)
    return blog


  @pytest.mark.asyncio
  async def test_get_all_public_blogs_by_author_returns_pagination(
    self,
    get_blog_use_case: GetBlogUseCase,
    create_test_user,
    db_session: AsyncSession,
  ):
    test_user = await create_test_user()

    await self._create_blog_with_publish_fields(
      db_session,
      id="pub-1",
      title="Draft After Edit 1",
      author_id=test_user.id,
      status="published",
      published_title="Snapshot 1",
      published_content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Snapshot 1 content.", "styles": {}}], "children": []}],
      published_at=datetime(2024, 6, 1, tzinfo=timezone.utc),
    )

    pagination = PaginationDTO(skip=0, limit=10)
    result = await get_blog_use_case.get_all_public_blogs_by_author(test_user.id, pagination)

    assert isinstance(result, PaginationResponseDTO)
    assert result.total == 1
    assert len(result.items) == 1
    assert isinstance(result.items[0], PublicBlogResponseDTO)
    assert result.items[0].title == "Snapshot 1"
    assert result.items[0].content == [{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Snapshot 1 content.", "styles": {}}], "children": []}]


  @pytest.mark.asyncio
  async def test_get_all_public_blogs_by_author_excludes_unpublished(
    self,
    get_blog_use_case: GetBlogUseCase,
    create_test_user,
    db_session: AsyncSession,
  ):
    test_user = await create_test_user()

    # Published (has published_at) — should appear.
    await self._create_blog_with_publish_fields(
      db_session,
      id="pub-1",
      title="Pub 1",
      author_id=test_user.id,
      status="published",
      published_title="Snap 1",
      published_content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Snap 1.", "styles": {}}], "children": []}],
      published_at=datetime(2024, 6, 1, tzinfo=timezone.utc),
    )
    # Never published (published_at IS NULL) — must be excluded.
    await self._create_blog_with_publish_fields(
      db_session,
      id="draft-1",
      title="Draft 1",
      author_id=test_user.id,
      status="draft",
    )

    pagination = PaginationDTO(skip=0, limit=10)
    result = await get_blog_use_case.get_all_public_blogs_by_author(test_user.id, pagination)

    assert result.total == 1
    assert len(result.items) == 1
    assert result.items[0].id == "pub-1"


  @pytest.mark.asyncio
  async def test_get_all_public_blogs_by_author_includes_edited_after_publish(
    self,
    get_blog_use_case: GetBlogUseCase,
    create_test_user,
    db_session: AsyncSession,
  ):
    """Regression guard for the published_at-vs-status semantic distinction."""
    test_user = await create_test_user()

    # status='draft' but has a non-null published_at and an intact snapshot.
    await self._create_blog_with_publish_fields(
      db_session,
      id="edited-after-publish",
      title="Edited Draft Title",
      author_id=test_user.id,
      status="draft",
      published_title="Original Snapshot Title",
      published_content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Original snapshot content.", "styles": {}}], "children": []}],
      published_at=datetime(2024, 5, 1, tzinfo=timezone.utc),
    )

    pagination = PaginationDTO(skip=0, limit=10)
    result = await get_blog_use_case.get_all_public_blogs_by_author(test_user.id, pagination)

    assert result.total == 1
    assert len(result.items) == 1
    # The use case swaps in the published snapshot — caller should see Original Snapshot Title.
    assert result.items[0].id == "edited-after-publish"
    assert result.items[0].title == "Original Snapshot Title"
    assert result.items[0].content == [{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Original snapshot content.", "styles": {}}], "children": []}]


  @pytest.mark.asyncio
  async def test_get_all_public_blogs_by_author_response_shape_omits_snapshot_fields(
    self,
    get_blog_use_case: GetBlogUseCase,
    create_test_user,
    db_session: AsyncSession,
  ):
    """PublicBlogResponseDTO does not expose published_title/published_content;
    those values appear as title/content after the snapshot swap."""
    test_user = await create_test_user()

    await self._create_blog_with_publish_fields(
      db_session,
      id="pub-shape",
      title="Shape Draft Title",
      author_id=test_user.id,
      status="published",
      published_title="Shape Snap Title",
      published_content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Shape snap content.", "styles": {}}], "children": []}],
      published_at=datetime(2024, 6, 1, tzinfo=timezone.utc),
    )

    pagination = PaginationDTO(skip=0, limit=10)
    result = await get_blog_use_case.get_all_public_blogs_by_author(test_user.id, pagination)

    assert len(result.items) == 1
    item = result.items[0]
    # The DTO has no published_title/published_content fields at all.
    item_dump = item.model_dump()
    assert "published_title" not in item_dump
    assert "published_content" not in item_dump
    # Title/content reflect the published snapshot.
    assert item.title == "Shape Snap Title"


  @pytest.mark.asyncio
  async def test_get_all_public_blogs_by_author_pagination_and_search(
    self,
    get_blog_use_case: GetBlogUseCase,
    create_test_user,
    db_session: AsyncSession,
  ):
    test_user = await create_test_user()

    # 12 published; 6 with "Foo" in title, 6 with "Bar" in title.
    for i in range(6):
      await self._create_blog_with_publish_fields(
        db_session,
        id=f"foo-{i:02d}",
        title=f"Foo Blog {i}",
        author_id=test_user.id,
        status="published",
        published_title=f"Foo Snap {i}",
        published_content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": f"Foo Snap {i}.", "styles": {}}], "children": []}],
        published_at=datetime(2024, 6, i + 1, tzinfo=timezone.utc),
      )
    for i in range(6):
      await self._create_blog_with_publish_fields(
        db_session,
        id=f"bar-{i:02d}",
        title=f"Bar Blog {i}",
        author_id=test_user.id,
        status="published",
        published_title=f"Bar Snap {i}",
        published_content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": f"Bar Snap {i}.", "styles": {}}], "children": []}],
        published_at=datetime(2024, 7, i + 1, tzinfo=timezone.utc),
      )

    # Pagination
    page_1 = await get_blog_use_case.get_all_public_blogs_by_author(
      test_user.id, PaginationDTO(skip=0, limit=5)
    )
    assert page_1.total == 12
    assert len(page_1.items) == 5

    page_2 = await get_blog_use_case.get_all_public_blogs_by_author(
      test_user.id, PaginationDTO(skip=10, limit=5)
    )
    assert page_2.total == 12
    assert len(page_2.items) == 2

    # Search — search runs against the draft title (the column the repo filters on).
    search_result = await get_blog_use_case.get_all_public_blogs_by_author(
      test_user.id, PaginationDTO(skip=0, limit=10, search="Foo")
    )
    assert search_result.total == 6
    assert all(item.id.startswith("foo-") for item in search_result.items)