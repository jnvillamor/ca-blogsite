from src.domain.entities import UserEntity
from app.database.models import UserModel

def user_entity_to_model(user_entity: UserEntity) -> UserModel:
  return UserModel(**user_entity.to_dict())

def user_model_to_entity(user_model: UserModel) -> UserEntity:
  return UserEntity(
    id=user_model.id,
    first_name=user_model.first_name,
    last_name=user_model.last_name,
    username=user_model.username,
    password=user_model.password,
    avatar=user_model.avatar,
    created_at=user_model.created_at,
    updated_at=user_model.updated_at
  )