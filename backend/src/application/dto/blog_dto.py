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
  status: str = "draft"
  published_title: Optional[str] = None
  published_content: Optional[list[dict[str, Any]]] = None
  published_at: Optional[datetime] = None
  created_at: datetime
  updated_at: datetime
  hero_image: Optional[str] = None
  author: Optional[BasicUserDTO] = None

class PublicBlogResponseDTO(BaseModel):
  """Response DTO for public-facing blog views. Serves the published snapshot."""
  id: str
  title: str
  content: list[dict[str, Any]]
  author_id: str
  status: str
  published_at: Optional[datetime] = None
  created_at: datetime
  updated_at: datetime
  hero_image: Optional[str] = None
  author: Optional[BasicUserDTO] = None
