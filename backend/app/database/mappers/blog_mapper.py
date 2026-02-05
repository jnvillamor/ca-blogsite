from app.database.models import BlogModel
from src.domain.entities import BlogEntity

def blog_entity_to_model(blog_entity: BlogEntity) -> BlogModel:
  return BlogModel(**blog_entity.to_dict())

def blog_model_to_entity(blog_model: BlogModel) -> BlogEntity:
  return BlogEntity(**blog_model.to_dict())