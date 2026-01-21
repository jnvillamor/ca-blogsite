import logging
from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.database.unit_of_work import get_uow
from app.services import PasswordHasher, UuidGenerator
from src.application.dto import CreateUserDTO, UserResponseDTO
from src.application.use_cases.users import CreateUserUseCase

logger = logging.getLogger(__name__)

router = APIRouter(
  prefix="/users",
  tags=["users"]
)

@router.post(
  "/register", 
  response_model=UserResponseDTO,
  response_model_exclude_none=True,
  responses={
    201: {"description": "User successfully registered."},
    400: {"description": "Bad Request."},
    409: {"description": "Conflict. User already exists."},
    500: {"description": "Internal Server Error."}
  }
)
def register_user(
  request: Request,
  user_data: CreateUserDTO,
  session: Session = Depends(get_db)
):
  logger.info(f"Registering user with username: {user_data.username}")
  password_hasher = PasswordHasher()
  uuid_generator = UuidGenerator()
  unit_of_work = get_uow(session)
  use_case = CreateUserUseCase(
    unit_of_work=unit_of_work,
    password_hasher=password_hasher,
    id_generator=uuid_generator
  )
  result = use_case.execute(user_data)
  logger.info(f"User registered with ID: {result.id}")
  return result