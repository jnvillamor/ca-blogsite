import pytest

class TestDeleteUserEndpoint:

  @pytest.mark.asyncio
  async def test_delete_user_success(
    self,
    authenticated_client,
    create_existing_users,
    api_version
  ):
    response = await authenticated_client.delete(
      f"/{api_version}/users/user1"
    )

    assert response.status_code == 204

    # Verify the user is actually deleted
    get_response = await authenticated_client.get(
      f"/{api_version}/users/user1"
    )

    assert get_response.status_code == 404


  @pytest.mark.asyncio
  async def test_delete_nonexistent_user(
    self,
    authenticated_client,
    api_version
  ):
    response = await authenticated_client.delete(
      f"/{api_version}/users/nonexistent"
    )

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "User with identifier 'user_id: nonexistent' was not found."