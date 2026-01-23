import pytest
from fastapi.testclient import TestClient

class TestDeleteUserEndpoint:
  def test_delete_user_success(self, client: TestClient, create_existing_users):
    response = client.delete("/users/user1")
    assert response.status_code == 204

    # Verify the user is actually deleted
    get_response = client.get("/users/user1")
    assert get_response.status_code == 404
  
  def test_delete_nonexistent_user(self, client: TestClient):
    response = client.delete("/users/nonexistent")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "User with identifier 'user_id: nonexistent' was not found."