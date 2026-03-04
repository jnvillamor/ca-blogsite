import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock

from app.auth import AuthService
from src.domain.entities import UserEntity


@pytest.fixture
def password_hasher(mocker):
  return mocker.Mock()


@pytest.fixture
def id_generator(mocker):
  generator = mocker.Mock()
  generator.generate.side_effect = lambda: f"token-{datetime.now().timestamp()}"
  return generator


@pytest.fixture
def user_repo(mocker):
  repo = mocker.Mock()
  repo.get_user_by_username = AsyncMock()
  repo.get_user_by_id = AsyncMock()
  repo.update_user = AsyncMock()
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
    access_token_id=None,
    refresh_token_id=None,
    created_at=datetime(2023,1,1,12,0,0,tzinfo=timezone.utc),
    updated_at=datetime(2023,1,1,12,0,0,tzinfo=timezone.utc)
  )


class TestAuthService:

  @pytest.mark.asyncio
  async def test_authenticate_user_success(
    self,
    auth_service,
    user_repo,
    password_hasher,
    existing_user,
    db_session,
    id_generator
  ):
    user_repo.get_user_by_username.return_value = existing_user
    password_hasher.verify.return_value = True

    result = await auth_service.authenticate_user(
      session=db_session,
      id_generator=id_generator,
      user_repo=user_repo,
      password_hasher=password_hasher,
      username=existing_user.username,
      password="plaintextpassword"
    )

    assert result.access_token is not None
    assert result.refresh_token is not None
    assert result.user.username == existing_user.username


  @pytest.mark.asyncio
  async def test_authenticate_user_invalid_credentials(
    self,
    auth_service,
    user_repo,
    password_hasher,
    db_session,
    id_generator
  ):
    user_repo.get_user_by_username.return_value = None

    with pytest.raises(Exception):
      await auth_service.authenticate_user(
        session=db_session,
        id_generator=id_generator,
        user_repo=user_repo,
        password_hasher=password_hasher,
        username="nonexistent",
        password="plaintextpassword"
      )


  @pytest.mark.asyncio
  async def test_authenticate_user_wrong_password(
    self,
    auth_service,
    user_repo,
    password_hasher,
    existing_user,
    db_session,
    id_generator
  ):
    user_repo.get_user_by_username.return_value = existing_user
    password_hasher.verify.return_value = False

    with pytest.raises(Exception):
      await auth_service.authenticate_user(
        session=db_session,
        id_generator=id_generator,
        user_repo=user_repo,
        password_hasher=password_hasher,
        username=existing_user.username,
        password="wrongpassword"
      )


  @pytest.mark.asyncio
  async def test_get_current_user_success(
    self,
    auth_service,
    password_hasher,
    user_repo,
    existing_user,
    db_session,
    id_generator
  ):
    user_repo.get_user_by_username.return_value = existing_user
    password_hasher.verify.return_value = True

    auth_result = await auth_service.authenticate_user(
      session=db_session,
      id_generator=id_generator,
      user_repo=user_repo,
      password_hasher=password_hasher,
      username=existing_user.username,
      password="plaintextpassword"
    )

    token = auth_result.access_token

    user_repo.get_user_by_id.return_value = existing_user

    result = await auth_service.get_current_user(
      user_repo=user_repo,
      token=token
    )

    assert result.username == existing_user.username


  @pytest.mark.asyncio
  async def test_get_current_user_invalid_token(
    self,
    auth_service,
    user_repo
  ):
    with pytest.raises(Exception):
      await auth_service.get_current_user(
        user_repo=user_repo,
        token="invalidtoken"
      )


  @pytest.mark.asyncio
  async def test_refresh_access_token_success(
    self,
    auth_service,
    password_hasher,
    user_repo,
    existing_user,
    db_session,
    id_generator
  ):
    user_repo.get_user_by_username.return_value = existing_user
    password_hasher.verify.return_value = True

    auth_result = await auth_service.authenticate_user(
      session=db_session,
      id_generator=id_generator,
      user_repo=user_repo,
      password_hasher=password_hasher,
      username=existing_user.username,
      password="plaintextpassword"
    )

    refresh_token = auth_result.refresh_token

    user_repo.get_user_by_id.return_value = existing_user
    user_repo.update_user.return_value = existing_user

    result = await auth_service.refresh_access_token(
      session=db_session,
      id_generator=id_generator,
      user_repo=user_repo,
      token=refresh_token
    )

    assert result.access_token is not None
    assert result.refresh_token is not None
    assert result.user.username == existing_user.username


  @pytest.mark.asyncio
  async def test_refresh_access_token_invalid_token(
    self,
    auth_service,
    user_repo
  ):
    with pytest.raises(Exception):
      await auth_service.refresh_access_token(
        user_repo=user_repo,
        token="invalidtoken"
      )