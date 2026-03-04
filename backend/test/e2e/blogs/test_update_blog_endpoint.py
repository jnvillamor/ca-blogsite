import re
import pytest


class TestUpdateBlogEndpoint:

  @pytest.mark.asyncio
  @pytest.mark.parametrize(
    "title, content, hero_image",
    [
      (None, None, None),
      ("Updated Title", None, None),
      (None, "Updated content.", None),
      (None, None, "http://example.com/updated_hero.jpg"),
      ("Updated Title", "Updated content.", "http://example.com/updated_hero.jpg"),
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
      "content": "Updated content.",
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
    "title, error_regex",
    [
      ("", r"Title cannot be empty."),
      (" " * 10, r"Title cannot be empty."),
      ("Shrt", r"Title must be at least 5 characters long."),
      ("T" * 101, r"Title cannot exceed 100 characters.")
    ]
  )
  async def test_update_blog_invalid_title(
    self,
    authenticated_client,
    api_version,
    existing_blogs,
    create_existing_blogs,
    title,
    error_regex
  ):
    existing_blog = existing_blogs[0]

    payload = {
      "title": title,
      "content": "Valid content for testing.",
      "hero_image": "http://example.com/valid_hero.jpg"
    }

    response = await authenticated_client.put(
      f"/{api_version}/blogs/{existing_blog['id']}",
      json=payload
    )

    assert response.status_code == 400
    data = response.json()

    assert re.search(error_regex, data["detail"])


  @pytest.mark.asyncio
  @pytest.mark.parametrize(
    "content, error_regex",
    [
      ("", r"Content cannot be empty."),
      (" " * 10, r"Content cannot be empty.")
    ]
  )
  async def test_update_blog_invalid_content(
    self,
    authenticated_client,
    api_version,
    existing_blogs,
    create_existing_blogs,
    content,
    error_regex
  ):
    existing_blog = existing_blogs[0]

    payload = {
      "title": "Valid Title",
      "content": content,
      "hero_image": "http://example.com/valid_hero.jpg"
    }

    response = await authenticated_client.put(
      f"/{api_version}/blogs/{existing_blog['id']}",
      json=payload
    )

    assert response.status_code == 400
    data = response.json()

    assert re.search(error_regex, data["detail"])


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
      "content": "Updated content.",
      "hero_image": "http://example.com/updated_hero.jpg"
    }

    response = await authenticated_client.put(
      f"/{api_version}/blogs/{existing_blog['id']}",
      json=payload
    )

    assert response.status_code == 401
    data = response.json()

    assert data["detail"] == "You are not authorized to update this blog."