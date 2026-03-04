import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import UserModel
from app.database.unit_of_work import UnitOfWork

from src.application.use_cases.users import DeleteUserUseCase
from src.domain.entities import UserEntity


@pytest.fixture
def delete_user_use_case(db_session: AsyncSession) -> DeleteUserUseCase:
  unit_of_work = UnitOfWork(session=db_session)
  return DeleteUserUseCase(unit_of_work=unit_of_work)


class TestDeleteUserUseCase:

  @pytest.mark.asyncio
  async def test_delete_user_success(
    self,
    db_session: AsyncSession,
    create_test_user,
    delete_user_use_case: DeleteUserUseCase
  ):
    test_user: UserEntity = await create_test_user()

    # Verify user exists
    user_in_db = await db_session.get(UserModel, test_user.id)

    assert user_in_db is not None
    assert user_in_db.username == test_user.username
    assert user_in_db.id == test_user.id

    await delete_user_use_case.execute(
      active_user=test_user,
      user_id=test_user.id
    )

    # Verify deletion
    user_after_delete = await db_session.get(UserModel, test_user.id)

    assert user_after_delete is None


  @pytest.mark.asyncio
  async def test_delete_user_non_existing(
    self,
    create_test_user,
    delete_user_use_case: DeleteUserUseCase
  ):
    non_existing_user_id = "non-existing-id"

    test_user: UserEntity = await create_test_user()

    with pytest.raises(Exception) as exc_info:
      await delete_user_use_case.execute(
        active_user=test_user,
        user_id=non_existing_user_id
      )

    assert "User with identifier 'user_id: non-existing-id' was not found." in str(exc_info.value)


  @pytest.mark.asyncio
  async def test_delete_user_unauthorized(
    self,
    create_test_user,
    delete_user_use_case: DeleteUserUseCase
  ):
    test_user: UserEntity = await create_test_user()

    with pytest.raises(Exception) as exc_info:
      await delete_user_use_case.execute(
        active_user=UserEntity(
          id="another_user_id",
          first_name="Another",
          last_name="User",
          username="anotheruser",
          password="AnotherPass123!",
          avatar=None,
          created_at=test_user.created_at,
          updated_at=test_user.updated_at
        ),
        user_id=test_user.id
      )

    assert "You are not authorized to delete this user." in str(exc_info.value)