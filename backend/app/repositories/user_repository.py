from app.database.mappers import user_entity_to_model, user_model_to_entity
from app.database.models import UserModel
from src.domain.exceptions import NotFoundException
from src.domain.entities.user_entity import UserEntity
from src.application.repositories import IUserRepository
from sqlalchemy.orm import Session

class UserRepository(IUserRepository):
  def __init__(self, session: Session):
    self.session = session
    
  def create_user(self, user):
    user_model = user_entity_to_model(user)
    self.session.add(user_model)
    
    self.session.flush()
    return user_model_to_entity(user_model)

  def get_user_by_id(self, user_id):
    user_model = self.session.get(UserModel, user_id)
    if user_model:
      return user_model_to_entity(user_model)
    return None
  
  def get_user_by_username(self, username):
    user_model = self.session.query(UserModel).filter(UserModel.username == username).first()
    if user_model:
      return user_model_to_entity(user_model)
    return None
  
  def get_all_users(self, skip = 0, limit = 10, search = None):
    query = self.session.query(UserModel)
    if search:
      query = query.filter(
        (UserModel.username.ilike(f"%{search}%")) |
        (UserModel.first_name.ilike(f"%{search}%")) |
        (UserModel.last_name.ilike(f"%{search}%"))
      )
    
    total = query.count()
    users = query.offset(skip).limit(limit).all()
    return [user_model_to_entity(user) for user in users], total

  def update_user(self, user_id: str, user: UserEntity) -> UserEntity:
    existing_user = self.session.get(UserModel, user_id)
    if not existing_user:
      raise NotFoundException("User", f"user_id: {user_id}")
    
    for field in user.to_dict():
      setattr(existing_user, field, getattr(user, field))
    
    self.session.flush()
    return user_model_to_entity(existing_user)
  
  def delete_user(self, user_id):
    user_model = self.session.get(UserModel, user_id)
    if not user_model:
      return False
    
    self.session.delete(user_model)
    self.session.flush()
    return True