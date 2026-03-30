from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel

from .basic_dto import BasicUserDTO

class CreateBlogDTO(BaseModel):
  title: str
  content: list[dict[str, Any]]
  author_id: str
  hero_image: Optional[str] = None

class UpdateBlogDTO(BaseModel):
  title: Optional[str] = None
  content: Optional[list[dict[str, Any]]] = None
  hero_image: Optional[str] = None

class BlogResponseDTO(BaseModel):
  id: str
  title: str
  content: list[dict[str, Any]]
  author_id: str
  created_at: datetime
  updated_at: datetime
  hero_image: Optional[str] = None
  author: Optional[BasicUserDTO] = None
