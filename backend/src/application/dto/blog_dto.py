from pydantic import BaseModel
from typing import Optional
from .basic_dto import BasicUserDTO

class CreateBlogDTO(BaseModel):
  title: str
  content: str
  author_id: str
  hero_image: Optional[str] = None

class UpdateBlogDTO(BaseModel):
  title: Optional[str] = None
  content: Optional[str] = None
  hero_image: Optional[str] = None

class BlogResponseDTO(BaseModel):
  id: str
  title: str
  content: str
  author_id: str
  created_at: str
  updated_at: str
  hero_image: Optional[str] = None 
  author: Optional[BasicUserDTO] = None