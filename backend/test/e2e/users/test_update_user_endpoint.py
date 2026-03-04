import re
import pytest


class TestUpdateUserEndpoint:

  @pytest.mark.asyncio
  async def test_update_user_success(
    self,
    authenticated_client,
    create_existing_users,
    api_version
  ):
    payload = {
      "first_name": "Arya",
      "last_name": "Stark",
      "username": "aryastark",
    }

    response = await authenticated_client.put(
      f"/{api_version}/users/user1",
      json=payload
    )

    assert response.status_code == 200
    data = response.json()

    for key in payload:
      assert data[key] == payload[key]


  @pytest.mark.asyncio
  @pytest.mark.parametrize(
    "field, invalid_value, error_regex",
    [
      ("first_name", "", r"First Name cannot be empty"),
      ("first_name", "J", r"First Name must be at least \d+ characters long"),
      ("first_name", "J" * 31, r"First Name cannot exceed \d+ characters"),

      ("last_name", "", r"Last Name cannot be empty"),
      ("last_name", "D", r"Last Name must be at least \d+ characters long"),
      ("last_name", "D" * 31, r"Last Name cannot exceed \d+ characters"),

      ("username", "", r"Username cannot be empty"),
      ("username", "ab", r"Username must be at least \d+ characters long"),
      ("username", "a" * 21, r"Username cannot exceed \d+ characters"),
    ]
  )
  async def test_invalid_value(
    self,
    create_existing_users,
    authenticated_client,
    api_version,
    field: str,
    invalid_value: str,
    error_regex: str
  ):
    payload = {field: invalid_value}

    response = await authenticated_client.put(
      f"/{api_version}/users/user1",
      json=payload
    )

    assert response.status_code == 400
    data = response.json()

    assert "detail" in data
    assert re.match(error_regex, data["detail"])


  @pytest.mark.asyncio
  async def test_update_nonexistent_user(
    self,
    authenticated_client,
    api_version
  ):
    payload = {
      "first_name": "Non",
      "last_name": "Existent",
      "username": "nonexistentuser",
    }

    response = await authenticated_client.put(
      f"/{api_version}/users/nonexistent",
      json=payload
    )

    assert response.status_code == 404
    data = response.json()

    assert data["detail"] == "User with identifier 'user_id: nonexistent' was not found."


  @pytest.mark.asyncio
  async def test_update_user_duplicate_username(
    self,
    create_existing_users,
    authenticated_client,
    api_version
  ):
    payload = {
      "first_name": "New",
      "last_name": "Name",
      "username": "bobjohnson",
    }

    response = await authenticated_client.put(
      f"/{api_version}/users/user1",
      json=payload
    )

    assert response.status_code == 400
    data = response.json()

    assert data["detail"] == "The username 'bobjohnson' is already taken."


  @pytest.mark.asyncio
  async def test_update_user_unauthenticated(
    self,
    client,
    api_version
  ):
    payload = {
      "first_name": "Unauth",
      "last_name": "User",
      "username": "unauthuser",
    }

    response = await client.put(
      f"/{api_version}/users/user1",
      json=payload
    )

    assert response.status_code == 401
    data = response.json()

    assert data["detail"] == "Not authenticated"


  @pytest.mark.asyncio
  async def test_update_unauthorized(
    self,
    authenticated_client,
    create_existing_users,
    api_version
  ):
    payload = {
      "first_name": "Mismatch",
      "last_name": "User",
      "username": "mismatchuser",
    }

    response = await authenticated_client.put(
      f"/{api_version}/users/user2",
      json=payload
    )

    assert response.status_code == 401
    data = response.json()

    assert data["detail"] == "You are not authorized to update this user."