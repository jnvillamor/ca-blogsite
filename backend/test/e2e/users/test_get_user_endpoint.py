import pytest
from datetime import datetime, timezone

from app.database.models import BlogModel


class TestGetUserEndpoint:

  @pytest.mark.asyncio
  @pytest.mark.parametrize(
    "limit, skip, expected_count",
    [
      (2, 0, 2),
      (2, 1, 2),
      (5, 0, 3),
      (1, 2, 1),
    ]
  )
  async def test_get_all_user_success(
    self,
    create_existing_users,
    client,
    api_version,
    limit: int,
    skip: int,
    expected_count: int
  ):
    response = await client.get(f"/{api_version}/users/?limit={limit}&skip={skip}")

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data["items"], list)
    assert len(data["items"]) == expected_count
    assert data["skip"] == skip
    assert data["limit"] == limit
    assert data["total"] == 3


  @pytest.mark.asyncio
  @pytest.mark.parametrize(
    "user_id",
    [
      "user1",
      "user2",
      "user3",
    ]
  )
  async def test_get_user_by_id_success(
    self,
    existing_users,
    create_existing_users,
    client,
    api_version,
    user_id: str
  ):
    response = await client.get(f"/{api_version}/users/{user_id}")

    assert response.status_code == 200
    data = response.json()

    expected_user = next(user for user in existing_users if user["id"] == user_id)

    for key in expected_user:
      if key in ("created_at", "updated_at"):
        actual_raw = data[key]
        actual_dt = datetime.fromisoformat(actual_raw.replace("Z", "+00:00"))

        assert actual_dt == expected_user[key]

      elif key != "password":
        assert data[key] == expected_user[key]


  @pytest.mark.asyncio
  async def test_get_user_by_id_not_found(
    self,
    create_existing_users,
    client,
    api_version
  ):
    non_existent_user_id = "nonexistentuser"

    response = await client.get(f"/{api_version}/users/{non_existent_user_id}")

    assert response.status_code == 404
    data = response.json()

    assert data["detail"] == f"User with ID '{non_existent_user_id}' not found."


  @pytest.mark.asyncio
  @pytest.mark.parametrize(
    "username",
    [
      "alicesmith",
      "bobjohnson",
      "charliebrown",
    ]
  )
  async def test_get_user_by_username_success(
    self,
    create_existing_users,
    existing_users,
    client,
    api_version,
    username: str
  ):
    response = await client.get(f"/{api_version}/users/by-username/{username}")

    assert response.status_code == 200
    data = response.json()

    expected_user = next(user for user in existing_users if user["username"] == username)

    for key in expected_user:
      if key in ("created_at", "updated_at"):
        assert data[key] == expected_user[key].isoformat()

      elif key != "password":
        assert data[key] == expected_user[key]


  @pytest.mark.asyncio
  async def test_get_user_by_username_not_found(
    self,
    create_existing_users,
    client,
    api_version
  ):
    non_existent_username = "nonexistentusername"

    response = await client.get(f"/{api_version}/users/by-username/{non_existent_username}")

    assert response.status_code == 404
    data = response.json()

    assert data["detail"] == f"User with username '{non_existent_username}' not found."


  @pytest.mark.asyncio
  async def test_get_user_by_id_without_include_blog_count_omits_field(
    self,
    create_existing_users,
    client,
    api_version,
  ):
    response = await client.get(f"/{api_version}/users/user1")

    assert response.status_code == 200
    data = response.json()

    # blog_count defaults to None when include_blog_count query param is absent.
    assert data.get("blog_count") is None


  @pytest.mark.asyncio
  async def test_get_user_by_id_with_include_blog_count(
    self,
    db_session,
    create_existing_users,
    client,
    api_version,
  ):
    # Seed two drafts and one published blog for user1.
    db_session.add_all([
      BlogModel(
        id="e2e-blog-1",
        title="Draft One",
        content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Content", "styles": {}}], "children": []}],
        author_id="user1",
        status="draft",
        created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
        updated_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
      ),
      BlogModel(
        id="e2e-blog-2",
        title="Draft Two",
        content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Content", "styles": {}}], "children": []}],
        author_id="user1",
        status="draft",
        created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
        updated_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
      ),
      BlogModel(
        id="e2e-blog-3",
        title="Published One",
        content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Content", "styles": {}}], "children": []}],
        author_id="user1",
        status="published",
        created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
        updated_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
      ),
    ])
    await db_session.commit()

    response = await client.get(
      f"/{api_version}/users/user1?include_blog_count=true"
    )

    assert response.status_code == 200
    data = response.json()

    assert data["blog_count"] == {
      "total_blogs": 3,
      "published_blogs": 1,
      "draft_blogs": 2,
    }


  @pytest.mark.asyncio
  async def test_get_user_by_username_with_include_blog_count(
    self,
    create_existing_users,
    client,
    api_version,
  ):
    # user with no blogs
    response = await client.get(
      f"/{api_version}/users/by-username/alicesmith?include_blog_count=true"
    )

    assert response.status_code == 200
    data = response.json()

    assert data["blog_count"] == {
      "total_blogs": 0,
      "published_blogs": 0,
      "draft_blogs": 0,
    }


  @pytest.mark.asyncio
  async def test_get_all_users_with_include_blog_count(
    self,
    db_session,
    create_existing_users,
    client,
    api_version,
  ):
    db_session.add(
      BlogModel(
        id="e2e-blog-a",
        title="Alice Blog",
        content=[{"id": "1", "type": "paragraph", "props": {"textColor": "default", "backgroundColor": "default", "textAlignment": "left"}, "content": [{"type": "text", "text": "Content", "styles": {}}], "children": []}],
        author_id="user1",
        status="published",
        created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
        updated_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
      )
    )
    await db_session.commit()

    response = await client.get(
      f"/{api_version}/users/?limit=10&skip=0&include_blog_count=true"
    )

    assert response.status_code == 200
    data = response.json()

    # Every user item carries a non-null blog_count shape.
    for item in data["items"]:
      assert item["blog_count"] is not None
      assert set(item["blog_count"].keys()) == {
        "total_blogs",
        "published_blogs",
        "draft_blogs",
      }

    user1_item = next(item for item in data["items"] if item["id"] == "user1")
    assert user1_item["blog_count"]["total_blogs"] == 1
    assert user1_item["blog_count"]["published_blogs"] == 1
    assert user1_item["blog_count"]["draft_blogs"] == 0


  @pytest.mark.asyncio
  async def test_get_all_users_without_include_blog_count_has_none_blog_count(
    self,
    create_existing_users,
    client,
    api_version,
  ):
    response = await client.get(f"/{api_version}/users/?limit=10&skip=0")

    assert response.status_code == 200
    data = response.json()

    for item in data["items"]:
      assert item.get("blog_count") is None