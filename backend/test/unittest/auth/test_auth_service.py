import pytest
from datetime import datetime, timezone

from app.auth import AuthService
from src.domain.entities import UserEntity

@pytest.fixture
def password_hasher(mocker):
  hasher = mocker.Mock()
  return hasher

@pytest.fixture
def user_repo(mocker):
  repo = mocker.Mock()
  return repo

@pytest.fixture
def auth_service():
  return AuthService()

@pytest.fixture
def existing_user():
  return UserEntity(
    id="user-123",
    first_name="John",
    last_name="Doe",
    username="johndoe",
    password="hashedpassword",
    avatar=None,
    # set created_at to a fixed datetime for consistent testing
    created_at=datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
    updated_at=datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
  )

class TestAuthService:
  def test_authenticate_user_success(
    self,
    auth_service,
    user_repo,
    password_hasher,
    existing_user
  ):
    user_repo.get_user_by_username.return_value = existing_user
    password_hasher.verify.return_value = True

    result = auth_service.authenticate_user(
      user_repo=user_repo,
      password_hasher=password_hasher,
      username=existing_user.username,
      password="plaintextpassword"
    )

    assert result.access_token is not None
    assert result.refresh_token is not None
    assert result.user.username == existing_user.username
  
  def test_authenticate_user_invalid_credentials(
    self,
    auth_service,
    user_repo,
    password_hasher
  ):
    user_repo.get_user_by_username.return_value = None

    with pytest.raises(Exception):
      auth_service.authenticate_user(
        user_repo=user_repo,
        password_hasher=password_hasher,
        username="nonexistent",
        password="plaintextpassword"
      )
  
  def test_authenticate_user_wrong_password(
    self,
    auth_service,
    user_repo,
    password_hasher,
    existing_user
  ):
    user_repo.get_user_by_username.return_value = existing_user
    password_hasher.verify.return_value = False

    with pytest.raises(Exception):
      auth_service.authenticate_user(
        user_repo=user_repo,
        password_hasher=password_hasher,
        username=existing_user.username,
        password="wrongpassword"
      )

  def test_get_current_user_success(
    self,
    auth_service,
    password_hasher,
    user_repo,
    existing_user
  ):
    # login to get a valid token
    user_repo.get_user_by_username.return_value = existing_user
    password_hasher.verify.return_value = True

    auth_result = auth_service.authenticate_user(
      user_repo=user_repo,
      password_hasher=password_hasher,
      username=existing_user.username,
      password="plaintextpassword"
    )
    token = auth_result.access_token
    user_repo.get_user_by_id.return_value = existing_user
    result = auth_service.get_current_user(
      user_repo=user_repo,
      token=token
    )
    assert result.username == existing_user.username
  
  def test_get_current_user_invalid_token(
    self,
    auth_service,
    user_repo
  ):
    with pytest.raises(Exception):
      auth_service.get_current_user(
        user_repo=user_repo,
        token="invalidtoken"
      )
  
  def test_refresh_access_token_success(
    self,
    auth_service,
    password_hasher,
    user_repo,
    existing_user
  ):
    # login to get a valid token
    user_repo.get_user_by_username.return_value = existing_user
    password_hasher.verify.return_value = True

    auth_result = auth_service.authenticate_user(
      user_repo=user_repo,
      password_hasher=password_hasher,
      username=existing_user.username,
      password="plaintextpassword"
    )
    refresh_token = auth_result.refresh_token
    user_repo.get_user_by_id.return_value = existing_user

    result = auth_service.refresh_access_token(
      user_repo=user_repo,
      token=refresh_token
    )
    assert result.access_token is not None
    assert result.refresh_token is not None
    assert result.user.username == existing_user.username

  def test_refresh_access_token_invalid_token(
    self,
    auth_service,
    user_repo
  ):
    with pytest.raises(Exception):
      auth_service.refresh_access_token(
        user_repo=user_repo,
        token="invalidtoken"
      )
  