import pytest
from fastapi.testclient import TestClient

class TestDeleteUserEndpoint:
  def test_delete_user_success(self, authenticated_client: TestClient, create_existing_users):
    response = authenticated_client.delete("v1/users/user1")
    assert response.status_code == 204

    # Verify the user is actually deleted
    get_response = authenticated_client.get("v1/users/user1")
    assert get_response.status_code == 404
  
  def test_delete_nonexistent_user(self, authenticated_client: TestClient):
    response = authenticated_client.delete("v1/users/nonexistent")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "User with identifier 'user_id: nonexistent' was not found."