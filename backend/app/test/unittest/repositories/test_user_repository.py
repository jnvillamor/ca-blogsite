import pytest
from sqlalchemy.orm import  Session
from app.repositories import UserRepository
from src.domain.entities import UserEntity

def make_user(
  id: str,
  first_name: str = "John",
  last_name: str = "Doe",
  username: str = "johndoe",
  password: str = "securepassword",
  avatar=None,
  created_at="2024-01-01T00:00:00Z",
  updated_at="2024-01-01T00:00:00Z"
) -> UserEntity:
  return UserEntity(
    id=id,
    first_name=first_name,
    last_name=last_name,
    username=username,
    password=password,
    avatar=avatar,
    created_at=created_at,
    updated_at=updated_at
  )


def assert_user_equal(entity1: UserEntity, entity2: UserEntity):
  assert entity1.id == entity2.id
  assert entity1.username == entity2.username
  assert entity1.first_name == entity2.first_name
  assert entity1.last_name == entity2.last_name
  assert entity1.password == entity2.password
  assert entity1.avatar == entity2.avatar
  assert entity1.created_at == entity2.created_at
  assert entity1.updated_at == entity2.updated_at


# -------------------------
# Tests
# -------------------------
class TestUserRepository:

  def test_create_and_get_user(self, db_session: Session):
    repo = UserRepository(db_session)
    user = make_user("123")
    repo.create_user(user)

    # get by id
    retrieved = repo.get_user_by_id("123")
    assert_user_equal(retrieved, user)

    # get by username
    retrieved_by_username = repo.get_user_by_username("johndoe")
    assert_user_equal(retrieved_by_username, user)

  def test_get_all_users(self, db_session: Session):
    repo = UserRepository(db_session)
    users = [make_user(str(i), username=f"user{i}") for i in range(3)]
    for u in users:
      repo.create_user(u)

    retrieved_users, total_count = repo.get_all_users()
    assert total_count == 3
    assert len(retrieved_users) == 3
    for u in users:
      assert any(u.username == ru.username for ru in retrieved_users)

  def test_update_user(self, db_session: Session):
    repo = UserRepository(db_session)
    user = make_user("999", first_name="Old", last_name="Name", username="olduser")
    repo.create_user(user)

    updated_user = make_user(
      "999",
      first_name="New",
      last_name="Name",
      username="newuser",
      updated_at="2024-01-08T00:00:00Z"
    )

    result = repo.update_user("999", updated_user)
    assert_user_equal(result, updated_user)

  @pytest.mark.parametrize("user_id", ["nonexistent"])
  def test_nonexistent_user(self, db_session: Session, user_id):
    repo = UserRepository(db_session)

    assert repo.get_user_by_id(user_id) is None
    assert repo.get_user_by_username(user_id) is None

    user = make_user(user_id)
    assert repo.update_user(user_id, user) is None

  def test_delete_user(self, db_session: Session):
    repo = UserRepository(db_session)
    user = make_user("to_delete")
    repo.create_user(user)

    repo.delete_user("to_delete")
    assert repo.get_user_by_id("to_delete") is None

  def test_get_all_users_empty(self, db_session: Session):
    repo = UserRepository(db_session)
    users, count = repo.get_all_users()
    assert count == 0
    assert len(users) == 0
