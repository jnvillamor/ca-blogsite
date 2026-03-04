import pytest
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import UserRepository
from src.domain.exceptions import NotFoundException
from src.domain.entities import UserEntity


def make_user(
  id: str,
  first_name: str = "John",
  last_name: str = "Doe",
  username: str = "johndoe",
  password: str = "securepassword",
  avatar=None,
  created_at=datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
  updated_at=datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
) -> UserEntity:
  return UserEntity(
    id=id,
    first_name=first_name,
    last_name=last_name,
    username=username,
    password=password,
    avatar=avatar,
    created_at=created_at,
    updated_at=updated_at
  )


def _normalize_datetime(dt: datetime) -> datetime:
  if dt.tzinfo is None:
    return dt.replace(tzinfo=timezone.utc)
  return dt


def assert_user_equal(entity1: UserEntity, entity2: UserEntity):
  assert entity1.id == entity2.id
  assert entity1.username == entity2.username
  assert entity1.first_name == entity2.first_name
  assert entity1.last_name == entity2.last_name
  assert entity1.password == entity2.password
  assert entity1.avatar == entity2.avatar
  assert _normalize_datetime(entity1.created_at) == _normalize_datetime(entity2.created_at)
  assert _normalize_datetime(entity1.updated_at) == _normalize_datetime(entity2.updated_at)


class TestUserRepository:

  @pytest.mark.asyncio
  async def test_create_and_get_user(self, db_session: AsyncSession):
    repo = UserRepository(db_session)

    user = make_user("123")
    await repo.create_user(user)

    retrieved = await repo.get_user_by_id("123")

    assert retrieved is not None
    assert_user_equal(retrieved, user)

    retrieved_by_username = await repo.get_user_by_username("johndoe")

    assert retrieved_by_username is not None
    assert_user_equal(retrieved_by_username, user)


  @pytest.mark.asyncio
  async def test_get_all_users(self, db_session: AsyncSession):
    repo = UserRepository(db_session)

    users = [make_user(str(i), username=f"user{i}") for i in range(3)]

    for u in users:
      await repo.create_user(u)

    retrieved_users, total_count = await repo.get_all_users()

    assert total_count == 3
    assert len(retrieved_users) == 3

    for u in users:
      assert any(u.username == ru.username for ru in retrieved_users)


  @pytest.mark.asyncio
  async def test_update_user(self, db_session: AsyncSession):
    repo = UserRepository(db_session)

    user = make_user("999", first_name="Old", last_name="Name", username="olduser")
    await repo.create_user(user)

    updated_user = make_user(
      "999",
      first_name="New",
      last_name="Name",
      username="newuser",
      updated_at=datetime(2024, 2, 2, tzinfo=timezone.utc)
    )

    result = await repo.update_user("999", updated_user)

    assert result is not None
    assert_user_equal(result, updated_user)


  @pytest.mark.asyncio
  @pytest.mark.parametrize("user_id", ["nonexistent"])
  async def test_nonexistent_user(self, db_session: AsyncSession, user_id):
    repo = UserRepository(db_session)

    assert await repo.get_user_by_id(user_id) is None
    assert await repo.get_user_by_username("nonexistent") is None

    with pytest.raises(NotFoundException):
      await repo.update_user(user_id, make_user(user_id))

    assert not await repo.delete_user(user_id)


  @pytest.mark.asyncio
  async def test_delete_user(self, db_session: AsyncSession):
    repo = UserRepository(db_session)

    user = make_user("to_delete")
    await repo.create_user(user)

    await repo.delete_user("to_delete")

    assert await repo.get_user_by_id("to_delete") is None


  @pytest.mark.asyncio
  async def test_get_all_users_empty(self, db_session: AsyncSession):
    repo = UserRepository(db_session)

    users, count = await repo.get_all_users()

    assert count == 0
    assert len(users) == 0