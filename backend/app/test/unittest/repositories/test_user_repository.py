import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.database.db import Base
from app.repositories import UserRepository
from src.domain.entities import UserEntity

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# -------------------------
# Fixtures
# -------------------------
@pytest.fixture
async def async_session():
  engine = create_async_engine(DATABASE_URL, echo=False, future=True)

  async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)

  AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
  )

  async with AsyncSessionLocal() as session:
    async with session.begin():
      yield session

  await engine.dispose()


# -------------------------
# Helper functions
# -------------------------
def make_user(
  id: str,
  first_name: str = "John",
  last_name: str = "Doe",
  username: str = "johndoe",
  password: str = "securepassword",
  avatar=None,
  created_at="2024-01-01T00:00:00Z",
  updated_at="2024-01-01T00:00:00Z"
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


def assert_user_equal(entity1: UserEntity, entity2: UserEntity):
  assert entity1.id == entity2.id
  assert entity1.username == entity2.username
  assert entity1.first_name == entity2.first_name
  assert entity1.last_name == entity2.last_name
  assert entity1.password == entity2.password
  assert entity1.avatar == entity2.avatar
  assert entity1.created_at == entity2.created_at
  assert entity1.updated_at == entity2.updated_at


# -------------------------
# Tests
# -------------------------
class TestUserRepository:

  @pytest.mark.asyncio
  async def test_create_and_get_user(self, async_session: AsyncSession):
    repo = UserRepository(async_session)
    user = make_user("123")
    await repo.create_user(user)

    # get by id
    retrieved = await repo.get_user_by_id("123")
    assert_user_equal(retrieved, user)

    # get by username
    retrieved_by_username = await repo.get_user_by_username("johndoe")
    assert_user_equal(retrieved_by_username, user)

  @pytest.mark.asyncio
  async def test_get_all_users(self, async_session: AsyncSession):
    repo = UserRepository(async_session)
    users = [make_user(str(i), username=f"user{i}") for i in range(3)]
    for u in users:
      await repo.create_user(u)

    retrieved_users, total_count = await repo.get_all_users()
    assert total_count == 3
    assert len(retrieved_users) == 3
    for u in users:
      assert any(u.username == ru.username for ru in retrieved_users)

  @pytest.mark.asyncio
  async def test_update_user(self, async_session: AsyncSession):
    repo = UserRepository(async_session)
    user = make_user("999", first_name="Old", last_name="Name", username="olduser")
    await repo.create_user(user)

    updated_user = make_user(
      "999", first_name="New", last_name="Name", username="newuser",
      updated_at="2024-01-08T00:00:00Z"
    )
    result = await repo.update_user("999", updated_user)
    assert_user_equal(result, updated_user)

  @pytest.mark.asyncio
  @pytest.mark.parametrize("user_id", ["nonexistent"])
  async def test_nonexistent_user(self, async_session: AsyncSession, user_id):
    repo = UserRepository(async_session)
    assert await repo.get_user_by_id(user_id) is None
    assert await repo.get_user_by_username(user_id) is None
    user = make_user(user_id)
    assert await repo.update_user(user_id, user) is None

  @pytest.mark.asyncio
  async def test_delete_user(self, async_session: AsyncSession):
    repo = UserRepository(async_session)
    user = make_user("to_delete")
    await repo.create_user(user)

    await repo.delete_user("to_delete")
    assert await repo.get_user_by_id("to_delete") is None

  @pytest.mark.asyncio
  async def test_get_all_users_empty(self, async_session: AsyncSession):
    repo = UserRepository(async_session)
    users, count = await repo.get_all_users()
    assert count == 0
    assert len(users) == 0
