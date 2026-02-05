from app.database.db import Base

from datetime import datetime
from sqlalchemy import String, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

class BlogModel(Base):
  __tablename__ = "blogs"

  id: Mapped[str] = mapped_column(primary_key=True)
  title: Mapped[str] = mapped_column(String(100), nullable=False)
  content: Mapped[str] = mapped_column(String, nullable=False)
  author_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
  hero_image: Mapped[Optional[str]] = mapped_column(String, nullable=True)
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
      "created_at": self.created_at,
      "updated_at": self.updated_at,
    }
