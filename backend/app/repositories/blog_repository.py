from app.database.mappers import blog_entity_to_model, blog_model_to_entity
from app.database.models import BlogModel
from src.domain.exceptions import NotFoundException
from src.domain.entities.blog_entity import BlogEntity
from src.application.repositories import IBlogRepository

from sqlalchemy.orm import Session
from typing import List, Optional, Tuple

class BlogRepository(IBlogRepository):
  def __init__(self, db_session: Session):
    self.session = db_session

  def create_blog(self, blog: BlogEntity) -> BlogEntity:
    blog_model = blog_entity_to_model(blog)
    self.session.add(blog_model)
    self.session.flush()
    return blog_model_to_entity(blog_model)
  
  def get_blog_by_id(self, blog_id: str) -> Optional[BlogEntity]:
    blog_model = self.session.get(BlogModel, blog_id)
    if blog_model:
      return blog_model_to_entity(blog_model)
    return None

  def get_all_blogs(
    self, 
    skip: int = 0, 
    limit: int = 10, 
    search: Optional[str] = None
  ) -> Tuple[List[BlogEntity], int]:
    query = self.session.query(BlogModel)
    if search:
      query = query.filter(BlogModel.title.ilike(f"%{search}%"))
    
    total = query.count()
    blogs = query.offset(skip).limit(limit).all()
    return [blog_model_to_entity(blog) for blog in blogs], total
  
  def get_all_blogs_by_author(
    self, 
    author_id: str, 
    skip: int = 0,
    limit: int = 10, 
    search: str | None = None
  ) -> Tuple[List[BlogEntity], int]:
    query = (
      self.session
      .query(BlogModel)
      .filter(BlogModel.author_id == author_id)
    )

    if search:
      query = query.filter(BlogModel.title.ilike(f"%{search}%"))
    
    total = query.count()
    blogs = query.offset(skip).limit(limit).all()
    return [blog_model_to_entity(blog) for blog in blogs], total

  def update_blog(self, blog_id: str, blog: BlogEntity) -> BlogEntity:
    existing_blog = self.session.get(BlogModel, blog_id)
    if not existing_blog:
      raise NotFoundException("Blog", f"blog_id: {blog_id}")

    for field in blog.to_dict():
      setattr(existing_blog, field, getattr(blog, field))
    self.session.flush()
    return blog_model_to_entity(existing_blog)
  
  def delete_blog(self, blog_id: str) -> bool:
    blog_model = self.session.get(BlogModel, blog_id)
    if not blog_model:
      raise NotFoundException("Blog", f"blog_id: {blog_id}")
    
    self.session.delete(blog_model)
    self.session.flush()
    return True