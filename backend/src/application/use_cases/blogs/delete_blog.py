from src.application.services import IUnitOfWork
from src.domain.exceptions import NotFoundException

class DeleteBlogUseCase:
  def __init__(self, unit_of_work: IUnitOfWork):
    self.uow = unit_of_work
  
  def execute(self, blog_id: str) -> None:
    with self.uow:
      blog = self.uow.blogs.get_blog_by_id(blog_id)

      if not blog:
        raise NotFoundException("Blog", f"blog_id: {blog_id}")
      
      self.uow.blogs.delete_blog(blog_id)