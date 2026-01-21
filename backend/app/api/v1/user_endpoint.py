from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.services import PasswordHasher, UuidGenerator
from src.application.dto import CreateUserDTO, UserResponseDTO
from src.application.use_cases.users import CreateUserUseCase

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
  password_hasher = PasswordHasher()
  uuid_generator = UuidGenerator()
  use_case = CreateUserUseCase(
    session=session,
    password_hasher=password_hasher,
    uuid_generator=uuid_generator
  )
  return use_case.execute(user_data)