import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import UserRepository, BlogRepository

from src.application.use_cases.users import GetUserUseCase
from src.application.dto import (
  PaginationDTO,
  PaginationResponseDTO,
  UserIncludeOptions,
)
from src.domain.entities import UserEntity, BlogEntity


@pytest.fixture
def get_user_use_case(db_session: AsyncSession) -> GetUserUseCase:
  user_repository = UserRepository(db_session)
  blog_repository = BlogRepository(db_session)
  return GetUserUseCase(user_repository, blog_repository)


class TestGetUserUseCase:

  @pytest.mark.asyncio
  async def test_get_by_id_existing_user(
    self,
    get_user_use_case: GetUserUseCase,
    create_test_user
  ):
    test_user: UserEntity = await create_test_user()

    result = await get_user_use_case.get_by_id(test_user.id)

    assert result is not None
    assert result.id == test_user.id
    assert result.username == test_user.username
    # blog_count is None by default (include_blog_count=False)
    assert result.blog_count is None


  @pytest.mark.asyncio
  async def test_get_by_id_non_existing_user(
    self,
    get_user_use_case: GetUserUseCase
  ):
    result = await get_user_use_case.get_by_id("non-existing-id")

    assert result is None


  @pytest.mark.asyncio
  async def test_get_by_id_with_blog_count_zero_blogs(
    self,
    get_user_use_case: GetUserUseCase,
    create_test_user,
  ):
    test_user: UserEntity = await create_test_user()

    include_options = UserIncludeOptions(include_blog_count=True)
    result = await get_user_use_case.get_by_id(test_user.id, include_options)

    assert result is not None
    assert result.blog_count is not None
    assert result.blog_count.total_blogs == 0
    assert result.blog_count.published_blogs == 0
    assert result.blog_count.draft_blogs == 0


  @pytest.mark.asyncio
  async def test_get_by_id_with_blog_count_mixed_statuses(
    self,
    db_session: AsyncSession,
    get_user_use_case: GetUserUseCase,
    create_test_user,
  ):
    test_user: UserEntity = await create_test_user()

    blog_repo = BlogRepository(db_session)
    # 2 drafts
    for i in range(2):
      await blog_repo.create_blog(BlogEntity(
        id=f"draft-{i}",
        title=f"Draft Blog {i}",
        content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Content", "styles": {}}], "children": []}],
        author_id=test_user.id,
        status="draft",
      ))
    # 3 published
    for i in range(3):
      await blog_repo.create_blog(BlogEntity(
        id=f"published-{i}",
        title=f"Published Blog {i}",
        content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Content", "styles": {}}], "children": []}],
        author_id=test_user.id,
        status="published",
      ))
    await db_session.commit()

    include_options = UserIncludeOptions(include_blog_count=True)
    result = await get_user_use_case.get_by_id(test_user.id, include_options)

    assert result is not None
    assert result.blog_count is not None
    assert result.blog_count.total_blogs == 5
    assert result.blog_count.published_blogs == 3
    assert result.blog_count.draft_blogs == 2


  @pytest.mark.asyncio
  async def test_get_by_username_existing_user(
    self,
    get_user_use_case: GetUserUseCase,
    create_test_user
  ):
    test_user: UserEntity = await create_test_user()

    result = await get_user_use_case.get_by_username(test_user.username)

    assert result is not None
    assert result.id == test_user.id
    assert result.username == test_user.username
    assert result.blog_count is None


  @pytest.mark.asyncio
  async def test_get_by_username_non_existing_user(
    self,
    get_user_use_case: GetUserUseCase
  ):
    result = await get_user_use_case.get_by_username("nonexistingusername")

    assert result is None


  @pytest.mark.asyncio
  async def test_get_by_username_with_blog_count(
    self,
    db_session: AsyncSession,
    get_user_use_case: GetUserUseCase,
    create_test_user,
  ):
    test_user: UserEntity = await create_test_user()

    blog_repo = BlogRepository(db_session)
    await blog_repo.create_blog(BlogEntity(
      id="blog-1",
      title="A Blog Title",
      content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Content", "styles": {}}], "children": []}],
      author_id=test_user.id,
      status="published",
    ))
    await db_session.commit()

    include_options = UserIncludeOptions(include_blog_count=True)
    result = await get_user_use_case.get_by_username(test_user.username, include_options)

    assert result is not None
    assert result.blog_count is not None
    assert result.blog_count.total_blogs == 1
    assert result.blog_count.published_blogs == 1
    assert result.blog_count.draft_blogs == 0


  @pytest.mark.asyncio
  async def test_get_all_users(
    self,
    get_user_use_case: GetUserUseCase,
    create_test_user
  ):
    test_user1: UserEntity = await create_test_user()

    test_user2: UserEntity = await create_test_user(
      id="test-user-id-2",
      first_name="Another",
      last_name="User",
      username="anotheruser"
    )

    pagination = PaginationDTO(skip=0, limit=10, search="")

    result = await get_user_use_case.get_all_users(pagination)

    assert result.total >= 2
    assert any(user.id == test_user1.id for user in result.items)
    assert any(user.id == test_user2.id for user in result.items)
    # blog_count defaults to None
    assert all(user.blog_count is None for user in result.items)


  @pytest.mark.asyncio
  async def test_get_all_users_with_blog_count(
    self,
    db_session: AsyncSession,
    get_user_use_case: GetUserUseCase,
    create_test_user,
  ):
    test_user1: UserEntity = await create_test_user()
    test_user2: UserEntity = await create_test_user(
      id="test-user-id-2",
      first_name="Another",
      last_name="User",
      username="anotheruser",
    )

    blog_repo = BlogRepository(db_session)
    # user1: 1 draft, 1 published
    await blog_repo.create_blog(BlogEntity(
      id="u1-draft",
      title="User1 Draft",
      content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Content", "styles": {}}], "children": []}],
      author_id=test_user1.id,
      status="draft",
    ))
    await blog_repo.create_blog(BlogEntity(
      id="u1-published",
      title="User1 Published",
      content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Content", "styles": {}}], "children": []}],
      author_id=test_user1.id,
      status="published",
    ))
    # user2: 0 blogs
    await db_session.commit()

    pagination = PaginationDTO(skip=0, limit=10, search="")
    include_options = UserIncludeOptions(include_blog_count=True)

    result = await get_user_use_case.get_all_users(pagination, include_options)

    user1_dto = next(u for u in result.items if u.id == test_user1.id)
    user2_dto = next(u for u in result.items if u.id == test_user2.id)

    assert user1_dto.blog_count is not None
    assert user1_dto.blog_count.total_blogs == 2
    assert user1_dto.blog_count.draft_blogs == 1
    assert user1_dto.blog_count.published_blogs == 1

    assert user2_dto.blog_count is not None
    assert user2_dto.blog_count.total_blogs == 0
    assert user2_dto.blog_count.draft_blogs == 0
    assert user2_dto.blog_count.published_blogs == 0


  @pytest.mark.asyncio
  @pytest.mark.parametrize(
    "pagination, expected_count, item_count",
    [
      (PaginationDTO(skip=0, limit=10), 5, 5),
      (PaginationDTO(skip=0, limit=3), 5, 3),
      (PaginationDTO(skip=3, limit=3), 5, 2),
      (PaginationDTO(skip=0, limit=10, search="Test"), 4, 4),
      (PaginationDTO(skip=0, limit=10, search="Another"), 1, 1),
      (PaginationDTO(skip=0, limit=10, search="Non-existing"), 0, 0),
    ]
  )
  async def test_get_all_users_with_pagination_and_search(
    self,
    get_user_use_case: GetUserUseCase,
    create_test_user,
    pagination: PaginationDTO,
    expected_count: int,
    item_count: int
  ):
    await create_test_user()

    await create_test_user(
      id="test-user-id-2",
      first_name="Another",
      last_name="User",
      username="anotheruser"
    )

    await create_test_user(
      id="test-user-id-3",
      first_name="Test3",
      last_name="User",
      username="testuser3"
    )

    await create_test_user(
      id="test-user-id-4",
      first_name="Test4",
      last_name="User",
      username="testuser4"
    )

    await create_test_user(
      id="test-user-id-5",
      first_name="Test5",
      last_name="User",
      username="testuser5"
    )

    result: PaginationResponseDTO = await get_user_use_case.get_all_users(pagination)

    assert result.total == expected_count
    assert len(result.items) == item_count
