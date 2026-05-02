import pytest
from httpx import AsyncClient

class TestCreateBlogEndpoint:
  async def test_create_blog_success(
    self, 
    api_version,
    existing_users,
    create_existing_users,
    client: AsyncClient,
  ):
    payload = {
      "title": "My First Blog",
      "content": [{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "This is the content of my first blog.", "styles": {}}], "children": []}],
      "author_id": existing_users[0]["id"]
    }
    response = await client.post(f"/{api_version}/blogs/", json=payload)

    assert response.status_code == 201
    data = response.json()
    for key in payload:
      assert data[key] == payload[key]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data
  
  async def test_create_blog_user_not_found(self, api_version, client: AsyncClient):
    payload = {
      "title": "Blog with Invalid Author",
      "content": [{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "This blog has an invalid author_id.", "styles": {}}], "children": []}],
      "author_id": "nonexistent-user-id"
    }
    response = await client.post(f"/{api_version}/blogs/", json=payload)

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Author not found."
  
  @pytest.mark.parametrize(
    "title",
    [
      "",
      " " * 10,
      "Shrt",
      "T" * 101,
    ],
    ids=["empty", "whitespace_only", "too_short", "too_long"]
  )
  async def test_create_blog_persists_draft_with_publish_invalid_title(
    self,
    existing_users,
    api_version,
    create_existing_users,
    client: AsyncClient,
    title
  ):
    """The endpoint must accept titles that would fail publish-time invariants
    when the blog is being created as a draft. Publish-time invariants are
    exercised separately at the entity / use-case layer."""
    payload = {
      "title": title,
      "content": [{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Valid content for draft.", "styles": {}}], "children": []}],
      "author_id": existing_users[0]["id"]
    }
    response = await client.post(f"/{api_version}/blogs/", json=payload)

    assert response.status_code == 201
    data = response.json()
    # Title is normalized via `(value or "").strip()` inside the Title VO.
    assert data["title"] == title.strip()
    assert data["status"] == "draft"
    assert "id" in data

  async def test_create_blog_persists_draft_with_empty_content(
    self,
    api_version,
    existing_users,
    create_existing_users,
    client: AsyncClient,
  ):
    """Empty content list is allowed at create time. The empty-content
    invariant fires only at publish."""
    payload = {
      "title": "Valid Title",
      "content": [],
      "author_id": existing_users[0]["id"]
    }
    response = await client.post(f"/{api_version}/blogs/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["content"] == []
    assert data["status"] == "draft"

  async def test_create_blog_persists_empty_draft(
    self,
    api_version,
    existing_users,
    create_existing_users,
    client: AsyncClient,
  ):
    """Positive-path case the frontend's 'Write New Blog' relies on:
    POST /blogs with empty title and empty content creates a draft and
    returns 201 with the persisted draft body."""
    payload = {
      "title": "",
      "content": [],
      "author_id": existing_users[0]["id"]
    }
    response = await client.post(f"/{api_version}/blogs/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == ""
    assert data["content"] == []
    assert data["status"] == "draft"
    assert "id" in data
    assert "created_at" in data