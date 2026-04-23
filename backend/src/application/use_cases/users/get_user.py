from src.application.dto import (
  UserResponseDTO,
  PaginationDTO,
  PaginationResponseDTO,
  UserIncludeOptions,
  UserBlogCountDTO,
)
from src.application.repositories import IUserRepository, IBlogRepository
from src.domain.entities import UserEntity

class GetUserUseCase:
  def __init__(
    self,
    user_repository: IUserRepository,
    blog_repository: IBlogRepository,
  ):
    self.user_repository = user_repository
    self.blog_repository = blog_repository

  async def get_by_id(
    self,
    user_id: str,
    include_options: UserIncludeOptions = UserIncludeOptions(),
  ) -> UserResponseDTO | None:
    user = await self.user_repository.get_user_by_id(user_id)
    if not user:
      return None

    return await self._build_response(user, include_options)

  async def get_by_username(
    self,
    username: str,
    include_options: UserIncludeOptions = UserIncludeOptions(),
  ) -> UserResponseDTO | None:
    user = await self.user_repository.get_user_by_username(username)
    if not user:
      return None

    return await self._build_response(user, include_options)

  async def get_all_users(
    self,
    pagination: PaginationDTO,
    include_options: UserIncludeOptions = UserIncludeOptions(),
  ) -> PaginationResponseDTO[UserResponseDTO]:
    users, count = await self.user_repository.get_all_users(
      skip=pagination.skip,
      limit=pagination.limit,
      search=pagination.search
    )

    user_dtos = [await self._build_response(user, include_options) for user in users]
    return PaginationResponseDTO(
      total=count,
      skip=pagination.skip,
      limit=pagination.limit,
      items=user_dtos
    )

  async def _build_response(
    self,
    user: UserEntity,
    include_options: UserIncludeOptions,
  ) -> UserResponseDTO:
    dto = UserResponseDTO.model_validate(user.to_dict())

    if include_options.include_blog_count:
      total, published, draft = await self.blog_repository.get_blog_counts_by_author(user.id)
      dto.blog_count = UserBlogCountDTO(
        total_blogs=total,
        published_blogs=published,
        draft_blogs=draft,
      )

    return dto
