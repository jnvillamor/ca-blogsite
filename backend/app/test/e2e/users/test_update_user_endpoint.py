import re
import pytest
from fastapi.testclient import TestClient

class TestUpdateUserEndpoint:
  def test_update_user_success(self, client: TestClient, create_existing_users):
    payload = {
      "first_name": "Arya",
      "last_name": "Stark",
      "username": "aryastark",
    }

    response = client.put("/users/user1", json=payload)
    assert response.status_code == 200
    data = response.json()
    for key in payload:
      assert data[key] == payload[key]
  
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
  def test_invalid_value(
    self,
    create_existing_users,
    client: TestClient,
    field: str,
    invalid_value: str,
    error_regex: str
  ):
    payloag = { field: invalid_value }

    response = client.put("/users/user1", json=payloag)
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert re.match(error_regex, data["detail"])
  
  def test_update_nonexistent_user(self, client: TestClient):
    payload = {
      "first_name": "Non",
      "last_name": "Existent",
      "username": "nonexistentuser",
    }

    response = client.put("/users/nonexistent", json=payload)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "User with identifier 'user_id: nonexistent' was not found."
  
  def test_update_user_duplicate_username(
    self,
    create_existing_users,
    client: TestClient
  ):
    payload = {
      "first_name": "New",
      "last_name": "Name",
      "username": "bobjohnson",  # username already taken by another user
    }

    response = client.put("/users/user1", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "The username 'bobjohnson' is already taken."
  
  def test_password_change_success(
    self,
    create_existing_users,
    client: TestClient
  ):
    payload = {
      "password": "NewStrongPass1!"
    }

    response = client.put("/users/user1", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data

  @pytest.mark.parametrize(
    "password, error_regex",
    [
      ("", r"Password cannot be empty"),
      ("short", r"at least 8 characters"),
      ("NoDigits!", r"at least one digit"),
      ("nouppercase1!", r"at least one uppercase letter"),
      ("NOLOWERCASE1!", r"at least one lowercase letter"),
      ("NoSpecial1", r"at least one special character"),
    ]
  )
  def test_invalid_password(
    self,
    create_existing_users,
    client: TestClient,
    password: str,
    error_regex: str
  ):
    payload = { "password": password }

    response = client.put("/users/user1", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert re.search(error_regex, data["detail"])