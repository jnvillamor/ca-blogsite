import pytest
from datetime import datetime, timezone

from app.database.models import BlogModel


class TestGetBlogEndpoint:

  @pytest.mark.asyncio
  @pytest.mark.parametrize(
    "limit, skip, expected_count",
    [
      (15, 0, 15),
      (15, 15, 0),
      (5, 0, 5),
      (1, 14, 1),
    ]
  )
  async def test_get_all_blogs_success(
    self,
    client,
    create_existing_blogs,
    limit,
    skip,
    expected_count
  ):
    response = await client.get(f"/v1/blogs/?limit={limit}&skip={skip}")

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data["items"], list)
    assert len(data["items"]) == expected_count
    assert data["skip"] == skip
    assert data["limit"] == limit
    assert data["total"] == 15


  @pytest.mark.asyncio
  @pytest.mark.parametrize(
    "search_query, expected_count",
    [
      ("Test Blog", 10),
      ("test blog 1", 7),
      ("Nonexistent", 0),
    ]
  )
  async def test_get_blogs_with_search(
    self,
    client,
    create_existing_blogs,
    search_query,
    expected_count
  ):
    response = await client.get(f"/v1/blogs/?search={search_query}")

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data["items"], list)
    assert len(data["items"]) == expected_count


  @pytest.mark.asyncio
  @pytest.mark.parametrize(
    "blog_id",
    [
      "blog-1",
      "blog-5",
      "blog-15",
    ]
  )
  async def test_get_blog_by_id_success(
    self,
    client,
    create_existing_blogs,
    blog_id
  ):
    response = await client.get(f"/v1/blogs/{blog_id}")

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == blog_id
    assert data["title"] == f"Test Blog {blog_id.split('-')[1]}"
    blog_num = blog_id.split('-')[1]
    expected_content = [{"id": blog_num, "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": f"This is the content of test blog {blog_num}.", "styles": {}}], "children": []}]
    assert data["content"] == expected_content
    assert data["author_id"] is not None


  @pytest.mark.asyncio
  async def test_get_blog_by_id_not_found(self, client):
    response = await client.get("/v1/blogs/nonexistent-blog-id")

    assert response.status_code == 404
    data = response.json()

    assert data["detail"] == "Blog with id 'nonexistent-blog-id' not found."


