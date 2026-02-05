import pytest
from src.application.dto import PaginationDTO, BlogResponseDTO, PaginationResponseDTO
from src.application.use_cases.blog import GetBlogUseCase
from src.domain.entities import BlogEntity

class TestGetBlogUseCase:
  @pytest.fixture
  def blog_repository(self, mocker):
    blog_repository = mocker.Mock()
    return blog_repository
  
  @pytest.fixture
  def use_case(self, blog_repository) -> GetBlogUseCase:
    return GetBlogUseCase(blog_repository=blog_repository)
  
  @pytest.fixture
  def valid_blog_data(self) -> BlogEntity:
    return BlogEntity(
      id='blog-123',
      title='Test Blog',
      content='This is a test blog content.',
      author_id='author-123',
      created_at='2024-01-01T00:00:00Z',
      updated_at='2024-01-01T00:00:00Z'
    )
  
  @pytest.fixture
  def valid_blogs_list(self) -> list[BlogEntity]:
    return [
      BlogEntity(
        id='blog-123',
        title='Test Blog 1',
        content='This is the first test blog content.',
        author_id='author-123',
        created_at='2024-01-01T00:00:00Z',
        updated_at='2024-01-01T00:00:00Z'
      ),
      BlogEntity(
        id='blog-124',
        title='Test Blog 2',
        content='This is the second test blog content.',
        author_id='author-124',
        created_at='2024-01-02T00:00:00Z',
        updated_at='2024-01-02T00:00:00Z'
      )
    ]
    
  def test_get_by_id_success(
    self, 
    use_case, 
    blog_repository, 
    valid_blog_data
  ):
    # Arrange
    blog_repository.get_blog_by_id.return_value = valid_blog_data
    
    # Act
    result = use_case.get_by_id('blog-123')

    # Assert
    assert result == BlogResponseDTO.model_validate(valid_blog_data.to_dict())
    blog_repository.get_blog_by_id.assert_called_once_with('blog-123')
  
  def test_get_by_id_not_found(
    self, 
    use_case, 
    blog_repository
  ):
    # Arrange
    blog_repository.get_blog_by_id.return_value = None
    
    # Act
    result = use_case.get_by_id('non-existing-blog-id')

    # Assert
    assert result is None
    blog_repository.get_blog_by_id.assert_called_once_with('non-existing-blog-id')

  def test_get_all_blogs(
    self, 
    use_case, 
    blog_repository, 
    valid_blogs_list
  ):
    # Arrange
    pagination = PaginationDTO(skip=0, limit=10, search=None)
    blog_repository.get_all_blogs.return_value = [valid_blogs_list, len(valid_blogs_list)]
    
    # Act
    result = use_case.get_all_blogs(pagination)

    # Assert
    expected_response = PaginationResponseDTO(
      items=[BlogResponseDTO.model_validate(blog.to_dict()) for blog in valid_blogs_list],
      total=len(valid_blogs_list),
      skip=pagination.skip,
      limit=pagination.limit
    )
    assert result == expected_response
    blog_repository.get_all_blogs.assert_called_once_with(
      skip=pagination.skip,
      limit=pagination.limit,
      search=pagination.search
    )