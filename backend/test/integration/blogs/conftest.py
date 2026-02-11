import pytest
from sqlalchemy.orm import Session
from typing import Callable
from app.database.models import BlogModel, UserModel

@pytest.fixture
def create_test_user(db_session) -> Callable[..., UserModel]:
  def _create_test_user(
    id: str = "test-user-id", 
    first_name: str = "Test", 
    last_name: str = "User", 
    username: str = "testuser") -> UserModel:
    
    test_user = UserModel(
      id=id,
      first_name=first_name,
      last_name=last_name,
      username=username,
      avatar="https://example.com/avatar.png",
      password="hashedpassword",
    )
    db_session.add(test_user)
    db_session.commit()
    return test_user

  return _create_test_user

@pytest.fixture
def create_test_blog(db_session) -> Callable[..., BlogModel]:
  def _create_test_blog(
    id: str = "test-blog-id",
    title: str = "Test Blog Title",
    content: str = "This is the content of the test blog.",
    author_id: str = "test-user-id",
    hero_image: str = "https://example.com/hero-image.png"
  ) -> BlogModel:
    
    test_blog = BlogModel(
      id=id,
      title=title,
      content=content,
      author_id=author_id,
      hero_image=hero_image
    )
    db_session.add(test_blog)
    db_session.commit()
    return test_blog

  return _create_test_blog