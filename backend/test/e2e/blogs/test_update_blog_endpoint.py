import pytest


class TestUpdateBlogEndpoint:

  @pytest.mark.asyncio
  @pytest.mark.parametrize(
    "title, content, hero_image",
    [
      (None, None, None),
      ("Updated Title", None, None),
      (None, [{"id": "2", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Updated content.", "styles": {}}], "children": []}], None),
      (None, None, "http://example.com/updated_hero.jpg"),
      ("Updated Title", [{"id": "2", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Updated content.", "styles": {}}], "children": []}], "http://example.com/updated_hero.jpg"),
    ]
  )
  async def test_update_blog_success(
    self,
    authenticated_client,
    api_version,
    existing_blogs,
    create_existing_blogs,
    title,
    content,
    hero_image
  ):
    existing_blog = existing_blogs[0]

    payload = {
      "title": title,
      "content": content,
      "hero_image": hero_image
    }

    response = await authenticated_client.put(
      f"/{api_version}/blogs/{existing_blog['id']}",
      json=payload
    )

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == existing_blog["id"]
    assert data["author_id"] == existing_blog["author_id"]
    assert data["title"] == (
      title if title is not None else existing_blog["title"]
    )
    assert data["content"] == (
      content if content is not None else existing_blog["content"]
    )
    assert data["hero_image"] == (
      hero_image if hero_image is not None else existing_blog["hero_image"]
    )


  @pytest.mark.asyncio
  async def test_update_blog_not_found(
    self,
    authenticated_client,
    api_version
  ):
    payload = {
      "title": "Updated Title",
      "content": [{"id": "2", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Updated content.", "styles": {}}], "children": []}],
      "hero_image": "http://example.com/updated_hero.jpg"
    }

    response = await authenticated_client.put(
      f"/{api_version}/blogs/nonexistent-blog-id",
      json=payload
    )

    assert response.status_code == 404
    data = response.json()

    assert data["detail"] == "Blog with identifier 'blog_id: nonexistent-blog-id' was not found."


  @pytest.mark.asyncio
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
  async def test_update_blog_persists_publish_invalid_title(
    self,
    authenticated_client,
    api_version,
    existing_blogs,
    create_existing_blogs,
    title
  ):
    """The endpoint must accept titles that would fail publish-time
    invariants. Validation moved to publish — exercised at the entity /
    use-case layer."""
    existing_blog = existing_blogs[0]

    payload = {
      "title": title,
      "content": [{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Valid content for testing.", "styles": {}}], "children": []}],
      "hero_image": "http://example.com/valid_hero.jpg"
    }

    response = await authenticated_client.put(
      f"/{api_version}/blogs/{existing_blog['id']}",
      json=payload
    )

    assert response.status_code == 200
    data = response.json()
    # Title is normalized via `(value or "").strip()` inside the Title VO.
    assert data["title"] == title.strip()


  @pytest.mark.asyncio
  async def test_update_blog_persists_empty_content(
    self,
    authenticated_client,
    api_version,
    existing_blogs,
    create_existing_blogs,
  ):
    """Empty content list is allowed at update time. The empty-content
    invariant fires only at publish."""
    existing_blog = existing_blogs[0]

    payload = {
      "title": "Valid Title",
      "content": [],
      "hero_image": "http://example.com/valid_hero.jpg"
    }

    response = await authenticated_client.put(
      f"/{api_version}/blogs/{existing_blog['id']}",
      json=payload
    )

    assert response.status_code == 200
    data = response.json()
    assert data["content"] == []


  @pytest.mark.asyncio
  async def test_update_blog_unauthorized(
    self,
    authenticated_client,
    api_version,
    existing_blogs,
    create_existing_blogs
  ):
    existing_blog = existing_blogs[1]

    payload = {
      "title": "Updated Title",
      "content": [{"id": "2", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Updated content.", "styles": {}}], "children": []}],
      "hero_image": "http://example.com/updated_hero.jpg"
    }

    response = await authenticated_client.put(
      f"/{api_version}/blogs/{existing_blog['id']}",
      json=payload
    )

    assert response.status_code == 401
    data = response.json()

    assert data["detail"] == "You are not authorized to update this blog."