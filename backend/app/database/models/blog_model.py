from app.database.db import Base

from datetime import datetime
from typing import Any, Optional

from sqlalchemy import JSON, String, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

class BlogModel(Base):
  __tablename__ = "blogs"

  id: Mapped[str] = mapped_column(primary_key=True)
  title: Mapped[str] = mapped_column(String(100), nullable=False)
  content: Mapped[list[dict[str, Any]]] = mapped_column(
    JSON().with_variant(JSONB, "postgresql"),
    nullable=False
  )
  author_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
  hero_image: Mapped[Optional[str]] = mapped_column(String, nullable=True)
  status: Mapped[str] = mapped_column(String(20), nullable=False, server_default="draft")
  published_title: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
  published_content: Mapped[Optional[list[dict[str, Any]]]] = mapped_column(
    JSON().with_variant(JSONB, "postgresql"),
    nullable=True
  )
  published_at: Mapped[Optional[datetime]] = mapped_column(
    DateTime(timezone=True),
    nullable=True
  )
  created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    nullable=False,
    server_default=func.now()
  )
  updated_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    nullable=False,
    server_default=func.now(),
    onupdate=func.now()
  )

  def to_dict(self) -> dict:
    return {
      "id": self.id,
      "title": self.title,
      "content": self.content,
      "author_id": self.author_id,
      "hero_image": self.hero_image,
      "status": self.status,
      "published_title": self.published_title,
      "published_content": self.published_content,
      "published_at": self.published_at,
      "created_at": self.created_at,
      "updated_at": self.updated_at,
    }
