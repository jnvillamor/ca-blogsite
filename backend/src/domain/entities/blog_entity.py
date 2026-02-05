from datetime import datetime
from typing import Optional
from src.domain.value_objects import Title, Content

class BlogEntity:
  def __init__(
    self,
    id: str,
    title: str,
    content: str,
    author_id: str,
    hero_image: Optional[str] = None,
    created_at: Optional[datetime] = None,
    updated_at: Optional[datetime] = None
  ):
    self.__id = id
    self.__title = Title(title) 
    self.__content = Content(content)
    self.__author_id = author_id
    self.__hero_image = hero_image
    self.__created_at = created_at or datetime.now()
    self.__updated_at = updated_at or datetime.now()
  
  @property
  def id(self) -> str:
    return self.__id
  
  @property
  def title(self) -> str:
    return self.__title.value
  
  @title.setter
  def title(self, value: str):
    self.__title = Title(value)
    self.__updated_at = datetime.now()

  @property
  def content(self) -> str:
    return self.__content.value
  
  @content.setter
  def content(self, value: str):
    self.__content = Content(value)
    self.__updated_at = datetime.now()

  @property
  def author_id(self) -> str:
    return self.__author_id
  
  @property
  def hero_image(self) -> Optional[str]:
    return self.__hero_image
  
  @hero_image.setter
  def hero_image(self, value: Optional[str]):
    self.__hero_image = value
    self.__updated_at = datetime.now()

  @property
  def created_at(self) -> datetime:
    return self.__created_at
  
  @property
  def updated_at(self) -> datetime:
    return self.__updated_at
  
  def to_dict(self) -> dict:
    return {
      "id": self.id,
      "title": self.title,
      "content": self.content,
      "author_id": self.author_id,
      "hero_image": self.hero_image,
      "created_at": self.created_at,
      "updated_at": self.updated_at,
    }