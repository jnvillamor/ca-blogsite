import pytest

class TestDeleteBlogEndpoint:
  def test_delete_blog_success(
    self,
    authenticated_client,
    api_version,
    existing_blogs,
    existing_users,
    create_existing_blogs,
  ):
    blog_to_delete = existing_blogs[0]
    response = authenticated_client.delete(
      f"/{api_version}/blogs/{blog_to_delete['id']}"
    )

    assert response.status_code == 204
  
  def test_delete_blog_not_found(
    self, 
    authenticated_client, 
    api_version
  ):
    response = authenticated_client.delete(
      f"/{api_version}/blogs/nonexistent-blog"
    )

    assert response.status_code == 404
    assert response.json() == {
      "detail": "Blog with identifier 'blog_id: nonexistent-blog' was not found."
    }
  
  def test_delete_blog_unauthorized(
    self, 
    authenticated_client, 
    api_version,
    existing_blogs,
    create_existing_blogs,
  ):
    blog_to_delete = existing_blogs[1]
    response = authenticated_client.delete(
      f"/{api_version}/blogs/{blog_to_delete['id']}"
    )

    assert response.status_code == 401
    assert response.json() == {
      "detail": "You are not authorized to delete this blog."
    }