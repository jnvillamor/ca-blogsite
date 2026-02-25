from src.application.dto import UpdateBlogDTO, BlogResponseDTO
from src.application.services import IUnitOfWork
from src.domain.entities import UserEntity
from src.domain.exceptions import NotFoundException, UnauthorizedException

class UpdateBlogUseCase:
  def __init__(self, unit_of_work: IUnitOfWork):
    self.uow = unit_of_work 
  
  def execute(
    self,
    current_user: UserEntity,
    blog_id: str,
    blog_data: UpdateBlogDTO
  ) -> BlogResponseDTO:
    with self.uow:
      blog = self.uow.blogs.get_blog_by_id(blog_id)

      if not blog:
        raise NotFoundException("Blog", f"blog_id: {blog_id}")
      
      if current_user.id != blog.author_id:
        raise UnauthorizedException("You are not authorized to update this blog.")
      
      for field, value in blog_data.model_dump(exclude_none=True).items():
        setattr(blog, field, value)
      
      updated_blog = self.uow.blogs.update_blog(blog_id, blog)
      return BlogResponseDTO.model_validate(updated_blog.to_dict())