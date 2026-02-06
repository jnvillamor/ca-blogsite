from abc import ABC, abstractmethod
from typing import Optional, Tuple, List
from src.domain.entities import BlogEntity

class IBlogRepository(ABC):
  @abstractmethod
  def create_blog(self, blog: BlogEntity) -> BlogEntity:
    """Create a new blog.

    Args:
      blog (BlogEntity): The blog entity to create.

    Returns:
      BlogEntity: The created blog entity
    """
    pass

  @abstractmethod
  def get_blog_by_id(self, blog_id: str) -> Optional[BlogEntity]:
    """Retrieve a blog by its ID.

    Args:
      blog_id (str): The ID of the blog to retrieve.

    Returns:
      Optional[BlogEntity]: The blog entity if found, otherwise None.
    """
    pass

  @abstractmethod
  def get_all_blogs(
    self,
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None
  ) -> Tuple[List[BlogEntity], int]:
    """Retrieve all blogs with pagination and optional search.

    Args:
      skip (int, optional): Number of records to skip. Defaults to 0.
      limit (int, optional): Maximum number of records to return. Defaults to 10.
      search (Optional[str], optional): Search term for filtering blogs. Defaults to None.

    Returns:
      Tuple[List[BlogEntity], int]: A tuple containing the list of blog entities and the total count.
    """
    pass

  @abstractmethod
  def get_all_blogs_by_author(
    self,
    author_id: str,
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None
  ) -> Tuple[List[BlogEntity], int]:
    """Retrieve all blogs by a specific author with pagination and optional search.

    Args:
      author_id (str): The ID of the author whose blogs to retrieve.
      skip (int, optional): Number of records to skip. Defaults to 0.
      limit (int, optional): Maximum number of records to return. Defaults to 10.
      search (Optional[str], optional): Search term for filtering blogs. Defaults to None.

    Returns:
      Tuple[List[BlogEntity], int]: A tuple containing the list of blog entities and the total count.
    """
    pass

  @abstractmethod
  def update_blog(self, blog_id: str, blog: BlogEntity) -> BlogEntity:
    """Update an existing blog.

    Args:
      blog_id (str): The ID of the blog to update.
      blog (BlogEntity): The blog entity with updated data.

    Returns:
      BlogEntity: The updated blog entity.
    """
    pass

  @abstractmethod
  def delete_blog(self, blog_id: str) -> bool:
    """Delete a blog by its ID.

    Args:
      blog_id (str): The ID of the blog to delete.
    """
    pass