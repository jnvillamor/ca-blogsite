from src.application.dto import BlogResponseDTO, PaginationDTO, PaginationResponseDTO
from src.application.repositories import IBlogRepository

class GetBlogUseCase:
  def __init__(self, blog_repository: IBlogRepository):
    self.blog_repository = blog_repository

  async def get_by_id(self, blog_id: str) -> BlogResponseDTO | None:
    blog = await self.blog_repository.get_blog_by_id(blog_id)
    if not blog:
      return None

    return BlogResponseDTO.model_validate(blog.to_dict())
  
  async def get_all_blogs(self, pagination: PaginationDTO) -> PaginationResponseDTO[BlogResponseDTO]:
    blogs, count = await self.blog_repository.get_all_blogs(
      skip=pagination.skip,
      limit=pagination.limit,
      search=pagination.search
    )

    blog_dtos = [BlogResponseDTO.model_validate(blog.to_dict()) for blog in blogs]
    return PaginationResponseDTO(
      total=count,
      skip=pagination.skip,
      limit=pagination.limit,
      items=blog_dtos
    )
  
  async def get_all_blogs_by_author(self, author_id: str, pagination: PaginationDTO) -> PaginationResponseDTO[BlogResponseDTO]:
    blogs, count = await self.blog_repository.get_all_blogs_by_author(
      author_id=author_id,
      skip=pagination.skip,
      limit=pagination.limit,
      search=pagination.search
    )

    blog_dtos = [BlogResponseDTO.model_validate(blog.to_dict()) for blog in blogs]
    return PaginationResponseDTO(
      total=count,
      skip=pagination.skip,
      limit=pagination.limit,
      items=blog_dtos
    )