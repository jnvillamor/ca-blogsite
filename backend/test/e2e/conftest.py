import copy
import pytest
from datetime import datetime, timezone
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from typing import AsyncGenerator

from app.database.db import Base, get_db
from app.database.models import UserModel
from app.services import PasswordHasher
from app.main import app


TEST_DB_URL = "sqlite+aiosqlite:///./test_e2e.db"


EXISTING_USERS = [
  {
    "id": "user1",
    "first_name": "Alice",
    "last_name": "Smith",
    "username": "alicesmith",
    "password": "SecurePass.123",
    "created_at": datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
    "updated_at": datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
  },
  {
    "id": "user2",
    "first_name": "Bob",
    "last_name": "Johnson",
    "username": "bobjohnson",
    "password": "SecurePass.123",
    "created_at": datetime(2024, 1, 2, 0, 0, 0, tzinfo=timezone.utc),
    "updated_at": datetime(2024, 1, 2, 0, 0, 0, tzinfo=timezone.utc)
  },
  {
    "id": "user3",
    "first_name": "Charlie",
    "last_name": "Brown",
    "username": "charliebrown",
    "password": "SecurePass.123",
    "created_at": datetime(2024, 1, 3, 0, 0, 0, tzinfo=timezone.utc),
    "updated_at": datetime(2024, 1, 3, 0, 0, 0, tzinfo=timezone.utc)
  }
]


@pytest.fixture(scope="function")
def existing_users():
  return copy.deepcopy(EXISTING_USERS)


engine = create_async_engine(
  TEST_DB_URL,
  connect_args={"check_same_thread": False},
)

TestingSessionLocal = async_sessionmaker(
  engine,
  expire_on_commit=False,
  class_=AsyncSession
)


@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
  async with TestingSessionLocal() as session:
    yield session


@pytest.fixture(scope="function", autouse=True)
async def setup_database():
  async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)

  yield

  async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client():

  async def override_get_db():
    async with TestingSessionLocal() as session:
      yield session

  app.dependency_overrides[get_db] = override_get_db

  transport = ASGITransport(app=app)

  async with AsyncClient(
    transport=transport,
    base_url="http://test"
  ) as client:
    yield client

  app.dependency_overrides.clear()

@pytest.fixture
async def create_existing_users(db_session: AsyncSession, existing_users):

  for payload in existing_users:
    payload["password"] = PasswordHasher().hash(payload["password"])
    user = UserModel(**payload)
    db_session.add(user)

  await db_session.commit()


@pytest.fixture
async def authenticated_client(client, create_existing_users):

  login_data = {
    "username": "alicesmith",
    "password": "SecurePass.123"
  }

  response = await client.post("/v1/auth/login", data=login_data)

  assert response.status_code == 200

  token = response.json()["access_token"]

  client.headers.update({
    "Authorization": f"Bearer {token}"
  })

  return client