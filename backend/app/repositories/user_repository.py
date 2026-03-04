from app.database.mappers import user_entity_to_model, user_model_to_entity
from app.database.models import UserModel

from src.domain.exceptions import NotFoundException
from src.domain.entities.user_entity import UserEntity
from src.application.repositories import IUserRepository

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from typing import Optional, Tuple, List


class UserRepository(IUserRepository):

  def __init__(self, session: AsyncSession):
    self.session = session


  async def create_user(self, user: UserEntity) -> UserEntity:
    user_model = user_entity_to_model(user)

    self.session.add(user_model)
    await self.session.flush()

    return user_model_to_entity(user_model)


  async def get_user_by_id(self, user_id: str) -> Optional[UserEntity]:
    user_model = await self.session.get(UserModel, user_id)

    if user_model:
      return user_model_to_entity(user_model)

    return None


  async def get_user_by_username(self, username: str) -> Optional[UserEntity]:
    stmt = select(UserModel).where(UserModel.username == username)

    result = await self.session.execute(stmt)
    user_model = result.scalar_one_or_none()

    if user_model:
      return user_model_to_entity(user_model)

    return None


  async def get_all_users(
    self,
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None
  ) -> Tuple[List[UserEntity], int]:

    stmt = select(UserModel)

    if search:
      stmt = stmt.where(
        or_(
          UserModel.username.ilike(f"%{search}%"),
          UserModel.first_name.ilike(f"%{search}%"),
          UserModel.last_name.ilike(f"%{search}%")
        )
      )

    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await self.session.execute(count_stmt)).scalar_one()

    stmt = stmt.offset(skip).limit(limit)

    result = await self.session.execute(stmt)
    users = result.scalars().all()

    return [user_model_to_entity(user) for user in users], total


  async def update_user(self, user_id: str, user: UserEntity) -> UserEntity:
    existing_user = await self.session.get(UserModel, user_id)

    if not existing_user:
      raise NotFoundException("User", f"user_id: {user_id}")

    for field, value in user.to_dict().items():
      setattr(existing_user, field, value)

    return user_model_to_entity(existing_user)


  async def delete_user(self, user_id: str) -> bool:
    user_model = await self.session.get(UserModel, user_id)

    if not user_model:
      return False

    await self.session.delete(user_model)
    await self.session.flush()

    return True