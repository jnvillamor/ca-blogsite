from src.domain.entities import UserEntity
from app.database.models import UserModel

def user_entity_to_model(user_entity: UserEntity) -> UserModel:
  return UserModel(**user_entity.to_dict())

def user_model_to_entity(user_model: UserModel) -> UserEntity:
  return UserEntity(**user_model.to_dict())