import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock

from src.application.dto import PaginationDTO, BlogResponseDTO, PublicBlogResponseDTO, PaginationResponseDTO
from src.application.use_cases.blogs import GetBlogUseCase
from src.domain.entities import BlogEntity


class TestGetBlogUseCase:

  @pytest.fixture
  def blog_repository(self, mocker):
    repo = mocker.Mock()
    repo.get_blog_by_id = AsyncMock()
    repo.get_all_blogs = AsyncMock()
    return repo

  @pytest.fixture
  def use_case(self, blog_repository) -> GetBlogUseCase:
    return GetBlogUseCase(blog_repository=blog_repository)

  @pytest.fixture
  def valid_blog_data(self) -> BlogEntity:
    return BlogEntity(
      id="blog-123",
      title="Test Blog",
      content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "This is a test blog content.", "styles": {}}], "children": []}],
      author_id="author-123",
      created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
      updated_at=datetime(2024, 1, 1, tzinfo=timezone.utc)
    )

  @pytest.fixture
  def valid_blogs_list(self) -> list[BlogEntity]:
    return [
      BlogEntity(
        id="blog-123",
        title="Test Blog 1",
        content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "This is the first test blog content.", "styles": {}}], "children": []}],
        author_id="author-123",
        created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
        updated_at=datetime(2024, 1, 1, tzinfo=timezone.utc)
      ),
      BlogEntity(
        id="blog-124",
        title="Test Blog 2",
        content=[{"id": "2", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "This is the second test blog content.", "styles": {}}], "children": []}],
        author_id="author-124",
        created_at=datetime(2024, 1, 2, tzinfo=timezone.utc),
        updated_at=datetime(2024, 1, 2, tzinfo=timezone.utc)
      )
    ]


  @pytest.mark.asyncio
  async def test_get_by_id_success(
    self,
    use_case,
    blog_repository,
    valid_blog_data
  ):
    blog_repository.get_blog_by_id.return_value = valid_blog_data

    result = await use_case.get_by_id("blog-123")

    assert result == BlogResponseDTO.model_validate(valid_blog_data.to_dict())
    blog_repository.get_blog_by_id.assert_awaited_once_with("blog-123")


  @pytest.mark.asyncio
  async def test_get_by_id_not_found(
    self,
    use_case,
    blog_repository
  ):
    blog_repository.get_blog_by_id.return_value = None

    result = await use_case.get_by_id("non-existing-blog-id")

    assert result is None
    blog_repository.get_blog_by_id.assert_awaited_once_with("non-existing-blog-id")


  @pytest.mark.asyncio
  async def test_get_all_blogs(
    self,
    use_case,
    blog_repository,
    valid_blogs_list
  ):
    pagination = PaginationDTO(skip=0, limit=10, search=None)

    blog_repository.get_all_blogs.return_value = (
      valid_blogs_list,
      len(valid_blogs_list)
    )

    result = await use_case.get_all_blogs(pagination)

    expected_response = PaginationResponseDTO(
      items=[BlogResponseDTO.model_validate(blog.to_dict()) for blog in valid_blogs_list],
      total=len(valid_blogs_list),
      skip=pagination.skip,
      limit=pagination.limit
    )

    assert result == expected_response

    blog_repository.get_all_blogs.assert_awaited_once_with(
      skip=pagination.skip,
      limit=pagination.limit,
      search=pagination.search
    )


  @pytest.mark.asyncio
  async def test_get_all_blogs_empty(
    self,
    use_case,
    blog_repository
  ):
    pagination = PaginationDTO(skip=0, limit=10, search=None)

    blog_repository.get_all_blogs.return_value = ([], 0)

    result = await use_case.get_all_blogs(pagination)

    expected_response = PaginationResponseDTO(
      items=[],
      total=0,
      skip=pagination.skip,
      limit=pagination.limit
    )

    assert result == expected_response

    blog_repository.get_all_blogs.assert_awaited_once_with(
      skip=pagination.skip,
      limit=pagination.limit,
      search=pagination.search
    )


  @pytest.mark.asyncio
  async def test_get_all_blogs_with_search(
    self,
    use_case,
    blog_repository,
    valid_blogs_list
  ):
    search_query = "Test Blog 1"

    pagination = PaginationDTO(skip=0, limit=10, search=search_query)

    filtered_blogs = [
      blog for blog in valid_blogs_list
      if search_query in blog.title
    ]

    blog_repository.get_all_blogs.return_value = (
      filtered_blogs,
      len(filtered_blogs)
    )

    result = await use_case.get_all_blogs(pagination)

    expected_response = PaginationResponseDTO(
      items=[BlogResponseDTO.model_validate(blog.to_dict()) for blog in filtered_blogs],
      total=len(filtered_blogs),
      skip=pagination.skip,
      limit=pagination.limit
    )

    assert result == expected_response

    blog_repository.get_all_blogs.assert_awaited_once_with(
      skip=pagination.skip,
      limit=pagination.limit,
      search=pagination.search
    )


