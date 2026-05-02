from src.application.dto import BlogResponseDTO, PublicBlogResponseDTO, PaginationDTO, PaginationResponseDTO
from src.application.repositories import IBlogRepository
from src.domain.entities import UserEntity
from src.domain.value_objects import BlogStatus

class GetBlogUseCase:
  def __init__(self, blog_repository: IBlogRepository):
    self.blog_repository = blog_repository

  async def get_public_by_id(self, blog_id: str) -> PublicBlogResponseDTO | None:
    """Get the public-facing view of a published blog.

    Returns the published snapshot (published_title/published_content) for published blogs.
    Returns None if the blog is missing OR is still a draft (not yet published).
    """
    blog = await self.blog_repository.get_blog_by_id(blog_id)
    if not blog or blog.status != BlogStatus.PUBLISHED:
      return None

    return PublicBlogResponseDTO.model_validate(self._apply_published_snapshot(blog.to_dict()))

  async def get_owner_by_id(self, current_user: UserEntity, blog_id: str) -> BlogResponseDTO | None:
    """Get a single blog (any status) owned by the current user, with raw draft fields.

    Returns None if the blog is missing OR belongs to a different user (deliberately
    avoids leaking existence of blogs the caller does not own).
    """
    blog = await self.blog_repository.get_blog_by_id(blog_id)
    if not blog or blog.author_id != current_user.id:
      return None

    return BlogResponseDTO.model_validate(blog.to_dict())

  async def get_all_public_blogs(self, pagination: PaginationDTO) -> PaginationResponseDTO[PublicBlogResponseDTO]:
    """Get the public-facing list of all published blogs.

    Serves the published snapshot (published_title/published_content) for each blog.
    """
    blogs, count = await self.blog_repository.get_all_public_blogs(
      skip=pagination.skip,
      limit=pagination.limit,
      search=pagination.search
    )

    blog_dtos = [
      PublicBlogResponseDTO.model_validate(self._apply_published_snapshot(blog.to_dict()))
      for blog in blogs
    ]

    return PaginationResponseDTO(
      total=count,
      skip=pagination.skip,
      limit=pagination.limit,
      items=blog_dtos
    )

  async def get_all_public_blogs_by_author(self, author_id: str, pagination: PaginationDTO) -> PaginationResponseDTO[PublicBlogResponseDTO]:
    """Get the public-facing list of an author's published blogs.

    Serves the published snapshot (published_title/published_content) for each blog.
    """
    blogs, count = await self.blog_repository.get_all_public_blogs_by_author(
      author_id=author_id,
      skip=pagination.skip,
      limit=pagination.limit,
      search=pagination.search
    )

    blog_dtos = [
      PublicBlogResponseDTO.model_validate(self._apply_published_snapshot(blog.to_dict()))
      for blog in blogs
    ]

    return PaginationResponseDTO(
      total=count,
      skip=pagination.skip,
      limit=pagination.limit,
      items=blog_dtos
    )

  async def get_all_blogs_for_owner(
    self,
    current_user: UserEntity,
    pagination: PaginationDTO,
  ) -> PaginationResponseDTO[BlogResponseDTO]:
    """Get the full list of blogs (any status) owned by the current user.

    Returns raw draft title/content (not the published snapshot) so the owner can
    see in-progress edits.
    """
    blogs, count = await self.blog_repository.get_all_blogs_by_author(
      author_id=current_user.id,
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

  @staticmethod
  def _apply_published_snapshot(blog_dict: dict) -> dict:
    """Replace the draft title/content with the published snapshot in-place.

    Used for public-facing responses so readers always see the last published version,
    not any in-progress edits.
    """
    if blog_dict.get("published_title") is not None:
      blog_dict["title"] = blog_dict["published_title"]
      blog_dict["content"] = blog_dict["published_content"]
    return blog_dict
