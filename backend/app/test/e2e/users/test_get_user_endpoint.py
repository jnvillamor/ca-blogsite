import pytest
from app.test.e2e.conftest import EXISTING_USERS
from fastapi.testclient import TestClient

class TestGetUserEndpoint:
  @pytest.mark.parametrize(
    "limit, skip, expected_count",
    [
      (2, 0, 2),
      (2, 1, 2),
      (5, 0, 3),
      (1, 2, 1),
    ]
  )
  def test_get_all_user_success(
    self,
    create_existing_users,
    client: TestClient,
    limit: int,
    skip: int,
    expected_count: int
  ):
    response = client.get(f"/users/?limit={limit}&skip={skip}")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["items"], list)
    assert len(data["items"]) == expected_count
    assert data["skip"] == skip
    assert data["limit"] == limit
    assert data["total"] == 3

  @pytest.mark.parametrize(
    "user_id",
    [
      "user1",
      "user2",
      "user3",
    ]
  )
  def test_get_user_by_id_success(
    self,
    create_existing_users,
    client: TestClient,
    user_id: str
  ):
    response = client.get(f"/users/{user_id}")

    assert response.status_code == 200
    data = response.json()
    expected_user = next(user for user in EXISTING_USERS if user["id"] == user_id)
    for key in expected_user:
      if key != "password":
        assert data[key] == expected_user[key]

  def test_get_user_by_id_not_found(
    self,
    create_existing_users,
    client: TestClient
  ):
    non_existent_user_id = "nonexistentuser"
    response = client.get(f"/users/{non_existent_user_id}")

    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == f"User with ID '{non_existent_user_id}' not found." 
  
  @pytest.mark.parametrize(
    "username",
    [
      "alicesmith",
      "bobjohnson",
      "charliebrown",
    ]
  )
  def test_get_user_by_username_success(
    self,
    create_existing_users,
    client: TestClient,
    username: str
  ):
    response = client.get(f"/users/by-username/{username}")

    assert response.status_code == 200
    data = response.json()
    expected_user = next(user for user in EXISTING_USERS if user["username"] == username)
    for key in expected_user:
      if key != "password":
        assert data[key] == expected_user[key]
  
  def test_get_user_by_username_not_found(
    self,
    create_existing_users,
    client: TestClient
  ):
    non_existent_username = "nonexistentusername"
    response = client.get(f"/users/by-username/{non_existent_username}")

    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == f"User with username '{non_existent_username}' not found."