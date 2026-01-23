from src.application.services import IUnitOfWork, IIdGenerator
from src.application.dto import CreateBlogDTO, BlogResponseDTO, BlogWithAuthorDTO
from src.domain.entities import BlogEntity
from src.domain.exceptions import NotFoundException

class CreateBlogUseCase:
  def __init__(
    self,
    unit_of_work: IUnitOfWork,
    id_generator: IIdGenerator
  ):
    self.uow = unit_of_work
    self.id_generator = id_generator

  def execute(
    self, 
    blog_data: CreateBlogDTO, 
    return_with_author: bool = False
  ) -> BlogResponseDTO | BlogWithAuthorDTO:
    with self.uow:
      user = self.uow.users.get_user_by_id(blog_data.author_id)

      if not user:
        raise NotFoundException("User", f"user_id: {blog_data.author_id}")
      
      blog_id = self.id_generator.generate()

      new_blog = BlogEntity(
        id=blog_id,
        title=blog_data.title,
        content=blog_data.content,
        author_id=blog_data.author_id,
        hero_image=blog_data.hero_image
      )
      created_blog = self.uow.blogs.create_blog(new_blog)

      if return_with_author:
        return BlogWithAuthorDTO.model_validate({
          **created_blog.to_dict(),
          "author": user.to_dict()
        })
      return BlogResponseDTO.model_validate(created_blog.to_dict())
