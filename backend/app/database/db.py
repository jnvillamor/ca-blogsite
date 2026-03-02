import logging
from app.config import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import Generator

logger = logging.getLogger(__name__)

# Base for models
Base = declarative_base()

# Sync engine
engine = create_engine(
  config.DATABASE_URL,
  echo=config.DB_ECHO,
  future=True
)

# Session factory
SessionLocal = sessionmaker(
  bind=engine,
  expire_on_commit=False,
  class_=Session
)

def get_db() -> Generator[Session, None, None]:
  """
  Yield a sync SQLAlchemy session for endpoints or CLI usage.
  """
  db = SessionLocal()
  try:
    logger.info("Database session created.")   
    yield db
  except Exception:
    raise
  finally:
    logger.info("Closing database session.")
    db.close()
