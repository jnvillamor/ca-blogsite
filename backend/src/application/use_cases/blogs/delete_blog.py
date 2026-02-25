from src.application.services import IUnitOfWork
from src.domain.entities import UserEntity
from src.domain.exceptions import NotFoundException, UnauthorizedException

class DeleteBlogUseCase:
  def __init__(self, unit_of_work: IUnitOfWork):
    self.uow = unit_of_work
  
  def execute(self, current_user: UserEntity, blog_id: str) -> None:
    with self.uow:
      blog = self.uow.blogs.get_blog_by_id(blog_id)

      if not blog:
        raise NotFoundException("Blog", f"blog_id: {blog_id}")

      if current_user.id != blog.author_id:
        raise UnauthorizedException("You are not authorized to delete this blog.")
      
      self.uow.blogs.delete_blog(blog_id)