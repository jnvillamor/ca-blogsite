import pytest
from sqlalchemy.orm import Session
from app.database.models import BlogModel
from app.database.unit_of_work import UnitOfWork
from src.application.use_cases.blog import DeleteBlogUseCase

@pytest.fixture
def delete_blog_use_case(db_session: Session) -> DeleteBlogUseCase:
  unit_of_work = UnitOfWork(session=db_session)
  use_case = DeleteBlogUseCase(unit_of_work=unit_of_work)
  return use_case

class TestDeleteBlogUseCase:
  def test_delete_blog_success(
    self,
    db_session: Session,
    create_test_blog,
    delete_blog_use_case: DeleteBlogUseCase,
  ):
    test_blog = create_test_blog()
    
    # Test if blog exists before deletion
    blog_in_db: BlogModel = db_session.query(BlogModel).filter_by(id=test_blog.id).first()
    assert blog_in_db is not None
    assert blog_in_db.title == test_blog.title
    assert blog_in_db.id == test_blog.id
    
    delete_blog_use_case.execute(blog_id=test_blog.id)
    
    # Test if blog is deleted
    blog_after_delete = db_session.query(BlogModel).filter_by(id=test_blog.id).first()
    
    assert blog_after_delete is None
  
  def test_delete_blog_non_existing(
    self,
    delete_blog_use_case: DeleteBlogUseCase,
  ):
    non_existing_blog_id = "non-existing-id"
    
    with pytest.raises(Exception) as exc_info:
      delete_blog_use_case.execute(blog_id=non_existing_blog_id)
    
    assert "Blog with identifier 'blog_id: non-existing-id' was not found." in str(exc_info.value)