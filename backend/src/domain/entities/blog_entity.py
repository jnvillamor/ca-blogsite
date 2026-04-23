from datetime import datetime
from typing import Any, Optional
from src.domain.value_objects import Title, Content, BlogStatus

class BlogEntity:
  def __init__(
    self,
    id: str,
    title: str,
    content: list[dict[str, Any]],
    author_id: str,
    hero_image: Optional[str] = None,
    status: str = BlogStatus.DRAFT,
    published_title: Optional[str] = None,
    published_content: Optional[list[dict[str, Any]]] = None,
    published_at: Optional[datetime] = None,
    created_at: Optional[datetime] = None,
    updated_at: Optional[datetime] = None
  ):
    self.__id = id
    self.__title = Title(title)
    self.__content = Content(content)
    self.__author_id = author_id
    self.__hero_image = hero_image
    self.__status = BlogStatus(status)
    self.__published_title = published_title
    self.__published_content = published_content
    self.__published_at = published_at
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
  def content(self) -> list[dict[str, Any]]:
    return self.__content.value

  @content.setter
  def content(self, value: list[dict[str, Any]]):
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
  def status(self) -> str:
    return self.__status.value

  @status.setter
  def status(self, value: str):
    self.__status = BlogStatus(value)
    self.__updated_at = datetime.now()

  @property
  def published_title(self) -> Optional[str]:
    return self.__published_title

  @published_title.setter
  def published_title(self, value: Optional[str]):
    self.__published_title = value

  @property
  def published_content(self) -> Optional[list[dict[str, Any]]]:
    return self.__published_content

  @published_content.setter
  def published_content(self, value: Optional[list[dict[str, Any]]]):
    self.__published_content = value

  @property
  def published_at(self) -> Optional[datetime]:
    return self.__published_at

  @published_at.setter
  def published_at(self, value: Optional[datetime]):
    self.__published_at = value

  @property
  def created_at(self) -> datetime:
    return self.__created_at

  @property
  def updated_at(self) -> datetime:
    return self.__updated_at

  def publish(self) -> None:
    """Publish the blog by copying current draft fields into the published snapshot."""
    self.__status = BlogStatus(BlogStatus.PUBLISHED)
    self.__published_title = self.__title.value
    self.__published_content = self.__content.value
    self.__published_at = datetime.now()
    self.__updated_at = datetime.now()

  def to_dict(self) -> dict:
    return {
      "id": self.id,
      "title": self.title,
      "content": self.content,
      "author_id": self.author_id,
      "hero_image": self.hero_image,
      "status": self.status,
      "published_title": self.published_title,
      "published_content": self.published_content,
      "published_at": self.published_at,
      "created_at": self.created_at,
      "updated_at": self.updated_at,
    }