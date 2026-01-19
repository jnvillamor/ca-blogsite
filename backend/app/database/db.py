from app.config import config
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

engine: AsyncEngine = create_async_engine(
  config.DATABASE_URL,
  echo=config.DB_ECHO,
  future=True
)

async_session = sessionmaker(
  engine, 
  expire_on_commit=False, 
  class_=AsyncSession
)