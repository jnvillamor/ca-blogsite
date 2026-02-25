import re
import pytest
from fastapi.testclient import TestClient

class TestChangePassEndpoint:
  def test_change_pass_success(
    self,
    authenticated_client: TestClient,
    create_existing_users
  ):
    user_id = "user1"
    payload = {
      "old_password": "SecurePass.123",
      "new_password": "NewPass.456",
      "confirm_new_password": "NewPass.456"
    }

    response = authenticated_client.put(f"v1/users/change-password/{user_id}", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert "password" not in data
  
  def test_change_pass_non_existent_user(
    self,
    authenticated_client: TestClient
  ):
    user_id = "non_existent_user"
    payload = {
      "old_password": "AnyOldPass.123",
      "new_password": "NewPass.456",
      "confirm_new_password": "NewPass.456"
    }

    response = authenticated_client.put(f"v1/users/change-password/{user_id}", json=payload)

    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == f"User with identifier 'user_id: {user_id}' was not found."

  def test_change_pass_incorrect_old_password(
    self,
    authenticated_client: TestClient,
    create_existing_users
  ):
    user_id = "user1"
    payload = {
      "old_password": "WrongOldPass",
      "new_password": "NewPass.456",
      "confirm_new_password": "NewPass.456"
    }

    response = authenticated_client.put(f"v1/users/change-password/{user_id}", json=payload)

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Old password is incorrect."
  
  def test_change_pass_mismatched_new_passwords(
    self,
    authenticated_client: TestClient,
    create_existing_users
  ):
    user_id = "user1"
    payload = {
      "old_password": "SecurePass.123",
      "new_password": "NewPass.456",
      "confirm_new_password": "DifferentPass.789"
    }
    response = authenticated_client.put(f"v1/users/change-password/{user_id}", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "New password and confirmation do not match."
  
  @pytest.mark.parametrize(
    "password, error_regex",
    [
      ("", r"Password cannot be empty"),
      ("short", r"at least 8 characters"),
      ("NoDigits!", r"at least one digit"),
      ("nouppercase1!", r"at least one uppercase"),
      ("NOLOWERCASE1!", r"at least one lowercase"),
      ("NoSpecial1", r"at least one special character"),
    ]
  )
  def test_change_pass_invalid_new_password(
    self,
    authenticated_client: TestClient,
    create_existing_users,
    password,
    error_regex
  ):
    user_id = "user1"
    payload = {
      "old_password": "SecurePass.123",
      "new_password": password,
      "confirm_new_password": password
    }

    response = authenticated_client.put(f"v1/users/change-password/{user_id}", json=payload)

    assert response.status_code == 400
    data = response.json()
    assert re.search(error_regex, data["detail"])
  
  def test_change_pass_unauthorized(self, authenticated_client: TestClient):
    user_id = "user2"  # user2 is not the authenticated user
    payload = {
      "old_password": "SecurePass.123",
      "new_password": "NewPass.456",
      "confirm_new_password": "NewPass.456"
    }

    response = authenticated_client.put(f"v1/users/change-password/{user_id}", json=payload)
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "You are not authorized to change the password for this user."

  def test_change_pass_missing_fields(self, authenticated_client: TestClient):
    user_id = "user1"
    payload = {
      "old_password": "SecurePass.123",
      # "new_password" is missing
      "confirm_new_password": "NewPass.456"
    }

    response = authenticated_client.put(f"v1/users/change-password/{user_id}", json=payload)
    assert response.status_code == 422

    data = response.json()

    assert data["message"] == "Invalid request data"
    assert "details" in data

    assert any(
      error["loc"][-1] == "new_password" and error["type"] == "missing"
      for error in data["details"]
    ), "Expected validation error for missing 'new_password' field"