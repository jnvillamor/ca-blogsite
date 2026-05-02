from app.database.mappers import blog_entity_to_model, blog_model_to_entity
from app.database.models import BlogModel

from src.domain.exceptions import NotFoundException
from src.domain.entities.blog_entity import BlogEntity
from src.application.repositories import IBlogRepository

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, case
from typing import List, Optional, Tuple

from src.domain.value_objects import BlogStatus


class BlogRepository(IBlogRepository):
  def __init__(self, db_session: AsyncSession):
    self.session = db_session


  async def create_blog(self, blog: BlogEntity) -> BlogEntity:
    blog_model = blog_entity_to_model(blog)

    self.session.add(blog_model)
    await self.session.flush()

    return blog_model_to_entity(blog_model)


  async def get_blog_by_id(self, blog_id: str) -> Optional[BlogEntity]:
    blog_model = await self.session.get(BlogModel, blog_id)

    if blog_model:
      return blog_model_to_entity(blog_model)

    return None


  async def get_all_public_blogs(
    self,
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None
  ) -> Tuple[List[BlogEntity], int]:

    stmt = select(BlogModel).where(BlogModel.published_at.is_not(None))

    if search:
      stmt = stmt.where(BlogModel.title.ilike(f"%{search}%"))

    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await self.session.execute(count_stmt)).scalar_one()

    stmt = stmt.offset(skip).limit(limit)

    result = await self.session.execute(stmt)
    blogs = result.scalars().all()

    return [blog_model_to_entity(blog) for blog in blogs], total


  async def get_all_blogs_by_author(
    self,
    author_id: str,
    skip: int = 0,
    limit: int = 10,
    search: str | None = None
  ) -> Tuple[List[BlogEntity], int]:

    stmt = select(BlogModel).where(BlogModel.author_id == author_id)

    if search:
      stmt = stmt.where(BlogModel.title.ilike(f"%{search}%"))

    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await self.session.execute(count_stmt)).scalar_one()

    stmt = stmt.offset(skip).limit(limit)

    result = await self.session.execute(stmt)
    blogs = result.scalars().all()

    return [blog_model_to_entity(blog) for blog in blogs], total


  async def get_all_public_blogs_by_author(
    self,
    author_id: str,
    skip: int = 0,
    limit: int = 10,
    search: str | None = None
  ) -> Tuple[List[BlogEntity], int]:

    stmt = select(BlogModel).where(
      BlogModel.author_id == author_id,
      BlogModel.published_at.is_not(None)
    )

    if search:
      stmt = stmt.where(BlogModel.title.ilike(f"%{search}%"))

    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await self.session.execute(count_stmt)).scalar_one()

    stmt = stmt.offset(skip).limit(limit)

    result = await self.session.execute(stmt)
    blogs = result.scalars().all()

    return [blog_model_to_entity(blog) for blog in blogs], total


  async def update_blog(self, blog_id: str, blog: BlogEntity) -> BlogEntity:

    existing_blog = await self.session.get(BlogModel, blog_id)

    if not existing_blog:
      raise NotFoundException("Blog", f"blog_id: {blog_id}")

    for field in blog.to_dict():
      setattr(existing_blog, field, getattr(blog, field))

    await self.session.flush()

    return blog_model_to_entity(existing_blog)


  async def delete_blog(self, blog_id: str) -> bool:

    blog_model = await self.session.get(BlogModel, blog_id)

    if not blog_model:
      raise NotFoundException("Blog", f"blog_id: {blog_id}")

    await self.session.delete(blog_model)
    await self.session.flush()

    return True


  async def get_blog_counts_by_author(self, author_id: str) -> Tuple[int, int, int]:
    published_count = func.coalesce(
      func.sum(case((BlogModel.status == BlogStatus.PUBLISHED, 1), else_=0)),
      0,
    )
    draft_count = func.coalesce(
      func.sum(case((BlogModel.status == BlogStatus.DRAFT, 1), else_=0)),
      0,
    )

    stmt = (
      select(func.count(), published_count, draft_count)
      .where(BlogModel.author_id == author_id)
    )

    result = await self.session.execute(stmt)
    total, published, draft = result.one()
    return int(total), int(published), int(draft)