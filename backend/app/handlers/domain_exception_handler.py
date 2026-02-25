import logging
from fastapi import status, FastAPI, Request
from fastapi.responses import JSONResponse
from src.domain.exceptions import (
  UnauthorizedException,
  InvalidDataException,
  UsernameExistsException,
  NotFoundException,
)

default_logger = logging.getLogger("uvicorn.error")

def register_domain_exception_handler(app: FastAPI, logger: logging.Logger = default_logger):
  @app.exception_handler(InvalidDataException)
  def handle_invalid_data_exception(request: Request, exc: InvalidDataException):
    logger.error(f"InvalidDataException: {str(exc)}")
    return JSONResponse(
      status_code=status.HTTP_400_BAD_REQUEST,
      content={"detail": str(exc)}
    )
  
  @app.exception_handler(UsernameExistsException)
  def handle_username_exists_exception(request: Request, exc: UsernameExistsException):
    logger.error(f"UsernameExistsException: {str(exc)}")
    return JSONResponse(
      status_code=status.HTTP_409_CONFLICT,
      content={"detail": str(exc)}
    )
  
  @app.exception_handler(NotFoundException)
  def handle_not_found_exception(request: Request, exc: NotFoundException):
    logger.error(f"NotFoundException: {str(exc)}")
    return JSONResponse(
      status_code=status.HTTP_404_NOT_FOUND,
      content={"detail": str(exc)}
    )
  
  @app.exception_handler(UnauthorizedException)
  def handle_unauthorized_exception(request: Request, exc: UnauthorizedException):
    logger.error(f"UnauthorizedException: {str(exc)}")
    return JSONResponse(
      status_code=status.HTTP_401_UNAUTHORIZED,
      content={"detail": str(exc)}
    )