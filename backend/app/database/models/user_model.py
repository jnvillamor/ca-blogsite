from app.database.db import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, func
from typing import Optional

class UserModel(Base):
  __tablename__ = 'users'

  id: Mapped[str] = mapped_column(primary_key=True)
  first_name: Mapped[str] = mapped_column(String(30), nullable=False)
  last_name: Mapped[str] = mapped_column(String(30), nullable=False)
  username: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
  password: Mapped[str] = mapped_column(String(255), nullable=False)
  avatar: Mapped[Optional[str]] = mapped_column(nullable=True)
  created_at: Mapped[str] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
  updated_at: Mapped[str] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

  def to_dict(self) -> dict:
    return {
      "id": self.id,
      "first_name": self.first_name,
      "last_name": self.last_name,
      "username": self.username,
      "password": self.password,
      "avatar": self.avatar,
      "created_at": self.created_at,
      "updated_at": self.updated_at
    }