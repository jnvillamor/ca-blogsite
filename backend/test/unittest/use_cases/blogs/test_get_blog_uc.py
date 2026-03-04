import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock

from src.application.dto import PaginationDTO, BlogResponseDTO, PaginationResponseDTO
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
      content="This is a test blog content.",
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
        content="This is the first test blog content.",
        author_id="author-123",
        created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
        updated_at=datetime(2024, 1, 1, tzinfo=timezone.utc)
      ),
      BlogEntity(
        id="blog-124",
        title="Test Blog 2",
        content="This is the second test blog content.",
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