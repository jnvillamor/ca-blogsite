import re
import pytest
from fastapi.testclient import TestClient

class TestCreateBlogEndpoint:
  def test_create_blog_success(
    self, 
    api_version,
    existing_users,
    create_existing_users,
    client: TestClient,
  ):
    payload = {
      "title": "My First Blog",
      "content": "This is the content of my first blog.",
      "author_id": existing_users[0]["id"]
    }
    response = client.post(f"/{api_version}/blogs/", json=payload)

    assert response.status_code == 201
    data = response.json()
    for key in payload:
      assert data[key] == payload[key]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data
  
  def test_create_blog_user_not_found(self, api_version, client: TestClient):
    payload = {
      "title": "Blog with Invalid Author",
      "content": "This blog has an invalid author_id.",
      "author_id": "nonexistent-user-id"
    }
    response = client.post(f"/{api_version}/blogs/", json=payload)

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Author not found."
  
  @pytest.mark.parametrize(
    "title, error_regex",
    [
      ("", r"Title cannot be empty."),
      (" " * 10, r"Title cannot be empty."),
      ("Shrt", r"Title must be at least 5 characters long."),
      ("T" * 101, r"Title cannot exceed 100 characters.")
    ]
  )
  def test_create_blog_invalid_title(
    self,
    existing_users,
    api_version,
    create_existing_users,
    client: TestClient,
    title,
    error_regex
  ):
    payload = {
      "title": title,
      "content": "Valid content for testing.",
      "author_id": existing_users[0]["id"]
    }
    response = client.post(f"/{api_version}/blogs/", json=payload)

    assert response.status_code == 400
    data = response.json()
    assert re.search(error_regex, data["detail"])
  
  @pytest.mark.parametrize(
    "content, error_regex",
    [
      ("", r"Content cannot be empty."),
      (" " * 10, r"Content cannot be empty.")
    ]
  )
  def test_invalid_content(
    self,
    api_version,
    existing_users,
    create_existing_users,
    client: TestClient,
    content,
    error_regex
  ):
    payload = {
      "title": "Valid Title",
      "content": content,
      "author_id": existing_users[0]["id"]
    }
    response = client.post(f"/{api_version}/blogs/", json=payload)

    assert response.status_code == 400
    data = response.json()
    assert re.search(error_regex, data["detail"])