import pytest
from datetime import datetime


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