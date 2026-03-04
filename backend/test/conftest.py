import pytest
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)
from typing import AsyncGenerator

from app.database.db import Base

TEST_DB_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
  TEST_DB_URL,
  echo=False
)

TestingSessionLocal = async_sessionmaker(
  bind=engine,
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