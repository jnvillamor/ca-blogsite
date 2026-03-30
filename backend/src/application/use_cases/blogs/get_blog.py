from src.application.dto import BlogResponseDTO, PublicBlogResponseDTO, PaginationDTO, PaginationResponseDTO
from src.application.repositories import IBlogRepository

class GetBlogUseCase:
  def __init__(self, blog_repository: IBlogRepository):
    self.blog_repository = blog_repository

  async def get_by_id(self, blog_id: str) -> BlogResponseDTO | None:
    blog = await self.blog_repository.get_blog_by_id(blog_id)
    if not blog:
      return None

    return BlogResponseDTO.model_validate(blog.to_dict())

  async def get_public_by_id(self, blog_id: str) -> PublicBlogResponseDTO | None:
    """Get the public-facing view of a blog.

    For published blogs, serves the published snapshot (published_title/published_content).
    For draft blogs, serves the current draft title/content.
    """
    blog = await self.blog_repository.get_blog_by_id(blog_id)
    if not blog:
      return None

    blog_dict = blog.to_dict()

    # If the blog has been published, serve the published snapshot
    if blog_dict["status"] == "published" and blog_dict["published_title"] is not None:
      blog_dict["title"] = blog_dict["published_title"]
      blog_dict["content"] = blog_dict["published_content"]

    return PublicBlogResponseDTO.model_validate(blog_dict)
  
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