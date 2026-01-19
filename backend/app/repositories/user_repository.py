from app.database.mappers import user_model_to_entity, user_entity_to_model
from app.database.models import UserModel
from src.application.repositories import IUserRepository
from src.domain.entities import UserEntity
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional

class UserRepository(IUserRepository):
  def __init__(self, session: AsyncSession):
    self.session = session
  
  async def create_user(self, user: UserEntity) -> UserEntity:
    user_model = user_entity_to_model(user)
    self.session.add(user_model)

    await self.session.flush()
    return user_model_to_entity(user_model)
  
  async def get_user_by_id(self, user_id: str) -> Optional[UserEntity]:
    result = await self.session.get(UserModel, user_id)
    if result:
      return user_model_to_entity(result)
    return None
  
  async def get_user_by_username(self, username: str) -> Optional[UserEntity]:
    result = await self.session.execute(
      select(UserModel).where(UserModel.username == username)
    )
    user_model = result.scalars().first()
    if user_model:
      return user_model_to_entity(user_model)
    return None
  
  async def get_all_users(self, skip = 0, limit = 10, search = None):
    total_query = select(func.count(UserModel.id)).select_from(UserModel)
    data_query = select(UserModel).offset(skip).limit(limit)
    
    if search:
      data_query = data_query.where(
        UserModel.username.ilike(f"%{search}%"),
        UserModel.first_name.ilike(f"%{search}%"),
        UserModel.last_name.ilike(f"%{search}%")
      )
    
    total_result = await self.session.execute(total_query)
    total_count = total_result.scalar_one()
    data_result = await self.session.execute(data_query)
    user_models = data_result.scalars().all()
    user_entities = [user_model_to_entity(user_model) for user_model in user_models]
    return user_entities, total_count
  
  async def update_user(self, user_id, user):
    user_model = await self.session.get(UserModel, user_id)
    if not user_model:
      return None
    
    for key, value in user.to_dict().items():
      if hasattr(user_model, key):
        setattr(user_model, key, value)
    
    await self.session.flush()
    return user_model_to_entity(user_model)
  
    
  async def delete_user(self, user_id):
    user_model = await self.session.get(UserModel, user_id)
    if user_model:
      await self.session.delete(user_model)
      await self.session.flush()
    