class TestGetPublicBlogById:

  @pytest.fixture
  def blog_repository(self, mocker):
    repo = mocker.Mock()
    repo.get_blog_by_id = AsyncMock()
    return repo

  @pytest.fixture
  def use_case(self, blog_repository) -> GetBlogUseCase:
    return GetBlogUseCase(blog_repository=blog_repository)

  @pytest.fixture
  def published_blog(self) -> BlogEntity:
    blog = BlogEntity(
      id="blog-123",
      title="Draft Title After Edit",
      content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Draft content after edit.", "styles": {}}], "children": []}],
      author_id="author-123",
      status="published",
      published_title="Published Title",
      published_content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Published content.", "styles": {}}], "children": []}],
      published_at=datetime(2024, 6, 1, tzinfo=timezone.utc),
      created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
      updated_at=datetime(2024, 6, 1, tzinfo=timezone.utc)
    )
    return blog

  @pytest.fixture
  def draft_blog(self) -> BlogEntity:
    return BlogEntity(
      id="blog-456",
      title="Draft Only Title",
      content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Draft only content.", "styles": {}}], "children": []}],
      author_id="author-123",
      status="draft",
      created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
      updated_at=datetime(2024, 1, 1, tzinfo=timezone.utc)
    )


  @pytest.mark.asyncio
  async def test_get_public_by_id_published_serves_published_snapshot(
    self,
    use_case,
    blog_repository,
    published_blog
  ):
    blog_repository.get_blog_by_id.return_value = published_blog

    result = await use_case.get_public_by_id("blog-123")

    assert isinstance(result, PublicBlogResponseDTO)
    assert result.title == "Published Title"
    assert result.content == [{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Published content.", "styles": {}}], "children": []}]
    assert result.status == "published"
    assert result.published_at == datetime(2024, 6, 1, tzinfo=timezone.utc)
    blog_repository.get_blog_by_id.assert_awaited_once_with("blog-123")


  @pytest.mark.asyncio
  async def test_get_public_by_id_draft_serves_draft_content(
    self,
    use_case,
    blog_repository,
    draft_blog
  ):
    blog_repository.get_blog_by_id.return_value = draft_blog

    result = await use_case.get_public_by_id("blog-456")

    assert isinstance(result, PublicBlogResponseDTO)
    assert result.title == "Draft Only Title"
    assert result.content == [{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Draft only content.", "styles": {}}], "children": []}]
    assert result.status == "draft"
    assert result.published_at is None
    blog_repository.get_blog_by_id.assert_awaited_once_with("blog-456")


  @pytest.mark.asyncio
  async def test_get_public_by_id_not_found(
    self,
    use_case,
    blog_repository
  ):
    blog_repository.get_blog_by_id.return_value = None

    result = await use_case.get_public_by_id("nonexistent-blog")

    assert result is None
    blog_repository.get_blog_by_id.assert_awaited_once_with("nonexistent-blog")


class TestGetAllPublicBlogsByAuthor:

  @pytest.fixture
  def blog_repository(self, mocker):
    repo = mocker.Mock()
    repo.get_all_public_blogs_by_author = AsyncMock()
    return repo

  @pytest.fixture
  def use_case(self, blog_repository) -> GetBlogUseCase:
    return GetBlogUseCase(blog_repository=blog_repository)

  @pytest.fixture
  def published_blog(self) -> BlogEntity:
    """A blog whose status is 'published' and has a complete published snapshot."""
    return BlogEntity(
      id="blog-pub-1",
      title="Draft Title After Edit",
      content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Draft content after edit.", "styles": {}}], "children": []}],
      author_id="author-123",
      status="published",
      published_title="Published Title",
      published_content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Published content.", "styles": {}}], "children": []}],
      published_at=datetime(2024, 6, 1, tzinfo=timezone.utc),
      created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
      updated_at=datetime(2024, 6, 1, tzinfo=timezone.utc)
    )

  @pytest.fixture
  def edited_published_blog(self) -> BlogEntity:
    """A blog that was published, then edited — status flipped to 'draft' but snapshot is intact."""
    return BlogEntity(
      id="blog-pub-2",
      title="Edited Draft Title",
      content=[{"id": "2", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Edited draft content.", "styles": {}}], "children": []}],
      author_id="author-123",
      status="draft",
      published_title="Snapshot Title",
      published_content=[{"id": "2", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Snapshot content.", "styles": {}}], "children": []}],
      published_at=datetime(2024, 5, 1, tzinfo=timezone.utc),
      created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
      updated_at=datetime(2024, 7, 1, tzinfo=timezone.utc)
    )

  @pytest.fixture
  def blog_with_only_published_at(self) -> BlogEntity:
    """Defensive-guard fixture: published_at is set but published_title is None.

    Use case must fall back to the draft title/content rather than crashing.
    """
    return BlogEntity(
      id="blog-pub-3",
      title="Fallback Title",
      content=[{"id": "3", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Fallback content.", "styles": {}}], "children": []}],
      author_id="author-123",
      status="published",
      published_title=None,
      published_content=None,
      published_at=datetime(2024, 4, 1, tzinfo=timezone.utc),
      created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
      updated_at=datetime(2024, 4, 1, tzinfo=timezone.utc)
    )


  @pytest.mark.asyncio
  async def test_returns_pagination_response_shape(
    self,
    use_case,
    blog_repository,
    published_blog
  ):
    pagination = PaginationDTO(skip=0, limit=10, search=None)

    blog_repository.get_all_public_blogs_by_author.return_value = (
      [published_blog],
      1
    )

    result = await use_case.get_all_public_blogs_by_author("author-123", pagination)

    assert isinstance(result, PaginationResponseDTO)
    assert result.total == 1
    assert result.skip == 0
    assert result.limit == 10
    assert len(result.items) == 1
    assert isinstance(result.items[0], PublicBlogResponseDTO)


  @pytest.mark.asyncio
  async def test_each_item_uses_published_snapshot(
    self,
    use_case,
    blog_repository,
    published_blog,
    edited_published_blog
  ):
    pagination = PaginationDTO(skip=0, limit=10, search=None)

    blog_repository.get_all_public_blogs_by_author.return_value = (
      [published_blog, edited_published_blog],
      2
    )

    result = await use_case.get_all_public_blogs_by_author("author-123", pagination)

    assert len(result.items) == 2

    # First item: published — snapshot replaces draft fields.
    assert result.items[0].title == "Published Title"
    assert result.items[0].content == [{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Published content.", "styles": {}}], "children": []}]

    # Second item: edited after publish — snapshot still served despite status="draft".
    assert result.items[1].title == "Snapshot Title"
    assert result.items[1].content == [{"id": "2", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Snapshot content.", "styles": {}}], "children": []}]


  @pytest.mark.asyncio
  async def test_falls_back_to_draft_when_published_title_is_none(
    self,
    use_case,
    blog_repository,
    blog_with_only_published_at
  ):
    """Defensive guard: if published_title is None, use case must not swap and must fall back to draft."""
    pagination = PaginationDTO(skip=0, limit=10, search=None)

    blog_repository.get_all_public_blogs_by_author.return_value = (
      [blog_with_only_published_at],
      1
    )

    result = await use_case.get_all_public_blogs_by_author("author-123", pagination)

    assert len(result.items) == 1
    assert result.items[0].title == "Fallback Title"
    assert result.items[0].content == [{"id": "3", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Fallback content.", "styles": {}}], "children": []}]


  @pytest.mark.asyncio
  async def test_repository_called_with_pagination_args(
    self,
    use_case,
    blog_repository
  ):
    pagination = PaginationDTO(skip=5, limit=20, search="hello")

    blog_repository.get_all_public_blogs_by_author.return_value = ([], 0)

    await use_case.get_all_public_blogs_by_author("author-xyz", pagination)

    blog_repository.get_all_public_blogs_by_author.assert_awaited_once_with(
      author_id="author-xyz",
      skip=5,
      limit=20,
      search="hello"
    )


  @pytest.mark.asyncio
  async def test_empty_result(
    self,
    use_case,
    blog_repository
  ):
    pagination = PaginationDTO(skip=0, limit=10, search=None)

    blog_repository.get_all_public_blogs_by_author.return_value = ([], 0)

    result = await use_case.get_all_public_blogs_by_author("author-with-no-blogs", pagination)

    assert isinstance(result, PaginationResponseDTO)
    assert result.total == 0
    assert result.items == []