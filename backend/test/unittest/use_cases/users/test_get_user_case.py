import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock

from src.application.dto import (
  PaginationDTO,
  PaginationResponseDTO,
  UserResponseDTO,
  UserIncludeOptions,
  UserBlogCountDTO,
)
from src.application.use_cases.users import GetUserUseCase
from src.domain.entities import UserEntity


class TestGetUserUseCase:

  @pytest.fixture
  def user_repository(self, mocker):
    repo = mocker.Mock()

    repo.get_user_by_id = AsyncMock()
    repo.get_user_by_username = AsyncMock()
    repo.get_all_users = AsyncMock()

    return repo

  @pytest.fixture
  def blog_repository(self, mocker):
    repo = mocker.Mock()

    repo.get_blog_counts_by_author = AsyncMock()

    return repo

  @pytest.fixture
  def use_case(self, user_repository, blog_repository) -> GetUserUseCase:
    return GetUserUseCase(
      user_repository=user_repository,
      blog_repository=blog_repository,
    )

  @pytest.fixture
  def valid_user_data(self) -> UserEntity:
    return UserEntity(
      id="123",
      first_name="John",
      last_name="Doe",
      username="johndoe",
      password="hashedpassword",
      avatar="",
      created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
      updated_at=datetime(2024, 1, 1, tzinfo=timezone.utc)
    )

  @pytest.fixture
  def valid_users_list(self) -> list[UserEntity]:
    return [
      UserEntity(
        id="123",
        first_name="John",
        last_name="Doe",
        username="johndoe",
        password="hashedpassword",
        avatar="",
        created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
        updated_at=datetime(2024, 1, 1, tzinfo=timezone.utc)
      ),
      UserEntity(
        id="124",
        first_name="Jane",
        last_name="Smith",
        username="janesmith",
        password="hashedpassword2",
        avatar="",
        created_at=datetime(2024, 1, 2, tzinfo=timezone.utc),
        updated_at=datetime(2024, 1, 2, tzinfo=timezone.utc)
      )
    ]

  @pytest.mark.asyncio
  async def test_get_by_id_success(
    self,
    use_case,
    user_repository,
    blog_repository,
    valid_user_data
  ):
    user_repository.get_user_by_id.return_value = valid_user_data

    result = await use_case.get_by_id("123")

    assert result == UserResponseDTO.model_validate(valid_user_data.to_dict())
    user_repository.get_user_by_id.assert_awaited_once_with("123")
    # By default, include_blog_count is False — blog repo must not be called
    blog_repository.get_blog_counts_by_author.assert_not_awaited()

  @pytest.mark.asyncio
  async def test_get_by_id_not_found(
    self,
    use_case,
    user_repository,
    blog_repository,
  ):
    user_repository.get_user_by_id.return_value = None

    result = await use_case.get_by_id("999")

    assert result is None
    user_repository.get_user_by_id.assert_awaited_once_with("999")
    blog_repository.get_blog_counts_by_author.assert_not_awaited()

  @pytest.mark.asyncio
  async def test_get_by_id_with_blog_count(
    self,
    use_case,
    user_repository,
    blog_repository,
    valid_user_data,
  ):
    user_repository.get_user_by_id.return_value = valid_user_data
    blog_repository.get_blog_counts_by_author.return_value = (7, 5, 2)

    include_options = UserIncludeOptions(include_blog_count=True)
    result = await use_case.get_by_id("123", include_options)

    assert result is not None
    assert result.blog_count == UserBlogCountDTO(
      total_blogs=7,
      published_blogs=5,
      draft_blogs=2,
    )
    blog_repository.get_blog_counts_by_author.assert_awaited_once_with("123")

  @pytest.mark.asyncio
  async def test_get_by_id_without_blog_count_leaves_field_none(
    self,
    use_case,
    user_repository,
    blog_repository,
    valid_user_data,
  ):
    user_repository.get_user_by_id.return_value = valid_user_data

    include_options = UserIncludeOptions(include_blog_count=False)
    result = await use_case.get_by_id("123", include_options)

    assert result is not None
    assert result.blog_count is None
    blog_repository.get_blog_counts_by_author.assert_not_awaited()

  @pytest.mark.asyncio
  async def test_get_by_username_success(
    self,
    use_case,
    user_repository,
    blog_repository,
    valid_user_data
  ):
    user_repository.get_user_by_username.return_value = valid_user_data

    result = await use_case.get_by_username("johndoe")

    assert result == UserResponseDTO.model_validate(valid_user_data.to_dict())
    user_repository.get_user_by_username.assert_awaited_once_with("johndoe")
    blog_repository.get_blog_counts_by_author.assert_not_awaited()

  @pytest.mark.asyncio
  async def test_by_username_not_found(
    self,
    use_case,
    user_repository,
    blog_repository,
  ):
    user_repository.get_user_by_username.return_value = None

    result = await use_case.get_by_username("unknownuser")

    assert result is None
    user_repository.get_user_by_username.assert_awaited_once_with("unknownuser")
    blog_repository.get_blog_counts_by_author.assert_not_awaited()

  @pytest.mark.asyncio
  async def test_get_by_username_with_blog_count(
    self,
    use_case,
    user_repository,
    blog_repository,
    valid_user_data,
  ):
    user_repository.get_user_by_username.return_value = valid_user_data
    blog_repository.get_blog_counts_by_author.return_value = (3, 1, 2)

    include_options = UserIncludeOptions(include_blog_count=True)
    result = await use_case.get_by_username("johndoe", include_options)

    assert result is not None
    assert result.blog_count == UserBlogCountDTO(
      total_blogs=3,
      published_blogs=1,
      draft_blogs=2,
    )
    blog_repository.get_blog_counts_by_author.assert_awaited_once_with("123")

  @pytest.mark.asyncio
  async def test_get_all_users(
    self,
    use_case,
    user_repository,
    blog_repository,
    valid_users_list
  ):
    pagination = PaginationDTO(skip=0, limit=10, search=None)

    user_repository.get_all_users.return_value = (
      valid_users_list,
      len(valid_users_list)
    )

    result = await use_case.get_all_users(pagination)

    expected_dtos = [
      UserResponseDTO.model_validate(user.to_dict())
      for user in valid_users_list
    ]

    assert result == PaginationResponseDTO(
      total=len(valid_users_list),
      skip=pagination.skip,
      limit=pagination.limit,
      items=expected_dtos
    )

    user_repository.get_all_users.assert_awaited_once_with(
      skip=pagination.skip,
      limit=pagination.limit,
      search=pagination.search
    )
    blog_repository.get_blog_counts_by_author.assert_not_awaited()

  @pytest.mark.asyncio
  async def test_get_all_users_with_search(
    self,
    use_case,
    user_repository,
    blog_repository,
    valid_users_list
  ):
    pagination = PaginationDTO(skip=0, limit=10, search="john")

    filtered_users = [
      user for user in valid_users_list if "john" in user.username
    ]

    user_repository.get_all_users.return_value = (
      filtered_users,
      len(filtered_users)
    )

    result = await use_case.get_all_users(pagination)

    expected_dtos = [
      UserResponseDTO.model_validate(user.to_dict())
      for user in filtered_users
    ]

    assert result == PaginationResponseDTO(
      total=len(filtered_users),
      skip=pagination.skip,
      limit=pagination.limit,
      items=expected_dtos
    )

    user_repository.get_all_users.assert_awaited_once_with(
      skip=pagination.skip,
      limit=pagination.limit,
      search=pagination.search
    )
    blog_repository.get_blog_counts_by_author.assert_not_awaited()

  @pytest.mark.asyncio
  async def test_get_all_users_with_blog_count(
    self,
    use_case,
    user_repository,
    blog_repository,
    valid_users_list,
  ):
    pagination = PaginationDTO(skip=0, limit=10, search=None)

    user_repository.get_all_users.return_value = (
      valid_users_list,
      len(valid_users_list),
    )

    # Return per-author counts in the order get_blog_counts_by_author is called
    blog_repository.get_blog_counts_by_author.side_effect = [
      (4, 3, 1),  # user 123
      (0, 0, 0),  # user 124
    ]

    include_options = UserIncludeOptions(include_blog_count=True)
    result = await use_case.get_all_users(pagination, include_options)

    assert result.total == len(valid_users_list)
    assert len(result.items) == len(valid_users_list)
    assert result.items[0].blog_count == UserBlogCountDTO(
      total_blogs=4,
      published_blogs=3,
      draft_blogs=1,
    )
    assert result.items[1].blog_count == UserBlogCountDTO(
      total_blogs=0,
      published_blogs=0,
      draft_blogs=0,
    )
    # One call per user
    assert blog_repository.get_blog_counts_by_author.await_count == len(valid_users_list)
