import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import BlogRepository
from src.application.use_cases.blogs import GetBlogUseCase
from src.application.dto import PaginationDTO, PaginationResponseDTO


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
        content=f"This is the content of test blog {i}.",
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
          content=f"This is the content of test blog {i}-{j}.",
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