class TestGetPublicBlogsByAuthorEndpoint:
  """E2E tests for GET /v1/blogs/author/{author_id}/public — no auth required."""

  @pytest.fixture
  async def public_blogs_for_author(self, db_session, create_existing_users):
    """Seed a mixed set of blogs for `user1`:

    - 2 published (status=published, published_at set, full snapshot)
    - 1 published-then-edited (status=draft, published_at still set, snapshot intact)
    - 1 never-published (status=draft, no published_at)
    - 1 published belonging to a *different* author (user2)
    """
    base_content = [{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Body.", "styles": {}}], "children": []}]

    blogs = [
      BlogModel(
        id="pub-a",
        title="Pub A draft title",
        content=base_content,
        author_id="user1",
        status="published",
        published_title="Pub A snap",
        published_content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Pub A snap content.", "styles": {}}], "children": []}],
        published_at=datetime(2024, 6, 1, tzinfo=timezone.utc),
      ),
      BlogModel(
        id="pub-b",
        title="Pub B draft title",
        content=base_content,
        author_id="user1",
        status="published",
        published_title="Pub B snap",
        published_content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Pub B snap content.", "styles": {}}], "children": []}],
        published_at=datetime(2024, 6, 2, tzinfo=timezone.utc),
      ),
      BlogModel(
        id="edited-after-pub",
        title="Edited Draft Title",
        content=base_content,
        author_id="user1",
        status="draft",
        published_title="Original Snap Title",
        published_content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Original snap content.", "styles": {}}], "children": []}],
        published_at=datetime(2024, 5, 1, tzinfo=timezone.utc),
      ),
      BlogModel(
        id="never-pub",
        title="Never Published",
        content=base_content,
        author_id="user1",
        status="draft",
      ),
      BlogModel(
        id="other-author-pub",
        title="Other author pub",
        content=base_content,
        author_id="user2",
        status="published",
        published_title="Other author snap",
        published_content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Other.", "styles": {}}], "children": []}],
        published_at=datetime(2024, 6, 5, tzinfo=timezone.utc),
      ),
    ]
    db_session.add_all(blogs)
    await db_session.commit()


  @pytest.mark.asyncio
  async def test_returns_200_with_paginated_results_no_auth(
    self,
    client,
    public_blogs_for_author,
  ):
    response = await client.get("/v1/blogs/author/user1/public")

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data["items"], list)
    assert "total" in data
    assert "skip" in data
    assert "limit" in data


  @pytest.mark.asyncio
  async def test_excludes_blogs_with_null_published_at(
    self,
    client,
    public_blogs_for_author,
  ):
    response = await client.get("/v1/blogs/author/user1/public")

    assert response.status_code == 200
    data = response.json()

    ids = sorted(item["id"] for item in data["items"])
    # never-pub has published_at IS NULL → excluded.
    # other-author-pub belongs to user2 → excluded.
    assert ids == ["edited-after-pub", "pub-a", "pub-b"]
    assert data["total"] == 3


  @pytest.mark.asyncio
  async def test_includes_draft_status_with_published_at(
    self,
    client,
    public_blogs_for_author,
  ):
    """Regression guard: a blog whose status is 'draft' but has a non-null
    published_at MUST be included (published-then-edited case)."""
    response = await client.get("/v1/blogs/author/user1/public")

    assert response.status_code == 200
    data = response.json()

    edited = next((i for i in data["items"] if i["id"] == "edited-after-pub"), None)
    assert edited is not None
    assert edited["status"] == "draft"
    # The use case swapped in the published snapshot.
    assert edited["title"] == "Original Snap Title"


  @pytest.mark.asyncio
  async def test_response_uses_public_dto_shape(
    self,
    client,
    public_blogs_for_author,
  ):
    response = await client.get("/v1/blogs/author/user1/public")

    assert response.status_code == 200
    data = response.json()

    for item in data["items"]:
      # PublicBlogResponseDTO does not expose published_title/published_content.
      assert "published_title" not in item
      assert "published_content" not in item
      # title/content are present (the swapped snapshot).
      assert "title" in item
      assert "content" in item

    # Spot-check the snapshot swap on a fully-published blog.
    pub_a = next(i for i in data["items"] if i["id"] == "pub-a")
    assert pub_a["title"] == "Pub A snap"


  @pytest.mark.asyncio
  async def test_pagination_query_params(
    self,
    client,
    public_blogs_for_author,
  ):
    response = await client.get("/v1/blogs/author/user1/public?skip=0&limit=2")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3
    assert len(data["items"]) == 2
    assert data["skip"] == 0
    assert data["limit"] == 2

    response_page_2 = await client.get("/v1/blogs/author/user1/public?skip=2&limit=2")
    assert response_page_2.status_code == 200
    data_page_2 = response_page_2.json()
    assert data_page_2["total"] == 3
    assert len(data_page_2["items"]) == 1


  @pytest.mark.asyncio
  async def test_search_query_param(
    self,
    client,
    public_blogs_for_author,
  ):
    # Search hits the draft title column. Only 'Pub A draft title' and 'Pub B draft title'
    # contain "Pub" — 'edited-after-pub' has draft title "Edited Draft Title" which does
    # not match.
    response = await client.get("/v1/blogs/author/user1/public?search=Pub")

    assert response.status_code == 200
    data = response.json()
    ids = sorted(item["id"] for item in data["items"])
    assert ids == ["pub-a", "pub-b"]
    assert data["total"] == 2


  @pytest.mark.asyncio
  async def test_returns_empty_for_author_with_no_published_blogs(
    self,
    client,
    public_blogs_for_author,
  ):
    # user3 exists (from EXISTING_USERS) but has no blogs at all.
    response = await client.get("/v1/blogs/author/user3/public")

    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0


  @pytest.mark.asyncio
  async def test_trailing_slash_alias(
    self,
    client,
    public_blogs_for_author,
  ):
    """The endpoint is registered with a trailing-slash alias (include_in_schema=False)."""
    response = await client.get("/v1/blogs/author/user1/public/")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3