import pytest
from fastapi.testclient import TestClient

class TestGetBlogEndpoint:
  @pytest.mark.parametrize(
    "limit, skip, expected_count",
    [
      (15, 0, 15),
      (15, 15, 0),
      (5, 0, 5),
      (1, 14, 1),
    ]
  )
  def test_get_all_blogs_success(
    self,
    client: TestClient,
    create_existing_blogs,
    limit,
    skip,
    expected_count
  ):
    response = client.get(f"v1/blogs/?limit={limit}&skip={skip}")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["items"], list)
    assert len(data["items"]) == expected_count
    assert data["skip"] == skip
    assert data["limit"] == limit
    assert data["total"] == 15 # This is based on the number of blogs created in the fixture, adjust if needed.

  @pytest.mark.parametrize(
    "search_query, expected_count",
    [
      ("Test Blog", 10), # Matches all but the default limit is 10
      ("test blog 1", 7), # Matches "Test Blog 1, 10, 11, 12, 13, 14, 15",
      ("Nonexistent", 0),
    ]
  )
  def test_get_blogs_with_search(
    self,
    client: TestClient,
    create_existing_blogs,
    search_query,
    expected_count
  ):
    response = client.get(f"v1/blogs/?search={search_query}")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["items"], list)
    assert len(data["items"]) == expected_count

  @pytest.mark.parametrize(
    "blog_id",
    [
      "blog-1",
      "blog-5",
      "blog-15",
    ]
  )
  def test_get_blog_by_id_success(
    self,
    client: TestClient,
    create_existing_blogs,
    blog_id
  ):
    response = client.get(f"v1/blogs/{blog_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == blog_id
    assert data["title"] == f"Test Blog {blog_id.split('-')[1]}"
    assert data["content"] == f"This is the content of test blog {blog_id.split('-')[1]}."
    assert data["author_id"] is not None
  
  def test_get_blog_by_id_not_found(self, client: TestClient):
    response = client.get("v1/blogs/nonexistent-blog-id")

    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Blog with id 'nonexistent-blog-id' not found."
