from src.application.dto import BlogResponseDTO
from src.application.services import IUnitOfWork
from src.domain.entities import UserEntity
from src.domain.exceptions import NotFoundException, UnauthorizedException

class PublishBlogUseCase:
  def __init__(self, unit_of_work: IUnitOfWork):
    self.uow = unit_of_work

  async def execute(
    self,
    current_user: UserEntity,
    blog_id: str,
  ) -> BlogResponseDTO:
    async with self.uow:
      blog = await self.uow.blogs.get_blog_by_id(blog_id)

      if not blog:
        raise NotFoundException("Blog", f"blog_id: {blog_id}")

      if current_user.id != blog.author_id:
        raise UnauthorizedException("You are not authorized to publish this blog.")

      blog.publish()

      updated_blog = await self.uow.blogs.update_blog(blog_id, blog)
      return BlogResponseDTO.model_validate(updated_blog.to_dict())
