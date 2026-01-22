import re
import pytest
from fastapi.testclient import TestClient

class TestCreateUserEndpoint:
  def test_create_user_success(self, client: TestClient):
    payload = {
      "first_name": "John",
      "last_name": "Doe",
      "username": "johndoe",
      "password": "SecurePass.123"
    }
    response = client.post("/users/register", json=payload)

    assert response.status_code == 201
    data = response.json()
    for key in payload:
      if key != "password":
        assert data[key] == payload[key]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data
  
  def test_create_user_conflict(self, client: TestClient):
    payload = {
      "first_name": "Jane",
      "last_name": "Doe",
      "username": "janedoe",
      "password": "AnotherPass.456"
    }
    # First creation should succeed
    response1 = client.post("/users/register", json=payload)
    assert response1.status_code == 201

    # Second creation with same username should fail
    response2 = client.post("/users/register", json=payload)
    assert response2.status_code == 409
    data = response2.json()
    assert data["detail"] == f"The username '{payload['username']}' is already taken."
  
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
  def test_create_user_invalid_names(
    self,
    client: TestClient,
    field: str,
    invalid_value: str,
    error_regex: str
  ):
    payload = {
      "first_name": "John",
      "last_name": "Doe",
      "username": "johndoe",
      "password": "SecurePass.123"
    }
    payload[field] = invalid_value

    response = client.post("/users/register", json=payload)
    assert response.status_code == 400
    data = response.json()

    assert "detail" in data
    assert re.match(error_regex, data["detail"])
  
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

  def test_create_user_invalid_password(
    self,
    client: TestClient,
    password: str,
    error_regex: str
  ):
    payload = {
      "first_name": "John",
      "last_name": "Doe",
      "username": "johndoe",
      "password": password
    }

    response = client.post("/users/register", json=payload)
    assert response.status_code == 400
    data = response.json()

    assert "detail" in data
    assert re.search(error_regex, data["detail"])