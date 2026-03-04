import logging
from app.config import config
from sqlalchemy.ext.asyncio import (
  create_async_engine,
  AsyncSession,
  async_sessionmaker
) 
from sqlalchemy.orm import declarative_base
from typing import AsyncGenerator

logger = logging.getLogger(__name__)

# Base for models
Base = declarative_base()

# Create the async engine
engine = create_async_engine(
  config.DATABASE_URL,
  echo=config.DB_ECHO
)

# Session factory
SessionLocal = async_sessionmaker(
  bind=engine,
  expire_on_commit=False,
  class_=AsyncSession
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
  """
  Yield an async SQLAlchemy session for endpoints or CLI usage.
  """
  async with SessionLocal() as db:
    try:
      logger.info("Database session created.")
      yield db
    except Exception:
      raise
    finally:
      logger.info("Closing database session.")
      await db.close()